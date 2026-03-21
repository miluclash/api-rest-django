from wikidata import wikidata_crime
import datetime
searching_crime= wikidata_crime('PruebaCrimenDjango/1.1 (aticasmia007@gmail.com)')
fecha_actual= datetime.datetime.now()

probando = searching_crime.get_crime("2022-05-25") #tendría que meterse la fecha XXXX-XX-XX
probando_fecha_actual= searching_crime.get_crime(fecha_actual)
probando_noCrimen= searching_crime.get_crime("0000-00-00")
#CREAR LOS TEST EN FUNCIONES, mantener los casos de prueba lo más simple posible 
#ej wiki_fechaPasado
#ej wiki_probando fechaFuturo
def wikidata_probando_fechaHardcode (): #-> CONFIRMADO, FUNCIONA!
    assert "homicidio de George Floyd"  in  probando["itemLabel"] #con name, no con el dic
    print("test fecha hardcodeada pasado")

def wikidata_probando_fechaIntroducida(): #-> CONFIRMADO, FUNCIONA!
    assert("homicidio de George Floyd" in probando["itemLabel"]) 
    print("test fecha introducida pasada")
    pass

def wikidata_probando_fechaActual(): 
    assert("Asesinato de Yasuko Watanabe" in probando_fecha_actual["itemLabel"]) #este assert cambiará en función del día!
    print("test fecha actual pasada")

def wikidata_probando_noHayCrimen():
    assert(probando_noCrimen["itemLabel"] is None)
    print("test fecha sin crimen pasada")

def wikidata_probando_muchasPeticiones():
    print("Bucle de peticiones para forzar RateLimit")
    try:
        for i in range(3000): #muchas peticiones, bucle.
            print(f"Petición número: {i}")
            searching_crime.get_crime(fecha_actual)
            
    except Exception:
        print("RageLimit alcanzado")

if __name__=="__main__":
    wikidata_probando_fechaHardcode() 
    wikidata_probando_fechaIntroducida()
    wikidata_probando_fechaActual()
    wikidata_probando_noHayCrimen()
    wikidata_probando_muchasPeticiones()