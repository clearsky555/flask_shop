from src.apps.accounts.forms import LoginForm


def get_form(request):
    return {'login_form': LoginForm()}