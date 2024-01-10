# Code créée par la AlexisCorp


# Importation des differents modules

import unittest

from Classes import Document, Author

from Corpus import Corpus



# ======== ZONE DE TEST ========


# ======= Test sur la classe Document ========


class TestDocument(unittest.TestCase):      

    def test_init(self):            # Test de la fonction init

        # Teste l'initialisation du document

        document = Document("Titre", "Auteur", "Date", "URL", "Texte")      # Ajout de valeur test

        self.assertEqual(document.titre, "Titre")

        self.assertEqual(document.auteur, "Auteur")

        self.assertEqual(document.date, "Date")

        self.assertEqual(document.url, "URL")

        self.assertEqual(document.texte, "Texte")

    def test_repr(self):        # Test de la fonction repr

        # Teste la représentation du document

        document = Document("Titre", "Auteur", "Date", "URL", "Texte")

        self.assertEqual(repr(document), "Titre : Titre\tAuteur : Auteur\tDate : Date\tURL : URL\tTexte : Texte\t")

    def test_str(self):          # Test de la fonction str

        # Teste la représentation du document

        document = Document("Titre", "Auteur", "Date", "URL", "Texte")

        self.assertEqual(str(document), "Titre, par Auteur")



# ========== Test sur la classe Author ==========
        

class TestAuthor(unittest.TestCase):        

    def test_init(self):                # Test de la fonction init

        # Teste l'initialisation de l'auteur

        author = Author("Auteur")

        self.assertEqual(author.name, "Auteur")     # Ajout de valeur test

        self.assertEqual(author.ndoc, 0)

        self.assertEqual(author.production, [])


    def test_add(self):

        # Teste l'ajout d'un document

        author = Author("Auteur")           # Ajout de valeur test

        document = Document("Titre", "Auteur", "Date", "URL", "Texte")

        author.add(document)

        self.assertEqual(author.ndoc, 1)

        self.assertEqual(author.production, [document])

    def test_str(self):

        # Teste la représentation

        author = Author("Auteur")

        self.assertEqual(str(author), "Auteur : Auteur\t# productions : 0")
        

# ========== Test sur la classe Corpus ==========
        
class CorpusTest(unittest.TestCase):

    def setUp(self):

        self.corpus = Corpus("Mon corpus")

    def test_init(self):                # Test de la fonction init

        self.assertEqual(self.corpus.nom, "Mon corpus")         # Ajout de valeur test

        self.assertEqual(self.corpus.authors, {})

        self.assertEqual(self.corpus.aut2id, {})

        self.assertEqual(self.corpus.id2doc, {})

        self.assertEqual(self.corpus.ndoc, 0)

        self.assertEqual(self.corpus.naut, 0)

        self.assertEqual(self.corpus.all_documents_text, "")

        self.assertEqual(self.corpus.vocabulary, set())



if __name__ == "__main__":       # Mise en fonction

    unittest.main()





# Code créée par la AlexisCorp