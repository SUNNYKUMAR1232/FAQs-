# Multilingual FAQ API

A Django-based FAQ management system with multilingual support, caching, and REST API.

## Features

- Multilingual FAQ support (English, Hindi, Bengali)
- Cached API responses for improved performance
- Admin interface for content management
- Comprehensive test coverage
- Docker support for easy deployment

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/multilingual-faq-api.git

    cd multilingual-faq-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

## Usage

Running the Development Server

```bash
python manage.py runserver
```

## API Endpoints

- List FAQs (default language: English):

    ```bash
    GET /api/faqs/
    ```

- List FAQs in specific language:

    ```bash
    GET /api/faqs/?lang=hi  # Hindi
    GET /api/faqs/?lang=bn  # Bengali
    ```

## Admin Interface

Access the admin interface at [http://localhost:8000/admin](http://localhost:8000/admin) to manage FAQ content.

## Development

### Running Tests

```bash
pytest
```

### Code Quality

We use flake8 for code quality checks:

```bash
flake8 .
```

### Docker Support

1. Build the image:

    ```bash
    docker-compose build
    ```

2. Run the containers:

    ```bash
    docker-compose up
    ```

## Contributing

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'feat: Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

### License

This project is licensed under the MIT License - see the LICENSE file for details.