# Inventory Management API

This is a Django REST Framework API for managing inventory items and transactions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Api_pro
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Inventory Items

- **GET /api/inventory/items/** - List all inventory items
  - Query params:
    - `product_id`: Filter by product ID
    - `low_stock=true`: Filter low stock items
  - Example request:
    ```bash
    curl -X GET "http://localhost:8000/api/inventory/items/?low_stock=true"
    ```
  - Example response (200 OK):
    ```json
    {
      "count": 2,
      "results": [
        {
          "id": 1,
          "product_id": "123",
          "name": "Product A",
          "quantity": 5,
          "price": 9.99
        },
        {
          "id": 2,
          "product_id": "124",
          "name": "Product B",
          "quantity": 3,
          "price": 14.99
        }
      ]
    }
    ```

- **POST /api/inventory/items/** - Create new inventory item
  - Example request:
    ```bash
    curl -X POST "http://localhost:8000/api/inventory/items/" \
      -H "Content-Type: application/json" \
      -d '{"product_id":"125","name":"Product C","quantity":20,"price":19.99}'
    ```
  - Example response (201 Created):
    ```json
    {
      "id": 3,
      "product_id": "125",
      "name": "Product C",
      "quantity": 20,
      "price": 19.99
    }
    ```
  - Error response (400 Bad Request):
    ```json
    {
      "product_id": ["This field is required."],
      "quantity": ["This field must be a positive integer."]
    }
    ```

- **GET /api/inventory/items/{id}/** - Retrieve specific item
  - Example request:
    ```bash
    curl -X GET "http://localhost:8000/api/inventory/items/1/"
    ```
  - Example response (200 OK):
    ```json
    {
      "id": 1,
      "product_id": "123",
      "name": "Product A",
      "quantity": 5,
      "price": 9.99
    }
    ```

- **PUT/PATCH /api/inventory/items/{id}/** - Update item
  - Example PUT request:
    ```bash
    curl -X PUT "http://localhost:8000/api/inventory/items/1/" \
      -H "Content-Type: application/json" \
      -d '{"quantity":10,"price":12.99}'
    ```
  - Example response (200 OK):
    ```json
    {
      "id": 1,
      "product_id": "123",
      "name": "Product A",
      "quantity": 10,
      "price": 12.99
    }
    ```

- **DELETE /api/inventory/items/{id}/** - Delete item
  - Example request:
    ```bash
    curl -X DELETE "http://localhost:8000/api/inventory/items/1/"
    ```
  - Example response (204 No Content):
    ```
    ""
    ```

### Inventory Transactions

- **GET /api/inventory/transactions/** - List all transactions
  - Query params:
    - `item_id`: Filter by inventory item ID
  - Example request:
    ```bash
    curl -X GET "http://localhost:8000/api/inventory/transactions/?item_id=1"
    ```
  - Example response (200 OK):
    ```json
    {
      "count": 2,
      "results": [
        {
          "id": 1,
          "item_id": 1,
          "transaction_type": "PURCHASE",
          "quantity_change": 5,
          "timestamp": "2023-01-01T12:00:00Z"
        },
        {
          "id": 2,
          "item_id": 1,
          "transaction_type": "SALE",
          "quantity_change": -2,
          "timestamp": "2023-01-02T12:00:00Z"
        }
      ]
    }
    ```

- **POST /api/inventory/transactions/** - Create new transaction
  - Example request:
    ```bash
    curl -X POST "http://localhost:8000/api/inventory/transactions/" \
      -H "Content-Type: application/json" \
      -d '{"item_id":1,"transaction_type":"PURCHASE","quantity_change":5}'
    ```
  - Example response (201 Created):
    ```json
    {
      "id": 3,
      "item_id": 1,
      "transaction_type": "PURCHASE",
      "quantity_change": 5,
      "timestamp": "2023-01-03T12:00:00Z"
    }
    ```

### Bulk Operations

- **POST /api/inventory/update/** - Bulk update inventory
  - Request body format:
    ```json
    {
      "product_id": "123",
      "quantity_change": 5,
      "transaction_type": "PURCHASE"
    }
    ```

- **POST /api/inventory/upload/** - Upload CSV file
  - Example CSV file (save as `inventory.csv`):
    ```csv
    product_id,name,quantity,price
    123,Product A,100,9.99
    124,Product B,50,14.99
    125,Product C,75,19.99
    ```
  - Example request:
    ```bash
    curl -X POST "http://localhost:8000/api/inventory/upload/" \
      -H "Content-Type: multipart/form-data" \
      -F "file=@inventory.csv"
    ```
  - Example response (200 OK):
    ```json
    {
      "message": "3 items processed successfully",
      "errors": []
    }
    ```
  - Error response (400 Bad Request):
    ```json
    {
      "message": "1 item processed, 2 errors",
      "errors": [
        "Row 2: Invalid quantity value",
        "Row 3: Missing product_id"
      ]
    }
    ```

### Reports

- **GET /api/inventory/report/** - Get inventory summary
  - Returns:
    - Total items count
    - Total quantity
    - Low stock count
    - Recent transactions

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

## Testing

Run tests with:
```bash
python manage.py test
```