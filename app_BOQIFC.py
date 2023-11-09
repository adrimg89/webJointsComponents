#Esta aplicación permite generar el coste y BOQ de todas las uniones informadas en un IFC
#Input necesario: Ruta del IFC
#Output: Excel en la misma ubicación con el mismo nombre

from classes.funciones import getboxesfilteredwithbalconies, ruta_corrector, boqfromlistofparents,guardarxls

ruta=input(r'Introduce la ruta del archivo IFC: ')

ruta_modificada=ruta_corrector(ruta)

parentsfromifc=getboxesfilteredwithbalconies(ruta)

coste,matjoints,herrajes=boqfromlistofparents(parentsfromifc)

guardarxls(coste,matjoints,herrajes,ruta_modificada)

