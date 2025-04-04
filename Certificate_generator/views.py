from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import CertificateForm
from pptx import Presentation
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import csv
import os
from django.contrib.auth import login as auth_login

# Inside your view function
# jqgh lxom weep metq
# xefl udtg wfkm ceev


def homepage(request):
    """Render the homepage."""
    return render(request, "homepage.html")

def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        # Retrieve form data
        First_name = request.POST.get('First_name')
        Last_name = request.POST.get('Last_name')
        User_name = request.POST.get('User_name')
        email = request.POST.get('email')
        Password1 = request.POST.get('Password1')
        Password2 = request.POST.get('Password2')
        
        # Check if the username already exists
        if User.objects.filter(username=User_name).exists():
            message = "Username already taken. Please choose a different one."
            return render(request, "signup.html", {'message': message})
        
        # Check if password and confirm password match
        if Password1 != Password2:
            message = "Passwords do not match. Please try again."
            return render(request, "signup.html", {'message': message})
        
        # Validate password
        try:
            validate_password(Password1)
        except ValidationError as e:
            message = ', '.join(e.messages)
            return render(request, "signup.html", {'message': message})
        
        # Create user if all checks pass
        my_user = User.objects.create_user(username=User_name, email=email, password=Password1, first_name=First_name, last_name=Last_name)
        my_user.save()
        
        # Redirect to home page after successful signup
        return redirect('homepage')  # Replace 'homepage' with the URL name of your home page
    
    return render(request, "signup.html")

def login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('User_name')  # Correct the key to 'User_name'
        password = request.POST.get('Password')  # Correct the key to 'Password'

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User credentials are correct, log the user in
            auth_login(request, user)
            # Redirect to homepage after successful login
            return redirect('homepage')  # Replace 'homepage' with the URL name of your home page
        else:
            # Authentication failed, render login page with error message
            message = "Invalid username or password. Please try again."
            return render(request, "signup.html", {'message': message})

    return render(request, "signup.html")

def generate_certificate(request):
    sent_certificates = []

    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.cleaned_data['template']
            student_details_file = form.cleaned_data['csvfile']
            sender_email = form.cleaned_data['sender_email']
            sender_password = form.cleaned_data['sender_password']
            
            fs = FileSystemStorage()
            filename = fs.save(student_details_file.name, student_details_file)

            try:

                detail = []
                with open(fs.path(filename), 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        detail.append([cell.strip() for cell in row])

                keys = detail[0]
                student_dict = {}
                for row in detail[1:]:
                    student_dict[row[0]] = dict(zip(keys[1:], row[1:]))

                for key, values in student_dict.items():
                    prs = Presentation(template)

                    for slide in prs.slides:
                        for shape in slide.shapes:
                            if shape.has_text_frame:
                                text_frame = shape.text_frame
                                for paragraph in text_frame.paragraphs:
                                    for run in paragraph.runs:
                                        for old_text, new_text in values.items():
                                            if old_text.upper() in run.text:
                                                run.text = run.text.replace(old_text.upper(), new_text)

                    certificate_file = f"{values['name']}_Certificate.pptx"
                    prs.save(certificate_file)

                    send_certificate(sender_email, sender_password, values['email'], values['name'], certificate_file)
                    sent_certificates.append({'name': values['name'], 'email': values['email']})

                    messages.success(request, f"Email sent successfully to {values['name']} ({values['email']})")

            except Exception as e:
                print("Error processing CSV data:", e)
            finally:

                fs.delete(filename)

            return redirect('mail_status')

        else:
            return render(request, "generatecerti.html", {"form": form, "sent_certificates": sent_certificates})

    else:
        form = CertificateForm()

    return render(request, "generatecerti.html", {"form": form, "sent_certificates": sent_certificates})



def send_certificate(sender_email, sender_password, recipient_email, recipient_name, certificate_file):
    """Send certificate via email."""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Certificate"

    with open(certificate_file, "rb") as file:
        attachment = MIMEBase("application", "vnd.openxmlformats-officedocument.presentationml.presentation")
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(certificate_file)}"')
        msg.attach(attachment)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Certificate sent to {recipient_email}")
        server.quit()

        if os.path.exists(certificate_file):
            os.remove(certificate_file)
            print(f"Certificate file {certificate_file} deleted.")
        else:
            print(f"Certificate file {certificate_file} does not exist.")
    except Exception as e:
        print("Error:", e)


def mail_status(request):
    """Render the mail status page."""
    return render(request, "mail_status.html")
