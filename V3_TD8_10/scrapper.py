# Code créée par la AlexisCorp



# Importation des differents modules

from Classes import RedditDocument
from Classes import ArxivDocument
from Classes import Document
from Classes import Author

from Corpus import Corpus

import pandas as pd
import numpy as np
import re
from collections import Counter       
import praw
import urllib, urllib.request, collections
import xmltodict
import datetime



# ===============  REDDIT ===============

# Fonction affichage hierarchie dict

def showDictStruct(d):

    def recursivePrint(d, i):

        for k in d:

            if isinstance(d[k], dict):

                print("-"*i, k)

                recursivePrint(d[k], i+2)

            else:

                print("-"*i, k, ":", d[k])

    recursivePrint(d, 1)

reddit = []



# Identification pour Reddit

reddit = praw.Reddit(client_id='MR0jyTs3U8XGLnbemELxuQ', client_secret='CRzHJbtQBHowRV4m_n7oldHGsu6YHg', user_agent='monapp')

# Requete

limit = 1000 # Limite de documents

hot_posts = reddit.subreddit('basketball').hot(limit=limit)   #.top("all", limit=limit)#

# Recuperation du texte

docs = []

docs_bruts = []

afficher_cles = False

for i, post in enumerate(hot_posts):

    if i%10==0: print("Reddit:", i, "/", limit)

    if afficher_cles:  # Pour connaitre les différentes variables et leur contenu

        for k, v in post.__dict__.items():

            pass

            print(k, ":", v)

    if post.selftext != "":  # Posts sans texte
        docs.append(" ".join(post.selftext.split("\n")))

        docs_bruts.append(("Reddit", post))
        pass

    

#print(docs)


# ===============  ArXiv ===============
    

# Parametres
    
query_terms = [ "science"]

max_results = 150       # Limitation des documents

# Requete

url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'

data = urllib.request.urlopen(url)

# Format dict (OrderedDict)

data = xmltodict.parse(data.read().decode('utf-8'))

#showDictStruct(data)

# Ajout resumes à la liste

for i, entry in enumerate(data["feed"]["entry"]):

    if i%10==0: print("ArXiv:", i, "/", limit)

    docs.append(" ".join(entry["summary"].split("\n")))

    docs_bruts.append(("ArXiv", entry))

    #showDictStruct(entry)



# =============== Exploitation ===============
    
print(f"# docs avec doublons : {len(docs)}")    

docs = list(set(docs))          # Evite les doublons

print(f"# docs sans doublons : {len(docs)}")


for i, doc in enumerate(docs):

    print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")

    if len(doc)<100:

        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)


# =============== CLASSE DOCUMENT ===============


# =============== MANIPS ===============

collection = []

for nature, doc in docs_bruts:

    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.

        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne

        try:

            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule

        except:

            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste

        summary = " ".join(doc["summary"].split("\n")) # On enlève les retours à la ligne

        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime
        
        if len(authors)>1:

            coa = authors[1:]

        else:

            coa = None
            
        doc_classe = ArxivDocument(titre, authors, date, doc["id"], summary , "Arxiv")  # Création du Document

        doc_classe.setnbr(coa)

        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":

        #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))

        titre = doc.title.replace("\n", '')

        auteur = str(doc.author)

        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")

        url = "https://www.reddit.com/"+doc.permalink

        texte = " ".join(doc.selftext.split("\n"))

        nbcom = doc.num_comments
        
        doc_classe = RedditDocument(titre, auteur, date, url, texte, "")

        doc_classe.setnbr(nbcom)

        collection.append(doc_classe)

# Création de l'index de document
        
id2doc = {}
for i, doc in enumerate(collection):

    id2doc[i] = doc.titre

# =============== CLASSE AUTEURS ===============

authors = {}

aut2id = {}

num_auteurs_vus = 0

# Création de la liste+index des Auteurs

for doc in collection:

    if doc.auteur not in aut2id:

        num_auteurs_vus += 1

        authors[num_auteurs_vus] = Author(doc.auteur)

        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)


# ===============  CORPUS ===============

corpus2 = Corpus("tested")

# Construction du corpus à partir des documents

for doc in collection:

    corpus2.add(doc)

corpus2.construire_vocabulaire()

corpus2.stats()

corpus2.matrix()

print("Vous pouvez commencer")

#print(corpus2)



#   Code créée par la AlexisCorp pour le AlexisCorp Search