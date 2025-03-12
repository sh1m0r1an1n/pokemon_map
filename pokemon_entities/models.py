from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.PositiveIntegerField(null=True)
    health = models.PositiveIntegerField(null=True)
    strength = models.PositiveIntegerField(null=True)
    defence = models.PositiveIntegerField(null=True)
    stamina = models.PositiveIntegerField(null=True)
