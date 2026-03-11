# Create your tests here.
from google_places import GooglePlacesServices
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env') # Carga las variables del .env
api_key = os.getenv('GOOGLE_API_KEY')
def search_places_by_text_test():
    query = "restaurantes cerca de Moratalaz"
    api_key = api_key
    return GooglePlacesServices.search_places_by_text(query=query,api_key=api_key)


def test_api_key_invalida():
    result = GooglePlacesServices.search_places_by_text(query="restaurantes", api_key="INVALID_KEY")
    print('test_api_key_invalida: ',result)
    assert "error" in result

def test_campos_correctos():
    result = GooglePlacesServices.search_places_by_text(query="restaurantes Moratalaz", api_key=api_key)
    print('test_campos_correctos: ',result)
    assert "error" not in result
    for place in result.get("places", []):
        assert "displayName" in place
        assert "formattedAddress" in place

def test_max_resultados():
    result = GooglePlacesServices.search_places_by_text(query="restaurantes Moratalaz", api_key=api_key)
    print('test_max_resultados: ',result)
    assert len(result.get("places", [])) <= 5

if __name__ == "__main__":
    # result = search_places_by_text_test()
    # print(result)
    test_api_key_invalida()
    print('\n')
    test_campos_correctos()
    print('\n')
    test_max_resultados()
    print('\n')
    print("Todos los tests pasaron ✅")
