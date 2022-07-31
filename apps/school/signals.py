from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from school.models import Class, School, Student

from services.email import send_student_notification_email


@receiver(post_save, sender=Student)
@transaction.atomic
def add_student_to_class(sender, instance, created, **kwargs):
    """
    Adds student to existing Class object else creates new class Object
    and add Student instance
    """

    if created:
        student_class = instance.student_class
        class_object = Class.objects.filter(name=student_class)

        if not class_object.exists():
            class_object = Class.objects.create(name=student_class, teacher=instance.created_by)
            class_object.students.add(instance)
        else:
            class_object = class_object.first()
            class_object.students.add(instance)

        # send notification email
        send_student_notification_email(instance, instance.created_by.full_name, instance.student_class)


@receiver(post_save, sender=Class)
@transaction.atomic
def add_class_to_school(sender, instance, created, **kwargs):
    """
    Adds student to existing School object else creates new School Object
    and add Class instance
    """

    if created:
        school, is_created = School.objects.get_or_create(name="Admin School")
        school.classes.add(instance)




