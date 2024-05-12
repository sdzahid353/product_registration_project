from product_registration_project.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }
}
