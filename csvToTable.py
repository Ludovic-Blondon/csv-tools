import os.path
import csv
import time
import argparse
from pathlib import Path
from services.database import Database
from services.progressbar import printProgressBar

# On check si le dossier ou on va deposer le csv a traiter existe sinon onle crée
Path("./input").mkdir(parents=True, exist_ok=True)

# Récuperation des params de la ligne de commande (Nom du fichier, Nom de la table [Optionnel], Separateur [Optionnel])
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Nom du fichier", required=True)
parser.add_argument("-t", "--tablename", help="Nom de la table temporaire", required=False)
parser.add_argument("-s", "--separator", help="Type de seprateur", default=";", required=False)

# Définition des variables globales
SEPARATOR = parser.parse_args().separator
FILENAME = parser.parse_args().filename
FILEPATH = f"./input/{FILENAME}"
TABLENAME = parser.parse_args().tablename if parser.parse_args(
).tablename is not None else os.path.splitext(FILENAME)[0]
HEADER = None
ROW_COUNT = 0
COLUMN_COUNT = 0
ERROR = None

# On recupere le header du csv pour le nommage des colonnes et le nombre de ligne
with open(FILEPATH,  encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    HEADER = next(reader)
    ROW_COUNT = sum(1 for row in reader)
    COLUMN_COUNT = len(HEADER)
f.close()

# Check des erreurs
if os.path.exists(FILEPATH) is False:
    ERROR = f"Le fichier {FILENAME} n'existe pas dans le repertoire ./input/ a la racine de ce projet."
elif HEADER is None or COLUMN_COUNT == 0 or ROW_COUNT == 1 or ROW_COUNT == 0:
    ERROR = "Le fichier contient probablement des erreurs ou est vide"

# Si erreur on la print
# Sinon on lance la création de la table a partir du CSV
if ERROR is not None:
    print(ERROR)
else:
    database = Database()
    cur = database.getCursor()
    table_name = f"tmp_{TABLENAME}_{int(time.time())}"

    q = f"CREATE TABLE {table_name} ("
    q += ', '.join(f"{col} VARCHAR(255)".format(col) for col in HEADER)
    q += ');'

    cur.execute(q)
    database.commit()

    q = f"INSERT INTO {table_name} VALUES ("
    q += ', '.join(('%s ' * COLUMN_COUNT).split())
    q += ');'
    printProgressBar(0, ROW_COUNT, prefix = 'Progress:', suffix = 'Complete', length = 50)
    with open(FILEPATH,  encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        i = 1
        for row in reader:
            cur.execute(q, tuple(row))
            printProgressBar(i, ROW_COUNT, prefix = 'Progress:', suffix = 'Complete', length = 50)
            i += 1

    database.commit()
    f.close()
    database.closeConnection()
