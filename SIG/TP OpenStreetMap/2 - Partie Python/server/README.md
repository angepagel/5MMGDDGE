# Serveur WMS en Python

> Ce projet fonctionne avec **Python 3**.

 ## Installation des dépendances

Ce programme Python utilise un ensemble de bibliothèques listées dans le fichier `requirements.txt`. Il est possible de télécharger ces dépendances avec le gestionnaire de paquet `pip` :

```shell
python -m pip install -r requirements.txt
```

## Démarrage du serveur

### Classique

Démarrer le serveur WMS avec la commande :

```shell
python WMSserver.py
```

### Docker

Construire l'image avec la commande :

```shell
docker build -t wmsserver .
```

Lancer le conteneur avec la commande :

```shell
docker run --rm -it wmsserver
```

