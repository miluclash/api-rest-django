from pokeapi import PokeAPI 
class PokeAPITest:

    def test_calcular_pesos(self):
        api = PokeAPI()
        weights = api.calcular_pesos(-5, 2, 600, 1)
        assert weights["ice"] > 0
        print("calcular_pesos OK")

    def test_seleccionar_tipo(self):
        api = PokeAPI()
        tipo = api.seleccionar_tipo({"fire":10,"water":0})
        assert tipo == "fire"
        print("seleccionar_tipo OK")

    def test_obtener_pokemon(self):
        api = PokeAPI()

        # caso 1: un solo Pokémon
        pokemon = api.obtener_pokemon_por_tipo("fire")
        assert isinstance(pokemon, dict)

        required_fields = ["name", "types"]
        for field in required_fields:
            assert field in pokemon

        print("obtener_pokemon_por_tipo (1 pokemon) OK")

        # caso 2: varios Pokémon
        pokemons = api.obtener_pokemon_por_tipo("fire", 3)
        assert isinstance(pokemons, list)
        assert len(pokemons) == 3

        for p in pokemons:
            assert isinstance(p, dict)
            for field in required_fields:
                assert field in p

        print("obtener_pokemon_por_tipo (varios pokemons) OK")

    def test_tipo_invalido(self):
        api = PokeAPI()

        try:
            api.obtener_pokemon_por_tipo("tipoinventado")
            assert False, "Debía lanzar error"
        except ValueError:
            print("tipo inválido detectado OK")

    def test_obtener_muchos_pokemons(self):
        api = PokeAPI()

        pokemons = api.obtener_pokemon_por_tipo("fire", 105)

        assert isinstance(pokemons, list)
        assert len(pokemons) > 0 
        print("obtener_pokemon_por_tipo maneja exceso de cantidad OK")


    def run_all(self):

        tests = [
            self.test_calcular_pesos,
            self.test_seleccionar_tipo,
            self.test_obtener_pokemon,
            self.test_tipo_invalido,
            self.test_obtener_muchos_pokemons
        ]

        for test in tests:
            try:
                test()
            except AssertionError as e:
                print(f" {test.__name__} falló:", e)
            except Exception as e:
                print(f"Error inesperado en {test.__name__}:", e)


if __name__ == "__main__":
    tester = PokeAPITest()
    tester.run_all()
    api = PokeAPI()
    # pokemon = api.seleccionar_pokemon(15, 5, 500, 1)
    # print(pokemon)
    # pokemones = api.obtener_pokemon_por_tipo("water", 10)
    # for p in pokemones:
    #     print(p["name"])
    # pokemones = api.obtener_pokemon_por_tipo("water", 1)
    # print("-----------------")
    # print(pokemones["name"])