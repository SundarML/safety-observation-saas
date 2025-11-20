# Create your views here.
# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model   
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from . forms import CustomUserCreationForm
# users/views.py
User = get_user_model()

def register(request):
    """
    Handle new user registrations.

    - Expects a CustomUserCreationForm (subclass of UserCreationForm) in users/forms.py
        that at minimum includes: username, email, password1, password2.
    - After successful registration the new user is auto-logged in and redirected.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # OPTIONAL: if your User model has role boolean fields and your form provides them,
            # you can set them here. Uncomment and adapt if needed:
            user.is_observer = form.cleaned_data.get('is_observer', True)
            user.is_action_owner = form.cleaned_data.get('is_action_owner', False)
            user.is_safety_manager = form.cleaned_data.get('is_safety_manager', False)

            user.save()

            # Auto-login the user after registration
            login(request, user)

            messages.success(request, "Account created successfully. You are now logged in.")
            return redirect('observations:observation_list')
        else:
            # show form errors (template will render them)
            messages.error(request, "There were errors in the form. Please correct them below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/login.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {})


