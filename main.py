import os
import csv
import argparse
from pathlib import Path
from click import prompt
from services.database import Database

# On check si le dossier ou on va stocker les CSV existe sinon on le crée
Path("./output").mkdir(parents=True, exist_ok=True)

# Récuperation des params de la ligne de commande (Requête MYSQL, Nom du fichier [Optionnel])
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="MYSQL Query")
parser.add_argument("-f", "--filename", help="Nom du fichier", default='output.csv')

# Définition des variables globales
QUERY = parser.parse_args().query
FILENAME = parser.parse_args().filename
FILEPATH = f"./output/{FILENAME}"
TEMPFILE = FILEPATH + '.tmp'
ERROR = None
OVERWRITE = 0

# Check des erreurs
if QUERY is None:
    ERROR = 'Argument -q obligatoire'
elif os.path.exists(FILEPATH):
    OVERWRITE = 1
    value = prompt(f"Le fichier {FILENAME} existe déjà, voulez vous l'écraser ? (y/n)")
    if value not in ('y', 'o'):
        ERROR = 'Exit'

# Si erreur on la print
# Sinon on lance la création du CSV a partir du résultat de la requête
if ERROR is not None:
    print(ERROR)
else:
    try:
        database = Database()
        cursor = database.connection.cursor()
        cursor.execute(QUERY)
        results = cursor.fetchall()
        database.closeConnection()

        column_names = []
        for i in cursor.description:
            column_names.append(i[0])

        results.insert(0, column_names)

        with open(TEMPFILE, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in results:
                csvwriter.writerow(row)

        csvfile.close()
        os.rename(TEMPFILE,FILEPATH)

        if OVERWRITE == 1:
            print(f"Le fichier {FILENAME} a bien été remplacé")
        else:
            print(f"Le fichier {FILENAME} a bien été créé")
    except Exception as error:
        print(error)
