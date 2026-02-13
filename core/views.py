from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from core.forms import OrganizationSignupForm
from core.models import Organization
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import UserInvite
from .forms import InviteUserForm

from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from users.models import CustomUser

from .forms import DemoRequestForm
from core.models import Plan, Subscription

# Create your views here.
def home_view(request):
    """Lightweight marketing-style homepage"""
    return render(request, "home.html", {})


def request_demo_view(request):
    if request.method == "POST":
        form = DemoRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Our team will contact you shortly to schedule the demo."
            )
            return redirect("home")
    else:
        form = DemoRequestForm()

    return render(request, "request_demo.html", {"form": form})



User = get_user_model()

# def organization_signup(request):
#     if request.method == 'POST':
#         form = OrganizationSignupForm(request.POST)
#         if form.is_valid():
#             org = Organization.objects.create(
#                 name=form.cleaned_data['organization_name'],
#                 domain=form.cleaned_data['domain']
#             )

#             email = form.cleaned_data['email']

#             if User.objects.filter(email=email).exists():
#                 form.add_error("email", "An account with this email already exists.")
#                 return render(request, "core/signup.html", {"form": form})
#             user = CustomUser.objects.create_user(
                
#                 email=email,
#                 password=form.cleaned_data['password1'],
#                 organization=org,
#                 is_manager=True,
                
#             )
#             # user.organization = org
#             user.is_manager = True
#             user.save()

#             managers_group, _ = Group.objects.get_or_create(name='Managers')
#             user.groups.add(managers_group)
#             login(request, user)
#             messages.success(request, "Organization created successfully.")
#             return redirect('observations:observation_list')
#     else:
#         form = OrganizationSignupForm()
#     free_plan = Plan.objects.get(name="Free")
#     Subscription.objects.create(
#         organization=org,
#         plan=free_plan,
#         start_date=timezone.now(),
#         end_date=timezone.now() + timedelta(days=90)  # 30-day free trial
#     )
#     return render(request, 'core/signup.html', {'form': form})


from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta

def organization_signup(request):

    if request.method == 'POST':
        form = OrganizationSignupForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            # ---------------------------
            # Prevent duplicate user
            # ---------------------------
            if User.objects.filter(email=email).exists():
                form.add_error("email", "An account with this email already exists.")
                return render(request, "core/signup.html", {"form": form})

            # ---------------------------
            # Create Organization
            # ---------------------------
            org = Organization.objects.create(
                name=form.cleaned_data['organization_name'],
                domain=form.cleaned_data['domain']
            )

            # ---------------------------
            # Create Manager User
            # ---------------------------
            user = CustomUser.objects.create_user(
                email=email,
                password=form.cleaned_data['password1'],
                organization=org,
                is_manager=True,
            )

            managers_group, _ = Group.objects.get_or_create(name='Managers')
            user.groups.add(managers_group)

            # ---------------------------
            # Create FREE Subscription
            # ---------------------------
            free_plan, _ = Plan.objects.get_or_create(name="Free")

            Subscription.objects.create(
                organization=org,
                plan=free_plan,
                started_at=timezone.now(),
                expires_at=timezone.now() + timedelta(days=30)
            )

            # ---------------------------
            # Login + Redirect
            # ---------------------------
            login(request, user)

            messages.success(request, "Organization created successfully.")
            return redirect('observations:observation_list')

    else:
        form = OrganizationSignupForm()

    return render(request, 'core/signup.html', {'form': form})





from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
# from djaango.template.loader import render_to_string



from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

from .forms import InviteUserForm
# from core.utils.email import send_email

from core.utils.email import send_brevo_email
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta



from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

from core.models import Subscription, Plan
from users.models import CustomUser as User


@login_required
def invite_user(request):

    if not request.user.is_manager:
        raise PermissionDenied

    # -------------------------------------------------
    # 1️⃣ Ensure subscription exists
    # -------------------------------------------------
    free_plan, _ = Plan.objects.get_or_create(name="Free")

    subscription, _ = Subscription.objects.get_or_create(
        organization=request.organization,
        defaults={"plan": free_plan}
    )

    # -------------------------------------------------
    # 2️⃣ Check user limit BEFORE invite
    # -------------------------------------------------
    current_users = User.objects.filter(
        organization=request.organization
    ).count()

    if current_users >= subscription.plan.max_users:
        messages.error(
            request,
            "User limit reached for current plan. Upgrade to invite more users."
        )
        return redirect("core:invite_user")

    # -------------------------------------------------
    # 3️⃣ Process form
    # -------------------------------------------------
    if request.method == "POST":
        form = InviteUserForm(request.POST)

        if form.is_valid():
            invite = form.save(commit=False)
            invite.organization = request.organization
            invite.save()

            invite_link = request.build_absolute_uri(
                reverse("core:accept_invite", args=[invite.token])
            )

            html = render_to_string(
                "emails/invite_user.html",
                {
                    "organization": invite.organization,
                    "invite_link": invite_link,
                }
            )

            send_brevo_email(
                to_email=invite.email,
                subject="You're invited to Safety Observation Platform",
                html_content=html,
            )

            messages.success(request, "Invitation sent successfully.")
            return redirect("core:invite_user")

    else:
        form = InviteUserForm()

    return render(request, "core/invite_user.html", {"form": form})




from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import get_user_model

User = get_user_model()

# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from django.contrib import messages
from .models import UserInvite
from .forms import AcceptInviteForm

User = get_user_model()

def accept_invite(request, token):
    invite = get_object_or_404(UserInvite, token=token)

    if invite.is_used or invite.expires_at < timezone.now():
        return render(request, "core/invite_invalid.html")

    if not invite.is_valid():
        return render(request, "core/invite_invalid.html")

    if request.method == "POST":

        form = AcceptInviteForm(request.POST)
        
        if form.is_valid():
            user = User.objects.filter(email=invite.email).first()
            if not user:
                user = User.objects.create_user(
                    email=invite.email,
                    password = form.cleaned_data["password1"],
                    organization=invite.organization,
                )
            else:
                user.organization = invite.organization
                user.set_password(form.cleaned_data["password1"])
                # Assign role
            if invite.role == "manager":
                user.is_manager = True
            
            user.save()

            invite.is_used = True
            invite.save()

            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("observations:observation_list")
    else:
        form = AcceptInviteForm()

    return render(request, "core/accept_invite.html", {
        "form": form,
        "invite": invite
    })






