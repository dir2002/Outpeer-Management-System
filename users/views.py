from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .forms import RegistrationForm
from .models import EmailActivation, CustomUser

def home(request):
    return render(request, 'users/home.html')

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("all_users")

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.set_password(form.cleaned_data["password1"])
        user.is_active = False  
        user.save() 

        
        activation = EmailActivation.objects.create(user=user)
        activation.send_email()    

        return super().form_valid(form)
    

class AllUsersView(View):
    def get(self, request):
        users_list = CustomUser.objects.filter(is_active=True).order_by("id")
        paginator = Paginator(users_list, 5)
        
        page_number = request.GET.get("page") 
        custom_users = paginator.get_page(page_number)
        return render(request, 'users/users_list.html', {"users": custom_users}) 


def activate_user(request, token: str):
    activation = EmailActivation.objects.get(token=token)
    activation.is_active = True
    activation.user.is_active = True
    activation.user.save()
    activation.save()

    return redirect('home')