# kneel-server

API Server for Kneel Diamonds front-end written in Python and using an sqlite database.

## Learning

### How to setup and seed a database

[kneeldiamonds.sql](./kneeldiamonds.sql)

### How to open a slqite connection and get rows

```py
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

```

### How to fetch a single row from a table

The `,` after the pk in the sql parameters seems to be necessary. Maybe because parameters needs to be a list.

```py
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
```

### How to insert a row to a table

```py
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
```

### How to delete a row from a table

```py
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
```

### How to updated a row

```py
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
```

## Joining tables to expand foreign keys

```py
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
```

### Using curl to test API

GET

```bash
curl 'http://localhost:8000/orders' | jq

curl 'http://localhost:8000/orders/1' | jq

curl -v 'http://localhost:8000/orders?_expand=metal&_expand=size&_expand=style' | jq

curl -v 'http://localhost:8000/orders/1?_expand=metal&_expand=size&_expand=style' | jq
```

POST

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"metalId":1,"styleId":1,"sizeId":1}' \
  'http://localhost:8000/orders'
```

DELETE

```bash
curl -v --header "Content-Type: application/json" \
  --request DELETE \
  'http://localhost:8000/orders/9' | jq
```

PUT

```bash
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"id":1,"metal":"Sterling Silver","price":12.34}' \
  'http://localhost:8000/metals/1'
```
