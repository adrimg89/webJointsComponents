from flask import Flask, render_template, request, redirect, url_for

from classes.funciones import get_joints, get_joint_layers, get_connectiontype, getcomp, getExecutionUnits, getLayerGroups

#Creamos una instancia de la aplicación Flask
app = Flask(__name__, static_folder='templates')


#Ruta para la página principal
@app.route("/")
def mensajewelcome():
    output=render_template("html/welcome.html")
    return output

#Llamada a airtable para mostrar joints
@app.route("/joints")
def joints():
    records_list = get_joints()
    return render_template("html/joints.html", records_list=records_list)

#Llamada a airtable para mostrar joint layers
@app.route("/jlayers/<joint>")
def layers(joint):
    records_list = get_joint_layers(joint)
    return render_template("html/jlayers.html", records_list=records_list, joint=joint)

#Llamada a airtable para mostrar joint layers
@app.route("/ctype/<cgt>")
def ctype(cgt):
    records_list = get_connectiontype(cgt)
    primer_elemento=records_list[0]
    CGT_description = primer_elemento['CGtype_description']
    #print(records_list['CGtype_description'])
    return render_template("html/contype.html", records_list=records_list, cgt=cgt, CGT_description=CGT_description)

#Llamada a database rt_buildplatf para mostrar componentes no deprecated
@app.route("/components")
def components():
    listacomponentes=getcomp()
    #print(listacomponentes)
    return render_template("html/components.html", listacomponentes=listacomponentes)
   


#Llamada a database rt_buildplatf para mostrar execution units del componente introducido
@app.route("/eus/<component_code>")
def geteus(component_code):
    listaeus=getExecutionUnits(component_code)
    #return listaeus
    return render_template("html/eus.html", listaeus=listaeus, component_code=component_code)

#Llamada a database rt_buildplatf para mostrar execution units del componente introducido
@app.route("/lg/<eu_code>")
def getlgs(eu_code):
    listalgs=getLayerGroups(eu_code)
    return render_template("html/lgs.html", listalgs=listalgs, eu_code=eu_code)

if __name__=="__main__":
    app.run()