#!/usr/bin/python3

#pour installer xlrd 1.2.0 : pip install xlrd==1.2.0
import xlrd
import os
import sys
import re
import colorsys

#Constantes en rapport avec le fond de carte
largeur_de_la_carte = 25000
hauteur_de_la_carte = 19675
latitude_max_niger = 23.55
latitude_min_niger = 11.745
longitude_max_niger = 15.983
longitude_min_niger = 0.15

#Fichiers nécessaires afin de générer la carte
dependances = ["fondCarte.txt", "script.js", "style.css"]

villages = {}
categories = []


#Fonctions permettant de créer cercles, rectangle, texte etc...

def CreerRectangle(id, x, y, w, h, classe, onclick=''):
    if( onclick == ''):
        string = '<rect id="%s"\n x="%s"\n y="%s"\n width="%s"\n height="%s"\n class="%s"></rect>\n' % (id, str(x), str(y), str(w), str(h), classe)
    else:
        string = '<rect id="%s"\n x="%s"\n y="%s"\n width="%s"\n height="%s"\n class="%s" onclick="%s"></rect>\n' % (id, str(x), str(y), str(w), str(h), classe, onclick)
    return string

def CreerTexte(id, x, y, texte, classe, onclick=''):
    if(onclick == '' and id == ''):
        string = '<text xml:space="preserve"><tspan x="%s" y="%s" class="%s">%s</tspan></text>\n' % (str(x), str(y), classe, texte)
    elif(onclick == '' and id != ''):
        string = '<text id="%s" xml:space="preserve"><tspan x="%s" y="%s" class="%s">%s</tspan></text>\n' % (id, str(x), str(y), classe, texte)
    elif(onclick != '' and id == ''):
        string = '<text class="%s" onclick="%s" xml:space="preserve"><tspan x="%s" y="%s" class="%s">%s</tspan></text>\n' % (classe, onclick, str(x), str(y), classe, texte)
    else:
        string = '<text id="%s" class="%s" onclick="%s" xml:space="preserve"><tspan x="%s" y="%s" class="%s">%s</tspan></text>\n' % (id, classe, onclick, str(x), str(y), classe, texte)
    return string

def CreerPanneauxInformation():
    global f
    
    espacement = 22
    
    OuvrirGroupeSvg('rectG', 1)
    for v in villages:
        Width = round(len(villages[v].nom)*1.5)
        for i in range(len(villages[v].categories)):
            if( len(villages[v].categories[i].nom) + len(villages[v].categories[i].commentaire) > Width ):
                Width = len(villages[v].categories[i].nom) + len(villages[v].categories[i].commentaire)
        
        y = (latitude_max_niger - float(villages[v].l)) / ((latitude_max_niger - latitude_min_niger) / hauteur_de_la_carte)
        x = (float(villages[v].L) - longitude_min_niger) / ((longitude_max_niger - longitude_min_niger) / largeur_de_la_carte)
        
        # l'id est choisi afin de permettre d'obtenir le rectangle en cliquant sur le point en utilisant la fonction display de script.txt
        
        OuvrirGroupeSvg(str(v) + 'R', 0)
    
        facteurEspacement = 12
        #grand rectangle
        rectFond = CreerRectangle(str(v) + "rect", x + 10, y - espacement, max(Width*facteurEspacement + espacement, 245) - 10, 50+espacement*len(villages[v].categories)+espacement, "rectFond", 'premierPlan(this.parentNode)')
        f.write(rectFond)
        
        #ce qui est clickable pour fermer le panneau d'information + son texte
        rectClick = CreerRectangle(str(v) + "c", max(x + (Width*facteurEspacement), x+225), y - 15, 16, 16, "xRect", "display(this.id)") 
        f.write(rectClick)
            
        textClick = CreerTexte(str(v) + "X", max(x +11+ Width*facteurEspacement-10, x+225), y, "X", "xTexte", "display(this.id)")
        f.write(textClick)

        #les informations du panneau selon disponibilité depuis le tableur
        textNom = CreerTexte("", x + 15, y, '<tspan class="nomVillageInfo">' + villages[v].nom + '</tspan>', "txtRect")
        f.write(textNom)
                    
        textPop = CreerTexte("", x + 15, y + espacement, '<tspan class="avantValeur">Population : </tspan>' + str(villages[v].population), "txtRect")
        f.write(textPop)
        
        for i in range(len(villages[v].categories)):
            text = CreerTexte("", x + 15, y + espacement*(i+2), '<tspan class="avantValeur">' + villages[v].categories[i].nom + ' : </tspan>' + villages[v].categories[i].commentaire, "txtRect")
            f.write(text)
            
        FermerGroupeSvg()
    FermerGroupeSvg()
        
    return()
        
