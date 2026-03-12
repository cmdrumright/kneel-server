import sqlite3
import json


def list_orders():
    """Run query to get all orders and return serialized results"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT * FROM Orders
            """)
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            orders.append(dict(row))

        serialized_orders = json.dumps(orders)

    return serialized_orders


def get_single_order(pk):
    """Run query to get a single order and return serialized result"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT * FROM Orders WHERE id = ?
            """,
            (pk,),
        )
        query_results = db_cursor.fetchone()
        serialized_order = json.dumps(dict(query_results))

    return serialized_order
