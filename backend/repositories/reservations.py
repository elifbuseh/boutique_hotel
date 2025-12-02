from datetime import date
from psycopg2 import Error
from psycopg2.extras import execute_values
from backend.database import get_connection, _handle_error


def _ensure_guest_count_column(cursor):
    """Adds guest_count column if it does not exist yet (default 1)."""
    try:
        cursor.execute("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS guest_count INTEGER DEFAULT 1;")
        cursor.connection.commit()
    except Exception:
        pass


def _replace_reservation_guests(cursor, reservation_id: int, guest_ids: list[int], primary_guest_id: int | None):
    """Clears and re-inserts reservation_guests rows."""
    cursor.execute("DELETE FROM reservation_guests WHERE reservation_id = %s;", (reservation_id,))
    if not guest_ids:
        return
    rows = [(reservation_id, gid, gid == primary_guest_id) for gid in guest_ids]
    execute_values(
        cursor,
        "INSERT INTO reservation_guests (reservation_id, guest_id, is_primary) VALUES %s",
        rows,
    )


def get_all_reservations():
    """
    Returns reservations with aggregated guest info.
    Row shape:
    (id, primary_guest_id, room_id, guest_names_str, room_number, check_in_date, check_out_date,
     status, total_amount, nightly_price, guest_count, guest_ids_array, guest_name_list)
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        _ensure_guest_count_column(cursor)
        cursor.execute(
            """
            SELECT r.id,
                   COALESCE(rg_primary.guest_id, r.guest_id) AS primary_guest_id,
                   r.room_id,
                   COALESCE(string_agg(DISTINCT (g_all.first_name || ' ' || g_all.last_name), ', '), '') AS guest_names,
                   rm.room_number,
                   r.check_in_date,
                   r.check_out_date,
                   r.status,
                   r.total_amount,
                   r.nightly_price,
                   COALESCE(r.guest_count, 1) AS guest_count,
                   COALESCE(array_remove(array_agg(DISTINCT rg_all.guest_id), NULL), ARRAY[]::int[]) AS guest_ids,
                   COALESCE(array_remove(array_agg(DISTINCT (g_all.first_name || ' ' || g_all.last_name)), NULL), ARRAY[]::text[]) AS guest_name_list
            FROM reservations r
            JOIN rooms rm ON r.room_id = rm.id
            LEFT JOIN reservation_guests rg_all ON rg_all.reservation_id = r.id
            LEFT JOIN guests g_all ON g_all.id = rg_all.guest_id
            LEFT JOIN reservation_guests rg_primary ON rg_primary.reservation_id = r.id AND rg_primary.is_primary = TRUE
            GROUP BY r.id, rm.room_number, rg_primary.guest_id
            ORDER BY r.check_in_date DESC, r.id DESC;
            """
        )
        return cursor.fetchall()
    except Error as e:
        _handle_error("Rezervasyon listesi alınırken hata oluştu:", e)
        return []
    finally:
        if conn:
            conn.close()


def room_has_conflict(
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_reservation_id: int | None = None,
    requested_guest_count: int = 1,
) -> bool:
    """Conflict if overlapping CONFIRMED/CHECKED_IN reservations exceed capacity."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT (rt.capacity_adult + rt.capacity_child) AS capacity
            FROM rooms r
            JOIN room_types rt ON r.room_type_id = rt.id
            WHERE r.id = %s;
            """,
            (room_id,),
        )
        cap_row = cursor.fetchone()
        capacity = int(cap_row[0]) if cap_row and cap_row[0] is not None else None
        if capacity is None:
            return True

        params = [room_id]
        exclude_clause = ""
        if exclude_reservation_id is not None:
            exclude_clause = "AND id <> %s"
            params.append(exclude_reservation_id)

        params.extend([check_in, check_out])

        cursor.execute(
            f"""
            SELECT COALESCE(SUM(COALESCE(guest_count, 1)), 0) AS total_guests
            FROM reservations
            WHERE room_id = %s
              AND status IN ('CONFIRMED', 'CHECKED_IN')
              {exclude_clause}
              AND NOT (
                    check_out_date <= %s
                OR  check_in_date >= %s
              );
            """,
            params,
        )
        sum_row = cursor.fetchone()
        total_existing = int(sum_row[0]) if sum_row and sum_row[0] is not None else 0

        proposed_total = total_existing + int(requested_guest_count or 1)
        return proposed_total > capacity

    except Error as e:
        _handle_error("Müsaitlik kontrolü yapılırken hata oluştu:", e)
        return True
    finally:
        if conn:
            conn.close()


def insert_reservation(
    guest_id: int,
    room_id: int,
    check_in: date,
    check_out: date,
    nightly_amount: float,
    guest_ids: list[int] | None = None,
    status: str = "CONFIRMED",
) -> int | None:
    """Inserts a new reservation and writes reservation_guests rows."""
    conn = None
    try:
        nights = (check_out - check_in).days
        if nights <= 0:
            print("Gece sayısı 0 veya negatif olamaz.")
            return None

        guest_ids = guest_ids or ([guest_id] if guest_id else [])
        guest_count = len(guest_ids) if guest_ids else 1
        total_amount = nightly_amount * nights * guest_count

        conn = get_connection()
        cursor = conn.cursor()
        _ensure_guest_count_column(cursor)

        cursor.execute(
            """
            INSERT INTO reservations
                (guest_id, room_id, check_in_date, check_out_date,
                 status, nightly_price, total_amount, guest_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id;
            """,
            (guest_id, room_id, check_in, check_out, status, nightly_amount, total_amount, guest_count),
        )

        new_id = cursor.fetchone()[0]
        _replace_reservation_guests(cursor, new_id, guest_ids, guest_id)

        conn.commit()
        print(f"Yeni rezervasyon eklendi. ID = {new_id}")
        return new_id

    except Error as e:
        _handle_error("Rezervasyon eklenirken hata oluştu:", e)
        if conn:
            conn.rollback()
        return None

    finally:
        if conn:
            conn.close()


def update_reservation(
    reservation_id: int,
    guest_id: int,
    room_id: int,
    check_in: date,
    check_out: date,
    nightly_amount: float,
    guest_ids: list[int] | None = None,
    status: str = "CONFIRMED",
) -> bool:
    """Updates reservation and rewrites reservation_guests."""
    conn = None
    try:
        nights = (check_out - check_in).days
        if nights <= 0:
            print("Gece sayısı 0 veya negatif olamaz.")
            return False

        guest_ids = guest_ids or ([guest_id] if guest_id else [])
        guest_count = len(guest_ids) if guest_ids else 1
        total_amount = nightly_amount * nights * guest_count

        conn = get_connection()
        cursor = conn.cursor()
        _ensure_guest_count_column(cursor)
        cursor.execute(
            """
            UPDATE reservations
            SET guest_id = %s,
                room_id = %s,
                check_in_date = %s,
                check_out_date = %s,
                status = %s,
                nightly_price = %s,
                total_amount = %s,
                guest_count = %s
            WHERE id = %s;
            """,
            (guest_id, room_id, check_in, check_out, status, nightly_amount, total_amount, guest_count, reservation_id),
        )

        _replace_reservation_guests(cursor, reservation_id, guest_ids, guest_id)

        conn.commit()
        print(f"Rezervasyon (id={reservation_id}) güncellendi.")
        return True
    except Error as e:
        _handle_error("Rezervasyon güncellenirken hata oluştu:", e)
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def update_reservation_status(reservation_id: int, new_status: str) -> bool:
    """Updates reservation status."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE reservations
            SET status = %s
            WHERE id = %s;
            """,
            (new_status, reservation_id),
        )
        conn.commit()
        print(f"Rezervasyon (id={reservation_id}) durumu '{new_status}' yapıldı.")
        return True
    except Error as e:
        _handle_error("Rezervasyon durumu güncellenirken hata oluştu:", e)
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
