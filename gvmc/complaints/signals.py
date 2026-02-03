# complaints/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from .models import Complaint

@receiver(post_save, sender=Complaint)
def complaint_status_email(sender, instance, created, **kwargs):
    """
    Sends emails when:
    1. Complaint is created
    2. Status changes (In Progress / Resolved)
    """
    # --- 1. Complaint created ---
    if created:
        subject = 'GVMC Complaint Registered'
        message = f"Hello {instance.name},\n\nYour complaint '{instance.subject}' is registered.\n\nGVMC Team"
        email = EmailMessage(subject, message, to=[instance.email])
        if instance.photo:
            email.attach_file(instance.photo.path)
        email.send(fail_silently=False)

        # Set initial previous_status without recursion
        Complaint.objects.filter(pk=instance.pk).update(previous_status=instance.status)
        return

    # --- 2. Status changed ---
    if instance.status != instance.previous_status:
        if instance.status == 'In Progress':
            subject = 'GVMC Complaint In Progress'
            message = f"Your complaint '{instance.subject}' is being worked on."
        elif instance.status == 'Resolved':
            subject = 'GVMC Complaint Resolved'
            message = f"Your complaint '{instance.subject}' has been resolved."
        else:
            return

        email = EmailMessage(
            subject,
            f"Hello {instance.name},\n\n{message}\n\nGVMC Team",
            to=[instance.email],
        )
        if instance.photo:
            email.attach_file(instance.photo.path)
        email.send(fail_silently=False)

        # Update previous_status safely (no instance.save)
        Complaint.objects.filter(pk=instance.pk).update(previous_status=instance.status)
