
# Django-VazifehBan

## Introduction

Django-VazifehBan is a web application built using Django and the Django REST Framework. This project aims to provide a task management system, enabling users to create, update, and manage tasks and projects.

## Features

- **User Authentication**: Register, login, and manage your user account.
- **Task Management**: Create, update, delete, and view tasks.
- **Project Management**: Organize tasks within projects.
- **RESTful API**: Access and manage resources using RESTful endpoints.

## Project Structure

```
.
├── accounts           # User account management
├── core               # Core functionalities
├── projects           # Project management
├── tasks              # Task management
├── VazifeBan          # Project settings
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## Requirements

- Python 3.x
- Django 4.2.4
- Django REST Framework 3.14.0

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/your_username/Django-VazifehBan.git
    ```

2. Navigate to the project directory:

    ```
    cd Django-VazifehBan
    ```

3. Create a virtual environment and activate it:

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venvScriptsactivate`
    ```

4. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

5. Apply migrations:

    ```
    python manage.py migrate
    ```

6. Run the server:

    ```
    python manage.py runserver
    ```

## Usage

To use the application, navigate to `http://localhost:8000/` in your web browser. You'll find options to manage tasks and projects.

## Contributing

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcomed.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
