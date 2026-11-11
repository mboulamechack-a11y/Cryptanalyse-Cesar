"""Interface graphique Tkinter de l'outil César."""
import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import string

from cesar import Cesar_chiffrer, Cesar_dechiffrer
from force_brute import Attaque_force_brute
from frequence import Attaque_frequence, normaliser_texte, ALPHABET


class CesarApp:
    def __init__(self, root):
        self.root = root
        root.title("César Cryptanalysis Tool")
        root.geometry("1000x720")
        root.minsize(780, 560)

        style = ttk.Style()
        style.configure("TButton", padding=6)

        ttk.Label(
            root, text="CESAR CRYPTANALYSIS TOOL",
            font=("Arial", 18, "bold")
        ).pack(pady=(12, 2))
        ttk.Label(
            root, text="Chiffrement classique et cryptanalyse pédagogique"
        ).pack(pady=(0, 10))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=8)

        self._creer_onglet_chiffrement()
        self._creer_onglet_force_brute()
        self._creer_onglet_frequence()

    def _creer_onglet_chiffrement(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Chiffrer / Déchiffrer")
        ttk.Label(tab, text="Texte à traiter :").pack(anchor="w")
        self.entree_texte = tk.Text(tab, height=7, wrap="word")
        self.entree_texte.pack(fill="x", pady=5)

        ligne = ttk.Frame(tab)
        ligne.pack(fill="x", pady=8)
        ttk.Label(ligne, text="Clé (0 à 25) :").pack(side="left")
        self.entree_cle = ttk.Entry(ligne, width=10)
        self.entree_cle.insert(0, "3")
        self.entree_cle.pack(side="left", padx=8)

        ttk.Button(ligne, text="Chiffrer", command=self.chiffrer).pack(side="left", padx=4)
        ttk.Button(ligne, text="Déchiffrer", command=self.dechiffrer).pack(side="left", padx=4)
        ttk.Button(ligne, text="Effacer", command=self.effacer_chiffrement).pack(side="left", padx=4)

        ttk.Label(tab, text="Résultat :").pack(anchor="w")
        self.sortie_texte = tk.Text(tab, height=7, wrap="word")
        self.sortie_texte.pack(fill="x", pady=5)
        ttk.Button(tab, text="Copier le résultat", command=self.copier_resultat).pack(anchor="e", pady=5)
        ttk.Label(
            tab, text="Les espaces, chiffres et caractères spéciaux sont conservés."
        ).pack(anchor="w", pady=8)

    def _obtenir_cle(self):
        try:
            cle = int(self.entree_cle.get())
            if not 0 <= cle <= 25:
                raise ValueError
            return cle
        except ValueError:
            messagebox.showerror("Clé invalide", "Entre un entier compris entre 0 et 25.")
            return None

    def chiffrer(self):
        cle = self._obtenir_cle()
        if cle is not None:
            texte = self.entree_texte.get("1.0", "end-1c")
            self._afficher_resultat(Cesar_chiffrer(texte, cle))

    def dechiffrer(self):
        cle = self._obtenir_cle()
        if cle is not None:
            texte = self.entree_texte.get("1.0", "end-1c")
            self._afficher_resultat(Cesar_dechiffrer(texte, cle))

    def _afficher_resultat(self, texte):
        self.sortie_texte.delete("1.0", "end")
        self.sortie_texte.insert("1.0", texte)

    def effacer_chiffrement(self):
        self.entree_texte.delete("1.0", "end")
        self.sortie_texte.delete("1.0", "end")

    def copier_resultat(self):
        resultat = self.sortie_texte.get("1.0", "end-1c")
        if not resultat:
            messagebox.showinfo("Information", "Aucun résultat à copier.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(resultat)
        self.root.update()
        messagebox.showinfo("Copie", "Résultat copié dans le presse-papiers.")

    def _creer_onglet_force_brute(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Force brute")
        ttk.Label(tab, text="Texte chiffré :").pack(anchor="w")
        self.entree_brute = tk.Text(tab, height=5, wrap="word")
        self.entree_brute.pack(fill="x", pady=5)
        ttk.Button(tab, text="Tester les 26 clés", command=self.lancer_force_brute).pack(anchor="w", pady=5)

        colonnes = ("cle", "texte")
        cadre = ttk.Frame(tab)
        cadre.pack(fill="both", expand=True, pady=5)
        self.table_brute = ttk.Treeview(cadre, columns=colonnes, show="headings", height=14)
        self.table_brute.heading("cle", text="Clé testée")
        self.table_brute.heading("texte", text="Texte obtenu")
        self.table_brute.column("cle", width=100, anchor="center")
        self.table_brute.column("texte", width=650)
        scroll = ttk.Scrollbar(cadre, orient="vertical", command=self.table_brute.yview)
        self.table_brute.configure(yscrollcommand=scroll.set)
        self.table_brute.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.table_brute.bind("<Double-1>", self.selectionner_resultat)

    def lancer_force_brute(self):
        texte = self.entree_brute.get("1.0", "end-1c")
        if not texte:
            messagebox.showwarning("Texte manquant", "Entre un texte chiffré.")
            return
        for item in self.table_brute.get_children():
            self.table_brute.delete(item)
        for cle, resultat in Attaque_force_brute(texte):
            self.table_brute.insert("", "end", values=(cle, resultat))

    def selectionner_resultat(self, event=None):
        selection = self.table_brute.selection()
        if not selection:
            return
        cle, texte = self.table_brute.item(selection[0], "values")
        self.entree_cle.delete(0, "end")
        self.entree_cle.insert(0, cle)
        self.entree_texte.delete("1.0", "end")
        self.entree_texte.insert("1.0", texte)
        self._afficher_resultat(texte)
        self.notebook.select(0)

    def _creer_onglet_frequence(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="Analyse fréquentielle")
        ttk.Label(tab, text="Texte chiffré :").pack(anchor="w")
        self.entree_frequence = tk.Text(tab, height=4, wrap="word")
        self.entree_frequence.pack(fill="x", pady=5)
        ttk.Button(tab, text="Analyser les fréquences", command=self.lancer_frequence).pack(anchor="w", pady=5)

        contenu = ttk.Frame(tab)
        contenu.pack(fill="both", expand=True, pady=5)
        gauche = ttk.Frame(contenu)
        gauche.pack(side="left", fill="both", expand=True)
        ttk.Label(gauche, text="Fréquences observées (%)").pack(anchor="w")
        self.graphique = tk.Canvas(gauche, height=250, background="white")
        self.graphique.pack(fill="both", expand=True, pady=5)

        droite = ttk.Frame(contenu)
        droite.pack(side="left", fill="both", expand=True, padx=10)
        ttk.Label(droite, text="Classement des lettres").pack(anchor="w")
        self.table_freq = ttk.Treeview(
            droite, columns=("lettre", "occurrences", "frequence"),
            show="headings", height=10
        )
        for col, titre, largeur in (
            ("lettre", "Lettre", 55),
            ("occurrences", "Nombre", 75),
            ("frequence", "Fréquence %", 100),
        ):
            self.table_freq.heading(col, text=titre)
            self.table_freq.column(col, width=largeur, anchor="center")
        self.table_freq.pack(fill="both", expand=True)

        ttk.Label(tab, text="Cinq clés candidates (score statistique)").pack(anchor="w", pady=(8, 2))
        self.sortie_candidats = tk.Text(tab, height=6, wrap="word")
        self.sortie_candidats.pack(fill="x")

    def lancer_frequence(self):
        texte = self.entree_frequence.get("1.0", "end-1c")
        analyse = Attaque_frequence(texte)
        if analyse is None:
            messagebox.showwarning("Analyse impossible", "Le texte doit contenir au moins une lettre.")
            return
        frequences, total, candidats = analyse
        for item in self.table_freq.get_children():
            self.table_freq.delete(item)

        normalise = normaliser_texte(texte)
        compteur = Counter(c for c in normalise if c in ALPHABET)
        for lettre in sorted(ALPHABET, key=lambda c: frequences[c], reverse=True):
            self.table_freq.insert(
                "", "end",
                values=(lettre, compteur.get(lettre, 0), f"{frequences[lettre]:.2f}")
            )

        self.graphique.delete("all")
        largeur = max(self.graphique.winfo_width(), 350)
        hauteur = max(self.graphique.winfo_height(), 220)
        marge = 25
        zone_largeur = largeur - 2 * marge
        zone_hauteur = hauteur - 2 * marge
        maximum = max(frequences.values()) or 1
        largeur_barre = zone_largeur / 26
        self.graphique.create_line(marge, hauteur - marge, largeur - marge, hauteur - marge)

        for i, lettre in enumerate(ALPHABET):
            valeur = frequences[lettre]
            h_barre = valeur / maximum * (zone_hauteur - 20)
            x1 = marge + i * largeur_barre + 1
            x2 = marge + (i + 1) * largeur_barre - 1
            y1 = hauteur - marge - h_barre
            y2 = hauteur - marge
            self.graphique.create_rectangle(x1, y1, x2, y2, fill="#3976b9", outline="")
            self.graphique.create_text((x1 + x2) / 2, hauteur - marge + 9, text=lettre, font=("Arial", 7))

        self.sortie_candidats.delete("1.0", "end")
        for score, cle, resultat in candidats[:5]:
            self.sortie_candidats.insert(
                "end", f"Clé {cle:2d} | Score : {score:.2f}\nTexte : {resultat[:120]}\n\n"
            )
        self.sortie_candidats.insert(
            "end",
            f"Nombre de lettres analysées : {total}\n"
            "Attention : ce classement est statistique. Les textes courts peuvent donner des résultats peu fiables."
        )


def main():
    root = tk.Tk()
    CesarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
