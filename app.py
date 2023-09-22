from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from classes.funciones import get_joints, get_joint_layers, get_connectiontype, getcomp, getExecutionUnits, getLayerGroups, getcgclass, getcgtype, get_clayers

from passwords import app_key

#Creamos una instancia de la aplicación Flask
app = Flask(__name__, static_folder='templates')
app.secret_key = app_key

login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

users = {
    'user': {'password': 'p'}
}

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contrasena = request.form.get("password")

        if usuario in users and users[usuario]['password'] == contrasena:
            user = User(usuario)
            login_user(user)
            return redirect(url_for("mensajewelcome"))
        else:
            return "Autenticación fallida. Intente nuevamente."

    return render_template("html/login.html")
    


#Ruta para la página principal
@app.route("/main")
@login_required
def mensajewelcome():
    output=render_template("html/welcome.html")
    return output

#Llamada a airtable para mostrar joints
@app.route("/joints")
@login_required
def joints():
    records_list = get_joints()
    return render_template("html/joints.html", records_list=records_list)

#Llamada a airtable para mostrar joint layers
@app.route("/jlayers/<joint>")
@login_required
def layers(joint):
    records_list = get_joint_layers(joint)
    return render_template("html/jlayers.html", records_list=records_list, joint=joint)

#Llamada a airtable para mostrar joint layers
@app.route("/ctype/<cgt>")
@login_required
def ctype(cgt):
    records_list = get_connectiontype(cgt)
    layers_list = get_clayers(cgt)
    primer_elemento=records_list[0]
    CGT_description = primer_elemento['CGtype_description']
    #print(records_list['CGtype_description'])
    return render_template("html/contype.html", records_list=records_list, cgt=cgt, CGT_description=CGT_description, layers_list=layers_list)
    
#Llamada a airtable para mostrar joints
@app.route("/cgclass")
@login_required
def web_cgclass():
    cgclass_list = getcgclass()
    return render_template("html/cgclass.html", cgclass_list=cgclass_list)
    #for i in getcgclass():print (i)

#Llamada a airtable para mostrar connectiongroup type
@app.route("/cgclass/<cgclass>")
@login_required
def web_getcgtype(cgclass):
    cgt_list=getcgtype(cgclass)    
    return render_template("html/cgt.html", cgt_list=cgt_list)

#Llamada a database rt_buildplatf para mostrar componentes no deprecated
@app.route("/components")
@login_required
def components():
    listacomponentes=getcomp()
    #print(listacomponentes)
    return render_template("html/components.html", listacomponentes=listacomponentes)
   


#Llamada a database rt_buildplatf para mostrar execution units del componente introducido
@app.route("/eus/<component_code>")
@login_required
def geteus(component_code):
    listaeus=getExecutionUnits(component_code)
    #return listaeus
    return render_template("html/eus.html", listaeus=listaeus, component_code=component_code)

#Llamada a database rt_buildplatf para mostrar execution units del componente introducido
@app.route("/lg/<eu_code>")
@login_required
def getlgs(eu_code):
    listalgs=getLayerGroups(eu_code)
    return render_template("html/lgs.html", listalgs=listalgs, eu_code=eu_code)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__=="__main__":
    app.run()