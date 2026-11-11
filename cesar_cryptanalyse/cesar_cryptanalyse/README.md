# César Cryptanalysis Tool

Application pédagogique en Python utilisant Tkinter pour explorer le chiffrement de César et deux méthodes de cryptanalyse.

## Fonctionnalités

- Chiffrement et déchiffrement de César (clés de 0 à 25).
- Attaque par force brute : affichage des 26 clés possibles.
- Analyse fréquentielle : occurrences, pourcentages, graphique et classement statistique des clés candidates.
- Tests automatisés avec `unittest`.

## Prérequis

Python 3. Sous Kali Linux, si Tkinter n'est pas disponible :

```bash
sudo apt update
sudo apt install python3-tk
```

Sous Windows, installe Python depuis le site officiel en veillant à inclure Tcl/Tk.

## Lancer l'application

Dans le dossier du projet :

```bash
python3 main.py
```

Sous Windows, la commande peut être :

```bash
python main.py
```

## Exécuter les tests

```bash
python3 -m unittest -v
```

## Principe du chiffrement de César

Pour une lettre représentée par une position `P` entre 0 et 25, le chiffrement utilise :

`C = (P + K) % 26`

Le déchiffrement applique le décalage inverse.

## Limites

La force brute produit les 26 possibilités, mais ne décide pas automatiquement laquelle est correcte. L'analyse fréquentielle classe des clés en comparant les fréquences obtenues à une distribution approximative du français. Les résultats sont moins fiables pour les textes courts ou inhabituels.

Les accents sont conservés dans le texte original lors du chiffrement/déchiffrement, mais normalisés pour les statistiques fréquentielles.
