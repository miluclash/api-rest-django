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
        pokemon = api.seleccionar_pokemon(15,5,500,1)

        assert isinstance(pokemon, dict)

        required_fields = ["name","types"]
        for field in required_fields:
            assert field in pokemon

        print("Pokemon válido")
    def test_tipo_invalido(self):
        api = PokeAPI()

        try:
            api.obtener_pokemon_por_tipo("tipoinventado")
            assert False, "Debía lanzar error"
        except ValueError:
            print("tipo inválido detectado")

    def run_all(self):

        tests = [
            self.test_calcular_pesos,
            self.test_seleccionar_tipo,
            self.test_obtener_pokemon,
            self.test_tipo_invalido
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
    pokemon = api.seleccionar_pokemon(15, 5, 500, 1)
    print(pokemon)