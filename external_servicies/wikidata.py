import requests

class wikidata_crime():
    def __init__(self, user_agent):
        self.user_agent = user_agent
        pass

    def get_crime(self, actual_date):
        try:
            if type(actual_date) == str:

                current_day=str(actual_date[8:10])  
                current_month=str(actual_date[5:7])
            #print(type(actual_date)) #-< esto me devuelve un str
            #print(current_day)
            #print(current_month)
            else:   
                current_day = str(actual_date.day) 
                current_month = str(actual_date.month)
            
            sparql_query = """SELECT ?itemLabel ?itemDescription ?enlaces WHERE {
            VALUES ?crimen {wd:Q132821 wd:Q318296 wd:Q329425 wd:Q891854} 
            { ?item wdt:P31 ?crimen. } UNION { ?item wdt:P509 ?crimen. }
            ?item wdt:P585 | wdt:P570 ?fecha.
            FILTER(MONTH(?fecha) = [month] && DAY(?fecha) = [day])
            OPTIONAL { ?item wikibase:sitelinks ?enlaces. }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
            }
            ORDER BY DESC(?enlaces)
            LIMIT 1"""

            wikidataURL= "https://query.wikidata.org/sparql"

            query_final = sparql_query.replace("[month]", current_month).replace("[day]", current_day)

            headers = { #para poder pasar el robot txt
                'User-Agent': self.user_agent,
                
            }
            params = {'query':query_final, 'format':'json'}

            response = requests.get(wikidataURL, headers=headers, params=params) 
            devuelve= response.json()
            crimen=devuelve.get("results", {}).get("bindings", []) 
            
            if not crimen: #control de errores, por si la fecha no devuelve ningún crimen!
                print("No se encontraron crímenes para esa fecha.")
                return { "itemLabel": None, "itemDescription": None, "enlaces": None }
            
            #recorro el json/diccionario creando un dic limpio, solo con los valores VALUE de cada KEY
            crimenLimpio={}
            for key in crimen[0].keys():
                value = crimen[0][key]["value"]
                crimenLimpio[key]=value #Lo añado al nuevo dic

            return crimenLimpio 
        except requests.exceptions.RequestException:
            raise Exception("Has alcanzado el RageLimit")

