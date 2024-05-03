import requests
import urllib.parse

url_ruta = "https://graphhopper.com/api/1/route?"
loc1 = ""
loc2 = ""
clave = "858dec81-70e6-4130-9606-d0bb10a2cd07"  

def geocodificacion(location, clave):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")

    url_geocodificacion = "https://graphhopper.com/api/1/geocode?" 
    url = url_geocodificacion + urllib.parse.urlencode({"q":location, "limit": "1", "key":clave})

    respuesta = requests.get(url)
    datos_json = respuesta.json()
    estado_json = respuesta.status_code
    
    if estado_json == 200 and len(datos_json["hits"]) != 0:
        datos_json = requests.get(url).json()

        latitud = datos_json["hits"][0]["point"]["lat"]
        longitud = datos_json["hits"][0]["point"]["lng"]
        nombre = datos_json["hits"][0]["name"]
        valor = datos_json["hits"][0]["osm_value"]
        
        if "country" in datos_json["hits"][0]:
            pais = datos_json["hits"][0]["country"]
        else:
            pais=""
        
        if "state" in datos_json["hits"][0]:
            estado = datos_json["hits"][0]["state"]
        else:
            estado=""
        
        if len(estado) !=0 and len(pais) !=0:
            nueva_loc = nombre + ", " + estado + ", " + pais
        elif len(estado) !=0:
            nueva_loc = nombre + ", " + pais
        else:
            nueva_loc = nombre
        
        print("URL de la API de Geocodificación para " + nueva_loc + " (Tipo de ubicación: " + valor + ")\n" + url)
    else:
        latitud="null"
        longitud="null"
        nueva_loc=location
        if estado_json != 200:
            print("Estado de la API de Geocodificación: " + str(estado_json) + "\nMensaje de error: " + datos_json["message"])
    return estado_json,latitud,longitud,nueva_loc

while True:
    loc1 = input("Ubicación de inicio: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocodificacion(loc1, clave)
    print(orig)
    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocodificacion(loc2, clave)
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("coche, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    perfil=["coche", "bicicleta", "a pie"]
    vehiculo = input("Ingrese un perfil de vehículo de la lista anterior: ")
    if vehiculo == "salir" or vehiculo == "s":
        break
    elif vehiculo in perfil:
        vehiculo = vehiculo
    else: 
        vehiculo = "coche"
        print("No se introdujo un perfil de vehículo válido. Usando el perfil de coche.")

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        url_rutas = url_ruta + urllib.parse.urlencode({"key":clave, "vehicle":vehiculo}) + op + dp
        estado_rutas = requests.get(url_rutas).status_code
        datos_rutas = requests.get(url_rutas).json()
        print("Estado de la API de Enrutamiento: " + str(estado_rutas) + "\nURL de la API de Enrutamiento:\n" + url_rutas)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3]+ " en " + vehiculo)
        print("=================================================")
        if estado_rutas == 200:
            millas = (datos_rutas["paths"][0]["distance"])/1000/1.61
            km = (datos_rutas["paths"][0]["distance"])/1000
            sec = int(datos_rutas["paths"][0]["time"]/1000%60)
            min = int(datos_rutas["paths"][0]["time"]/1000/60%60)
            hr = int(datos_rutas["paths"][0]["time"]/1000/60/60)
            print("Distancia Recorrida: " + str(datos_rutas["paths"][0]["distance"]) + " m")
            print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(datos_rutas["paths"][0]["instructions"])):
                camino = datos_rutas["paths"][0]["instructions"][each]["text"]
                distancia = datos_rutas["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(camino, distancia/1000, distancia/1000/1.61))
                print("=============================================")
        else:
            print("Mensaje de error: " + datos_rutas["message"])
            print("*************************************************")
