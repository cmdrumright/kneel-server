import sqlite3
import json


def create_order(order_data):
    """Take new order_data and run query to insert it"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                INSERT INTO Orders VALUES (null, ?, ?, ?)
                """,
            (order_data["metalId"], order_data["styleId"], order_data["sizeId"]),
        )

    return True if db_cursor.rowcount > 0 else False


def delete_order(pk):
    """Take an order id and execute query to remove that entry from orders table"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            DELETE FROM Orders WHERE id = ?
            """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_orders():
    """Run query to get all orders and return serialized results"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT * FROM Orders
            """
        )
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
