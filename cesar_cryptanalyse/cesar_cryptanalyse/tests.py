"""Tests unitaires des fonctions de César."""
import unittest
from cesar import Cesar_chiffrer, Cesar_dechiffrer
from force_brute import Attaque_force_brute
from frequence import Attaque_frequence


class TestCesar(unittest.TestCase):
    def test_chiffrement(self):
        self.assertEqual(Cesar_chiffrer("BONJOUR", 3), "ERQMRXU")

    def test_dechiffrement(self):
        self.assertEqual(Cesar_dechiffrer("ERQMRXU", 3), "BONJOUR")

    def test_caracteres_non_lettres(self):
        self.assertEqual(Cesar_chiffrer("Salut, 123 !", 3), "Vdoxw, 123 !")

    def test_cle_invalide(self):
        with self.assertRaises(ValueError):
            Cesar_chiffrer("ABC", 26)

    def test_force_brute(self):
        resultats = Attaque_force_brute("ERQMRXU")
        self.assertEqual(len(resultats), 26)
        self.assertEqual(resultats[3], (3, "BONJOUR"))

    def test_frequence_texte_sans_lettres(self):
        self.assertIsNone(Attaque_frequence("123 !?"))

    def test_frequence_texte_avec_lettres(self):
        resultat = Attaque_frequence("BONJOUR")
        self.assertIsNotNone(resultat)
        frequences, total, candidats = resultat
        self.assertEqual(total, 7)
        self.assertEqual(len(candidats), 26)
        self.assertAlmostEqual(sum(frequences.values()), 100.0)


if __name__ == "__main__":
    unittest.main()
