from django.conf import settings
from datetime import datetime

def site_data(request):
    return {
        'site_name': settings.SITE_NAME,
        'year': datetime.today().year,
    }
