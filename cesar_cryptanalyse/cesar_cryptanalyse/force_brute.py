"""Attaque par force brute du chiffrement de César."""
from cesar import Cesar_dechiffrer


def Attaque_force_brute(texte_chiffre):
    """Retourne les 26 couples (clé, texte déchiffré)."""
    return [
        (cle, Cesar_dechiffrer(texte_chiffre, cle))
        for cle in range(26)
    ]
