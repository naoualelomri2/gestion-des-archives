import os     #pour gérer les chemins des fichiers et créer les dossiers 
from flask import Flask, render_template, request, redirect,  url_for #Flask: framework web , render_template: afficher les pages HTML, request: recupere les données d'un formulaire , redirect:redirige vers une autre page , url_for:genere lurl d'une fonction flask , send_from_directory:
from werkzeug.utils import secure_filename  #nettoie les noms de fichiers dangereux
from datetime import datetime    #manipuler les dates
from models import db,  Archive
from extensions import db
from flask import send_from_directory  #pour envoyer un fichier en téléchargement 
from sqlalchemy import func   #sqlalchemy est une bibliotheque python qui permet de gerer une base de donnees sans devoir ecrire des requetes sql brutes a la main et on peut representer chaque ligne en un objet python a manipuler 
import re
app = Flask(__name__) # creation de l'application flask

basedir = os.path.abspath(os.path.dirname(__file__))   #récupere le chemin absolu du projet
#app.config est dictionnaire de configuration qui permet la definition des parametres de lapp
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'archive.db')     #utilise une base de données SQLite locale archive.db qui se trouve dans le dossier du projet



# Lie et initialise SQLAlchemy sur l’app
db.init_app(app)   #lie sqlalchemy a flask
os.makedirs(os.path.join(basedir, 'uploads', 'recu'), exist_ok=True)
os.makedirs(os.path.join(basedir, 'uploads', 'envoye'), exist_ok=True)

# Crée les dossiers et la base

with app.app_context():  #creation de la base de donnees et des tables 
    db.create_all()          # on utilise withapp.app_context  car cette operation de create all ne se trouve dans aucune route donc il est necessaire de rappeler le contexte qui est en meme temps lapp

@app.route('/') # ce bloc veut dire que lorsque quelqu'un visite la page daccueil le fct home() sexecute
def home():
    return render_template('index.html')

@app.route('/select_category')
def select_category():
    return render_template('category_select.html')



@app.route('/dashboard/<string:type_doc>')
def dashboard(type_doc):
    folder_path = os.path.join(basedir, 'uploads', type_doc)
    all_archives = Archive.query.all()
    pattern = re.compile(rf"uploads[\\/]{type_doc}[\\/]", re.IGNORECASE)
    archives = [a for a in all_archives if pattern.search(a.chemin)]
    total_archives = len(archives)
    total_size = sum(
        os.path.getsize(os.path.join(folder_path, a.filename))
        for a in archives if os.path.exists(os.path.join(folder_path, a.filename))
    )

    return render_template('dashboard.html',
        total_archives=total_archives,
        total_size=round(total_size / 1024, 2),
        archives=archives,
        selected_type=type_doc
    )


@app.route('/upload/<string:type_doc>', methods=['GET', 'POST'])
def upload(type_doc):
    upload_path = os.path.join(basedir, 'uploads', type_doc)
    os.makedirs(upload_path, exist_ok=True)

    if request.method == 'POST':
        titre = request.form['titre']
        date = request.form['date']
        fichier = request.files['fichier']
        filename = secure_filename(fichier.filename)
        chemin = os.path.join(upload_path, filename)
        fichier.save(chemin)

        archive = Archive(
            titre=titre,
            date_upload=datetime.strptime(date, "%Y-%m-%d"),
            filename=filename,
            chemin=chemin
        )
        db.session.add(archive)
        db.session.commit()
        return redirect(url_for('dashboard', type_doc=type_doc))

    return render_template('upload.html', selected_type=type_doc)





@app.route('/delete/<int:id>/<string:type_doc>')
def delete(id, type_doc):
    archive = Archive.query.get(id)
    if archive:
        try:
            os.remove(archive.chemin)
        except FileNotFoundError:
            pass
        db.session.delete(archive)
        db.session.commit()
    return redirect(url_for('dashboard', type_doc=type_doc))




@app.route('/download/<string:type_doc>/<filename>')
def download(type_doc, filename):
    path = os.path.join(basedir, 'uploads', type_doc)
    return send_from_directory(path, filename)


@app.route('/filter/<string:type_doc>')
def filter_page(type_doc):
    return render_template('filter.html', selected_type=type_doc)



@app.route('/filter_results/<string:type_doc>')
def filter_results(type_doc):
    keyword = request.args.get('keyword', '').lower()
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    #  Filtrer d'abord par dossier "recu" ou "envoye"
    all_archives = Archive.query.all()
    pattern = re.compile(rf"uploads[\\/]{type_doc}[\\/]", re.IGNORECASE)
    filtered_archives = [a for a in all_archives if pattern.search(a.chemin)]

    # filtrer par mot-clé si précisé
    if keyword:
        filtered_archives = [
            a for a in filtered_archives
            if keyword in a.titre.lower() or keyword in a.filename.lower()
        ]

    #  par jour, mois, année
    if day:
        filtered_archives = [a for a in filtered_archives if a.date_upload.day == int(day)]
    if month:
        filtered_archives = [a for a in filtered_archives if a.date_upload.month == int(month)]
    if year:
        filtered_archives = [a for a in filtered_archives if a.date_upload.year == int(year)]

    return render_template('results.html', archives=filtered_archives, selected_type=type_doc)

