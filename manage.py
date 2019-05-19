#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == 'doit':
        os.system('pip3 install -r requirements.txt')
        os.system('python3 manage.py makemigrations --empty spis_tel')
        os.system('python3 manage.py loaddata fixture.json')
        os.system('python3 manage.py migrate')
        os.system('python3 manage.py runserver')
    execute_from_command_line(sys.argv)
