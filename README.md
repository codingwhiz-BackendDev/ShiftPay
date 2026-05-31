# ShiftPay — AI-Powered Salary Advances for Nigerian Gig Workers

ShiftPay is a Django-based platform that provides instant salary advances to Nigerian gig workers using AI-powered trust scoring. Workers can log their shifts, build a trust score, and receive advances based on their earnings history — no collateral required.

## 🚀 Features

- **User Authentication**: Secure registration with job type, phone number, and daily earnings
- **Shift Logging**: Track daily work hours, earnings, and job descriptions
- **AI Trust Score**: Machine learning-powered scoring based on shift patterns and earnings consistency
- **Instant Advance Requests**: Request salary advances with AI-powered approval decisions
- **Multiple Payout Methods**: OPay, PalmPay, Bank Transfer, or Cash Agent pickup
- **Repayment Scheduling**: Automatic 14-day repayment with 10% flat fee
- **AI Earnings Insights**: Daily personalized insights powered by Google Gemini AI
- **Dashboard**: Real-time overview of shifts, earnings, trust score, and eligibility
- **Mobile-First Design**: Optimized for gig workers who use smartphones

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
pip install django google-generativeai python-decouple
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
```

**Important:** Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

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

- **Landing Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Log Shift**: http://127.0.0.1:8000/shift/log/
- **Request Advance**: http://127.0.0.1:8000/advance/request/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
PayTrack/
├── App/                      # Main application directory
│   ├── __init__.py
│   ├── admin.py              # Django admin configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Database models (WorkerProfile, ShiftLog, AdvanceRequest, RepaymentSchedule)
│   ├── urls.py               # App URL patterns
│   └── views.py              # View functions (dashboard, log_shift, advance_request, AI insights)
├── PayTrack/                 # Project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Project URL patterns
│   └── wsgi.py               # WSGI configuration
├── static/                   # Static files (CSS, JS, images)
│   └── css/
│       ├── index.css         # Landing page styles
│       ├── auth.css          # Authentication page styles
│       └── dashboard.css     # Dashboard styles
├── templates/                # HTML templates
│   ├── index.html            # ShiftPay landing page
│   ├── login.html            # Login page
│   ├── register.html         # Registration page with ShiftPay fields
│   ├── dashboard.html        # Worker dashboard with AI insights
│   ├── advance_request.html  # Advance request form with payout methods
│   └── advance_result.html   # AI decision result page
├── media/                    # User-uploaded files
├── db.sqlite3                # SQLite database (default)
├── manage.py                 # Django management script
└── .env                      # Environment variables (GEMINI_API_KEY)
```

## 🔐 Authentication System

The application includes a custom authentication system with the following features:

### Registration
- Email-based registration with full name
- Job type selection (Uber/Bolt Driver, Bus Driver, Market Trader, Artisan, Delivery Rider, Other)
- Phone number collection
- Daily average earnings input
- Password validation (minimum 8 characters)
- Automatic WorkerProfile creation

### Login
- Email and password authentication
- Session management
- Redirects logged-in users to dashboard

## 🤖 AI Features

### Gemini AI Integration
- **Advance Decision AI**: Uses Google Gemini (gemini-1.5-flash) to make instant, fair advance approval decisions
- **Earnings Insight AI**: Generates daily personalized insights based on shift patterns and earnings data
- **Warm, Human-like Responses**: AI is configured to speak like it understands Nigerian gig worker hustle

### Trust Score Calculation
- Base score of 50 points
- Bonus points for total shifts logged (+10 for 3+ shifts, +15 for 5+ shifts)
- Earnings stability bonus (within 30% of daily average)
- Volume bonus (if earnings today > daily average)
- Hackathon mode: No penalty for gaps between shifts (allows same-day logging)

### Eligibility Requirements (Hackathon Mode)
- **Minimum 3 shifts logged** (down from 5 for hackathon)
- **Trust score of 50+** (down from 60 for hackathon)
- **Max advance amount**: 50% of last 7 days earnings

## 🗺️ Roadmap

### Phase 1 — Manual shift logging with AI trust score
**Status: Live Now**

- Workers manually log their shifts with hours, earnings, and job descriptions
- AI calculates trust score based on shift patterns and earnings consistency
- Instant advance decisions powered by Gemini AI
- Multiple payout methods (OPay, PalmPay, Bank Transfer, Cash Agent)
- Repayment scheduling with automatic daily deductions

### Phase 2 — Bolt and Uber API integration for automatic verified earnings
**Status: Planned**

- Direct API integration with ride-hailing platforms
- Automatic earnings verification and import
- Reduced fraud risk with verified data
- Faster trust score building
- Real-time earnings tracking

### Phase 3 — Licensed microfinance partner integration for real capital deployment
**Status: Planned**

- Partnership with licensed Nigerian microfinance institutions
- Real capital deployment for advances
- Regulatory compliance and licensing
- Larger advance amounts with institutional backing
- Credit bureau integration for broader financial inclusion

### Phase 4 — USSD version for workers without smartphones
**Status: Planned**

- USSD-based interface for feature phone users
- Voice and SMS support for accessibility
- Expanded reach to underserved workers
- Offline capability for areas with poor connectivity
- Agent network for cash-in/cash-out services

## 🎨 Customization

### Changing the Secret Key

Generate a new secret key:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Update `SECRET_KEY` in `PayTrack/settings.py` or `.env` file.

### Database Configuration

By default, ShiftPay uses SQLite. To use PostgreSQL or MySQL:

**PostgreSQL:**
```bash
pip install psycopg2-binary
```

Update `DATABASES` in `PayTrack/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shiftpay_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'google.generativeai'

```bash
pip install google-generativeai
```

### Gemini API Error

- Verify your `GEMINI_API_KEY` in `.env` file
- Check that the API key is valid and has credits
- The app has fallback logic to auto-approve if API fails

### Trust Score Not Updating

- Ensure you're logging shifts with valid hours and earnings
- Check that the WorkerProfile is created for the user
- Try logging 3+ shifts to see the trust score increase

### Advance Request Not Approved

- Ensure you have logged at least 3 shifts
- Check that your trust score is 50+
- Verify your last 7 days earnings are sufficient

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
6. Secure your environment variables

### Environment Variables

Use environment variables for sensitive information:

```python
import os
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
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
- Google Gemini AI
- Bootstrap 5
- All contributors and users of ShiftPay

---

**Built with ❤️ using Django & Google Gemini AI**
