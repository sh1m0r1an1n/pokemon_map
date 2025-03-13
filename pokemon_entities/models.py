from django.db import models # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название на японском')
    photo = models.ImageField(null=True, blank=True, default='default_pokemon.png', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        null=True,
        related_name='entities',
        verbose_name='Покемон'
    )
    appeared_at = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='Время исчезновения')
    level = models.PositiveIntegerField(blank=True, default=1, verbose_name='Уровень')
    health = models.PositiveIntegerField(blank=True, default=1, verbose_name='Здоровье')
    strength = models.PositiveIntegerField(blank=True, default=1, verbose_name='Сила')
    defence = models.PositiveIntegerField(blank=True, default=1, verbose_name='Защита')
    stamina = models.PositiveIntegerField(blank=True, default=1, verbose_name='Выносливость')
