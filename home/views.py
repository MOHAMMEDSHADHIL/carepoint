import os

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UserProfile, book_appointment
from .forms import UserUpdateForm, ProfileUpdateForm
from django.utils import timezone

from .forms import Booking_Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from .recommendation import recommend_doctors, find_specializations


from .models import  doctors, dpt

# Create your views here.
@login_required
def index(request):
    context = {
        'departments': dpt.objects.all(),
        'doctors': doctors.objects.select_related("department_name").all()[:3],
    }
    return render(request, 'index.html', context)
def about(request):
    fruits={'names': ['apple','banana','orange','grapes','kiwi','mango']}
    return render(request, 'about.html', fruits)
def contact(request):
    person={'names': ['shadhil','anuvind','adhthyan','tenson','vishnu','soorya','anagha']}
    return render(request, 'contact.html', person)
def doctor(request):
    data = doctors.objects.select_related("department_name").all()
    dict_doctors = {'doctors': data}
    return render(request, 'doctors.html', dict_doctors)
def department(request):
    dict_dpt ={ 'departments': dpt.objects.all() }
    return render(request, 'department.html', dict_dpt)


def booking(request):

    if request.method == "POST":
        form = Booking_Form(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            if request.user.is_authenticated:
                appointment.user = request.user

            appointment.save()

            messages.success(
                request,
                'Your appointment has been booked successfully!'
            )

            return redirect('index')

    else:
        initial = {}
        selected_doctor = None
        doctor_id = request.GET.get("doctor")

        if request.user.is_authenticated:
            profile_data, _ = UserProfile.objects.get_or_create(
                user=request.user
            )
            full_name = " ".join(
                part for part in (
                    request.user.first_name.strip(),
                    request.user.last_name.strip(),
                )
                if part
            )

            initial.update({
                "patient_name": full_name or request.user.username,
                "patient_email": request.user.email,
                "patient_phone": profile_data.phone,
            })

        if doctor_id:
            selected_doctor = get_object_or_404(doctors, pk=doctor_id)
            initial["doctor_name"] = selected_doctor

        initial["booked_on"] = timezone.localdate()
        form = Booking_Form(initial=initial)

    return render(request, "booking.html", {
        "form": form
    })

def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect("index")
    else:
        form=UserCreationForm()
    return render(request,"signup.html",{"form":form})
@login_required
def smart_recommendation(request):
    doctors = []
    symptoms = ""
    searched = False

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip()
        searched = True

        if symptoms:
            doctors = recommend_doctors(symptoms)

    return render(
        request,
        "smart_recommendation.html",
        {
            "doctors": doctors,
            "symptoms": symptoms,
            "searched": searched,
        },
    )


@login_required
def profile(request):

    profile_data, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    appointments = book_appointment.objects.filter(
        user=request.user
    ).select_related(
        'doctor_name',
        'doctor_name__department_name'
    ).order_by('-booked_on')

    return render(request, 'profile.html', {
        'profile_data': profile_data,
        'appointments': appointments,
        'today': timezone.localdate(),
    })
@login_required
def edit_profile(request):
    profile_data, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_data
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_data)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(
                request,
                'Your password has been changed successfully!'
            )

            return redirect('profile')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {
        'form': form
    })
