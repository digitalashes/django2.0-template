import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from taskapp.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_email(self, subject_template, message_template, emails, context=None, from_email=None, content_subtype='html'):
    if context is None:
        context = {}
    subject = render_to_string(subject_template, context)
    message = render_to_string(message_template, context)
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    logger.info(f'Send email to {" ".join(emails)} emails. Subject {subject}.')
    msg = EmailMessage(subject, message, from_email, emails)
    msg.content_subtype = content_subtype
    msg.send(fail_silently=False)
