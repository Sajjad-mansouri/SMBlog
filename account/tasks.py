
from time import sleep
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from celery import shared_task


@shared_task()
def send_email(

        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        if not isinstance(subject_template_name,str):
            subject = loader.render_to_string(subject_template_name, context)
        else:
            subject=subject_template_name
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()