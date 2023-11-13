#Esta aplicación permite generar el coste y BOQ de todas las uniones informadas en un IFC
#Input necesario: Ruta del IFC
#Output: Excel en la misma ubicación con el mismo nombre

from classes.funciones import getboxesfilteredwithbalconies, ruta_corrector, boqfromlistofparents,guardarxlsfromIFC, leer_archivo_xlsx, boqfromlistofparentsJ3, guardarxlsfromxls

input_usuario=input("""Elige una opción:
    a) Leer un IFC y exportar excel con BOQ (Joints 2)
    b) Generar un BOQ a partir de un excel con los Parent Joints
    """)

if input_usuario=='a':    
    print('Has elegido la opción "a"')
    ruta=input(r'Introduce la ruta del archivo IFC: ')
    print('Generando info...')

    ruta_modificada=ruta_corrector(ruta)

    parentsfromifc=getboxesfilteredwithbalconies(ruta)

    coste,matjoints,herrajes=boqfromlistofparents(parentsfromifc)

    guardarxlsfromIFC(coste,matjoints,herrajes,ruta_modificada)
    
if input_usuario=='b': 
    print("""
        Recuerda que este archivo debe contener en cada columna los valores correspondientes a:
        
        JS_ParentJointInstanceID, JS_JointTypeID, JS_ConnectionGroupTypeID, Core Matgroup, Q1 Matgroup, Q2 Matgroup, Q3 Matgroup, Q4 Matgroup, QU_Length_m, nrbalconies
        
        """)   
    ruta=input(r'Pásame por favor la ruta del archivo excel: ')
    print('Editando archivo...')
    ruta_modificada=ruta_corrector(ruta)
    listaparents=leer_archivo_xlsx(ruta_modificada)

    listaconcoste,listamateriales,listadeherrajes=boqfromlistofparentsJ3(listaparents)

    guardarxlsfromxls(listaconcoste,listamateriales,listadeherrajes,ruta_modificada)
    
    

