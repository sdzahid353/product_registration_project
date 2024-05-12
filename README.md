# Product Registration Project

This README provides information on how to interact with the project APIs and perform basic operations such as user registration, login, and product management.

## Prerequisites
- Python (>=3.7)
- Django (>=3.0)
- Django Rest Framework (>=3.12)

### Running the Server
To start the Django server, run the following command:
  ```bash
  python manage.py runserver
  ```



### User Authentication
#### User Login
- Endpoint: `http://127.0.0.1:8000/user/login/`
- Method: POST
- Payload:
  ```json
  {
      "username": "user1",
      "password": "password1"
  }
  ```


#### User Registartion
- Endpoint: `http://127.0.0.1:8000/user/register/`
- Method: POST
- Payload:
  ```json
  {
    "username": "user2",
    "password": "password2"
  }
  ```

All product-related APIs require authentication using a JWT token. After login, copy the access token from the response. Add the token in the header of product APIs as `Authorization: Bearer <token>` for authentication.


### Product APIs
#### List Products
- Endpoint: `http://127.0.0.1:8000/product/products/`
- Method: GET
- Sample Response:
  ```json
  {
    "count": 7,
    "next": "http://127.0.0.1:8000/product/products/?page_size=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Product A",
            "description": "This is a sample product description.",
            "manufacturer": "Manufacturer X",
            "serial_number": "SN123456",
            "date_of_manufacture": "2024-05-07",
            "warranty_information": "1.5 year",
            "category": "Electronics"
        },
        // Other products...
    ]
  }
  ```


#### Register Product
- Endpoint: `http://127.0.0.1:8000/product/products/register/`
- Method: POST
- Payload:
  ```json
  {
    "name": "Product T",
    "description": "Description of Product T",
    "manufacturer": "Manufacturer T",
    "serial_number": "98732113345",
    "date_of_manufacture": "2023-06-06",
    "warranty_information": "Limited lifetime warranty",
    "category": "Category T"
  }
  ```
  

#### Get Single Product
- Endpoint: `http://127.0.0.1:8000/product/products/<int:pk>/`
- Method: GET
- Sample Response:
  ```json
  {
    "id": 3,
    "name": "Product C",
    "description": "Description of Product C",
    "manufacturer": "Manufacturer C",
    "serial_number": "456123789",
    "date_of_manufacture": "2024-05-03",
    "warranty_information": null,
    "category": "Category C"
  }
  ```

#### Update Product
- Endpoint: `http://127.0.0.1:8000/product/products/<int:pk>/`
- Method: PUT or PATCH
- Payload:
  ```json
  {
    "name": "Product E2",
    "description": "Description of Product E2",
    "warranty_information": "Limited lifetime warranty",
    "category": "Category E2"
  }
  ```


#### Delete Product
- Endpoint: `http://127.0.0.1:8000/product/products/<int:pk>/`
- Method: DELETE
- Sample Response:
  ```json
  {
    "message": "Product Deleted"
  }
  ```

#### Query Parameters

Products can be filtered using query parameters. For example:

- `http://127.0.0.1:8000/product/products/?manufacturer=Manufacturer C`
- `http://127.0.0.1:8000/product/products/?name=product&manufacturer=manufacturer B&category=Category B`


### Testing
To run tests, ensure you have two terminals open: one for running the Django server and another for testing.

Note: There is no need to run Django server while unit testing. The two terminals are to setup the two different environments for server and testing.

#### Setting Up Test Environment
Before running tests, set the test settings using the following command in the testing terminal:
```bash
export DJANGO_SETTINGS_MODULE=tests.tests_settings
```

#### Running Tests
For normal testing, use the following command:
```bash
pytest -v
```

For comprehensive code coverage, use the following command:
```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```


### Database Backup
To back up the SQLite database, use the following command:
```bash
python manage.py backup_db
```
