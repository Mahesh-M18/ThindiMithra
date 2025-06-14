# Tindimithra - Cloud Kitchen Platform

Tindimithra is a Django-based cloud kitchen platform that connects home chefs with customers. It allows chefs to showcase their culinary skills and customers to discover and order delicious home-cooked meals.

## Features

- User Authentication (Chef/Customer)
- Dish Management for Chefs
- Order Management
- Subscription System
- Review and Rating System
- Search and Filter Functionality
- Payment Integration

## Tech Stack

- Python 3.12
- Django 5.2
- Bootstrap 5
- SQLite (Development)
- PostgreSQL (Production)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tindimithra.git
cd tindimithra
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
tindimithra/
├── manage.py
├── requirements.txt
├── tindimithra/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── meals/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
└── templates/
    ├── base.html
    ├── home.html
    ├── users/
    └── meals/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/tindimithra 