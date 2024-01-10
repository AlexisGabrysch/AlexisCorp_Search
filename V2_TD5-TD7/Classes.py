# Code créée par la AlexisCorp


# =============== La classe Document ===============

class Document:

    # ==== Initialisation des variables de la classe ====

    def __init__(self, titre="", auteur="", date="", url="", texte="" , typed=""):

        self.titre = titre      # Titre

        self.auteur = auteur    # Auteur

        self.date = date        # Date

        self.url = url          # Url          

        self.texte = texte      # Texte

        self.type = typed       # type

# ===============  REPRESENTATIONS ===============

    # ==== Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe) ====

    def __repr__(self):

        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # ==== Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe) ====

    def __str__(self):

        return f"{self.titre}, par {self.auteur}"

# =============== La classe Author ===============

class Author:

    # ==== Initialisation des variables de la classe ====
    
    def __init__(self, name):

        self.name = name        # Nom

        self.ndoc = 0           # Nombre de documents

        self.production = []    # Production

# ==== Fonction ADD ajout ====

    def add(self, production):

        self.ndoc += 1

        self.production.append(production)

    # ==== Affichage ====

    def __str__(self):

        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

# =============== La classe RedditDocument fille de Document ===============
    
class RedditDocument(Document):   

    # ==== Initialisation des variables de la classe ==== 

    def __init__(self, titre="", auteur="", date="", url="", texte="", typed="", __nbcom = 0  ):

        super().__init__( titre, auteur, date, url, texte ,typed)
   
    # ==== Affichage ====
        
    def __str__(self):

        parent = super().__str__()

        return f"{parent}, {self.__nbcom} comments "
    
    # ==== Fonction GET du nombre de commentaires ====

    def getnbr(self):

        return self.__nbcom
      
    # ==== Fonction SET du nombre de commentaires ====

    def setnbr(self, nbcom):

        self.__nbcom = nbcom

    # ==== Fonction GET du type ====
        
    def getType(self):

        return self.type

        
# =============== La classe ArxivDocument fille de Document ===============
        
class ArxivDocument(Document):

    # ==== Initialisation des variables de la classe ====

    def __init__(self, titre="", auteur="", date="", url="", texte="",  typed="", __coauteur = "" ):

        super().__init__( titre, auteur, date, url, texte ,typed)    

    # ==== Affichage ====
        
    def __str__(self):

        parent = super().__str__()

        return f"{parent}, {self.__coauteur} coauthors "
    
    # ==== Fonction GET du nombre de commentaires ====

    def getnbr(self):

        return self.__coauteur

    # ==== Fonction SET du nombre de commentaires ====

    def setnbr(self, coauteur):

        self.__coauteur = coauteur

    # ==== Fonction GET du type ====

    def getType(self):

        return self.type






#   Code créée par la AlexisCorp pour le AlexisCorp Search

