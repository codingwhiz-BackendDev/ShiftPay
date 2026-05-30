# PayTrack - Invoice Tracking System

A modern Django-based invoice tracking application that helps freelancers and small businesses manage their invoices, track payments, and get paid faster.

## 🚀 Features

- **User Authentication**: Secure registration, login, and password reset
- **Dashboard**: Real-time overview of your financial status
- **Invoice Management**: Create, track, and manage invoices
- **Client Management**: Organize your clients and their payment history
- **Payment Tracking**: Monitor outstanding, overdue, and paid invoices
- **Analytics**: Visual insights into your revenue trends
- **Email Notifications**: Automated reminders for overdue invoices

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** (recommended) - `python -m venv`

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd PayTrack
```

### Step 2: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install the required packages manually:

```bash
pip install django django-ratelimit
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root (optional but recommended):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@paytrack.ng
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000`

## 🌐 Accessing the Application

- **Home Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
PayTrack/
├── App/                      # Main application directory
│   ├── __init__.py
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Database models
│   ├── tokens.py             # Token generators for email verification
│   ├── urls.py               # App URL patterns
│   └── views.py              # View functions
├── PayTrack/                 # Project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Project URL patterns
│   └── wsgi.py               # WSGI configuration
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── index.css         # Landing page styles
│   │   ├── auth.css          # Authentication page styles
│   │   └── dashboard.css     # Dashboard styles
│   └── js/
│       └── auth.js           # Authentication JavaScript
├── templates/                # HTML templates
│   ├── index.html            # Landing page
│   ├── login.html            # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html        # Dashboard page
│   ├── forgot_password.html  # Password reset request
│   ├── reset_password.html   # Password reset form
│   ├── reset_email_sent.html # Reset email sent confirmation
│   └── reset_result.html     # Password reset result
├── media/                    # User-uploaded files
├── db.sqlite3                # SQLite database (default)
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## 🔐 Authentication System

The application includes a custom authentication system with the following features:

### Registration
- Email-based registration
- Password validation (minimum 8 characters)
- Automatic username generation
- Immediate account activation (no email verification required)

### Login
- Email and password authentication
- Session management
- Rate limiting (10 requests per minute)

### Password Reset
- Email-based password reset
- Secure token-based reset links
- 24-hour token expiration

## 🎨 Customization

### Changing the Secret Key

Generate a new secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Update `SECRET_KEY` in `PayTrack/settings.py`.

### Email Configuration

To enable email notifications, configure the following in `PayTrack/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@paytrack.ng'
```

**Note:** For Gmail, you'll need to use an App Password instead of your regular password.

### Database Configuration

By default, PayTrack uses SQLite. To use PostgreSQL or MySQL:

**PostgreSQL:**
```bash
pip install psycopg2-binary
```

Update `DATABASES` in `PayTrack/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paytrack_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'django-ratelimit'

```bash
pip install django-ratelimit
```

### RuntimeError: Model class doesn't declare an explicit app_label

Ensure all apps are properly listed in `INSTALLED_APPS` in `PayTrack/settings.py`.

### Static files not loading

Run the following command:
```bash
python manage.py collectstatic
```

### Email not sending

- Check your email configuration in settings.py
- Verify your email provider's SMTP settings
- For Gmail, use an App Password instead of your regular password

## 📝 Development

### Running Tests

```bash
python manage.py test
```

### Creating New Models

```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell

```bash
python manage.py shell
```

## 🚀 Deployment

### Production Settings

1. Set `DEBUG = False` in `PayTrack/settings.py`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set up a production web server (Gunicorn + Nginx)

### Environment Variables

Use environment variables for sensitive information:

```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please open an issue on the repository.

## 🙏 Acknowledgments

- Django Framework
- Django Ratelimit
- All contributors and users of PayTrack

---

**Built with ❤️ using Django**
