from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm


class SignUp(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'signup.html'
