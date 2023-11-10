#Esta aplicación permite generar el coste y BOQ de todas las uniones informadas en un IFC
#Input necesario: Ruta del IFC
#Output: Excel en la misma ubicación con el mismo nombre

from classes.funciones import getboxesfilteredwithbalconies, ruta_corrector, boqfromlistofparents,guardarxls, leer_archivo_xlsx

input_usuario=input("""Elige una opción:
    a) Leer un IFC y exportar excel con BOQ (Joints 2)
    b) Prueba de lectura de xls
    """)

if input_usuario=='a':    
    print('Has elegido la opción "a". Generando info...')
    ruta=input(r'Introduce la ruta del archivo IFC: ')

    ruta_modificada=ruta_corrector(ruta)

    parentsfromifc=getboxesfilteredwithbalconies(ruta)

    coste,matjoints,herrajes=boqfromlistofparents(parentsfromifc)

    guardarxls(coste,matjoints,herrajes,ruta_modificada)
    
if input_usuario=='b':
    print('Has elegido la opción de leer el xls')
    ruta=input(r'Introduce la ruta del xls: ')
    print('Aquí tienes tu resultado: ')
    ruta_modificada=ruta_corrector(ruta)
    resultado=leer_archivo_xlsx(ruta)
    for i in resultado:print(i)
    
    

