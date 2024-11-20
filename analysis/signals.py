from django.db.models.signals import post_save
from django.dispatch import receiver
from apartments.models import Project
from .models import ProjectCost

@receiver(post_save, sender=Project)
def create_project_cost(sender, instance, created, **kwargs):
    if created:
        ProjectCost.objects.create(project=instance)
