# CoachForLife
Version 1.0



## Description du Projet

Ce projet a été réalisé lors de la formation Tech IA chez Simplon HDF. L'objectif faire un site  en utilisant Django.


### Contexte du projet


Un coach en développement personnel souhaite un système de prise de rendez-vous automatique en ligne. Aidez-le à l'aide de vos connaissances sur python et Django.

​

Le client souhaite les fonctionnalités suivantes :


   *  une page d'accueil qui présente son travail
   *  un système d'authentification afin que lui et ses utilisateurs puissent se connecter au site.
   *  un système de prise de rdv.
   *  un historique des séances précédentes avec chaque client avec la possibilité pour le coach de conserver des notes sur chacune des séances

​

Pour la prise de rendez-vous :


   * le coach ne peut être dans deux rendez-vous en même temps
   * il faut au moins 10mins entre deux rdv
   * les rdv ne peuvent être pris que de 9h à 12h30 et de 13h30 à 17h
   * lors de la prise de rdv, le client peut entrer dans un formulaire l'objet de la séance




## Organisation du dossier

Le dossier contient une fonctionallité principale nommé "user_appointment", dans ce dossier on retrouve plusieurs fichier et dossier : 
- Dossier "static" : Où se trouve tout les fichiers CSS et les images utilisés pour les besoin du site;
- Dossier "templates" : Où se trouves toutes les pages HTML;
- Fichier "forms.py" : Contenant un exemple de formulaire Django "UserCreationForm" modifié pour les besoins du site;
- Fichier "models.py": Contenant les Modéles de class crée pour les besoin du site;
- Fichier "views.py" : Contenant toutes le vues, et les fonction crée pour les besoin du site;
- Fichier "requirements.txt : Contenant la liste des dépendances Python nécessaires pour exécuter l'application.



## Utiliser CoachForLife 

### Pré-requis et installation:

- Pour utiliser le site il suffit de cloner le projet depuis ce Lien GitHub en [Cliquant Ici](https://github.com/ForskyOnly/CoachForLife) ;
- Avoir installé Python sur sa machine et avoir  derniere version de Django;

