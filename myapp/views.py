
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment,Patient
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib.auth import logout

# View for logging out the user
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Logs out the user
        return redirect('home')  # Redirect to the home page after logging out

    return render(request, 'logged_out.html') 

def home(request):
    return render(request,'index.html')
# View for listing all doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

# View for creating an appointment without a form class
def login_view(request):
    if request.user.is_authenticated:
        # If user is already authenticated, redirect to book appointment
        return redirect('create_appointment')
        
    return render(request, 'login.html')

# View for booking appointment
@login_required(login_url='/login/')
def book_appointment(request):
    # If the user is logged in, they will be redirected to the booking form
    doctors = Doctor.objects.all()  # Fetch all available doctors
    return render(request, 'appointments/create_appointment.html', {'doctors': doctors})

# View to handle the appointment creation
@login_required(login_url='/login/')
def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')  # Get the selected doctor ID
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason_for_visit = request.POST.get('reason_for_visit')

        # Fetch the selected doctor object
        doctor = get_object_or_404(Doctor, id=doctor_id)
        user = request.user
        # if not hasattr(user, 'patient'):
        #     # Create a new Patient profile for the logged-in user
        #     patient = Patient.objects.create(user=user)
        # else:
        #     # Fetch the existing Patient profile
        #     patient = user.patient
        patient, created = Patient.objects.get_or_create(user=request.user)
        try:
            # Try to fetch the patient object related to the logged-in user
            patient = request.user.patient
        except Patient.DoesNotExist:
            # Handle the case where the user does not have a patient profile
            return HttpResponse("<h1>Successfully Booked Appointment.</h1>", status=400)

        # Create a new appointment
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason_for_visit=reason_for_visit
        )

        # Redirect to the success page
        return redirect('appointment_success')
    else:
        # If GET request, show the appointment creation form again
        doctors = Doctor.objects.all()
        return render(request, 'create_appointment.html', {'doctors': doctors})

def appointment_success(request):
    return render(request, 'succes.html')

# View for listing appointments for a patient
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user.patient)
    return render(request, 'appointment_list.html', {'appointments': appointments})
def about(request):
    return render (request,'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process the form data (e.g., save to database, send email, etc.)
        return HttpResponse(f"Thank you, {name}! We have received your message.")
    
    return render(request, 'contact.html')

def blog(request):
    # Sample data for blog posts
    blog_posts = [
        {
            'title': 'First Blog Post',
            'author': 'John Doe',
            'date': 'September 14, 2024',
            'content': 'This is the content of the first blog post.'
        },
        {
            'title': 'Second Blog Post',
            'author': 'Jane Smith',
            'date': 'September 13, 2024',
            'content': 'This is the content of the second blog post.'
        },
        {
            'title': 'Third Blog Post',
            'author': 'Alice Johnson',
            'date': 'September 12, 2024',
            'content': 'This is the content of the third blog post.'
        },
    ]
    return render(request, 'blog.html', {'posts': blog_posts})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # You can add more fields like email, etc.
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        
        # Redirect to login page after successful registration
        return redirect('login')
    
    return render(request, 'register.html')

# def appointment_success(request):
#     return render(request, 'appointment_success.html')

def display(request):
    try:
      
        patient = request.user.patient
        appointments = Appointment.objects.filter(patient=patient)
        return render(request, 'appointment_list.html', {'appointments': appointments})
    except Patient.DoesNotExist:
        
        return render(request, 'appointment_list.html', {'appointments': [], 'error': 'No patient profile found.'})
