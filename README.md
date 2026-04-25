# Si-N07-_Ahmed-Zemouche_Mahmoudi-Abderrahmane_DSS

Projet DSS L3 : gestion des trajets ferroviaires a partir du fichier XML `transport.xml`.

## Contenu du projet

- `transport.xml` : fichier XML fourni pour le projet.
- `trains.xsl` : transformation XSLT pour afficher les trajets sous forme HTML.
- `app.py` : application web Flask.
- `index.html` : page HTML de l'application Flask.
- `style.css` : style de l'application.
- `requirements.txt` : dependance Python necessaire.

## Installation

Installer les dependances avec :

```bash
pip install -r requirements.txt
```

## Execution

Lancer l'application avec :

```bash
python app.py
```

Ouvrir ensuite dans le navigateur :

```text
http://127.0.0.1:5000
```

## Partie XSLT

Pour voir la transformation XSLT, ouvrir :

```text
http://127.0.0.1:5000/transport.xml
```

Le fichier `transport.xml` utilise `trains.xsl` pour afficher les trajets dans une page HTML.

## Fonctionnalites

- Recherche d'un trajet par code.
- Filtrage par ville de depart.
- Filtrage par ville d'arrivee.
- Filtrage par type de train.
- Filtrage par prix maximum.
- Statistiques par ligne et par type de train.
