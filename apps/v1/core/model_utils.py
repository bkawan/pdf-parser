import os

from django.utils import timezone
from django.utils.text import slugify


def image_upload_to(instance, filename):
    """Store image in the directory of it's class name."""
    class_name = instance.__class__.__name__
    app_label = instance._meta.app_label
    upload_to = f'uploads/images/{app_label}/{class_name}'
    now = timezone.now()
    filename, extension = os.path.splitext(filename)
    path = os.path.join(upload_to,
                        now.strftime('%Y'),
                        now.strftime('%m'),
                        now.strftime('%d'),
                        '{}{}'.format(slugify(filename), extension))

    return path


def file_upload_to(instance, filename):
    """Store image in the directory of it's class name."""
    class_name = instance.__class__.__name__
    app_label = instance._meta.app_label
    upload_to = f'uploads/file/{app_label}/{class_name}'
    now = timezone.now()
    filename, extension = os.path.splitext(filename)
    path = os.path.join(upload_to,
                        now.strftime('%Y'),
                        now.strftime('%m'),
                        now.strftime('%d'),
                        '{}{}'.format(slugify(filename), extension))

    return path


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.slug_field)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{id}".format(
            slug=slug,
            id=instance.pk
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
