import os
import uuid

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from .model_utils import image_upload_to, file_upload_to


class AbstractCreatedAtModifiedAt(models.Model):
    """
    This is an abstract class which provide created_at and modified_at DateTimeField
    """
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AbstractReview(models.Model):
    """
    This is an abstract class which provide basic fields for Review Model.
    """
    SCORE_CHOICES = [(x, x) for x in range(1, 6)]
    score = models.SmallIntegerField(choices=SCORE_CHOICES)
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractSlug(models.Model):
    slug = models.SlugField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def slug_field(self):
        raise NotImplementedError("Must Implement slug_field")

    __original_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.slug_field

    def save(self, *args, **kwargs):
        if self.slug_field != self.__original_name:
            self.slug = self.unique_slug_generator(self)
        elif not self.slug:
            self.slug = self.unique_slug_generator(self)
        super().save(*args, **kwargs)
        self.__original_name = self.slug_field

    def unique_slug_generator(self, instance, new_slug=None):
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
                id=instance.pk if instance.pk else  uuid.uuid4().hex[:6].upper()
            )
            return self.unique_slug_generator(instance, new_slug=new_slug)
        return slug


class AbstractCategory(MPTTModel, AbstractSlug):
    """
    Simple model for categorizing entries.
    """

    title = models.CharField(
        _('title'), max_length=255)

    description = models.TextField(
        _('description'), blank=True)

    parent = TreeForeignKey(
        'self',
        related_name='children',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('parent category'))

    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

    objects = TreeManager()

    class Meta:
        abstract = True

    class MPTTMeta:
        """
        Category MPTT's meta informations.
        """
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class AbstractDocument(AbstractCreatedAtModifiedAt):
    name = models.CharField(blank=True, null=True, max_length=255)
    file = models.FileField(upload_to=file_upload_to, blank=True, null=True)
    direct_link = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.name:
            self.name, ext = os.path.splitext(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}-{self.file}'
