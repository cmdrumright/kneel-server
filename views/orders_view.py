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


def list_orders(url):
    """Run query to get all orders and return serialized results"""
    # Initialize query strings
    select_string = """
        SELECT
            o.id,
            o.size_id,
            o.style_id,
            o.metal_id"""
    from_string = """
        FROM Orders o
        """
    if "_expand" in url["query_params"]:
        for value in url["query_params"]["_expand"]:
            if value == "size":
                select_string += """,
                    si.carets,
                    si.price as size_price"""
                from_string += """
                    JOIN sizes si
                        ON si.id = o.size_id
                    """
            if value == "metal":
                select_string += """,
                    m.metal,
                    m.price as metal_price"""
                from_string += """
                    JOIN metals m
                        ON m.id = o.metal_id
                    """
            if value == "style":
                select_string += """,
                    st.style,
                    st.price as style_price"""
                from_string += """
                    JOIN styles st 
                        ON st.id = o.style_id
                    """

    query_string = select_string + from_string

    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(query_string)
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            order = {
                "id": row["id"],
                "size_id": row["size_id"],
                "style_id": row["style_id"],
                "metal_id": row["metal_id"],
            }
            if "_expand" in url["query_params"]:
                for value in url["query_params"]["_expand"]:
                    if value == "size":
                        order["size"] = {
                            "carets": row["carets"],
                            "price": row["size_price"],
                        }
                    if value == "style":
                        order["style"] = {
                            "style": row["style"],
                            "price": row["style_price"],
                        }
                    if value == "metal":
                        order["metal"] = {
                            "metal": row["metal"],
                            "price": row["metal_price"],
                        }
            orders.append(order)

        serialized_orders = json.dumps(orders)

    return serialized_orders


def get_single_order(url):
    """Run query to get a single order and return serialized result"""
    # Initialize query strings
    select_string = """
        SELECT
            o.id,
            o.size_id,
            o.style_id,
            o.metal_id"""
    from_string = """
        FROM Orders o
        """
    where_string = """
        WHERE o.id = ?
        """

    if "_expand" in url["query_params"]:
        for value in url["query_params"]["_expand"]:
            if value == "size":
                select_string += """,
                    si.carets,
                    si.price as size_price"""
                from_string += """
                    JOIN sizes si
                        ON si.id = o.size_id
                    """
            if value == "metal":
                select_string += """,
                    m.metal,
                    m.price as metal_price"""
                from_string += """
                    JOIN metals m
                        ON m.id = o.metal_id
                    """
            if value == "style":
                select_string += """,
                    st.style,
                    st.price as style_price"""
                from_string += """
                    JOIN styles st 
                        ON st.id = o.style_id
                    """

    query_string = select_string + from_string + where_string

    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            query_string,
            (url["pk"],),
        )
        row = db_cursor.fetchone()
        order = {
            "id": row["id"],
            "size_id": row["size_id"],
            "style_id": row["style_id"],
            "metal_id": row["metal_id"],
        }
        if "_expand" in url["query_params"]:
            for value in url["query_params"]["_expand"]:
                if value == "size":
                    order["size"] = {
                        "carets": row["carets"],
                        "price": row["size_price"],
                    }
                if value == "style":
                    order["style"] = {
                        "style": row["style"],
                        "price": row["style_price"],
                    }
                if value == "metal":
                    order["metal"] = {
                        "metal": row["metal"],
                        "price": row["metal_price"],
                    }
        serialized_order = json.dumps(dict(order))

    return serialized_order
