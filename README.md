# Vendor Management System API

This is a Django-based Vendor Management System that allows users

## Requirements

- Python 3.10.12

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Salmanulhamdan/Vendor-Management-System.git
    ```


2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv env
    # On Windows: env\Scripts\activate
    # On macOS/Linux: source env/bin/activate
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python3 manage.py migrate
    ```

5.Create a superuser (for accessing the Django admin):

        ```bash
        python manage.py createsuperuser
        ```
        username:admin
        password:1234


6. Run the development server:

    ```bash
    python3 manage.py runserver
    ```

7. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)





## API Endpoints

### Vendor Profile Management
```POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.```
