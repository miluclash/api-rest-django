import random
import requests


class PokeAPI:

    def calcular_pesos(self, temperature, windspeed, weather_code, is_day):
        weather_code = weather_code / 100
        windspeed = (windspeed / 1000) * 3600

        weights = {
            "ice": 0, "water": 0, "steel": 0, "grass": 0, "normal": 0, "ground": 0,
            "fire": 0, "electric": 0, "fighting": 0, "dragon": 0, "flying": 0,
            "ghost": 0, "psychic": 0, "dark": 0
        }

        # --- TEMPERATURA ---
        if temperature < 0:
            weights["ice"] += 5
        elif temperature < 10:
            weights["water"] += 4
            weights["steel"] += 2
        elif temperature < 20:
            weights["grass"] += 3
            weights["normal"] += 2
            weights["ground"] += 2
        elif temperature < 30:
            weights["fire"] += 3
            weights["electric"] += 2
            weights["fighting"] += 2
        else:
            weights["fire"] += 3
            weights["dragon"] += 3

        # --- VIENTO ---
        if windspeed > 25:
            weights["flying"] += 5
            weights["dragon"] += 2
        elif windspeed > 10:
            weights["flying"] += 3
            weights["electric"] += 2
        else:
            weights["normal"] += 1
            weights["grass"] += 1

        # --- WEATHER CODE ---
        if weather_code == 0:
            weights["fire"] += 3
            weights["flying"] += 2
            weights["dragon"] += 1

        elif weather_code in [1, 3, 8]:
            weights["grass"] += 3
            weights["normal"] += 2
            weights["ghost"] += 1
            weights["water"] += 2
            weights["dragon"] += 1

        elif weather_code == 2:
            weights["electric"] += 4
            weights["water"] += 3
            weights["dragon"] += 1

        elif weather_code == 7:
            weights["ghost"] += 3
            weights["psychic"] += 2

        elif weather_code == 5:
            weights["water"] += 4
            weights["dragon"] += 1

        elif weather_code == 6:
            weights["ice"] += 5
            weights["water"] += 1
            weights["dragon"] += 1

        # --- DÍA / NOCHE ---
        if is_day == 1:
            weights["normal"] += 3
            weights["grass"] += 2
            weights["fire"] += 2
            weights["flying"] += 2
            weights["ghost"] -= 1
            weights["dark"] -= 1
        else:
            weights["ghost"] += 4
            weights["dark"] += 3
            weights["psychic"] += 2
            weights["grass"] -= 1
            weights["fire"] -= 1

        return {t: max(0, w) for t, w in weights.items()}

    def seleccionar_tipo(self, weights):
        tipos = list(weights.keys())
        probs = list(weights.values())
        total = sum(probs)

        if total == 0:
            return "normal"

        return random.choices(tipos, weights=probs, k=1)[0]

    def obtener_pokemon_por_tipo(self, tipo):
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/type/{tipo}")
            if response.status_code != 200:
                raise ValueError(f"Tipo de pokemon inválido: {tipo}")
            data = response.json()
            if "pokemon" not in data or len(data["pokemon"]) == 0:
                raise ValueError("No se encontraron pokemon para este tipo")
            entry = random.choice(data["pokemon"])
            pokemon_url = entry["pokemon"]["url"]
            pokemon_response = requests.get(pokemon_url)
            if pokemon_response.status_code != 200:
                raise RuntimeError("Error obteniendo datos del pokemon")
            return pokemon_response.json()
        except requests.exceptions.RequestException:
            raise ConnectionError("No se pudo conectar con PokeAPI")

    def seleccionar_pokemon(self, temperature, windspeed, weather_code, is_day):
        if not isinstance(temperature, (int, float)):
            raise TypeError("temperature debe ser numérico")
        if not isinstance(windspeed, (int, float)):
            raise TypeError("windspeed debe ser numérico")
        if is_day not in [0,1]:
            raise ValueError("is_day debe ser 0 o 1")
        weights = self.calcular_pesos(temperature, windspeed, weather_code, is_day)
        tipo = self.seleccionar_tipo(weights)
        return self.obtener_pokemon_por_tipo(tipo)


