from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.template import loader
from django.core.mail import EmailMultiAlternatives

UserModel = get_user_model()
class EmailConfirmation:
   
    domain_override=None
    subject_template_name="registration/confirmation_email_subject.txt"
    email_template_name="registration/confirmation_email.html"
    use_https=False
    token_generator=default_token_generator
    from_email=None
    request=None
    html_email_template_name=None
    extra_email_context=None

    def __init__(self,email,request):
        self.email=email
        self.request=request

    def send_mail(
        self,
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

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
        )
    def save(self):
        """
        Generate a one-use only link for email confirmation
        """
        if not self.domain_override:
            current_site = get_current_site(self.request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = self.domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(self.email):
            user_email = getattr(user, email_field_name)       
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": self.token_generator.make_token(user),
                "protocol": "https" if self.use_https else "http",
                **(self.extra_email_context or {}),
            }
            self.send_mail(
                self.subject_template_name,
                self.email_template_name,
                context,
                self.from_email,
                user_email,
                self.html_email_template_name
            )
