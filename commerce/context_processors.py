from django.conf import settings
from datetime import datetime

def metadata(request):
    return {
        'site_name': settings.SITE_NAME,
        'year': datetime.today().year,
    }
