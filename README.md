# DIRECTIVE FOR RUNNING THE PROJECT

All the packages use during the implementation are listed in the requirement.txt data with their
corresponding version. Since virtual environments can go beyond lot of GB of data, the venv of the project is not pushed into Github and a virtual env. need to be created and the packages need to be installed inside.

---

##### CREATION OF VIRTUAL ENVIRONMENT AND PACKAGE INSTALLATION (windows)

#### 1. creation of venv

    - python -m venv ["name of the virtual env"] (for Windows users)
    - python3 -m venv ["name of the virtual env"] (for MAC or Linux users)
    e.x. : python -m venv join_venv

#### 2. activation of venv

    - .\join_venv\Scripts\activate and press ENTER    (for Windows users)
    - source join_venv/bin/activate and press ENTER (for MAC or Linux users)

#### 3. Install the packages from requirements.txt

    - pip install -r requirements.txt

Now we need to create a DB with the models define in all apps inside the project
Please notice that a project need to be structured in different apps for simplicity and re-usability.

PLEASE BUILDING THE DB WITH THE COMMAND : "python manage.py makemigrations" IS NOT CORRECT since the project is already build with apps inside python need to know with app he need to run the migrations for. Otherwise a standard DB will be created and only the USER Table will be created.

Notice that in the app : join_auth_permission the method "def save()" of the Class RegistrationSerializer contains a Contact instance to create a Contact with the name of the user who signed up. If the Contact table is not there then the user will be created from the User Table but the contact part will throw a 500 SERVER ERROR.

For the sake of experiment let's do it:

#### 1. Creation of DB and migration

    - python manage.py makemigrations join_app join_auth_permission
    - python manage.py migrate

#### START OF THE DEVELOPMENT SERVER

    - python manage.py runserver

## API Documentation (join_auth_permission)

This documentation describes the endpoints and functionality of the Django application. The application provides user management, authentication, and password reset capabilities.

## Table of Contents

