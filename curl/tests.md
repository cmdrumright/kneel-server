# Endpoints

## /orders

### GET

```bash
curl -v 'http://localhost:8000/orders' | jq

curl 'http://localhost:8000/orders/1' | jq

```

### POST

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"metalId":1,"styleId":1,"sizeId":1}' \
  'http://localhost:8000/orders'
```

### DELETE

```bash
curl -v --header "Content-Type: application/json" \
  --request DELETE \
  'http://localhost:8000/orders/9' | jq
```

## /metals

### PUT

```bash
curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"id":1,"metal":"Sterling Silver","price":12.34}' \
  'http://localhost:8000/metals/1'
```
