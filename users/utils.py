from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils import timezone
import random
import os
import dotenv
from twilio.rest import Client

from django.conf import settings

dotenv.load_dotenv()


class Authentication():

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp_email(to_email):

        otp = Authentication.generate_otp()

        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        sender_email = os.getenv('sender_email')
        subject = 'Your verification Code'
        message = f'Your code is: {otp}'

        User

        class Authentication():

            @staticmethod
            def generate_otp():
                return str(random.randint(100000, 999999))

            @staticmethod
            def send_otp_email(to_email):

                otp = Authentication.generate_otp()

                otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

                sender_email = os.getenv('sender_email')
                sender_password = os.getenv('sender_password')

                subject = 'Your verification Code'
                message = f'Your code is: {otp}'

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                try:
                    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, to_email, msg.as_string())
                    return otp, otp_expiry
                except Exception:
                    return redirect('users:register')
                    return False

        make
        this
        work
        with djnago email service
        ChatGPT
        To
        make
        the
        provided
        code
        work
        with Django's email service, you need to modify the send_otp_email method. Django provides a built-in send_mail function that simplifies sending emails. Here's an updated version of your code:

        python
        Copy
        code
        from django.core.mail import send_mail
        from django.conf import settings
        from django.utils import timezone
        import random
        import os

        class Authentication():

            @staticmethod
            def generate_otp():
                return str(random.randint(100000, 999999))

            @staticmethod
            def send_otp_email(to_email):

                otp = Authentication.generate_otp()

                otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

                sender_email = settings.EMAIL_HOST_USER  # Use the sender email from your Django settings
                subject = 'Your verification Code'
                message = f'Your code is: {otp}'

                try:
                    send_mail(
                        subject,
                        message,
                        sender_email,
                        [to_email],
                        fail_silently=False,
                    )
                    return otp, otp_expiry
                except Exception as e:
                    # Handle the exception as needed
                    print(f"Error sending email: {e}")
                    return None

        In
        this
        modified
        version, send_mail is used
        instead
        of
        creating
        an
        smtplib.SMTP
        instance.The
        sender
        email is retrieved
        from settings.EMAIL_HOST_USER.Make sure
        to
        configure
        your
        Django
        email
        settings
        properly in your
        settings.py
        file.Update
        the
        email - related
        settings in your
        Django
        settings
        file
        according
        to
        your
        email
        provider(e.g., EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, etc.).

        Note: Using
        fail_silently = False in send_mail
        will
        raise exceptions if there is an
        error
        sending
        the
        email.Adjust
        the
        exception
        handling
        according
        to
        your
        application
        's needs.

        User

        @staticmethod
        def send_otp_email(to_email):

            otp = Authentication.generate_otp()

            otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

            sender_email = os.getenv('sender_email')
            subject = 'Your verification Code'
            message = f'Your code is: {otp}'

            try:
                send_mail(
                    subject,
                    message,
                    sender_email,
                    [to_email],
                    fail_silently=False,
                )
                return otp, otp_expiry
            except Exception as e:
                print(f"Error sending email: {e}")
                return None

    Error
    sending
    email: (530,
            b'5.7.0 Authentication Required. For more information, go to\n5.7.0  https://support.google.com/mail/?p=WantAuthError n18-20020a05600c501200b0040b37f1079dsm28135266wmr.29 - gsmtp',
            'yosofasady3@gmail.com')
    Internal
    Server
    Error: / users / verification
    Traceback(most
    recent
    call
    last):
    ChatGPT
    The
    error
    message
    indicates
    that
    authentication is required
    when
    trying
    to
    send
    the
    email, and it
    points
    to
    the
    fact
    that
    the
    Gmail
    SMTP
    server
    requires
    authentication.To
    fix
    this
    issue, you
    should
    provide
    the
    sender
    's email and password when calling the send_mail function.

    However, hardcoding
    email
    credentials in your
    code is not recommended
    for security reasons.Instead, use Django's settings to store sensitive information. Update your send_otp_email method as follows:

    python
    Copy
    code
    from django.core.mail import send_mail
    from django.conf import settings
    from django.utils import timezone
    import random
    import os

    class Authentication():

        @staticmethod
        def generate_otp():
            return str(random.randint(100000, 999999))

        @staticmethod
        def send_otp_email(to_email):
            otp = Authentication.generate_otp()

            otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

            sender_email = settings.EMAIL_HOST_USER
            subject = 'Your verification Code'
            message = f'Your code is: {otp}'

            try:
                send_mail(
                    subject,
                    message,
                    sender_email,
                    [to_email],
                    fail_silently=False,
                    auth_user=settings.EMAIL_HOST_USER,  # Add this line
                    auth_password=settings.EMAIL_HOST_PASSWORD  # Add this line
                )
            return otp, otp_expiry
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

    @staticmethod
    def send_otp(phone_number):
        otp = Authentication.generate_otp()
        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        twilio_phone_number = os.getenv('twilio_phone_number')

        dist_phone_number = phone_number.replace("0", "+98", 1)

        client = Client(account_sid, auth_token)
        print("Phone Number:", dist_phone_number)
        message = client.messages.create(
            body=f'Your code is: {otp}',
            from_=twilio_phone_number,
            to=dist_phone_number
        )

        print("Twilio Response:", message)
        return otp, otp_expiry

    @staticmethod
    def check_otp(otp, otp_expiry, entered_otp):
        return otp == entered_otp and timezone.now() < otp_expiry
