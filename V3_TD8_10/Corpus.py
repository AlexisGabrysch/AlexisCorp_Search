# Code créée par la AlexisCorp


# Importation des differents modules

import re
import pandas as pd
from Classes import Author
import string
from collections import Counter
import numpy as np

# Importation des differentes Classes
from Classes import ArxivDocument
from Classes import RedditDocument



# Defnitions de patrons

def singleton(cls):

    instance = [None]

    def wrapper(*args, **kwargs):

        if instance[0] is None:

            instance[0] = cls(*args,**kwargs)

        return instance[0]

    return wrapper
      

class generatorofparticules:

    @staticmethod

    def factory(type, nom):         # Polymorphisme de classe

        if type == "Arxiv": return ArxivDocument(nom)       # Renvoie vers la classe ArxivDocument 

        if type == "Reddit": return RedditDocument(nom)     # Renvoie vers la classe RedditDocument

        assert 0, "Error 404" + type


# ===============  CLASSE CORPUS ===============

@singleton #Patron de conception

class Corpus:

    def __init__(self, nom):

        self.nom = nom      # Nom

        self.authors = {}   # Auteurs

        self.aut2id = {}    # Id d'auteur

        self.id2doc = {}    # Id du document

        self.ndoc = 0       # Nombre de documents

        self.naut = 0       # Nombre d'auteur

        self.all_documents_text = ""        # Regroupement de tout les textes

        self.vocabulary = set()     # Vocabulaire du corpus sous set

        self.frequency_table = pd.DataFrame()       # Tableau de frequence fonction Stats

        self.vocab = {}     # Vocabulaire du corpus sous dico

        self.nbr_words = 0      # Nombre de mots differents du corpus

        self.mat_TF = pd.DataFrame()        # Matrice term_frequency

        self.mat_TFi = pd.DataFrame()       # Matrice term_frequency par term total doc

        self.idf = pd.DataFrame()       # Matrice IDF

        self.mat_TFxIDF = pd.DataFrame()        # Matrice TFxIDF

        self.sim_indices = []       # Liste des indices de similiraté 


# ============ Fonction ADD d'ajout des documents ============
        
    def add(self, doc):         

        if doc.auteur not in self.aut2id:

            self.naut += 1

            self.authors[self.naut] = Author(doc.auteur)

            self.aut2id[doc.auteur] = self.naut

        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.all_documents_text += doc.texte + " "

        self.ndoc += 1

        self.id2doc[self.ndoc] = doc



# ===============  REPRESENTATION ===============

    def show(self, n_docs=-1, tri="abc"):

        docs = list(self.id2doc.values())

        if tri == "abc":  # Tri alphabétique

            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]

        elif tri == "123":  # Tri temporel

            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))


    def __repr__(self):

        docs = list(self.id2doc.values())

        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))


# ===============  SPECIFICITE ===============
    

# ============ Fonction SEARCH pour trouver les mots dans leur contexte ============

    def search(self, keyword):

        # Utilise les expressions regulieres pour trouver les passages des mots

        matches = re.finditer(keyword, self.all_documents_text, flags=re.IGNORECASE)

        # Collecter les passages

        passages = []

        context_window = 15  # Ajuster la fenetre de contexte

        for match in matches:

            start_index = max(0, match.start() - context_window)

            end_index = min(len(self.all_documents_text), match.end() + context_window)

            passage = self.all_documents_text[start_index:end_index]

            passages.append(passage)

        return passages


# ============ Fonction CONCORDE pour trouver les mots dans leur contexte predefini ============
    
    def concorde(self, expression, context_size):

        # Utilise les expressions regulieres pour trouver les passages des mots

        matches = re.finditer(expression, self.all_documents_text, flags=re.IGNORECASE)

        # Collecter les passages
        concordances = []

        for match in matches:

            start_index = max(0, match.start() - context_size)

            end_index = min(len(self.all_documents_text), match.end() + context_size)

            conc_left = self.all_documents_text[start_index:match.start()]

            conc_right = self.all_documents_text[match.end():end_index]

            concordance = {

                'contexte_gauche': conc_left,

                'motif_trouvé': match.group(),

                'contexte_droit': conc_right
            }

            concordances.append(concordance)

        # Convertir en DataFrame
            
        concordances_df = pd.DataFrame(concordances)

        return concordances_df
    

