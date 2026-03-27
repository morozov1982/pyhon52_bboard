from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE

from bboard.models import get_timestamp_path


class AdvUser(models.Model):
    is_activated = models.BooleanField(
        default=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.username}'


class Spare(models.Model):
    name = models.CharField(max_length=30)

    notes = GenericRelation('Note', related_query_name='spare')

    def __str__(self):
        return f'{self.name}'


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit',
                        through_fields=('machine', 'spare'))

    notes = GenericRelation('Note', related_query_name='machine')

    def __str__(self):
        return f'{self.name}'


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=CASCADE)
    spare = models.ForeignKey(Spare, on_delete=CASCADE)
    count = models.IntegerField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')


# class Message(models.Model):
#     content = models.TextField()
#     published = models.DateTimeField(auto_now_add=True, db_index=True)
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None
#
#     class Meta(Message.Meta):
#         ordering = ['order', 'name']

class Img(models.Model):
    img = models.ImageField(
        verbose_name='Изображение',
        upload_to=get_timestamp_path,
    )

    desc = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# class Profile(models.Model):
#     phone = models.CharField(max_length=20)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


# class AdvUser(AbstractUser):
#     phone = models.CharField(max_length=20)


# class AdvUser(User):
#     phone = models.CharField(max_length=20)
#
#     class Meta:
#         proxy = True
