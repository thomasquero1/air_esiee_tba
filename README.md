# air_esiee_tba
Projet final pour le module python

### Un jeu d’aventure textuel éducatif en Python  
*Projet réalisé par Messad Houcine & Thomas Quéro – ESIEE Paris (2025)*

---

## 🧭 Guide Utilisateur

### 🎮 Description du jeu

**Air ESIEE – Copilote A320** est un jeu d’aventure textuel dans lequel vous incarnez un **copilote stagiaire** à bord d’un **Airbus A320** de la compagnie *Air ESIEE*.  

Lors d’un vol d’entraînement entre Paris et Nice, diverses **pannes techniques**, **urgences ECAM** et **situations humaines complexes** surviennent.  
Votre rôle est de :
- Diagnostiquer les anomalies à l’aide du système **ECAM** (*Electronic Centralized Aircraft Monitor*),
- Appliquer les **procédures QRH** (*Quick Reference Handbook*),
- Dialoguer efficacement avec le commandant et les passagers,
- Prendre des décisions rapides mais réfléchies.

Le jeu mélange apprentissage technique, simulation de vol et réflexion éthique.

---

### 🎯 Objectif du joueur

Le but est de **ramener l’avion en sécurité** tout en maintenant un bon score de performance.  
Chaque action a une conséquence : résoudre les pannes, gérer le stress de l’équipage, et assurer la sécurité du vol.

---

### 🧮 Système de points

Les décisions prises par le joueur influencent directement son **score final**.  
L’évaluation repose sur trois domaines : **technique**, **communication**, et **gestion**.

#### 🛠️ Actions techniques

| Situation | Décision du joueur | Points |
|------------|-------------------|--------:|
| Regarder les instruments après une urgence | Bonne analyse | **+1** |
| Résoudre une partie du problème | Avancée partielle | **+3** |
| Résoudre le problème sans perte | Excellente maîtrise | **+7** |
| Résoudre le problème avec légère perte | Bonne réaction | **+4** |
| Résoudre le problème avec pertes majeures | Sauvetage minimal | **+1** |
| Ignorer un message ECAM ou une alarme | Mauvaise gestion | **–3** |
| Mauvaise procédure / checklist erronée | Erreur critique | **–5** |

#### 🧑‍✈️ Gestion humaine

| Situation | Décision / attitude | Points |
|------------|--------------------|--------:|
| Interaction positive avec le commandant | Bonne communication | **+2** |
| Interaction positive avec les passagers / ATC | Empathie et sang-froid | **+2** |
| Rassure un PNJ en détresse | Leadership | **+3** |
| Comportement froid ou agressif | Manque de communication | **–2** |
| Garde son calme en urgence | Professionnalisme | **+4** |
| Perd son sang-froid | Stress mal géré | **–3** |

#### ⚙️ Gestion et anticipation

| Situation | Décision du joueur | Points |
|------------|-------------------|--------:|
| Vérifie les systèmes avant d’agir | Anticipation | **+2** |
| Utilise le bon outil au bon moment | Bon jugement | **+3** |
| Oublie un élément essentiel | Inattention | **–2** |
| Priorise les urgences correctement | Excellente hiérarchisation | **+4** |

#### 🏁 Fin de mission

| Résultat | Points |
|-----------|--------:|
| Vol terminé sans incident | **+10** |
| Vol terminé avec déroutement maîtrisé | **+5** |
| Vol terminé avec pertes majeures | **+2** |
| Crash ou erreur fatale | **–10** |
| Quitte la partie avant la fin | **–5** |

#### 💯 Évaluation finale

| Score total | Évaluation | Mention |
|--------------|-------------|----------|
| **90–100 pts** | Pilote d’exception | 🥇 *Certification Or Air ESIEE* |
| **75–89 pts** | Copilote confirmé | 🥈 *Certification Argent* |
| **50–74 pts** | Copilote stagiaire | 🥉 *Certification Bronze* |
| **0–49 pts** | Non qualifié | ❌ *Échec de la mission* |

---

### 🧩 Conditions de victoire et de défaite

- 🏆 **Victoire** : le vol se termine sans incident majeur.  
- 💀 **Défaite** : erreur critique ou crash.  
- 🧠 **Mode apprentissage** : chaque erreur est commentée pour progresser.

---

### 💻 Installation

#### Prérequis
- Python **3.10+**
- Tkinter (inclus par défaut)
- OS : Windows, macOS, Linux

#### Étapes
```bash
git clone http://github.com/PoyTuSadre/air_esiee_tba
cd air_esiee_tba


🚀 Lancer le jeu
Mode terminal :
python AirEsiee.py

Mode graphique :
python AirEsiee.py --gui

💡 Si Tkinter n’est pas disponible, le jeu bascule automatiquement en mode texte.

🕹️ Commandes principales
Commande	Action
look	Observer l’environnement
go <direction>	Se déplacer
take <objet>	Prendre un objet
drop <objet>	Poser un objet
inventory	Voir votre inventaire
talk <pnj>	Parler à un personnage
ecam	Consulter les messages ECAM
use <objet>	Utiliser un équipement
history	Voir les actions passées
undo	Revenir en arrière
help	Liste des commandes
quit	Quitter le jeu

**Exemple**
✈️ Air ESIEE – Copilote A320
Bienvenue à bord du vol Air ESIEE Training Flight 2025.

> look
Vous êtes dans le cockpit. L’ECAM affiche une alarme moteur gauche.

> ecam
[ECAM ALERT] ENGINE 1 FIRE
Procédure : IDLE – ENG MASTER OFF – FIRE PB – AGENT 1 DISP.

> take QRH
Vous prenez le QRH et suivez la checklist d’urgence.

> talk captain
Commandant : "Feu moteur maîtrisé ! Excellent réflexe, copilote."

> ecam
Tous les systèmes sont stables. Le vol peut continuer.



classDiagram
    Game --> Player
    Game --> Room
    Game --> Actions
    Room --> Item
    Room --> Character
    Player --> Item
    Player --> Command
    Character --> Command
    Game --> Win

    class Game {
        +start()
        +process_command()
        +trigger_event()
    }

    class Player {
        -inventory
        +move()
        +take()
        +drop()
        +talk()
    }

    class Room {
        +description
        +exits
        +items
    }

    class Item {
        +name
        +description
        +use()
    }

    class Character {
        +name
        +dialogue()
    }

    class Win {
        +check_victory()
        +check_defeat()
    }

Perspectives de Développement

🎨 Interface et immersion

Interface graphique plus complète avec jauges ECAM et sons cockpit

Intégration du logo Air ESIEE et d’un thème visuel

Effets sonores : alarmes, dialogues audio

🧠 Gameplay et IA

PNJ avec comportements et émotions

Système de décisions multiples et conséquences à long terme

Pannes dynamiques générées aléatoirement

🌍 Extensions

Mode multijoueur (pilote/copilote en réseau) Jeu type COOP

Intégration d’un mode formation avec score détaillé et feedback

Historique des sessions et analyse de performance


Auteurs

Messad Houcine

Thomas Quéro

Projet développé à ESIEE Paris dans le cadre du module de Programmation Orientée Objet (2025).
Langage : Python 3
Licence : Usage pédagogique (CC BY-NC 4.0)