# ============ Fonction NETTOYER_TEXTE pour nettoyer le texte en parametre ============
    
    def nettoyer_texte(self, texte):
  

        cleaned_text = texte.lower()  # Convertir en minuscule

        cleaned_text = re.sub(r'\n', ' ', cleaned_text)     # Remplace les nouvelles lignes par des espaces

        cleaned_text = re.sub(r'\d+', ' ', cleaned_text)    # Remplace les chiffres par des espaces

        cleaned_text = re.sub(r'[^\w\s]', ' ', cleaned_text)# Remplace les ponctuations par des espaces

        cleaned_text = re.sub("_", ' ', cleaned_text)       # Remplace les underscore par des espaces

        cleaned_text = re.sub(r'\d+', ' ', cleaned_text)    # Remplace les chiffres par des espaces

        cleaned_text = " ".join(cleaned_text.split())       # Enleve les espaces en trop

        return cleaned_text
    
# ============ Fonction CONSTRUIRE_VOCABULAIRE pour la creation du vocabulaire du corpus ============
    
    def construire_vocabulaire(self):

        for id, doc in self.id2doc.items():

            cleaned_text = self.nettoyer_texte(doc.texte)       # Appel de la fonction nettoyer_texte

            words = re.split(r'[\s,;.:!?\-"\']+', cleaned_text)     # Tokenization

            self.vocabulary.update(filter(lambda x: x != '', words))    # supprimer les espaces vides


# ============ Fonction STATS pour la frequence des termes et plus ============ 

    def stats(self , n=10):
        
        term_frequency_counter = Counter()      # Initialise le compteur de la frequence des termes dans les documents

        document_frequency_counter = Counter()  # Initialise le compteur de la frequence des documents comprenant le mot 


        for doc_id, doc in self.id2doc.items():      # Boucle sur les documents 

            cleaned_text = self.nettoyer_texte(doc.texte)        # Appel de la fonction nettoyer_texte

            words = re.split(r'[\s,;.:!?\-"\']+', cleaned_text)     # Tokenization
            
            term_frequency_counter.update(words)    # Mise a jour du compteur

            document_frequency_counter.update(set(words))   # Mise a jour du compteur

        # Mise a jour du DataFrame des frequences

        self.frequency_table['word'] = list(self.vocabulary)    # Ajout des mots du vocabulaire
        
        self.frequency_table['term_frequency'] = [term_frequency_counter[word] for word in self.vocabulary]     # Ajout de la frequence terme

        self.frequency_table['document_frequency'] = [document_frequency_counter[word] for word in self.vocabulary]     # Ajout de la frequence documents
        
        self.frequency_table.sort_values(by= "word", ascending=True)
        
        self.frequency_table = self.frequency_table.sort_values("term_frequency",ascending= False ) # Trie le tableau decroissant par frequence 

        self.frequency_table['id'] = [id for id in range(len(self.vocabulary))] # Ajout d'un ID unique

        self.vocab = self.frequency_table.set_index("word").T.to_dict()     # Vocabulaire sous forme de dictionnaire

        self.nbr_words = len(self.vocab)    # Mise a jour du nombre de mots

        return self.frequency_table.head(n) ,  print(f"Il y a {self.nbr_words} mots differents dans le corpus.")


