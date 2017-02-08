from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime

def metadata(request):
    return {
        'site_name': get_current_site(request).name,
        'year': datetime.today().year,
    }
