# Bug/Test Project

Description générale du système ou du projet

Projet qui permet de réserver des places dans des compétitions.Ici plusiseurs bug on était corrigés,
et un feature a été implémenté.Une serie de test a été mis en place avec le module pytest ainsi
qu'un test de performance avec le module locuste.
Six Branche on été crée. Une pour chaque bug et feature.Une branch master réunis le tout.
Pour lancer les tests taper la commande : pytest -vvv(à la racine du projet).
Un module coverage a été installé pour voir le pourcentage de couverture des tests sur le fichier server.py.
Taper la commande :coverage report -m server.py.
Pour lancer le test de performance avec locust taper : locust -f locust.py(à la racine du projet).
Une fois la commande locust tapé rendez vous à l'adresse : localhost:8089 

Statut du projet

Le développement du projet est fini.

Installation

2. créer le virtual env : python -m venv venv (à la racine du projet)
3. switcher sur le virtual env : source venv/bin/activate pour linux ou venv\Scripts\activate pour windows(à la racine du projet)
4. récupérer les modules du fichier requirements.txt sur votre venv : pip install -r requirements.txt(à la racine du projet)

Démarrage

 1. Taper la commande :set FLASK_APP=server.py (à la racine du projet)
 2. lancer le serveur: flask run(à la racine du projet)
Rendez-vous dans votre navigateur web à l'url indiquée par la ligne de commande,  http://127.0.0.1:5000/ 

Fabriqué avec:

Pycharm

Auteurs :

Florent Peyre alias Alucard