# ============ Fonction MATRIX pour la creation des matrices ============ 
    
    def matrix(self):
              
        ll = {}     # Initialisation de variables

        length = []

        data=[]


        for doc_id, doc in self.id2doc.items():         # Boucle sur les documents

            cleaned_text = self.nettoyer_texte(doc.texte)       # Appel de la fonction nettoyer_texte

            words = re.split(r'[\s,;.:!?\-"\']+', cleaned_text)     # Tokenization

            ll[doc_id] = Counter(filter(lambda x: x != '', words))  # Dico des compteurs

            a = [ x for x in words if x != '']      # Passage par variable en supprimant les espaces vides

            length.append(len(a))           # Ajout des longeurs de mots de chaque document

        self.mat_TF = pd.DataFrame(ll).T.replace(np.nan, 0).sort_index(axis=1)      # Matrice Term_Frequency

        self.mat_TFi =  pd.DataFrame(ll).T.replace(np.nan, 0).sort_index(axis=1)    # Matrice Term_Frequency en proportion


        for i, m in enumerate(length):

            if m!= 0:                                                           # On ne peut diviser par 0 

                self.mat_TFi.iloc[i,:] = self.mat_TFi.iloc[i,:]/m               # Remplissage de la matrice Term_Frequency en proportion

        a = self.frequency_table[["word", "document_frequency"]].copy()         # Copie du DataFrame pour garder les longueurs et index

        a["idf"] = np.log(self.ndoc/a["document_frequency"])                    # Ajout du calcul de IDF

        self.idf = a.sort_values("word").set_index("word")                      # Ajout de IDF
        
    
        for i in range(len(self.idf)):

            data.append(self.idf["idf"][self.mat_TFi.columns[i]]*self.mat_TFi[self.mat_TFi.columns[i]])     # Remplissage des valeurs
        
        self.mat_TFxIDF =  pd.DataFrame(data).T              # Matrice TFxIDF
        


# ============ Fonction RECHERCHE_PAR_SIMILARITE_COSINUS pour la recherche de documents  ============ 

    def recherche_par_similarite_cosinus(self,mots_cles="", n=10 , type_envoie="web"):

        df = pd.DataFrame()     # Initialisation des variables

        similarites = []

        a = []

        if type_envoie == "alexiscorp_admin":       # test pour Dash ou Jupyter

            mots_cles = input("Entrez quelques mots-clés séparés par des espaces : ")   # Mise en variable des mots utilisateurs

        cleaned_text = self.nettoyer_texte(mots_cles)       # Appel de la fonction nettoyer_texte
        
        cleaned_text = re.split(r'[\s,;.:!?\-"\']+', cleaned_text)      # Tokenization      
        print(cleaned_text)
        term = Counter(mots_cles)       # Mise a jour du compteur

        df['word'] = list(self.vocab.keys())    # Mise a jour du DataFrame par les mots du vocabulaire

        df['term_frequency'] = [term[word] for word in self.vocab.keys()]   # Mise a jour du DataFrame par les frequences des mots utilisateurs

        vecteur_mots_cles = np.asarray(df['term_frequency'])    # Conversion en array pour calcul


        for doc_id  in range(self.ndoc):  

            vecteur_document = self.mat_TFxIDF.iloc[doc_id, :]

            if not np.allclose(np.linalg.norm(vecteur_mots_cles), 0) and not np.allclose(np.linalg.norm(vecteur_document), 0):      # On ne peut diviser par 0 
                    
                    similarites.append([doc_id, np.dot(vecteur_mots_cles, vecteur_document) / (np.linalg.norm(vecteur_mots_cles) * np.linalg.norm(vecteur_document))])      # Calcul 

            else:
                
                similarites.append([doc_id,0])      # Cas pour 0  

        indices = sorted(similarites, key=lambda x: x[1], reverse=True)     # Trie des resultats par similarité decroissante 

        self.sim_indices = indices
        
        for rank, doc_index in enumerate(indices[:n]):      # Affichage des N premiers resultats
            print(rank)
            print(doc_index[1])
            print(doc_index[0])
            if doc_index[1]>0:          # Index doit etre positif

                a.append(f"{rank +1}. {self.id2doc[doc_index[0]].titre} (similarity = {(100*doc_index[1]):.2f}%) URL = {self.id2doc[doc_index[0]].url}")
        
        return a







#   Code créée par la AlexisCorp pour le AlexisCorp Search