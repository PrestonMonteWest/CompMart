from django.contrib.auth.decorators import login_required as log_req

def login_required(function=None, *args, **kwargs):
    if function:
        func = log_req(function=function, *args, **kwargs)
        func.login_required = True
    else:
        func = log_req(*args, **kwargs)

    return func
