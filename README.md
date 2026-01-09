# Horloge de Mamie Jeannine

## Présentation du projet

Lors d'un dimanche calme, vous rendez visite à votre grand-mère, **Mamie Jeannine**.  
Comme à son habitude, elle vous accueille chaleureusement et vous prépare de nombreux petits plats faits avec amour.

Malheureusement, son horloge préférée est cassée : son vilain chat l'a fait tomber.  
Afin de la remercier et de mettre en pratique vos **compétences récemment acquises en Python**, vous décidez de créer une **horloge numérique fonctionnelle**.

## Objectif du projet

Ce projet a pour but de :
- Afficher l'heure au format **HH:MM:SS**
- Mettre à jour l'heure **automatiquement** toutes les secondes
- Initialiser l'horloge avec **l'heure locale de la machine**
- Permettre à l'utilisateur de régler l'heure manuellement
- Ajouter une fonctionnalité d'alarme
- Accepter les commandes utilisateur pendant que l'horloge fonctionne
- Mettre en œuvre une exécution concurrente simple avec **threading**

## Fonctionnalités

### Affichage de l'heure
- Affichage au format **HH:MM:SS**
- Actualisation toutes les secondes
- Heure de départ synchronisée avec l'horloge de la machine

### Réglage manuel de l'heure

L'utilisateur peut modifier l'heure à tout moment pendant l'exécution du programme.  
**Commande :**  
`h HH MM SS` (exemple : `h 16 30 00`)

### Réglage d'une alarme

L'utilisateur peut ajouter une alarme à tout moment pendant l'exécution du programme.  
Lorsque l'heure actuelle correspond à l'heure de l'alarme, un message est affiché.  

**Commande :**  
`a HH MM SS` (exemple : `a 06 45 00`)

### Arrêt du programme

L'utilisateur peut arrêter le programme à tout moment pendant son exécution.  
**Commande :**  
`CTRL + C` ou `stop`

## Choix techniques

- Utilisation du module **time** pour la gestion du temps
- Utilisation du module **threading** pour l'exécution concurrente
- Un thread dédié à l'affichage de l'heure
- Un thread dédié à la saisie des commandes utilisateur
- État du programme stocké dans une structure partagée (**state**)
- Synchronisation des accès grâce à **threading.Lock**

## Installation et exécution

### Prérequis
Python 3 installé sur la machine.

### Lancer le programme

Dans un terminal, se placer dans le dossier du projet puis exécuter :  
`python clock.py`

## Fonctionnalités bonus

Les fonctionnalités suivantes font partie des bonus de l'énoncé du projet :
- Mode d'affichage **12h / 24h** (AM / PM)
- Mise en pause et reprise de l'horloge
- Mise en place d'une interface graphique

## Conclusion

Ce projet permet de mettre en pratique :
- La manipulation du temps en Python
- L'utilisation de fonctions
- La gestion des entrées utilisateur en temps réel
- Les bases du multithreading et de la synchronisation
