import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from constante import *  
from base_de_donnee import BaseDeDonnees

class AppPOOFusion:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("StudyHub")
        self.fenetre.geometry("900x650")
        self.db = BaseDeDonnees()
        self.nom = ""; self.score = 0; self.niveau = 1; self.login_streak = 0
        self.points_du_niveau = 0; self.index_question = 0; self.questions_niveau_actuel = []
        self.container = None; self.frame_contenu = None
        self.label_sidebar_score = None; self.label_sidebar_niveau = None
        self.ecran_accueil()

    def nettoyer_completement(self):
        if self.container: self.container.destroy()
        self.container = tk.Frame(self.fenetre, bg=COULEUR_FOND)
        self.container.pack(fill="both", expand=True)

    def nettoyer_contenu(self):
        if self.frame_contenu:
            for w in self.frame_contenu.winfo_children(): w.destroy()
        else: self.nettoyer_completement()

    def creer_bouton(self, parent, text, command, style='primary'):
        styles = {
            'primary':  {'bg': COULEUR_PRIMAIRE, 'font': ('Arial', 12, 'bold')}, 
            'success':  {'bg': COULEUR_SUCCES,  'font': ('Arial', 11, 'bold')}, 
            'warning':  {'bg': COULEUR_STREAK, 'font': ('Arial', 11, 'bold')},
            'sidebar':  {'bg': COULEUR_SIDEBAR, 'font': ('Arial', 11, 'bold')},
            'sidebar_logout': {'bg': COULEUR_MUTED, 'font': ('Arial', 10)}
        }
        s = styles.get(style, styles['primary'])
        btn = tk.Button(parent, text=text, command=command, bg=s['bg'], fg='white', font=s['font'],padx=15, pady=8, border=0, cursor="hand2")
        if style.startswith('sidebar'): btn.configure(anchor="w", relief="flat")
        return btn
    # ---------------- Accueil / Login ----------------
    def ecran_accueil(self):
        self.nettoyer_completement()
        f = tk.Frame(self.container, bg=COULEUR_CARD, padx=40, pady=30, relief="solid", bd=1); f.pack(expand=True)
        tk.Label(f, text="Bienvenue sur StudyHub", font=("Arial",22,"bold"), bg=COULEUR_CARD, fg=COULEUR_PRIMAIRE).pack(pady=(0,20))
        tk.Label(f, text="Votre prénom :", font=("Arial",12), bg=COULEUR_CARD, fg=COULEUR_TEXTE).pack(anchor="w")
        self.entry_nom = tk.Entry(f, font=("Arial",14), width=30, relief="solid", bd=1, bg="#F9FAFB"); self.entry_nom.pack(pady=(5,15), ipady=8)
        self.entry_nom.focus()  
        self.creer_bouton(f,"🚀 Commencer",self.demarrer_session,'primary').pack(fill="x")
        self.entry_nom.bind("<Return>", lambda e:self.demarrer_session())
    
    def demarrer_session(self):
        self.nom = self.entry_nom.get().strip()
        if not self.nom: messagebox.showwarning("Attention","Entre ton prénom !"); return
        self.score,self.niveau,last_login,self.login_streak=self.db.charger_joueur(self.nom)
        self.points_du_niveau=0
        self.creer_layout_principal()
    
   # ---------------- Layout Principal ----------------
    def creer_layout_principal(self):
        self.nettoyer_completement()
        sidebar = tk.Frame(self.container, bg=COULEUR_SIDEBAR, width=240); sidebar.pack(side="left",fill="y"); sidebar.pack_propagate(False)
        self.frame_contenu = tk.Frame(self.container, bg=COULEUR_FOND, padx=25, pady=20); self.frame_contenu.pack(side="right",fill="both",expand=True)
        tk.Label(sidebar,text="StudyHub",font=("Arial",18,"bold"),bg=COULEUR_SIDEBAR,fg="white").pack(pady=(20,25),padx=20,anchor="w")
        tk.Label(sidebar,text=f"👤 {self.nom}",font=("Arial",12,"bold"),bg=COULEUR_SIDEBAR,fg="white").pack(pady=(0,5),padx=20,anchor="w")
        self.label_sidebar_score=tk.Label(sidebar,text=f"🏆 {self.score} pts",font=("Arial",11),bg=COULEUR_SIDEBAR,fg=COULEUR_SUCCES); self.label_sidebar_score.pack(pady=2,padx=20,anchor="w")
        self.label_sidebar_niveau=tk.Label(sidebar,text=f"📊 Niveau {self.niveau}",font=("Arial",11),bg=COULEUR_SIDEBAR,fg="white"); self.label_sidebar_niveau.pack(pady=2,padx=20,anchor="w")
        tk.Frame(sidebar,height=2,bg=COULEUR_MUTED).pack(fill="x",pady=20,padx=15)
        for t,s in [("Dashboard",self.ecran_dashboard),("Gestion Formation",self.ecran_gestion_formation),("Prendre un Quiz",self.demarrer_quiz),("Défis de Code",self.ecran_defis_code),("❓ Centre d'Aide",self.ecran_aide)]:
            self.creer_bouton(sidebar,t,s,'sidebar').pack(fill="x",padx=15,pady=4)
        self.creer_bouton(sidebar,"🚪 Quitter",self.ecran_accueil,'sidebar_logout').pack(side="bottom",fill="x",padx=15,pady=20)
        self.ecran_dashboard()
    # ---------------- Mise à jour stats ----------------
    def mettre_a_jour_stats(self):
        if self.label_sidebar_score: self.label_sidebar_score.config(text=f"🏆 {self.score} pts")
        if self.label_sidebar_niveau: self.label_sidebar_niveau.config(text=f"📊 Niveau {self.niveau}")
    # ---------------- Dashboard ----------------
    def ecran_dashboard(self):
        self.nettoyer_contenu()
        tk.Label(self.frame_contenu, text=f"Bienvenue, {self.nom} !", font=("Arial",22,"bold"), bg=COULEUR_FOND, fg=COULEUR_TEXTE).pack(anchor="w")
        tk.Label(self.frame_contenu, text="Prêt à relever un nouveau défi aujourd'hui ?", font=("Arial",12), bg=COULEUR_FOND, fg=COULEUR_MUTED).pack(anchor="w", pady=(0,20))
        chart_frame = tk.Frame(self.frame_contenu,bg=COULEUR_CARD,relief="solid",bd=1,padx=20,pady=20); chart_frame.pack(fill="x", pady=10)
        tk.Label(chart_frame,text="📊 Votre Progression",font=("Arial",16,"bold"),bg=COULEUR_CARD,fg=COULEUR_PRIMAIRE).pack(anchor="w")
        canvas = tk.Canvas(chart_frame,width=600,height=200,bg=COULEUR_CARD,highlightthickness=0); canvas.pack(pady=10)
        max_niveau = 3; bar_width = 80; spacing = 120; max_height = 150
        for i in range(1,max_niveau+1):
            x = 50 + (i-1)*spacing
            height = (self.score/(max_niveau*10))*max_height if i<=self.niveau else 20
            color = COULEUR_SUCCES if i<=self.niveau else COULEUR_MUTED
            canvas.create_rectangle(x,180-height,x+bar_width,180,fill=color,outline=""); canvas.create_text(x+bar_width//2,195,text=f"Niveau {i}", font=("Arial",10), fill=COULEUR_TEXTE)
        tk.Label(chart_frame,text=f"Score Total: {self.score} | Niveau Actuel: {self.niveau} | Série: {self.login_streak} jours",
                 font=("Arial",11),bg=COULEUR_CARD,fg=COULEUR_MUTED).pack(pady=5)
        card_quiz = tk.Frame(self.frame_contenu,bg=COULEUR_CARD,relief="solid",bd=1,padx=20,pady=20); card_quiz.pack(fill="x",pady=10)
        tk.Label(card_quiz,text="📝 Prendre un Quiz",font=("Arial",16,"bold"),bg=COULEUR_CARD,fg=COULEUR_PRIMAIRE).pack(anchor="w")
        tk.Label(card_quiz,text=f"Testez vos connaissances et passez au niveau {self.niveau+1} !",font=("Arial",11),bg=COULEUR_CARD,fg=COULEUR_MUTED).pack(anchor="w",pady=5)
        self.creer_bouton(card_quiz,"Commencer le Quiz",self.demarrer_quiz,'primary').pack(anchor="e", pady=10)
    # ---------------- Quiz ----------------
    def demarrer_quiz(self):
        self.questions_niveau_actuel = [q for q in QUESTIONS_QUIZ if q["niveau"]==self.niveau]
        if not self.questions_niveau_actuel:
            messagebox.showinfo("🏆 Victoire Totale !",f"Bravo {self.nom} ! Tu as terminé tous les niveaux !\nScore final: {self.score} points 🎉")
            self.ecran_dashboard(); return
        self.index_question = 0; self.points_du_niveau = 0
        self.nettoyer_contenu(); self.frame_question_quiz = tk.Frame(self.frame_contenu,bg=COULEUR_FOND); self.frame_question_quiz.pack(fill="both",expand=True)
        self.afficher_question()
    def afficher_question(self):
        for w in self.frame_question_quiz.winfo_children(): w.destroy()
        if self.index_question>=len(self.questions_niveau_actuel):
            if self.points_du_niveau>=POINTS_POUR_PASSER_NIVEAU: self.passer_niveau_suivant()
            else:
                messagebox.showinfo("Niveau incomplet",f"Il te manque {POINTS_POUR_PASSER_NIVEAU-self.points_du_niveau} point(s) !"); self.demarrer_quiz()
            return
        q = self.questions_niveau_actuel[self.index_question]
        tk.Label(self.frame_question_quiz,text=f"Progression: {self.points_du_niveau}/{POINTS_POUR_PASSER_NIVEAU} ⭐",
                 font=("Arial",12),bg=COULEUR_FOND,fg=COULEUR_MUTED).pack(anchor="e", pady=5, padx=20)
        frame_q = tk.Frame(self.frame_question_quiz,bg=COULEUR_CARD,relief="solid",bd=1); frame_q.pack(fill="x",expand=True,padx=20,pady=10)
        tk.Label(frame_q,text=f"Question {self.index_question+1}/{len(self.questions_niveau_actuel)} (Niveau {self.niveau})", font=("Arial",10),
                 bg=COULEUR_CARD,fg=COULEUR_MUTED).pack(pady=(15,5))
        tk.Label(frame_q,text=q["question"], font=("Arial",14,"bold"), bg=COULEUR_CARD, fg=COULEUR_TEXTE, wraplength=550).pack(pady=20,padx=20)
        self.var_option=tk.IntVar(value=-1)
        for i,opt in enumerate(q["options"]): ttk.Radiobutton(frame_q,text=opt,variable=self.var_option,value=i,style="Pro.TRadiobutton").pack(anchor="w", padx=30, pady=5)
        self.creer_bouton(self.frame_question_quiz,"Valider",self.verifier_reponse,'primary').pack(pady=20)

    def verifier_reponse(self):
        r=self.var_option.get(); q=self.questions_niveau_actuel[self.index_question]
        if r==-1: messagebox.showwarning("Attention","Sélectionne une réponse !"); return
        if r==q["reponse"]: self.score+=1; self.points_du_niveau+=1; messagebox.showinfo("✅ Correct !","Bonne réponse ! +1 point")
        else: messagebox.showerror("❌ Incorrect",f"La bonne réponse était : {q['options'][q['reponse']]}")
        self.db.sauvegarder_joueur(self.nom,self.score,self.niveau); self.mettre_a_jour_stats()
        self.index_question+=1; self.afficher_question()

    def passer_niveau_suivant(self):
        self.niveau+=1; self.points_du_niveau=0
        self.db.sauvegarder_joueur(self.nom,self.score,self.niveau); self.mettre_a_jour_stats()
        messagebox.showinfo("🎉 Bravo !",f"Niveau {self.niveau} débloqué !"); self.ecran_dashboard()
    def ecran_gestion_formation(self):
        self.nettoyer_contenu()
        tk.Label(self.frame_contenu, text="🎓 Gestion de Formation", font=("Arial",22,"bold"), bg=COULEUR_FOND, fg=COULEUR_TEXTE).pack(anchor="w", pady=(0,20))
        tk.Label(self.frame_contenu, text="Formations Disponibles", font=("Arial",16,"bold"), bg=COULEUR_FOND, fg=COULEUR_PRIMAIRE).pack(anchor="w", pady=(0,10))
        inscrites=[f[0] for f in self.db.get_formations_joueur(self.nom)]
        for f in FORMATIONS_DATA:
            card=tk.Frame(self.frame_contenu,bg=COULEUR_CARD,relief="solid",bd=1,padx=20,pady=15); card.pack(fill="x",pady=5)
            tk.Label(card,text=f['nom'],font=("Arial",14,"bold"),bg=COULEUR_CARD,fg=COULEUR_TEXTE).pack(anchor="w")
            tk.Label(card,text=f['desc'],font=("Arial",11),bg=COULEUR_CARD,fg=COULEUR_MUTED).pack(anchor="w",pady=2)
            if f['nom'] in inscrites: self.creer_bouton(card,"Voir Leçons",lambda ff=f:self.voir_lessons(ff),'success').pack(anchor="e",pady=5)
            elif self.niveau>=f['niveau_requis']: self.creer_bouton(card,"S'inscrire",lambda n=f['nom']: self.inscrire_formation(n),'success').pack(anchor="e",pady=5)
            else: tk.Label(card,text=f"🔒 Niveau {f['niveau_requis']} requis", font=("Arial",11,"bold"),bg=COULEUR_CARD,fg=COULEUR_ERREUR).pack(anchor="e",pady=5)

    def inscrire_formation(self, nom_formation):
        if self.db.inscrire_joueur_formation(self.nom, nom_formation):
            messagebox.showinfo("Inscription Réussie", f"Vous êtes inscrit à {nom_formation}")
        else: messagebox.showwarning("Déjà Inscrit", "Vous êtes déjà inscrit.")
        self.ecran_gestion_formation()

    def voir_lessons(self, formation):
        top=tk.Toplevel(self.fenetre); top.title(f"Leçons - {formation['nom']}"); top.geometry("500x400"); top.configure(bg=COULEUR_FOND)
        tk.Label(top,text=formation['nom'],font=("Arial",16,"bold"),bg=COULEUR_FOND,fg=COULEUR_PRIMAIRE).pack(pady=15)
        canvas=tk.Canvas(top,bg=COULEUR_FOND,highlightthickness=0); sb=ttk.Scrollbar(top,orient="vertical",command=canvas.yview)
        frame=tk.Frame(canvas,bg=COULEUR_FOND); canvas.create_window((0,0),window=frame,anchor="nw"); canvas.configure(yscrollcommand=sb.set)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        colors={'not_started':COULEUR_MUTED,'in_progress':COULEUR_STREAK,'completed':COULEUR_SUCCES}
        labels={'not_started':'⚪ Non Commencé','in_progress':'🟡 En Cours','completed':'✅ Terminé'}
        for l in formation['lessons']:
            s=self.db.get_lesson_status(self.nom,formation['nom'],l)
            c=tk.Frame(frame,bg=COULEUR_CARD,relief="solid",bd=1,padx=15,pady=10); c.pack(fill="x",pady=5,padx=10)
            tk.Label(c,text=l,font=("Arial",12,"bold"),bg=COULEUR_CARD,fg=COULEUR_TEXTE).pack(anchor="w")
            tk.Label(c,text=labels[s],font=("Arial",10),bg=COULEUR_CARD,fg=colors[s]).pack(anchor="w",pady=2)
            bf=tk.Frame(c,bg=COULEUR_CARD); bf.pack(anchor="e")
            if s!='completed':
                tk.Button(bf,text="En Cours",command=lambda ll=l:self.changer_statut(ll,formation['nom'],'in_progress',top),bg=COULEUR_STREAK,fg='white',font=("Arial",9),padx=8,pady=4,border=0).pack(side="left",padx=2)
                tk.Button(bf,text="Terminer",command=lambda ll=l:self.changer_statut(ll,formation['nom'],'completed',top),bg=COULEUR_SUCCES,fg='white',font=("Arial",9),padx=8,pady=4,border=0).pack(side="left",padx=2)
            else:
                tk.Button(bf,text="Reset",command=lambda ll=l:self.changer_statut(ll,formation['nom'],'not_started',top),
                          bg=COULEUR_MUTED,fg='white',font=("Arial",9),padx=8,pady=4,border=0).pack(side="left",padx=2)
        canvas.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")

    def changer_statut(self, lesson, formation, statut, top_window):
        self.db.set_lesson_status(self.nom,formation,lesson,statut); top_window.destroy()
        for f in FORMATIONS_DATA:
            if f['nom']==formation: self.voir_lessons(f); break

    # ---------------- Défis de Code ----------------
    def ecran_defis_code(self):
        self.nettoyer_contenu(); tk.Label(self.frame_contenu,text="💻 Défis de Code",font=("Arial",22,"bold"),bg=COULEUR_FOND,fg=COULEUR_TEXTE).pack(anchor="w",pady=(0,20))
        nb=ttk.Notebook(self.frame_contenu)
        for i,(enonce,sol) in enumerate(CODE_CHALLENGES):
            f=tk.Frame(nb,bg=COULEUR_CARD,padx=20,pady=20); nb.add(f,text=f"Défi {i+1}")
            tk.Label(f,text=enonce,font=("Arial",12),bg=COULEUR_CARD,fg=COULEUR_TEXTE,wraplength=600,justify="left").pack(pady=10,anchor="w")
            txt=scrolledtext.ScrolledText(f,height=10,font=("Courier New",11),relief="solid",bd=1,bg="#F9FAFB"); txt.pack(fill="x",pady=10,padx=10)
            bf=tk.Frame(f,bg=COULEUR_CARD); bf.pack(fill="x",padx=10)
            self.creer_bouton(bf,"Voir Solution",lambda s=sol:self.voir_solution(s),'success').pack(side="left",padx=5)
            self.creer_bouton(bf,"Reset",lambda t=txt:t.delete("1.0",tk.END),'warning').pack(side="left",padx=5)
            self.creer_bouton(bf,"Défi Suivant ➡",lambda n=nb:self.passer_au_defi_suivant(n),'primary').pack(side="right",padx=5)
        nb.pack(expand=True,fill="both")

    def passer_au_defi_suivant(self, notebook):
        next_index = (notebook.index(notebook.select())+1)%len(notebook.tabs()); notebook.select(next_index)

    def voir_solution(self, solution):
        top=tk.Toplevel(self.fenetre); top.title("Solution"); top.geometry("450x300"); top.configure(bg=COULEUR_CARD)
        tk.Label(top,text="💡 Solution de Référence",font=("Arial",14,"bold"),bg=COULEUR_CARD,fg=COULEUR_PRIMAIRE).pack(pady=10)
        txt=scrolledtext.ScrolledText(top,height=10,font=("Courier New",11),relief="solid",bd=1,bg="#F9FAFB"); txt.pack(fill="both",expand=True,padx=10,pady=10); txt.insert("1.0",solution); txt.config(state="disabled")

    # ---------------- Centre d'Aide / FAQ ----------------
    def ecran_aide(self):
        self.nettoyer_contenu(); tk.Label(self.frame_contenu,text="❓ Centre d'Aide (FAQ)",font=("Arial",22,"bold"),bg=COULEUR_FOND,fg=COULEUR_TEXTE).pack(anchor="w",pady=(0,20))
        canvas=tk.Canvas(self.frame_contenu,bg=COULEUR_FOND,highlightthickness=0); sb=ttk.Scrollbar(self.frame_contenu,orient="vertical",command=canvas.yview)
        frame=tk.Frame(canvas,bg=COULEUR_FOND); canvas.create_window((0,0),window=frame,anchor="nw"); canvas.configure(yscrollcommand=sb.set)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        for item in FAQ_DATA:
            f=tk.Frame(frame,bg=COULEUR_CARD,relief="solid",bd=1,padx=15,pady=10); f.pack(fill="x",pady=5)
            tk.Label(f,text=f"Q: {item['question']}",font=("Arial",12,"bold"),bg=COULEUR_CARD,fg=COULEUR_PRIMAIRE,wraplength=550,justify="left").pack(anchor="w")
            tk.Label(f,text=f"A: {item['answer']}",font=("Arial",11),bg=COULEUR_CARD,fg=COULEUR_TEXTE,wraplength=550,justify="left").pack(anchor="w",pady=(3,0))
        canvas.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
if __name__ == "__main__":
    root = tk.Tk()
    root.title("StudyHub")
    root.geometry("900x650")
    root.configure(bg="#F0F2F5")
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TNotebook', background="#F0F2F5", borderwidth=0)
    style.configure('TNotebook.Tab', background="#F0F2F5", foreground="#888", borderwidth=1, padding=[10,5])
    style.map('TNotebook.Tab', background=[('selected', "#FFF")], foreground=[('selected', "#2B6CB0")])
    style.configure('TFrame', background="#F0F2F5")
    style.configure('Pro.TRadiobutton', background="#FFF", foreground="#000", font=('Arial',12), padding=5)
    app = AppPOOFusion(root)
    root.mainloop()    
