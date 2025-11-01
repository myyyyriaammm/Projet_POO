COULEUR_FOND = "#F9FAFB"
COULEUR_PRIMAIRE = "#4F46E5"
COULEUR_SUCCES = "#10B981"
COULEUR_ERREUR = "#EF4444"
COULEUR_CARD = "#FFFFFF"
COULEUR_TEXTE = "#1F2937"
COULEUR_MUTED = "#6B7280"
COULEUR_SIDEBAR = "#1F2937"
COULEUR_STREAK = "#F59E0B"
POINTS_POUR_PASSER_NIVEAU = 3

QUESTIONS_QUIZ = [
    {"question": "Qu'est-ce qu'une classe en Python ?", "options": ["Un modèle pour créer des objets", "Une fonction spéciale", "Une variable globale"], "reponse": 0, "niveau": 1},
    {"question": "Comment crée-t-on un objet à partir d'une classe 'Personne' ?", "options": ["Personne.new()", "create Personne()", "Personne()"], "reponse": 2, "niveau": 1},
    {"question": "Que signifie 'self' dans une méthode de classe ?", "options": ["Le nom de la classe", "L'instance actuelle de la classe", "Une variable globale"], "reponse": 1, "niveau": 1},
    {"question": "Quelle méthode est appelée automatiquement lors de la création d'un objet ?", "options": ["__start__()", "__create__()", "__init__()"], "reponse": 2, "niveau": 1},
    {"question": "Comment une classe 'Etudiant' hérite de la classe 'Personne' ?", "options": ["class Etudiant extends Personne:", "class Etudiant(Personne):", "class Etudiant inherits Personne:"], "reponse": 1, "niveau": 2},
    {"question": "Que permet l'héritage en POO ?", "options": ["De créer plusieurs objets", "De réutiliser le code d'une classe parent", "D'accélérer le programme"], "reponse": 1, "niveau": 2},
    {"question": "Comment appelle-t-on le constructeur de la classe parent ?", "options": ["parent.__init__()", "super().__init__()", "self.parent.__init__()"], "reponse": 1, "niveau": 2},
    {"question": "Comment définit-on un attribut privé en Python ?", "options": ["private attribut", "__attribut", "_attribut"], "reponse": 1, "niveau": 3},
    {"question": "Qu'est-ce qu'un getter ?", "options": ["Une méthode pour supprimer un attribut", "Une méthode pour obtenir la valeur d'un attribut", "Une méthode pour créer un objet"], "reponse": 1, "niveau": 3}
]
CODE_CHALLENGES = [
    ("Write a class Animal with attribute 'name' and afficher().", "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def afficher(self):\n        print(self.name)"),
    ("Create class Book (title, author), method show().", "class Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n    def show(self):\n        print(f'{self.title} - {self.author}')"),
    ("Code class User with login property and afficher().", "class User:\n    def __init__(self, login):\n        self.login = login\n    def afficher(self):\n        print(self.login)"),
    ("Create class Rectangle (length, width), method surface().", "class Rectangle:\n    def __init__(self, length, width):\n        self.length = length\n        self.width = width\n    def surface(self):\n        return self.length * self.width"),
]
FAQ_DATA = [
    {'question': 'Comment gagner des points ?', 'answer': "Vous gagnez des points (score) en complétant les quiz (+1 par bonne réponse). Les défis de code sont pour la pratique."},
    {'question': 'Comment monter de niveau ?', 'answer': f"Vous montez d'un niveau à chaque fois que vous donnez {POINTS_POUR_PASSER_NIVEAU} bonnes réponses dans un quiz de votre niveau actuel."},
    {'question': "Que se passe-t-il si je rate un quiz ?", 'answer': "Ne vous inquiétez pas ! Vous pouvez repasser le quiz de votre niveau autant de fois que nécessaire pour apprendre."},
    {'question': 'Où écrire mon code pour les défis ?', 'answer': "Allez dans 'Défis de Code', écrivez dans la zone de texte, et utilisez 'Voir Solution' ou 'Reset' pour vous entraîner."}
]
FORMATIONS_DATA = [
    {'nom': 'Fondamentaux Python', 'desc': 'Apprendre les bases de Python (variables, boucles, fonctions).', 'niveau_requis': 1,
     'lessons': ['Variables et Types', 'Structures de Contrôle', 'Fonctions', 'Listes et Dictionnaires']},
    {'nom': 'Maîtrise de la POO', 'desc': 'Devenir un expert des classes, de l\'héritage et du polymorphisme.', 'niveau_requis': 2,
     'lessons': ['Classes et Objets', 'Héritage', 'Polymorphisme', 'Encapsulation']},
    {'nom': 'Python Avancé', 'desc': 'Explorer les décorateurs, générateurs et la métaprogrammation.', 'niveau_requis': 3,
     'lessons': ['Décorateurs', 'Générateurs', 'Context Managers', 'Métaclasses']},
]

