import sqlite3
from datetime import date
class BaseDeDonnees:
    def __init__(self):
        self.connexion = sqlite3.connect("fusion_poo_pro.db")
        self.creer_table()
    
    def creer_table(self):
        cursor = self.connexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS joueurs (nom TEXT PRIMARY KEY, score INTEGER DEFAULT 0, niveau INTEGER DEFAULT 1)''')
        #cursor.execute('''CREATE TABLE IF NOT EXISTS joueurs (nom TEXT PRIMARY KEY, score INTEGER DEFAULT 0, niveau INTEGER DEFAULT 1, last_login_date TEXT, login_streak INTEGER DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS inscriptions_formations (id INTEGER PRIMARY KEY AUTOINCREMENT, nom_joueur TEXT, nom_formation TEXT, date_inscription TEXT, UNIQUE(nom_joueur, nom_formation))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS progres_lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, nom_joueur TEXT, nom_formation TEXT, lesson TEXT, statut TEXT DEFAULT 'not_started', UNIQUE(nom_joueur, nom_formation, lesson))''')
        self.connexion.commit()
    
    def charger_joueur(self, nom):
        cursor = self.connexion.cursor()
        #cursor.execute('SELECT score, niveau, login_streak FROM joueurs WHERE nom = ?', (nom,))
        cursor.execute('SELECT score, niveau, last_login_date, login_streak FROM joueurs WHERE nom = ?', (nom,))
        resultat = cursor.fetchone()
        if resultat:
            return resultat[0], resultat[1], resultat[2],resultat[3]
        else:
            cursor.execute('INSERT INTO joueurs (nom) VALUES (?)', (nom,))
            self.connexion.commit()
            return 0, 1, None,0
    
    def sauvegarder_joueur(self, nom, score, niveau):
        cursor = self.connexion.cursor()
        cursor.execute('UPDATE joueurs SET score = ?, niveau = ? WHERE nom = ?', (score, niveau, nom))
        self.connexion.commit()
    
    def mettre_a_jour_login(self, nom, new_streak):
        today_iso = date.today().isoformat()
        cursor = self.connexion.cursor()
        cursor.execute('UPDATE joueurs SET last_login_date = ?, login_streak = ? WHERE nom = ?', (today_iso, new_streak, nom))
        self.connexion.commit()

    def inscrire_joueur_formation(self, nom_joueur, nom_formation):
        cursor = self.connexion.cursor()
        today_iso = date.today().isoformat()
        cursor.execute('INSERT INTO inscriptions_formations (nom_joueur, nom_formation, date_inscription) VALUES (?, ?, ?)', (nom_joueur, nom_formation, today_iso))
        self.connexion.commit()
        return True

    def get_formations_joueur(self, nom_joueur):
        cursor = self.connexion.cursor()
        cursor.execute('SELECT nom_formation FROM inscriptions_formations WHERE nom_joueur = ?', (nom_joueur,))
        return cursor.fetchall()

    def set_lesson_status(self, nom_joueur, nom_formation, lesson, statut):
        cursor = self.connexion.cursor()
        cursor.execute('INSERT OR REPLACE INTO progres_lessons (nom_joueur, nom_formation, lesson, statut) VALUES (?, ?, ?, ?)', (nom_joueur, nom_formation, lesson, statut))
        self.connexion.commit()

    def get_lesson_status(self, nom_joueur, nom_formation, lesson):
        cursor = self.connexion.cursor()
        cursor.execute('SELECT statut FROM progres_lessons WHERE nom_joueur = ? AND nom_formation = ? AND lesson = ?', (nom_joueur, nom_formation, lesson))
        result = cursor.fetchone()
        return result[0] if result else 'not_started'

    def get_stats_formation(self, nom_joueur, nom_formation):
        cursor = self.connexion.cursor()
        cursor.execute('SELECT statut, COUNT(*) FROM progres_lessons WHERE nom_joueur = ? AND nom_formation = ? GROUP BY statut', (nom_joueur, nom_formation))
        return cursor.fetchall()
    