# Projet Dankassari

## Article
Lien vers l'article du projet :  
http://blog.univ-angers.fr/polytechangers3asagi/2021/03/14/projet-dankassari/

## Préparation
Installer Python 3.7 ou plus sur votre pc  

Windows/Mac OS X : https://www.python.org/downloads/  

Linux : 
```bash
sudo apt install python3 python3-pip
```

### Installation de la librairie

Python a besoin de la librairie xlrd en version 1.2.0 afin d'ouvrir les fichiers xlsx
```bash
pip install xlrd==1.2.0
```

## Créer la carte
```bash
python Cartographier.py <fichier-activites> <fichier-population> <nom-de-la-carte>
```
Exemple :
```bash
python Cartographier.py Activites.xlsx Population.xlsx "Carte Dankassari"
```

Ceci va créer un fichier "Carte Dankassari.html" exécutable avec un navigateur internet.  

**Yanis Rigaudeau et Alexandre Bocquier**  
**Polytech Angers 2021**
