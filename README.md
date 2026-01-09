# clock
Horloge de Mamie
# Projet Horloge Python

## Description
Ce projet consiste à créer une horloge en Python qui affiche l’heure au format hh:mm:ss et qui s’actualise chaque seconde.
Une alarme peut être réglée par l’utilisateur et se déclenche lorsque l’heure courante correspond à l’heure programmée.

Le projet utilise des tuples pour représenter l’heure et respecte les consignes données dans le cadre du module Data/IA.

## Fonctionnalités

- Affichage de l’heure au format hh:mm:ss
- Actualisation automatique chaque seconde
- Réglage d’une alarme
- Déclenchement de l’alarme lorsque l’heure correspond
- Mode d’affichage 24h ou 12h (AM/PM) *(bonus)*
- Pause et reprise de l’horloge *(bonus)*
- Arrêt propre du programme sans interruption brutale

## Choix techniques

- L’heure est représentée par un tuple `(heures, minutes, secondes)`
- Les tuples étant immuables, un nouveau tuple est recréé à chaque seconde
- L’alarme est également stockée sous forme de tuple
- Une boucle `while True` permet le fonctionnement continu de l’horloge
- Le module `time` est utilisé pour gérer le temps réel
- Le module `select` permet de lire des commandes utilisateur sans bloquer l’exécution

## Utilisation


