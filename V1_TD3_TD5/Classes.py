


# Correction de G. Poux-Médard, 2021-2022



# =============== 2.1 : La classe Document ===============

class Document:

    # Initialisation des variables de la classe

    def __init__(self, titre="", auteur="", date="", url="", texte="" , typed=""):

        self.titre = titre

        self.auteur = auteur

        self.date = date

        self.url = url

        self.texte = texte

        self.type = typed



# =============== 2.2 : REPRESENTATIONS ===============

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)

    def __repr__(self):

        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"



    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)

    def __str__(self):

        return f"{self.titre}, par {self.auteur}"







# =============== 2.4 : La classe Author ===============

class Author:

    def __init__(self, name):

        self.name = name

        self.ndoc = 0

        self.production = []

# =============== 2.5 : ADD ===============

    def add(self, production):

        self.ndoc += 1

        self.production.append(production)

    def __str__(self):

        return f"Auteur : {self.name}\t# productions : {self.ndoc}"





# In[21]:





class RedditDocument(Document):    

    def __init__(self, titre="", auteur="", date="", url="", texte="", typed="", __nbcom = 0  ):



        super().__init__( titre, auteur, date, url, texte ,typed)

      

    def __str__(self):

        parent = super().__str__()

        return f"{parent}, {self.__nbcom} comments "

    def getnbr(self):

        return self.__nbcom

        

    def setnbr(self, nbcom):

        self.__nbcom = nbcom

    def getType(self):

        return self.type

        

class ArxivDocument(Document):

    def __init__(self, titre="", auteur="", date="", url="", texte="",  typed="", __coauteur = "" ):



        super().__init__( titre, auteur, date, url, texte ,typed)

      

    def __str__(self):

        parent = super().__str__()

        return f"{parent}, {self.__coauteur} coauthors "

    def getnbr(self):

        return self.__coauteur

        

    def setnbr(self, coauteur):

        self.__coauteur = coauteur

    def getType(self):

        return self.type


