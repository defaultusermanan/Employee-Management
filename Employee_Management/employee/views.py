from django.shortcuts import render, redirect
from .models import employees , feedback
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .forms import EmployeeFeedbackForm
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from .forms import EmployeeFeedbackForm
import uuid
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string 
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
from django.templatetags.static import static
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from django.template.loader import get_template
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your Password and confirm password are not the same")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or Password is Invalid!")
    return render(request, 'HR.html')

def dashboard(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        name = request.POST.get('name')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        joined_date = request.POST.get('joined_date')
        role_position = request.POST.get('role_position')
        manager = request.POST.get('manager')
        email = request.POST.get('email')
        markytics_email = request.POST.get('markytics_email')
        manager_email = request.POST.get('manager_email')
        address = request.POST.get('address')
        updated_employee= employees(emp_id=emp_id,name=name,city=city,state=state,zip=zip,joined_date=joined_date,role_position=role_position,
                                    manager=manager,email=email,markytics_email=markytics_email,manager_email=manager_email,address=address)
        updated_employee.save()
        
        randompassword = User.objects.make_random_password()
        expiration_time = timezone.now() + timedelta(hours=24)
        user = User.objects.create_user(username=markytics_email,email=markytics_email,password=randompassword)
        user.password_expiration = expiration_time
        user.set_password(randompassword)
        user.save()

        subject = 'Login Credentials'
        message = f'Hello {name}, your login credentials for markytics are: Username {markytics_email} Password:{randompassword}. Please Login https://www.markytics.com/employees/login/ using the given credentials. Your manager is {manager},Please contact him as soon as possible'
        email_from = settings.EMAIL_HOST_USER
        recipient_list =[email]

        email=EmailMessage(
            subject,
            message,
            email_from,
            recipient_list
        )
        email.send()

        subject = 'Greetings'
        message = f'Hello {manager}.{name} is the new employee who has been assigned under you.Please contact him. {name},{role_position}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [manager_email]
        Email = EmailMessage(
            subject,
            message,
            email_from,
            recipient_list
        )
        Email.send()
        return redirect('dashboard')
        
    return render(request, 'edit_employee.html')

from django.contrib.auth import authenticate,login
from django.shortcuts import render , redirect

def login1(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('reset_password')
        else:
            return HttpResponse("Invalid Credentials.Please check the email for correct credentials")
    return render(request,'login1.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        newpass = request.POST.get('password')
        newsspassconf = request.POST.get('confirm_password')

        if newpass != newsspassconf:
            return HttpResponse("The passwords do not match")
        else:
            emailid = {email}  
            user = User.objects.get(email=email)
            user.set_password(newpass)
            user.save()

            user = authenticate(request, username=email, password=newpass)
            if user is not None:
                auth_login(request, user)
                return HttpResponse('Your passowrd has been changes successfully.')
            else:
                return HttpResponse("Invalid credentials")

    else:
        return render(request, 'reset_password.html')  

def feedback_form(request):
    if request.method == 'POST':
        try:
            # Get form data from POST request
            employee_name = request.POST.get('employee')
            manager_name = request.POST.get('manager')
            rating1 = float(request.POST.get('rating1'))
            rating2 = float(request.POST.get('rating2'))
            rating_scale = float(request.POST.get('rating_scale'))
            commentText1 = request.POST.get('commentText1')
            commentText2 = request.POST.get('commentText2')
            commentText3 = request.POST.get('commentText3')

            # Create feedback instance and save it to the database
            employee = employees.objects.get(name=employee_name)
            feedback_instance = feedback.objects.create(
                employee_name=employee,
                manager_name=manager_name,
                overall_performance=rating1,
                behaviour=rating2,
                deadlines=rating_scale,
                positives=commentText1,
                negatives=commentText2,
                scope_of_improvement=commentText3
            )

            # Send feedback emails
            employee_mail = employee.email
            manager_obj = employees.objects.get(name=manager_name)
            manager_mail = manager_obj.manager_email

            message = f"Dear {employee_name},\n\nI hope this email finds you well.\n\nWe are writing you today to provide you with some feedback on your performance since you joined the company 7 days ago.\n\nWe've been quite impressed with your work.\n\nHere are a few areas where we think you could improve:\n{commentText3}{rating1}\nThank you for your hard work. We're excited to see how you continue to grow and develop in your role.\n\nSincerely,\n{manager_name}."
            send_mail(
                'Manager Feedback',
                message,
                settings.EMAIL_HOST_USER,
                [employee_mail],
                fail_silently=False
            )

            message1 = f"Your feedback has been submitted successfully. Thank you!"
            send_mail(
                'Submission Successful',
                message1,
                settings.EMAIL_HOST_USER,
                [manager_mail],
                fail_silently=False
            )

            return redirect("feedback_form")  # Redirect to the feedback form after successful submission
        except Exception as e:
            print(f"Error: {str(e)}")
            # Handle the error here, show an error message, or redirect to the form page with an error indicator.
            # For example, using Django messages framework to show an error message:
            from django.contrib import messages
            messages.error(request, "Error submitting feedback form. Please try again.")
            return redirect("feedback_form")

    # Retrieve distinct employee names and manager names for the dropdowns
    employeesDropdown = employees.objects.values_list('name', flat=True).distinct()
    managersDropdown = employees.objects.values_list('manager', flat=True).distinct()
    return render(request, 'feedback.html', {'employeesDropdown': employeesDropdown, 'managersDropdown': managersDropdown})

    


def send_remainder_email():
            current_date = timezone.now().date()
            joining_month_start = employees.objects.first().joined_date.replace(day=1)
            fifth_day = joining_month_start + timedelta(days=4)
            twelfth_day = joining_month_start + timedelta(days=11)
            twenty_eight_day = joining_month_start + timedelta(days=27)

            manager_email = employees.objects.first().manager_email

            send_mail(
                'Employee Feedback Form Remainder',
                f"Dear Manager, please fill up the employee feedback form on the following dates:\n\n"
                f"{fifth_day.strftime('%d %B %Y')}\n"
                f"{twelfth_day.strftime('%d %B %Y')}\n"
                f"{twenty_eight_day.strftime('%d %B %Y')}\n"
                f"Thank You",
                settings.EMAIL_HOST_USER,

                [manager_email],
                fail_silently=False
            )
            if current_date.day in [7 , 14 , 30]:
                feedback_link = f"http://127.0.0.1:8000/feedback_form/"
                send_mail(
                    'Feedback Form Link',
                    f"Dear Manager, Please provide feedback for the employee using the following link"
                    f"{feedback_link}\n\n"
                    f"Thank you.",
                    settings.EMAIL_HOST_USER,
                    [manager_email],
                    fail_silently=False,
                )
def edit_dashboard(request):
    if request.method == 'POST':
        form = EmployeeFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            scheduler = BackgroundScheduler()
            scheduler.add_job(send_remainder_email,'interval',days=1)
            scheduler.start()

            return redirect('edit_employees.html')
    else:
        form = EmployeeFeedbackForm()
    return render(request,'edit_employee.html',{'form':form})    

#def feedback_form(request):
    #employeesDropdown = employees.objects.values_list('name',flat=True).distinct()
    #managersDropdown = employees.objects.values_list('manager',flat=True).distinct()
    #return render (request,'feedback.html',{'employeesDropdown':employeesDropdown,'managersDropdown':managersDropdown})
def learnings(request):
    return render(request,'learnings.html')


    
def test(request):
    if request.method == 'POST':
        employee_name = request.POST.get('employee_name')
        employee_email = request.POST.get('employee_email')
        review = request.POST.get('review')
        manager_name = request.POST.get('manager_name')
        
        html_content = render_to_string("employee_feedback_email.html", {
            'request':request,
            'title': 'Feedback Response',
            'employee_name': employee_name,
            'review': review,
            'manager_name': manager_name
        })
        
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            'Feedback Response',
            text_content,
            settings.EMAIL_HOST_USER,
            [employee_email]
        )
        email.mixed_subtype='related'
        email.attach_alternative(html_content, "text/html")
        email.send()

        return HttpResponse("Submitted successfully")

    return render(request, 'test.html', {'title': 'Feedback Form'})

def intern(request):
    return render(request,'intern_feedback.html')

def client_email(request):
    return render(request,'client_email.html')

def client_email1(request):
    return render(request,'client_email1.html')

def find_image_paths(html_content):
    pattern = r'<img.*?src=["\'](.*?)["\'].*?>'
    image_paths = re.findall(pattern, html_content)
    print(image_paths)
    return (image_paths)


def manan(request):
    from_email = 'rgasylum1212@gmail.com'
    to_email = 'mukkawar.utkarsh2129@gmail.com'
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD
    subject = "Request to fill Learnings Form"
    email_template = 'client_email1.html'
    template = get_template(email_template)
    html_content = render_to_string('client_email1.html')
    text_content = strip_tags(html_content) 
    # email_content = template.render({'url': url})
    # message = MIMEMultipart()
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.mixed_subtype = 'related'

    # Find all image paths in the HTML content
    image_paths = find_image_paths(html_content)

    # Attach images as inline attachments
    # for image_path in image_paths:
    #     image_full_path = os.path.join(settings.BASE_DIR, image_path)
    #     if not os.path.exists(image_full_path):
    #         continue
    #     # with open(image_path, 'rb') as f:
    #     with open(image_path, "rb") as f:
    #         encoded_string = base64.b64encode(f.read()).decode("utf-8")
    #     print(encoded_string)
    #     image_data = f.read()
    #     image_filename = os.path.basename(image_path)
    #     email_image = EmailMultiAlternatives('', '', from_email, [to_email])
    #     email_image.attach(image_filename, image_data, 'image/png')
    #     email_image.content_id = image_filename
    #     email_image['Content-ID'] = f'<{image_filename}>'
    #     email.attach_related(email_image)
    for image_path in image_paths:
        image_full_path = os.path.join(settings.BASE_DIR, image_path)
        if not os.path.exists(image_full_path):
            continue

        with open(image_full_path, "rb") as f:
            image_data = f.read()
        encoded_image_data = base64.b64encode(image_data).decode("utf-8")

        image_filename = os.path.basename(image_path)
        email_image = EmailMultiAlternatives('', '', from_email, [to_email])
        email_image.attach(image_filename, None, 'image/png')
        email_image.content_subtype = "png"
        email_image.content_id = image_filename
        email_image['Content-ID'] = f'<{image_filename}>'
        email_image.attach_alternative(f'<img src="data:image/png;base64,{encoded_image_data}" alt="{image_filename}">', "text/html")
        email.attach_related(email_image)

    email.send()
    return HttpResponse("Email-Sent successfully")

def details(request):
    employeesDropdown = employees.objects.values_list('name', flat=True).distinct()
    return render(request,'details.html',{'employeesDropdown':employeesDropdown})