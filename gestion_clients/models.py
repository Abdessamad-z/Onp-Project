# Create your models here.
import os
from datetime import datetime
from os.path import splitext

from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from .validators import validate_file_extension


def att_list(Class, exclude=None):
    excluded = ["_meta", "objects", "pk"] if exclude is None else ["_meta", "objects", "pk"].extend(exclude)
    listy = [a for a in dir(Class) if not a.startswith('__') and not callable(getattr(Class, a)) and a not in excluded]
    last = [listy.pop()]
    listy = last + listy
    return listy


def user_directory_path(instance, filename):
    _, extension = splitext(filename)
    now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    client = str(instance.client.pk).replace("/", "_")
    return f"{instance.client.__class__.__name__}/{client}/{instance.__class__.__name__}_{now}.pdf"


class Client(models.Model):
    pass


class Navire(Client):
    matricule = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return str(self.matricule)

    def get_absolute_url(self):
        return reverse("navire_detail", args=[self.slug])


class Mareyeur(Client):
    code_national = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return str(self.code_national)

    def get_absolute_url(self):
        return reverse("mareyeur_detail", args=[self.slug])


def init_slug(**kwargs):
    instance = kwargs.get('instance')
    if instance.__class__.__name__ == "Navire":
        instance.slug = slugify(instance.matricule)
    elif instance.__class__.__name__ == "Mareyeur":
        instance.slug = slugify(instance.code_national)


pre_save.connect(init_slug, Navire)
pre_save.connect(init_slug, Mareyeur)


class Document(models.Model):
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension], null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=CASCADE, null=True, related_name='documents')

    def __str__(self):
        return str(self.file)


class ActeNationaliteNavire(Document):
    def label(self):
        return "Acte de nationalité"


class ArmateurRcNavire(Document):
    def label(self):
        return "Armateur ou Rc"


class ActeCessionNavire(Document):
    def label(self):
        return "Acte de cession"


class DiversNavire(Document):
    def label(self):
        return "Divers"


class RcStatutMareyeur(Document):
    def label(self):
        return "Rc ou statut"


class ActeCessionMareyeur(Document):
    def label(self):
        return "Acte de cession"


class CarteAutorisationMareyeur(Document):
    def label(self):
        return "Carte d'autorisation"


class CinMareyeur(Document):
    def label(self):
        return "Cin"


class DiversMareyeur(Document):
    def label(self):
        return "Divers"


# @receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            if instance.file == "":
                return
            os.remove(instance.file.path)

# @receiver(models.signals.pre_save, sender=Document)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return False
#     try:
#         old_file = Document.objects.get(pk=instance.pk).file
#         if old_file == "":
#             raise Document.DoesNotExist
#     except Document.DoesNotExist:
#         return False
#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
