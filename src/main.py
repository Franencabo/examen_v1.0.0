from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import session
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

import os

MONGO_ULR_ATLAS = 'mongodb+srv://Franencabo:Aerobictotal2019@cluster0-8p1xr.mongodb.net/test?retryWrites=true&w=majority'

client = MongoClient(MONGO_ULR_ATLAS, ssl_cert_reqs = False)
db = client['gastos']
collection_usuarios = db['usuarios']
collection_coche = db['coche']


app = Flask(__name__)
app.secret_key = 'gastos'


@app.route('/', methods=['GET','POST'])
def index():
    if 'email' in session:
        
        return redirect('vergastos')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje=""
    email="" 
    
    if request.method == 'POST':
        nick = request.form.get('nick')
        email = request.form.get('email')
        password = request.form.get('password')

        # comprobamos si el email está en la base de datos
        busqueda_por_email = list(collection_usuarios.find({'email': email}))
        # sino está lo registramos
        if nick != "" and email != "" and password !="":
            if len(busqueda_por_email) == 0:
                nuevo_registro = collection_usuarios.insert_one({
            "nick": nick,
            "email": email,
            "password": password
        })
                session['nombre'] = nick
                session['email'] = email
                session['password'] = password
                return render_template('/creargastos.html')
            # si está sale un mensaje en pantalla
            else:
                mensaje = "Ya estás registrado en este sorteo"
                return render_template('login.html',mensaje=mensaje)
        else:
            mensaje = "Rellena los campos, por favor."
            return render_template('login.html', mensaje=mensaje)
    
    return render_template('login.html')

@app.route('/creargastos', methods=['GET','POST'])
def creargastos():
    if request.method == 'POST':
        mensaje = "Creado con éxito"
        fecha = request.form.get('fecha')
        cantidad = request.form.get('cantidad')
        titulo = request.form.get('titulo')
        lugar = request.form.get('cantidad')
        texto = request.form.get('texto')
        
        if texto != "":
            nuevogasto = collection_coche.insert_one({'fecha':fecha, 'cantidad': cantidad, 'titulo': titulo, 'lugar':lugar, 'texto':texto})
            return render_template('exito.html', mensaje=mensaje)
        else:
            mensaje = "La nota no puede estar vacía."
            return render_template('creargastos.html', mensaje=mensaje)

    fecha = "{0}-{1}-{2}".format(datetime.now().day, datetime.now().month, datetime.now().year)
      
    
    return render_template('creargastos.html', fecha=fecha)


    return render_template('creargastos.html')


@app.route('/vergastos', methods=['GET','POST'])
def vergastos():
    resultados=""
    if request.method == 'GET':
        resultados = collection_coche.find({}).sort("fecha", 1)
        lista = []
        if resultados != None:
            for elemento in resultados:
                lista.append(elemento)
            lista.sort( key=lambda results: datetime.strptime(results["fecha"], "%d-%m-%Y"), reverse=True)
            return render_template('vergastos.html', datos=lista, len=len(lista))
    return render_template('vergastos.html')


@app.route('/actualizargastos/<string:id>,<string:titulo>,<string:fecha>,<string:texto>', methods=['GET'])
@app.route('/actualizargastos', methods=['POST'])
def actualizar(id=None, fecha=None, titulo=None, texto=None):
    
    
    # fecha = request.args.get('fecha')
    # texto = request.args.get('texto')
    
    if request.method == 'POST':
        mensaje = "Actualizado con éxito"
        id = request.form.get('id')
        nuevotitulo = request.form.get('nuevo_titulo')
        nuevotexto = request.form.get('nuevo_texto')
        nuevafecha = request.form.get('nueva_fecha')

        print(nuevotexto)
        resultadonew = collection_coche.update_one({"_id": ObjectId(id)},{"$set": {"fecha": nuevafecha, "titulo":nuevotitulo, "texto" : nuevotexto}})
        
        return render_template('exito.html', mensaje=mensaje)
    else:
        return render_template('actualizar.html', id=id, fecha=fecha, titulo=titulo, texto=texto)
    return render_template('actualizar.html')


@app.route('/salir', methods =['GET','POST'])
def salir():
    if request.method =='POST':
        session.clear()
        return render_template('index.html')
    return render_template("salir.html")
    
    


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)