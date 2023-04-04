"""
This module is a utility class that provides Email sending functionality
"""

from django.core.mail import EmailMessage

class Util:
    """
    A utility class that provides Email sending functionality.

    parameters:
        - to_email: The email address of the recipient
        - email_subject: The email subject
        - email_body: The email body
        
    Raises error if the data is invalid else it returns nothing
    """
    @classmethod
    def send_email(self, data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        
        email.send()