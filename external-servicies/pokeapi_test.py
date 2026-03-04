from pokeapi import PokeAPI


class PokeAPITest:

    def run_tests(self):
        api = PokeAPI()

        pokemon = api.seleccionar_pokemon(
            temperature=15,
            windspeed=5,
            weather_code=500,
            is_day=1
        )

        weights = api.calcular_pesos(-5, 2, 600, 1)
        assert weights["ice"] > 0
        print("✔ TEST OK Comprobación de pesos")

        tipo = api.seleccionar_tipo({"fire": 10, "water": 0})
        assert tipo == "fire"
        print("✔ TEST OK Comprobacion de tipos")

        assert isinstance(pokemon, dict), "La respuesta debe ser un diccionario"
        print("✔ TEST OK La respuesta es un diccionario")
        # Campos mínimos que siempre existen en PokeAPI
        required_fields = ["id", "name", "height", "weight", "types", "sprites"]
        for field in required_fields:
            assert field in pokemon, f"Falta el campo obligatorio: {field}"
        print("✔ TEST OK Tiene todos los campos obligatorios")
        # Validar tipos
        assert isinstance(pokemon["types"], list), "types debe ser una lista"
        print("✔ TEST OK Types es una lista")
        assert len(pokemon["types"]) > 0, "Debe tener al menos un tipo"
        print("✔ TEST OK Tiene al menos un tipo")
        for t in pokemon["types"]:
            assert "type" in t, "Cada entrada en types debe tener 'type'"
            assert "name" in t["type"], "Cada type debe tener 'name'"
        print("✔ TEST OK Todas las entradas de types tiene type y name")
        # Validar sprites
        assert isinstance(pokemon["sprites"], dict), "sprites debe ser un dict"
        print("✔ TEST OK Sprites es un diccionario")


# Ejecutar tests si se llama directamente
if __name__ == "__main__":
    tester = PokeAPITest()
    tester.run_tests()
