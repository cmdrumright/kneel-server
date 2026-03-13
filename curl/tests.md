# Endpoints

## /orders

### GET

```bash
curl 'http://localhost:8000/orders' | jq

curl 'http://localhost:8000/orders/1' | jq

```

### POST

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"metalId":1,"styleId":1,"sizeId":1}' \
  'http://localhost:8000/orders'
```
