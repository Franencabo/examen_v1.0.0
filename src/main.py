from flask import Flask
from flask import render_template, request, redirect, url_for
from GestionMongo.GestorMongoDb import gestormongo

from flask import session
from datetime import datetime

import os

app = Flask(__name__)
app.secret_key = 'gastos'


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)