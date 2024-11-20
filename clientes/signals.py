from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Meeting, Interaction
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=Meeting)
def send_meeting_reminder(sender, instance, created, **kwargs):
    subject = f"Reminder: Meeting Scheduled with {instance.client.nombre}"
    message = (
        f"Hello {instance.salesperson.username},\n\n"
        f"This is a reminder for your upcoming meeting with {instance.client.nombre} {instance.apellido}.\n"
        f"Details:\n"
        f"Date and Time: {instance.date_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"Client Email: {instance.client.get_email()}\n\n"
        f"Best regards,\nYour Team"
    )
    recipient_list = [instance.salesperson.email]
    try:
        send_mail(subject, message, 'jose.aguilera.lazol@gmail.com', recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Failed to send email: {e}")

@receiver(post_save, sender=Interaction)
@receiver(post_delete, sender=Interaction)
def update_client_interaction_status(sender, instance, **kwargs):
    # Update the status of the associated client
    instance.cliente.update_interaction_status()