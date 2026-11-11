"""Analyse fréquentielle et classement de clés candidates."""
import string
import unicodedata
from collections import Counter
from cesar import Cesar_dechiffrer

ALPHABET = string.ascii_uppercase

# Fréquences approximatives en français, en pourcentage.
FREQUENCES_FR = {
    "A": 7.6, "B": 0.9, "C": 3.3, "D": 3.7, "E": 14.7,
    "F": 1.1, "G": 1.0, "H": 0.7, "I": 7.5, "J": 0.6,
    "K": 0.1, "L": 5.5, "M": 3.0, "N": 7.1, "O": 5.8,
    "P": 3.0, "Q": 1.4, "R": 6.6, "S": 7.9, "T": 7.2,
    "U": 6.3, "V": 1.6, "W": 0.1, "X": 0.4, "Y": 0.3,
    "Z": 0.1,
}


def normaliser_texte(texte):
    """Retire les accents pour les statistiques, sans modifier l'original."""
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte.upper()


def Attaque_frequence(texte_chiffre):
    """
    Retourne (fréquences, nombre_de_lettres, candidats).
    Chaque candidat est un tuple (score_chi2, clé, texte_déchiffré).
    Le meilleur score statistique est placé en premier.
    """
    texte = normaliser_texte(texte_chiffre)
    lettres = [c for c in texte if c in ALPHABET]
    total = len(lettres)
    if total == 0:
        return None

    compteur = Counter(lettres)
    frequences = {
        lettre: compteur.get(lettre, 0) / total * 100
        for lettre in ALPHABET
    }

    candidats = []
    for cle in range(26):
        dechiffre = Cesar_dechiffrer(texte, cle)
        compteur_dechiffre = Counter(c for c in dechiffre if c in ALPHABET)
        score = 0.0
        for lettre in ALPHABET:
            observe = compteur_dechiffre.get(lettre, 0)
            attendu = FREQUENCES_FR[lettre] / 100 * total
            if attendu > 0:
                score += (observe - attendu) ** 2 / attendu
        candidats.append((score, cle, dechiffre))

    candidats.sort(key=lambda item: item[0])
    return frequences, total, candidats
