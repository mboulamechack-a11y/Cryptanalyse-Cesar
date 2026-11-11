"""Fonctions de chiffrement et de déchiffrement de César."""


def Cesar_chiffrer(texte, cle):
    """Chiffre les lettres ASCII avec une clé comprise entre 0 et 25."""
    if not isinstance(cle, int) or not 0 <= cle <= 25:
        raise ValueError("La clé doit être un entier compris entre 0 et 25.")

    resultat = []
    for caractere in texte:
        if caractere.isascii() and caractere.isalpha():
            base = ord("A") if caractere.isupper() else ord("a")
            position = ord(caractere) - base
            resultat.append(chr(base + (position + cle) % 26))
        else:
            resultat.append(caractere)
    return "".join(resultat)


def Cesar_dechiffrer(texte, cle):
    """Déchiffre un texte avec une clé comprise entre 0 et 25."""
    if not isinstance(cle, int) or not 0 <= cle <= 25:
        raise ValueError("La clé doit être un entier compris entre 0 et 25.")
    return Cesar_chiffrer(texte, (26 - cle) % 26)
