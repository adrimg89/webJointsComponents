#Esta aplicación permite generar el coste y BOQ de todas las uniones informadas en un IFC
#Input necesario: Ruta del IFC
#Output: Excel en la misma ubicación con el mismo nombre

from classes.funciones import getboxesfilteredwithbalconies, ruta_corrector,guardarxlsfromIFC, leer_archivo_xlsx, boqfromlistofparentsJ3, guardarxlsfromxls,export2excel,export_excel_infoallboxes,export_excel_infofilteredboxes, getmodeledconnections



input_usuario=input("""Elige una opción:
    a) Leer un IFC y exportar excel con BOQ
    b) Generar un BOQ a partir de un excel con los Parent Joints
    c) Sólo extraer datos de las cajas de un IFC
    """)

if input_usuario=='a':    
    print('Has elegido la opción "a"')
    ruta=input(r'Introduce la ruta del archivo IFC: ')
    inputcalculoconexion=input("""Indícame qué situación hay en el proyecto:
        a) No hay herrajes modelados
        b) Hay herrajes modelados y tienen asignados los parent correctamente. 
        c) Hay herrajes modelados. No todos los parent están bien informados
                               """)
    
    if inputcalculoconexion == 'a':
        print('Se reportarán los datos inferidos en las cajas')
    elif inputcalculoconexion=='b':
        print('Se comprobará para cada parent si tiene herrajes modelados. Si hay algo modelado será reportado junto con lo inferido que tenga tipificado "is_modeled=No"')
    elif inputcalculoconexion=='c':
        print("""De las cajas únicamente se reportará todo lo que esté marcado como "is_modeled=No".
La pestaña "Parentwithcost" no mostrará el coste correcto. Revisar coste en Listamateriales y Listaherrajes""")
    else:
        print('No has elegido una opción válida. Por favor, elige a, b ó c.')
    
    print('Generando info...')

    ruta_modificada=ruta_corrector(ruta)

    parentsfromifc=getboxesfilteredwithbalconies(ruta_modificada)
    
    herrajesmodelados=getmodeledconnections(ruta_modificada)

    coste,matjoints,herrajes=boqfromlistofparentsJ3(parentsfromifc,herrajesmodelados,inputcalculoconexion)

    guardarxlsfromIFC(coste,matjoints,herrajes,ruta_modificada)
    
if input_usuario=='b': 
    print("""
        Recuerda que este archivo debe contener en cada columna los valores correspondientes a:
        
        JS_ParentJointInstanceID, JS_JointTypeID, JS_ConnectionGroupTypeID, Core Matgroup, Q1 Matgroup, Q2 Matgroup, Q3 Matgroup, Q4 Matgroup, QU_Length_m, nrbalconies
        
        """)   
    ruta=input(r'Pásame por favor la ruta del archivo excel: ')
    # rutaIFC=input(r'Ahora pásame por favor la ruta del archivo IFC para ver si tiene herrajes modelados: ')
    print('Editando archivo...')
    ruta_modificada=ruta_corrector(ruta)
    # rutaIFC_correcta=ruta_corrector(rutaIFC)
    listaparents=leer_archivo_xlsx(ruta_modificada)

    herrajesmodelados=[]

    herrajesmodelados=getmodeledconnections(ruta_modificada)

    listaconcoste,listamateriales,listadeherrajes=boqfromlistofparentsJ3(listaparents,herrajesmodelados,'a')

    guardarxlsfromxls(listaconcoste,listamateriales,listadeherrajes,ruta_modificada)
    
if input_usuario=='c':
    inputcajas=input("""Elige por favor el tipo de exportación
    a) Todas las cajas del modelo
    b) La info de los parent joint, excluyendo repetidos
    c) La info de los parent joint, excluyendo repetidos, e incluyendo número de openings que generan HoldDown
    """)
    
    rutaIFC=input(r'Ahora pásame por favor la ruta del archivo IFC: ')
    rutaIFC_correcta=ruta_corrector(rutaIFC)
    
    if inputcajas=="a":
        export_excel_infoallboxes(rutaIFC_correcta)
    

    if inputcajas=="b":
        export_excel_infofilteredboxes(rutaIFC_correcta)
        

    if inputcajas=="c":
        export2excel(rutaIFC_correcta)
    
    

