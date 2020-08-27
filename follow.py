import json
from pymongo import MongoClient
from leer_archivo import leer_problem
from models.dato import dato
from os import remove, path

#inicializaciones
datos = []
courses = []
registros = 0
mongoClient = MongoClient('localhost',27017)
db = mongoClient.followup
collection = db.registros


#Se crea lista de todos los registros problem_check del tracking.log
#Realiza toda la extracción de los datos y los deja listos para guardarlo en MongoDB
#####YES
datos = leer_problem(collection)


#Inserta los datos en MongoDB
for dato in datos:
   # print(dato)
    registros = registros + 1
    collection.insert_one(dato.toDBCollection())
   # print (dato)
print("Registros Insertados: ", registros)


#Lee todos los registros que sean de envío de exámenes
#Esto para sacar una lista de los cursos en los que hubo cambios.

for dato in datos:
    if dato.course in courses:
        print('Ya está')
    else:
        if dato.name == 'problem_check':
            courses.append(dato.course)
            
        else: 
            print('no problem')


if path.exists('courses.txt'):
    
    for course in courses:
        f = open ('courses.txt','a')
        f.writelines('\n'+ course)
        f.close()
else:
    f = open ('courses.txt','a')
    f.writelines('Course')
    for course in courses:
        f = open ('courses.txt','a')
        f.writelines('\n'+ course)
        f.close()
    
mongoClient.close()


