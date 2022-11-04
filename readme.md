# Installation

Créer un fichier .env a la racine en se basant sur .env.example et y mettre les infos de la base de donées voulues

Installer les dépendances avec la commande

```
pip3 install -r requirements.txt
```

Liste des paquets qui vont être installés:
- python-dotenv (Library to retrieve variables in the .env)
- mysql-connector-python-rf (Library for the database)


# Utilisation


## Créer un CSV depuis une requête MYSQL

Lancer la ligne de commande :

```
python3 tableToCsv.py -q 'SELECT * from TABLE' -f 'nom_du_fichier.csv'
```

Paramètres:
```
-q, --query        Requête MYSQL - string - Obligatoire - Pas de valeur par défaut - Ex: 'SELECT email, login from users'
-f, --filename     Nom du fichier - string - Optionnel - Valeur par défaut: output.csv - Ex: users.csv
```

## Créer une table depuis un CSV

Placer votre fichier dans le répertoire ./input/ a la racine du projet et lancer la ligne de commande suivante :

```
python3 csvToTable.py -f commande_fantome.csv
```

Paramètres:
```
-f, --filename     Nom du fichier - string - Obligatoire - Pas de valeur défaut - Ex: commande_fantome.csv
-t, --tablename    Nom de la table a créer - string - Optionnel - Valeur défaut: Nom du fichier (sans l'extension) - Ex: commande_fantome
-s, --separator    Séparateur du fichier CSV - string - Optionnel - Valeur défaut: ; - Ex: ,
```

Infos supplémentaires :

La table créer sera préfixé par tmp_ et se terminera par _{timestamp}, ce qui donnera pour l'exemple ci-dessus: tmp_commande_fantome_1667475241