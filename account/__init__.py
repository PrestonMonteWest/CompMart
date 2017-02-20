from django.contrib.auth.decorators import login_required as log_req

def login_required(view, **kwargs):
    view = log_req(view, **kwargs)
    view.login_required = True
    return view