1. [Endpoints Overview](#endpoints-overview)
2. [Endpoints Details](#endpoints-details)
   - [Users List](#users-list)
   - [User Detail](#user-detail)
   - [Registration](#registration)
   - [Login](#login)
   - [Guest Login](#guest-login)
   - [Password Reset Request](#password-reset-request)
   - [Password Reset Confirm](#password-reset-confirm)

---

## Endpoints Overview

| URL                        | Method           | Description                                                   |
| -------------------------- | ---------------- | ------------------------------------------------------------- |
| `/users/`                  | GET              | Retrieve a list of users (Admin only).                        |
| `/users/<int:pk>/`         | GET, PUT, DELETE | Retrieve, update, or delete a user (Owner/Admin permissions). |
| `/register/`               | POST             | Register a new user.                                          |
| `/login/`                  | POST             | Login a user and generate an authentication token.            |
| `/guest-login/`            | POST             | Login as a guest user.                                        |
| `/password-reset-request/` | POST             | Request a password reset link.                                |
| `/password-reset-confirm/` | POST             | Reset the password using the reset link.                      |

---

## Endpoints Details

### **Users List**

- **URL:** `/users/`
- **Method:** `GET`
- **Description:** Retrieve a list of all registered users. Accessible only by admin users.
- **Permissions:** `IsAdminUser`
- **Response:** JSON list of users.

---

### **User Detail**

- **URL:** `/users/<int:pk>/`
- **Methods:** `GET`, `PUT`, `DELETE`
- **Description:** Retrieve, update, or delete a specific user.
  - **GET:** Accessible to the user themselves or an admin.
  - **PUT/DELETE:** Restricted to the user themselves.
- **Permissions:** `IsOwnerOrReadOnlyIfAdmin`
- **Response:**
  - **GET:** User details as JSON.
  - **PUT:** Updated user details as JSON.
  - **DELETE:** Confirmation message.

---

### **Registration**

- **URL:** `/register/`
- **Method:** `POST`
- **Description:** Create a new user account.
- **Permissions:** `AllowAny`
- **Request Payload:**
  ```json
  {
    "name": "string",
    "email": "string",
    "password": "string",
    "confirm_password": "string"
  }
  ```
  **Response**:
  ```json
  {
    "token": "string",
    "username": "string",
    "email": "string"
  }
  ```

### **Login**

- **URL:** `/login/`
- **Method:** `POST`
- **Description:** Authenticate a user and return a token.
- **Permissions:** `AllowAny`
- **Request Payload:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
  **Response**:
  ```json
  {
    "token": "string",
    "email": "string",
    "password": "string",
    "is_guest": false
  }
  ```

### **Guest Login**

- **URL:** `/guest-login/`
- **Method:** `POST`
- **Description:** Create a temporary guest user account and authenticate.
- **Permissions:** `AllowAny`
  **Response**:
  ```json
  {
    "token": "string",
    "email": "string",
    "first_name": "Guest",
    "is_guest": true
  }
  ```

### **Password Reset Request**

- **URL:** `/password-reset-request/`
- **Method:** `POST`
- **Description:**Request a password reset link to be sent to the user's email.
- **Permissions:** `AllowAny`
- **Request Payload:**
  ```json
  {
    "email": "string"
  }
  ```
  **Response**:
  ```json
  {
    "message": "Password reset link sent to your email!"
  }
  ```

### **Password Reset Confirm**

- **URL:** `/password-reset-confirm/`
- **Method:** `POST`
- **Description:** Reset the password using the reset link.
- **Permissions:** `AllowAny`
- **Request Payload:**

  ```json
  {
    "token": "string",
    "new_password": "string"
  }
  ```

  **Response**:

  ```json
  {
    "message": "Password successfully reset!"
  }
  ```

# API Documentation (join_app)

This document provides a detailed description of the API endpoints and their corresponding views in my Django project. The endpoints are categorized based on their functionalities, such as user accounts, contacts, categories, subtasks, and tasks.

---

## Endpoints

### User Accounts

1. **List User Accounts**  
   **`GET /accounts/`**

   - **Description**: Returns a list of user accounts.
   - **Permissions**: Authenticated users.
   - **Notes**:
     - Superusers can view all user accounts.
     - Regular users can view only their account details.

2. **Retrieve/Update/Delete User Account**  
   **`GET/PUT/DELETE /accounts/<int:pk>/`**

   - **Description**: Retrieves, updates, or deletes a user account by ID.
   - **Permissions**: Authenticated users who are either the account owner or superusers.

3. **User-Specific Account Details**  
   **`GET /users/accounts/<int:pk>/`**
   - **Description**: Retrieves details of a specific user account.
   - **Permissions**: Authenticated users who are either the account owner or superusers.

---

### Contacts

1. **List/Create Contacts**  
   **`GET/POST /contacts/`**

   - **Description**:
     - `GET`: Lists contacts of the authenticated user. Superusers see all contacts.
     - `POST`: Creates a new contact for the authenticated user.
   - **Permissions**: Authenticated users.

2. **Retrieve/Update/Delete Contact**  
   **`GET/PUT/DELETE /contacts/<int:pk>/`**
   - **Description**: Retrieves, updates, or deletes a contact by ID.
   - **Permissions**: Authenticated users with object-specific permissions.

---

### Categories

1. **List Categories**  
   **`GET /categories/`**

   - **Description**: Lists all available categories. Only superusers can modify categories.
   - **Permissions**: Authenticated users.

2. **Retrieve/Update/Delete Category**  
   **`GET/PUT/DELETE /categories/<int:pk>/`**

   - **Description**: Retrieves, updates, or deletes a category by ID.
   - **Permissions**: Superusers or users with object-specific permissions.

3. **Category Options**  
   **`GET /category_options/`**
   - **Description**: Retrieves predefined category options.
   - **Permissions**: Open to all users (no authentication required).

---

### Subtasks

1. **List Subtasks**  
   **`GET /subtasks/`**

   - **Description**: Lists all subtasks for the authenticated user. Superusers see all subtasks.
   - **Permissions**: Authenticated users.

2. **Retrieve/Update/Delete Subtask**  
   **`GET/PUT/DELETE /subtasks/<int:pk>/`**

   - **Description**: Retrieves, updates, or deletes a subtask by ID.
   - **Permissions**: Authenticated users with object-specific permissions.

3. **User-Specific Subtasks**  
   **`GET /users/subtasks/<int:author>/`**
   - **Description**: Lists subtasks created by a specific user.
   - **Permissions**: Authenticated users or superusers.

---

### Tasks

1. **List/Create Tasks**  
   **`GET/POST /tasks/`**

   - **Description**:
     - `GET`: Lists tasks for the authenticated user. Superusers see all tasks.
     - `POST`: Creates a new task for the authenticated user.
   - **Permissions**: Authenticated users.

2. **Retrieve/Update/Delete Task**  
   **`GET/PUT/DELETE /tasks/<int:pk>/`**
   - **Description**: Retrieves, updates, or deletes a task by ID.
   - **Permissions**: Authenticated users with object-specific permissions.

---

## View Comments and Details

### AccountsView

- **Description**: Provides a list of user accounts based on user permissions.
- **Notes**: Unauthorized users attempting to access other accounts receive a 401 error.

### AccountsDetail

- **Description**: Allows retrieving, updating, or deleting a single user account. Restricted to owners or superusers.

### ContactList

- **Description**: Lists or creates contacts. Regular users can only access their contacts, while superusers see all contacts.

### ContactDetail

- **Description**: Provides detailed operations for a single contact, including retrieval, updates, and deletion.

### CategoryList

- **Description**: Lists all available categories. Categories are managed by superusers.

### CategoryDetail

- **Description**: Detailed operations for categories, including retrieval, updates, and deletion.

### CategoryOptionList

- **Description**: Provides predefined category options. Open to all users without authentication.

### SubtaskList

- **Description**: Lists subtasks associated with the authenticated user. Subtasks are created via tasks.

### SubtaskDetail

- **Description**: Detailed operations for subtasks, including retrieval, updates, and deletion.

### TaskList

- **Description**: Lists tasks associated with the authenticated user or creates new tasks.

### TaskDetail

- **Description**: Detailed operations for tasks, including retrieval, updates, and deletion.

---

## Notes

- **Permission Classes**:

  - `IsAuthenticated`: Ensures the user is authenticated.
  - `IsAuthenticatedOrNot`: Custom permission for object-specific access.
  - `AllowAny`: No restrictions; open to all users.
  - `IsAdminUser`: Grants access to superusers.
  - `IsUserAccount`: Custom permission for user account access.

- **Error Handling**:
  - Unauthorized users attempting restricted actions will receive `401 Unauthorized` or `403 Forbidden` responses.
  - Objects not found will return `404 Not Found`.

---
