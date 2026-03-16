import datetime

from external_servicies.gemini import Gemini
from external_servicies.pokeapi import PokeAPI
from external_servicies.wikidata import wikidata_crime

searching_crime= wikidata_crime('PruebaCrimenDjango/1.1 (aticasmia007@gmail.com)')
fecha_actual= datetime.datetime.now()
probando_fecha_actual= searching_crime.get_crime("2026-04-08")

api = PokeAPI()
pokemon = api.seleccionar_pokemon(15,5,500,1)
ai = Gemini()
ai.generar_broma(pokemon,"Thunderstorm",probando_fecha_actual["itemLabel"], "Piantao Legazpi | Restaurante Argentino Madrid")