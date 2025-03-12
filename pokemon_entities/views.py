import folium
import json

from django.http import HttpResponseNotFound
from .models import Pokemon, PokemonEntity
from django.shortcuts import render
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    time_now = timezone.localtime()

    active_entities = PokemonEntity.objects.filter(
        appeared_at__lte=time_now,
        disappeared_at__gt=time_now
    ).select_related('pokemon')

    pokemon_ids = active_entities.values_list('pokemon_id', flat=True).distinct()

    pokemons = Pokemon.objects.filter(id__in=pokemon_ids).prefetch_related('pokemonentity_set')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_on_page = []

    for pokemon in pokemons:
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        active_pokemon_entities = active_entities.filter(pokemon=pokemon)
        for entity in active_pokemon_entities:
            add_pokemon(
                folium_map,
                entity.lat,
                entity.lon,
                img_url
            )

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    time_now = timezone.localtime()

    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__lte=time_now,
        disappeared_at__gt=time_now
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    if pokemon.photo:
        img_url = request.build_absolute_uri(pokemon.photo.url)
    else:
        img_url = DEFAULT_IMAGE_URL

    for entity in pokemon_entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            img_url
        )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'img_url': img_url,
        'description': '',
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
