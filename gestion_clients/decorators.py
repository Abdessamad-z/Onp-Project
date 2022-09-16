from django.shortcuts import redirect
from django.shortcuts import redirect
from django.contrib import messages


def is_auth(fnc):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "Vous êtes déjà connecte")
            return redirect("home")
        else:
            return fnc(request, *args, **kwargs)

    return wrap


def allowed_users(required_permissions):
    def dec(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.has_perms(required_permissions):
                messages.warning(request, "Vous n'avez pas le droit d'acceder a cette page")
                return redirect("home")
            return view_func(request, *args, **kwargs)
        return wrap
    return dec
