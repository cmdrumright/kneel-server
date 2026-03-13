import sqlite3


def update_metal(id, metal_data):
    """Take metal id and new metal_data, execute query to updated metal data, return true if success or false if error"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            UPDATE Metals
                SET
                    metal = ?,
                    price = ?
            WHERE id = ?
            """,
            (metal_data["metal"], metal_data["price"], id),
        )
    return True if db_cursor.rowcount > 0 else False