def CreerBouton(classe, id, onClick, couleur, texte):
    global f
    f.write('<button class ="%s" id="%s" onClick="%s" style="background-color: %s">%s</button>\n' %
            (classe, id, onClick, couleur, texte))

def OuvrirGroupeSvg(id, afficher):
    global f
    f.write('<g id="%s" style="display: %s">\n' % 
            (id, 'none' if afficher == 0 else 'block'))

def FermerGroupeSvg():
    global f
    f.write('</g>\n')

def CreerPointVillage(nom, latitude, longitude, population, maxpop, fillColor, strokeColor):
    global f
    # pour le coordonnees voici le calcul y=(latitude_max_niger - latitude)/((latitude_max_niger-latitude_min_niger)/hauteur de la carte)
    y = (latitude_max_niger - float(latitude)) / ((latitude_max_niger - latitude_min_niger) / hauteur_de_la_carte)
    # x=(longitude-longitude_min)/((longitude_max_niger-longitude_min_niger)/largeur de de la carte)
    x = (float(longitude) - longitude_min_niger) / ((longitude_max_niger - longitude_min_niger) / largeur_de_la_carte)
    r = 5+10*float(population)/maxpop
    f.write('<circle onclick="display(this.parentNode.id)"\n cx="%5.3f" \n cy="%5.3f"\n r="%f"\n id="%sV"\n fill="%s"\n stroke-width="0.5"\n stroke="%s"\n fill-opacity="0.7"\n style="cursor: pointer">\n</circle>\n' %
            (x, y, r, nom, fillColor, strokeColor))

def CreerTexteVillage(nom, texte, latitude, longitude, afficher):
    global f
    y = (latitude_max_niger - float(latitude)) / ((latitude_max_niger - latitude_min_niger) / hauteur_de_la_carte)
    x = (float(longitude - longitude_min_niger) / ((longitude_max_niger - longitude_min_niger) / largeur_de_la_carte))
    display = 'none' if afficher == 0 else 'block'
    displayClass = '' if afficher == 0 else 'persistant'
    f.write('<text onclick="display(this.parentNode.id)" id="%sT" class="nomVillageCarte %s" style="display: %s">\n <tspan x="%5.3f" y="%5.3f">%s</tspan>\n</text>\n' %
            (nom, displayClass, display, x, y, texte))


#Classes comprenant les fichiers excel en entrée, les villages et les travaux

class Fichier:
    def __init__(self, lien, stringPop):
        self.feuille = xlrd.open_workbook(lien).sheet_names()[0]
        self.f = xlrd.open_workbook(lien).sheet_by_name(self.feuille)
        
        self.village = -1
        self.longitude = -1
        self.latitude = -1
        self.pop = -1
        self.categorie = -1
        
        [self.village, self.categorie] = self.ChercherPaterneXLS(self.f, 'Villages')
        [self.pop, self.longitude, self.latitude] = self.CherchePaterneListe(self.f.row_values(self.categorie), stringPop, 'L', 'l')
    
    
    def ChercherPaterneXLS(self, fichier, paterne, mode=1): #attention à l'ordre des variables en sortie
        if( mode == 1 ):
            for rownum in range(fichier.nrows):
                col = self.CherchePaterneListe(fichier.row_values(rownum), paterne)
                if( col != -1 ):
                    return [col, rownum]
            return [1, 0] #car la case "Villages" du fichier 2 n'existe pas
        
        elif( mode == 2 ):
            for colnum in range(fichier.ncols):
                row = self.CherchePaterneListe(fichier.col_values(colnum), paterne)
                if( row != -1 ):
                    return [colnum, row]
            return [-1, -1]
            
        else:
            print("incorrect mode value")
    
    
    
    def CherchePaterneListe(self, liste, *args): #attention à l'ordre des variables en sortie
        lengthArgs = len(args)
        out = []
        
        if( lengthArgs <= 0 ):
            print(" cherchePaterneListe() error number of arg in args")
            return -2
            
        for i in range(len(liste)):
            if( lengthArgs > 1 ):
                for j in args:
                    if( liste[i] == j ):
                        out.append(i)
            else:
                if( liste[i] == args[0] ):
                    return i
            
        if( len(out) == lengthArgs ):
            return out
        elif( lengthArgs > 1 ):
            return [-1]*lengthArgs
    
        return -1
    
    def __str__(self):
        return ("village : " + str(self.village) + ", L : " + str(self.latitude) + ", l : " + str(self.longitude) + ", pop : " + str(self.pop) + ", categorie : " + str(self.categorie))

