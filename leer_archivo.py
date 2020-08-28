from contador import contar
from pymongo import MongoClient
from busquedas import busqueda_contenidos, busqueda_ingreso
import json
from models.dato import dato


def leer_problem(collection):
    contProblem = 0
    contProblemGraded = 0
    contMenu = 0
    contMenuClick = 0
    contClickNext = 0
    contClickPrev = 0
    contClickTab = 0
    contPlayVideo = 0
    contPauseVideo = 0
    contStopVideo = 0
    contForocreado = 0
    contForoResponse = 0
    contForocomment = 0
    contIngresos = 0

    # vector para guardar los datos extraídos
    datos = []
    #ruta al archivo tracking.log
    ruta = r'D:\Nueva carpeta\tracking5julio.log'
    archivo = open(ruta, 'r')
    #Leemos linea por linea
    for linea in archivo:
        if not '"username": ""' in linea:
            #Comprobar si existen las lineas con Probem_Check
            if '"name": "problem_check"' in linea:
                contProblem = contar(linea, contProblem)
                #Se convierte en JSON
                linea = json.loads(linea)
                #print(linea)
                dat = dato(
                    linea["username"],
                    linea["name"],
                    linea["time"],
                    linea["time"].split("T")[0],
                    linea["time"].split("T")[1].split(".")[0],
                    linea["page"],
                    linea["page"].split("/")[6],
                    linea["page"].split("/")[7],
                    "Null",
                    linea["session"],
                    linea["context"]["course_id"].split(":")[1],
                    linea["event"])
                
                #print(dat)
                #Se busca si existe ya el registro
                busqueda = collection.find_one({"username": linea["username"],
                                                "name": linea["name"],
                                                "date": linea["time"].split("T")[0],
                                                "time": linea["time"].split("T")[1].split(".")[0]}
                                                )
                
                #Si NO existe se agrega a la lista
                if busqueda:
                    print("Linea existente")
                else:
                    #print(dat)
                    datos.append(dat)
        
            if '"name": "problem_graded"' in linea:
                #print("segunda parte")
                #print(linea)
                contProblemGraded = contar(linea, contProblemGraded)
                #Se convierte en JSON
                linea = linea.split(", \"\\n\\n")[0]
                linea = linea + "]}"
                #print(linea)
                linea = json.loads(linea)
                #print(linea)
                dat2 = dato(
                    linea["username"],
                    linea["name"],
                    linea["time"],
                    linea["time"].split("T")[0],
                    linea["time"].split("T")[1].split(".")[0],
                    linea["page"],
                    linea["page"].split("/")[6],
                    linea["page"].split("/")[7],
                    "Null",
                    linea["session"],
                    linea["context"]["course_id"].split(":")[1],
                    linea["event"][0])
                
                #print(dat2)
                #Se busca si existe ya el registro
                busqueda2 = collection.find_one({"username": linea["username"],
                                                "name": linea["name"],
                                                "date": linea["time"].split("T")[0],
                                                "time": linea["time"].split("T")[1].split(".")[0]}
                                                )
                
                #Si NO existe se agrega a la lista
                if busqueda2:
                    print("Linea existente")
                else:
                    #print(dat2)
                    datos.append(dat2)

            if '"name": "edx.bi.course.upgrade.sidebarupsell.displayed"' in linea:
                #print("Contenidos_Menu")
                #print(linea)
                contMenu = contar(linea, contMenu)
                #Se convierte en JSON
                #linea = linea.split(", \"\\n\\n")[0]
                #linea = linea + "]}"
                #print(linea)
                linea = json.loads(linea)
                #print(linea)
                dat3 = dato(
                    linea["username"],
                    "nav_content",
                    linea["time"],
                    linea["time"].split("T")[0],
                    linea["time"].split("T")[1].split(".")[0],
                    linea["page"],
                    "Null",
                    "Null",
                    "Null",
                    linea["session"],
                    linea["context"]["course_id"].split(":")[1],
                    "Null")
                
                #print(dat3)
                #Se busca si existe ya el registro
                busqueda3 = collection.find_one({"username": linea["username"],
                                                "name": "nav_content",
                                                "date": linea["time"].split("T")[0],
                                                "time": linea["time"].split("T")[1].split(".")[0]}
                                                )
                
                #Si NO existe se agrega a la lista
                if busqueda3:
                    print("Linea existente")
                else:
                    #print(dat)
                    datos.append(dat3)

            if '"name": "edx.ui.lms.link_clicked"' in linea:
                if 'type@vertical' in linea:
                    #print("Contenidos_Click!")
                    #print(linea)
                    contMenuClick = contar(linea, contMenuClick)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    #print(linea)
                    dat4 = dato(
                        linea["username"],
                        "nav_content_click",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        "Null",
                        "Null",
                        linea["event"]['target_url'].split("@")[2],
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    
                    time = dat4.time
                    timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+time[6]+time[7]
                    
                    section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+(time[6])
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                        
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+(time[4])
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                        
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+1)
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-1)
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+2)
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-2)
                        section = busqueda_contenidos(dat4.username,dat4.date,timeSring,dat4.session)

                    dat4.page = section
                    dat4.section = section.split("/")[4]
                    dat4.subsection = section.split("/")[5]
                    dat4.unit = section.split("/")[6]
                    #print(dat4)
                    
                    
                    #Se busca si existe ya el registro
                    busqueda4 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_click",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda4:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat4)

            if '"name": "edx.ui.lms.sequence.next_selected"' in linea:
                if '\\"new\\":' in linea:
                    #print("Contenidos_Click_Siguiene")
                    #print(linea)
                    contClickNext = contar(linea, contClickNext)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    #print(linea)
                    
                    dat5 = dato(
                        linea["username"],
                        "nav_content_next",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        linea["event"]['new'],
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    #Se busca si existe ya el registro
                    busqueda5 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_next",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda5:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat5) 

            if '"name": "edx.ui.lms.sequence.previous_selected"' in linea:
                if '\\"new\\":' in linea:
                    #print("Contenidos_Click_Anterior")
                    #print(linea)
                    contClickPrev = contar(linea, contClickPrev)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    #print(linea)
                    
                    dat6 = dato(
                        linea["username"],
                        "nav_content_prev",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        linea["event"]['new'],
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    #Se busca si existe ya el registro
                    busqueda6 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_prev",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda6:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat6)

            if '"name": "edx.ui.lms.sequence.tab_selected"' in linea:
                if '\\"new\\":' in linea:
                    #print("Contenidos_Click_Tab")
                    #print(linea)
                    contClickTab = contar(linea, contClickTab)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    #print(linea)
                    
                    dat7 = dato(
                        linea["username"],
                        "nav_content_tab",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        linea["event"]['new'],
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    #Se busca si existe ya el registro
                    busqueda7 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_tab",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda7:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat7)

            if '"name": "edx.ui.lms.sequence.next_selected"' in linea:
                if '"event_type": "edx.ui.lms.sequence.next_selected"' in linea:
                    #print("Contenidos_Click_SigContenido")
                    #print(linea)
                    contClickNext = contar(linea, contClickNext)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    
                    dat8 = dato(
                        linea["username"],
                        "nav_content_next",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        "1",
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    time = dat8.time
                    timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+time[6]+time[7]
                    section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+(time[6])
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+(time[4])
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+1)
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-1)
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+2)
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-2)
                        section = busqueda_contenidos(dat8.username,dat8.date,timeSring,dat8.session)

                    
                    
                    dat8.page = section
                    dat8.section = section.split("/")[4]
                    dat8.subsection = section.split("/")[5]
                    
                    #Se busca si existe ya el registro
                    busqueda8 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_next",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda8:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat8) 

            if '"name": "edx.ui.lms.sequence.previous_selected"' in linea:
                if '"event_type": "edx.ui.lms.sequence.previous_selected"' in linea:
                    #print("Contenidos_Click_SigContenido")
                    #print(linea)
                    contClickPrev = contar(linea, contClickPrev)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    
                    dat9 = dato(
                        linea["username"],
                        "nav_content_prev",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        "last",
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        "Null")
                    
                    time = dat9.time
                    timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+time[6]+time[7]
                    section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+(time[6])
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+(time[4])
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+1)
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-1)
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+2)
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    if "Sin Coincidencia" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-2)
                        section = busqueda_contenidos(dat9.username,dat9.date,timeSring,dat9.session)
                    
                    dat9.page = section
                    dat9.section = section.split("/")[4]
                    dat9.subsection = section.split("/")[5]
                    
                    #Se busca si existe ya el registro
                    busqueda9 = collection.find_one({"username": linea["username"],
                                                    "name": "nav_content_prev",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda9:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat9)

            if '"name": "play_video"' in linea:
                
                if '"event_type": "play_video"' in linea:
                    #print("Play Video")
                    #print(linea)
                    contPlayVideo = contar(linea, contPlayVideo)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    
                    unit = linea["page"].split("/")[8].split("?")[0]
                    
                    if unit =="":
                        unit = "1"
                    
                    
                    dat10 = dato(
                        linea["username"],
                        "play_video",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["currentTime"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        unit,
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["code"]
                        )
                    
                    #Se busca si existe ya el registro
                    busqueda10 = collection.find_one({"username": linea["username"],
                                                    "name": "play_video",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda10:
                        print("Linea existente")
                    else:
                        #print(dat)
                        datos.append(dat10)

            if '"name": "pause_video"' in linea:
                
                if '"event_type": "pause_video"' in linea:
                    #print("Pause Video")
                    #print(linea)
                    contPauseVideo = contar(linea, contPauseVideo)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    
                    unit = linea["page"].split("/")[8].split("?")[0]
                    
                    if unit =="":
                        unit = "1"
                    
                    
                    dat11 = dato(
                        linea["username"],
                        "pause_video",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["page"].split("?")[0],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        unit,
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["code"]
                        )
                    
                    #Se busca si existe ya el registro
                    busqueda11 = collection.find_one({"username": linea["username"],
                                                    "name": "pause_video",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda11:
                        print("Linea existente")
                    else:
                        
                        datos.append(dat11)

            if '"name": "stop_video"' in linea:
                
                if '"event_type": "stop_video"' in linea:
                    #print("Stop Video")
                    #print(linea)
                    contStopVideo = contar(linea, contStopVideo)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    
                    unit = linea["page"].split("/")[8].split("?")[0]
                    
                    if unit =="":
                        unit = "1"
                    
                    
                    dat12 = dato(
                        linea["username"],
                        "stop_video",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["currentTime"],
                        linea["page"].split("/")[6],
                        linea["page"].split("/")[7],
                        unit,
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["code"]
                        )
                    #print(dat10)
                    #Se busca si existe ya el registro
                    busqueda12 = collection.find_one({"username": linea["username"],
                                                    "name": "stop_video",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda12:
                        print("Linea existente")
                    else:
                        #print("Prueba")
                        datos.append(dat12)


            if '"name": "edx.forum.thread.created"' in linea:
                #print(linea)
                if '"event_type": "edx.forum.thread.created"' in linea:
                    #print("Foro creado")
                    #print(linea)
                    contForocreado = contar(linea, contForocreado)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    if "courseware" in linea["referer"]:
                        dat13 = dato(
                        linea["username"],
                        "edx.forum.thread.created",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["commentable_id"],
                        linea["referer"].split("/")[6],
                        linea["referer"].split("/")[7],
                        linea["referer"].split("/")[8].split("?")[0],
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["title"]
                        )
                    
                    if "discussion/forum/" in linea["referer"]:
                        dat13 = dato(
                        linea["username"],
                        "edx.forum.thread.created",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["commentable_id"],
                        "disscussion",
                        "Forum",
                        "1",
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["title"]
                        )

                    
                    #print(dat13)
                    #Se busca si existe ya el registro
                    busqueda13 = collection.find_one({"username": linea["username"],
                                                    "name": "edx.forum.thread.created",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda13:
                        print("Linea existente")
                    else:
                        #print("Prueba")
                        datos.append(dat13)


            if '"name": "edx.forum.response.created"' in linea:
                #print(linea)
                if '"event_type": "edx.forum.response.created"' in linea:
                    print("Foro respuesta creada")
                    #print(linea)
                    contForoResponse = contar(linea, contForoResponse)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    if "courseware" in linea["referer"]:    
                        dat14 = dato(
                            linea["username"],
                            "edx.forum.response.created",
                            linea["time"],
                            linea["time"].split("T")[0],
                            linea["time"].split("T")[1].split(".")[0],
                            linea["referer"].split("?")[0],
                            linea["referer"].split("/")[6],
                            linea["referer"].split("/")[7],
                            linea["referer"].split("/")[8].split("?")[0],
                            linea["session"],
                            linea["context"]["course_id"].split(":")[1],
                            linea["event"]["title"]
                            )
                    
                    if "discussion/forum/" in linea["referer"]:
                        dat14 = dato(
                        linea["username"],
                        "edx.forum.response.created",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["commentable_id"],
                        "disscussion",
                        "Forum",
                        "1",
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["title"]
                        )
                    
                    
                    #print(dat13)
                    #Se busca si existe ya el registro
                    busqueda14 = collection.find_one({"username": linea["username"],
                                                    "name": "edx.forum.response.created",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda14:
                        print("Linea existente")
                    else:
                        #print("Prueba")
                        datos.append(dat14)


            if '"name": "edx.forum.comment.created"' in linea:
                #print(linea)
                if '"event_type": "edx.forum.comment.created"' in linea:
                    print("Foro Comentario creada")
                    #print(linea)
                    contForocomment = contar(linea, contForocomment)
                    #Se convierte en JSON
                    linea = linea.replace('"{', '{', 1)
                    linea = linea.replace('}"', '}', 1)
                    linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                    linea = json.loads(linea)
                    
                    if "courseware" in linea["referer"]:                                                                
                        dat15 = dato(
                            linea["username"],
                            "edx.forum.comment.created",
                            linea["time"],
                            linea["time"].split("T")[0],
                            linea["time"].split("T")[1].split(".")[0],
                            linea["referer"].split("?")[0],
                            linea["referer"].split("/")[6],
                            linea["referer"].split("/")[7],
                            linea["referer"].split("/")[8].split("?")[0],
                            linea["session"],
                            linea["context"]["course_id"].split(":")[1],
                            linea["event"]["title"]
                            )
                    
                    if "discussion/forum/" in linea["referer"]:
                        dat15 = dato(
                        linea["username"],
                        "edx.forum.comment.created",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        linea["event"]["commentable_id"],
                        "disscussion",
                        "Forum",
                        "1",
                        linea["session"],
                        linea["context"]["course_id"].split(":")[1],
                        linea["event"]["title"]
                        )

                    #print(dat13)
                    #Se busca si existe ya el registro
                    busqueda15 = collection.find_one({"username": linea["username"],
                                                    "name": "edx.forum.comment.created",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    
                    #Si NO existe se agrega a la lista
                    if busqueda15:
                        print("Linea existente")
                    else:
                        #print("Prueba")
                        datos.append(dat15)


            if '"referer": "http://selene.unicauca.edu.co/dashboard"' in linea:
                
                #print("INGRESOS")
                #print(linea)
                
                    #Se convierte en JSON
                linea = linea.replace('"{', '{', 1)
                linea = linea.replace('}"', '}', 1)
                linea = linea.replace('\\"', '"')
                    
                    #linea = linea + "]}"
                    #print(linea)
                linea = json.loads(linea)
                if 'course' in linea["event_type"]:
                    #print(linea["event_type"])
                    validar = linea["event_type"].split("/")[3]
                
                if 'course' in validar:
                    contIngresos = contar(linea, contIngresos)                                        
                    dat16 = dato(
                        linea["username"],
                        "Signin",
                        linea["time"],
                        linea["time"].split("T")[0],
                        linea["time"].split("T")[1].split(".")[0],
                        "NULL",
                        "NULL",
                        "NULL",
                        "NULL",
                        "Buscar",
                        linea["context"]["course_id"].split(":")[1],
                        "NULL"
                        )
                    
                    time = dat16.time
                    timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+time[6]+time[7]
                    section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                    
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+time[4]+time[5]+(time[6])
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                        
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+(time[4])
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                        
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+1)
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-1)
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])+2)
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                    if "Sin Sesion" in section:
                        timeSring = ""+time[0]+time[1]+time[2]+time[3]+str(int(time[4])-2)
                        section = busqueda_ingreso(dat16.username,dat16.date,timeSring)
                    
                    dat16.session = section


                    #Se busca si existe ya el registro
                    busqueda16 = collection.find_one({"username": linea["username"],
                                                    "name": "Signin",
                                                    "date": linea["time"].split("T")[0],
                                                    "time": linea["time"].split("T")[1].split(".")[0]}
                                                    )
                    validar = "null"
                    #Si NO existe se agrega a la lista
                    if busqueda16:
                        print("Linea existente")
                    else:
                        #print(dat16)
                        datos.append(dat16)

    print ("Problem_Check: ", contProblem)
    print ("Problem_Graded: ", contProblemGraded)
    print ("Nav_Menu: ", contMenu)
    print ("Nav_Click: ", contMenuClick)
    print ("Nav_Siguiente: ", contClickNext)
    print ("Nav_Previo: ", contClickPrev)
    print ("Nav_Tab: ", contClickTab)
    print ("Play_video: ", contPlayVideo)
    print ("Pause_video: ", contPauseVideo)
    print ("Stop_video: ", contStopVideo)
    print ("Foro creado: ", contForocreado)
    print ("Foro respuesta: ", contForoResponse) 
    print ("Foro Comentario: ", contForocomment)
    print ("Ingresos: ", contIngresos) 
    archivo.close()
    return datos


