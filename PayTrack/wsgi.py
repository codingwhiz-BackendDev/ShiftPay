import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PayTrack.settings')

# Auto-migrate on startup so Neon tables are created automatically
try:
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb', verbosity=0)
    print("Migrations complete")
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()
