from django.db import models
from django.contrib.auth.models import User as BaseUser

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# Create your models here.

class SeriesStatus:
    released = 0
    comming_soon = 1


SERIES_STATUS_CHOICES_DICT = {
    (SeriesStatus.released, 'Вышла'),
    (SeriesStatus.comming_soon, 'Скоро будет'),
}


class Series(models.Model):
    title = models.CharField(max_length=120)
    showtime = models.DateTimeField()
    number = models.SmallIntegerField()
    img = models.ImageField(upload_to='series_preview')
    status = models.PositiveSmallIntegerField(choices=SERIES_STATUS_CHOICES_DICT, default=SeriesStatus.comming_soon)

    def __str__(self):
        return f'Эпизод {self.number} - {self.get_status_display()}'


class CharacterStatus:
    is_dead = 0
    is_alive = 1
    is_wights = 2


CHARACTER_STATUS_CHOICES_DICT = {
    (CharacterStatus.is_dead, 'Мертв'),
    (CharacterStatus.is_alive, 'Жив'),
    (CharacterStatus.is_wights, 'Вихт')
}


class Character(models.Model):
    name = models.CharField(max_length=120)
    img = models.ImageField(upload_to='character')

    description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=CHARACTER_STATUS_CHOICES_DICT, default=CharacterStatus.is_alive)

    def __str__(self):
        return f'{self.name} - {self.get_status_display()}'


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    base_user = models.OneToOneField(BaseUser, primary_key=True, on_delete=models.CASCADE, related_name='user_profile')
    username = models.CharField(max_length=120)

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    url = models.URLField(null=True, blank=True)


class UserDevices(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=200, unique=True, blank=True, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)


class Card(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(null=True, blank=True)
    question = models.CharField(max_length=120, blank=True)
    img = models.ImageField(upload_to='card_img', blank=True)

    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='cards', verbose_name='Серия')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character',
                                  verbose_name='Персонаж',
                                  null=True, blank=True)
    is_death = models.BooleanField(default=True)


class CardAnswer(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='answers')


class UserAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_answer = models.ForeignKey(CardAnswer, on_delete=models.CASCADE)


def create_answers(card, answers):
    for answer in answers:
        CardAnswer.objects.create(title=answer, card=card)


@receiver(pre_save, sender=Card, weak=False)
def character_death(sender: Card, instance: Card, **kwargs):
    if instance.is_death and instance.character is not None:
        character = Character.objects.get(pk=instance.character_id)
        instance.img = character.img
        instance.title = character.name
        instance.question = 'Умрет?'


@receiver(post_save, sender=Card, weak=False)
def character_death_answers(sender: Card, instance: Card, **kwargs):
    if not CardAnswer.objects.filter(card=instance).exists() and instance.is_death:
        answers = ['Умрет', ' Выживет']
        create_answers(instance, answers)