class Categorie:
    def __init__(self, nom, commentaire=''):
        self.nom = nom
        self.commentaire = commentaire

class Village:
    def __init__(self, nom, population, nbHommes, nbFemmes, longitude, latitude, nbMenages, nbAgric):
        self.nom = nom
        self.population = population
        self.hommes = nbHommes
        self.femmes = nbFemmes
        self.L = longitude
        self.l = latitude
        self.menages = nbMenages
        self.agric = nbAgric
        self.categories = []

    def AjouterCategorie(self, categorie):
        if isinstance(categorie, Categorie):
            self.categories.append(categorie)
        else:
            return None


#Fonction principale

def Cartographier(lien1, lien2, Name="carte"):
    global f, villages, categories

    global fichier1, fichier2
    fichier1 = Fichier(lien1, "Pop")
    fichier2 = Fichier(lien2, "pop. totale")

    print("fichier 1 :", lien1)
    print("fichier 2 :", lien2)

    #print(fichier1)
    #print(fichier2)

    #On récupère ici la population maximum dans un village afin de définir une taille maximum pour les cercles
    maxpop = 0
    for rownum in range(1, fichier2.f.nrows):
        if not isinstance(fichier2.f.row_values(rownum)[fichier2.pop], str):
            if maxpop < float(fichier2.f.row_values(rownum)[fichier2.pop]) and float(fichier2.f.row_values(rownum)[fichier2.pop]) < 50000:
                maxpop = fichier2.f.row_values(rownum)[fichier2.pop]

    #On commence le fichier html avec le head et le css
    f = open('tmp.txt', "w", encoding='utf8')
    f.write('<!DOCTYPE html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <title>%s</title>\n' % Name)
    
    fStyle = open("style.css", 'r', encoding='utf8')
    f.write('<style>\n%s</style>\n' % fStyle.read())
    fStyle.close()
    f.write("</head>\n<body>\n")
    
    #On lit dans le fichier 1 la liste de tous les travaux
    for colnum in range(fichier1.latitude+1, fichier1.f.ncols):
        if fichier1.f.col_values(colnum)[fichier1.categorie] != '' and fichier1.f.col_values(colnum)[fichier1.categorie] != ' ':
            categories.append(fichier1.f.col_values(colnum)[fichier1.categorie])
        else:
            categories.append(fichier1.f.col_values(colnum)[fichier1.categorie-1])

    #Création des boutons d'affichages
    CreerBouton("bouton active", "PV", "afficher_villages(this)", "brown", "Villages")
    CreerBouton("bouton active", "PT", "afficher_villages(this)", "brown", "Travaux")

    #On lit la liste des catégories à masquer
    banListe = []
    ligne = fichier1.categorie - 2
    for i in range(fichier1.latitude+1, fichier1.f.ncols):
        if int(fichier1.f.row_values(ligne)[i]) == 0:
            banListe.append(0)
        else:
            banListe.append(1)
    #print(banListe)
    
    #On crée les boutons catégories en leur assignant une couleur
    for i in range(len(categories)):
        if( banListe[i] == 0 ):
            value = int(i/2) if i%2==0 else int(value+len(categories)/2)
            [r, g, b] = tuple(round(j * 255) for j in colorsys.hsv_to_rgb(value / len(categories), 1, 1))
            couleur = '#%02x%02x%02x' % (r, g, b)
            CreerBouton("bouton categories", categories[i], "reply_click(this)", couleur, categories[i])
            #print(couleur, categories[i])

    #Boutons zoom
    CreerBouton("zoomer", "zoom_in", "btnzoom(1)", "brown", "+")
    CreerBouton("zoomer", "zoom_out", "btnzoom(-1)", "brown", "-")    
    
    #L'échelle de distance
    f.write('<div style="position: fixed;right: 1px;bottom: 1px;"><svg fill="#d2aa6d" stroke="#ffffff" height="50px" width="110px"><line x1="1" y1="15" x2="1" y2="35" class="echelleLine"></line><line x1="0" y1="25" x2="100" y2="25" class="echelleLine"></line><line x1="100" y1="15" x2="100" y2="35" class="echelleLine"></line></svg><span id="echelle" valeurBase="10" x="45" y="20" style="position:fixed;right:45px;">10 km</span></div>')
    
    
    #Ajout des points cardinaux
    f.write('<div id="ptCardinaux"><svg fill="#d2aa6d" stroke="#ffffff" height="60px" width="30px"><polygon id="Nord" points="15,0 30,30 0,30"></polygon><text id="NordTexte" xml:space="preserve"><tspan x="10" y="25">N</tspan></text><polygon id="Sud" points="15,60 30,30 0,30"></polygon></svg></div>')

    #On ajoute le fond de carte
    fondCarte = open("fondCarte.txt", 'r', encoding='utf8')
    f.write('<svg id="carte" fill="#d2aa6d" stroke="#ffffff" height="100%" width="100%">\n<g id="zoom" transform="matrix(0.745058 0 0 0.745058 -4321.54 -11822.9)">\n')
    f.write(fondCarte.read())
    fondCarte.close()
    
    #Lecture de la liste des villages
    for rownum in range(fichier2.f.nrows):
        if fichier2.f.row_values(rownum)[0] != '':
            if fichier2.f.row_values(rownum)[fichier2.longitude] != '?' and fichier2.f.row_values(rownum)[fichier2.longitude] != '' and fichier2.f.row_values(rownum)[fichier2.longitude] != ' ':
                #dictionnaire de villages, chaque village est identifié par son id convertit en int
                villages[int(fichier2.f.row_values(rownum)[0])] = Village(fichier2.f.row_values(rownum)[fichier2.village],
                                                                          int(fichier2.f.row_values(rownum)[fichier2.pop]),
                                                                          int(fichier2.f.row_values(rownum)[fichier2.pop+1]),
                                                                          int(fichier2.f.row_values(rownum)[fichier2.pop+2]),
                                                                          fichier2.f.row_values(rownum)[fichier2.longitude],
                                                                          fichier2.f.row_values(rownum)[fichier2.latitude],
                                                                          int(fichier2.f.row_values(rownum)[fichier2.pop+8]),
                                                                          int(fichier2.f.row_values(rownum)[fichier2.pop+9]))
                #print(int(fichier2.f.row_values(rownum)[0]))

    #Ajouts des catégories pour chaque village
    for rownum in range(fichier1.categorie + 1, fichier1.f.nrows):
        if fichier1.f.row_values(rownum)[fichier1.latitude] != '?' and fichier1.f.row_values(rownum)[fichier1.latitude] != '' and fichier1.f.row_values(rownum)[fichier1.longitude] != ' ':
            for colnum in range(fichier1.latitude+1, fichier1.f.ncols):
                if fichier1.f.row_values(rownum)[colnum] != '':
                    comm = fichier1.f.row_values(rownum)[colnum]
                    if not isinstance(comm, str):   #astuce permettant de convertir l'année en int
                        comm = str(int(comm))
                    if fichier1.f.row_values(fichier1.categorie)[colnum] != '':
                        nouvelleCategorie = Categorie(fichier1.f.row_values(fichier1.categorie)[colnum], comm)
                    else:
                        nouvelleCategorie = Categorie(fichier1.f.row_values(fichier1.categorie-1)[colnum], comm)
                    villages[int(fichier1.f.row_values(rownum)[0])].AjouterCategorie(nouvelleCategorie)

    #On crée les cercles correspondant aux villages
    OuvrirGroupeSvg("PVG", 1)
    for v in villages:
        OuvrirGroupeSvg(str(v) + 'G', 1)
        if len(villages[v].categories) > 0:
            CreerPointVillage(villages[v].nom,
                              villages[v].l,
                              villages[v].L,
                              villages[v].population,
                              maxpop,
                              "black",
                              "white")
        else:
            CreerPointVillage(villages[v].nom,
                              villages[v].l,
                              villages[v].L,
                              villages[v].population,
                              maxpop,
                              "white",
                              "black")
        #Si la population est supérieur à 1000 le nom du village sera affiché de manière permanente
        if villages[v].population > 1000:
            CreerTexteVillage(str(v),
                              villages[v].nom,
                              villages[v].l,
                              villages[v].L,
                              1)
        else:
            CreerTexteVillage(str(v),
                              villages[v].nom,
                              villages[v].l,
                              villages[v].L,
                              0)
        FermerGroupeSvg()
    FermerGroupeSvg()

    CreerPanneauxInformation()
    
    f.write('</g>\n</svg>\n')
    
    #Construction d'un tableau de villages pour l'affichage dans le js
    tableauVillage = '{'
    for v in villages:
        tableauVillage += '"%d":0,' % v
    tableauVillage = tableauVillage[:-1]    #Suppression de la virgule en trop
    tableauVillage += '}'

    #Construction d'un tableau de correspondances catégories/villages pour le js
    tableauCatVillage = '{'
    for c1 in categories:
        nbVillages = 0
        tableauCatVillage += '\n"%s":[' % c1
        for v in villages:
            for c2 in villages[v].categories:
                if c1 == c2.nom:
                    nbVillages += 1
                    tableauCatVillage += '"%d",' % v
        if nbVillages > 0:
            tableauCatVillage = tableauCatVillage[:-1]
        tableauCatVillage += '],'
    tableauCatVillage = tableauCatVillage[:-1]
    tableauCatVillage += '}'
    
    #Construction d'un tableau répertoriant le nombre de travaux par village pour le js
    tableauNbrTravauxVillage = '{'
    for v in villages:
        tableauNbrTravauxVillage += '"%d":%d,' % (v, len(villages[v].categories))
    tableauNbrTravauxVillage = tableauNbrTravauxVillage[:-1]
    tableauNbrTravauxVillage += '}'
        
    fScript = open("script.js", 'r', encoding='utf8')
    texte = fScript.read()
    fScript.close()
    
    texte = texte.replace('% tableauNbrTravauxVillage %', tableauNbrTravauxVillage)
    texte = texte.replace('% tableauVillage %', tableauVillage)
    texte = texte.replace('% tableauCatVillage %', tableauCatVillage)

    f.write('<script>\n%s</script>\n' % texte)

    f.write('\n</body>\n</html>\n')
    f.close()
    
    print()
    if os.path.exists(Name + '.html'):
        print('Mise à jour carte existante')
        os.remove(Name + '.html')
        os.rename(r"tmp.txt", Name + '.html')
    else:
        print('Création nouvelle carte')
        os.rename(r"tmp.txt", Name + '.html')
        
    print('Nom de la carte : %s.html' % Name)

#Début du programme

if __name__ == '__main__':
    for fichier in dependances:
        if not os.path.exists(fichier):
            print('Le fichier "%s" est manquant' % fichier)
            exit()

    if len(sys.argv) < 3:
        path = re.split(r'\\|/', sys.argv[0])
        fileName = path[len(path)-1]
        print('Utilisation : %s fichier1 fichier2 ' %fileName)
        print('         Ou : %s fichier1 fichier2 "Nom de la carte"' % fileName)
        print()
        print('    Exemple : %s Activites.xlsx Population.xlsx "Carte Dankassari"' % fileName)
    elif os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2]):
        if len(sys.argv) < 4:
            Cartographier(sys.argv[1], sys.argv[2])
        else:
            Cartographier(sys.argv[1], sys.argv[2], sys.argv[3])
