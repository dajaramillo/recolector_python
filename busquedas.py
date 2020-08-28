import json

def busqueda_contenidos(username,date,time,session):
    ruta = r'D:\Nueva carpeta\tracking5julio.log'
    archivo = open(ruta, 'r')
    busqueda = "/1/2/Sin Coincidencia/Sin Coincidencia/Sin Coincidencia/Sin Coincidencia"
    #Leemos linea por linea
    for linea in archivo:
        if username in linea:
            if "courseware" in linea:
                if ', "event_type": "/' in linea:
                    if not "/discussion/forum" in linea:
                        
                        
                        if time in linea:
                            linea = json.loads(linea)
                            comprobar = linea["event_type"]
                            comprobar = comprobar.split("/")[3]
                            if "courseware" in comprobar:
                                
                                busqueda = linea["event_type"]
                        
              

    return busqueda

def busqueda_ingreso(username,date,time):
    ruta = r'D:\Nueva carpeta\tracking5julio.log'
    archivo = open(ruta, 'r')
    busqueda = "Sin Sesion"
    #Leemos linea por linea
    for linea in archivo:
        if username in linea:
            if '"session"' in linea:
                if time in linea:
                    linea = json.loads(linea)
                    busqueda = linea["session"]
                        
              

    return busqueda
