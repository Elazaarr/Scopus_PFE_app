📚 Application de gestion des publications scientifiques indexées

Cette application permet de rechercher des publications scientifiques à partir de l’API Scopus, d’enrichir les résultats avec les données du fichier SCImago (quartile, H-index, SJR), puis de générer un rapport au format PDF, Excel ou les deux.  
Elle est destinée aux chercheurs, enseignants et étudiants souhaitant consulter ou évaluer les performances de publication d’un auteur.


✨ Fonctionnalités

- 🔍 Recherche d’auteur via **nom complet** ou **Scopus ID**
- 📊 Filtrage des publications (par année, titre, type, etc.)
- 🧠 Enrichissement avec les données SCImago
- 📝 Génération de rapports au **format PDF**, **Excel**, ou **les deux**
- 💾 Téléchargement du fichier généré
- 🌐 Interface web simple et ergonomique  


🧰 Prérequis

Avant de lancer l'application, assurez-vous d'avoir installé :

- [Python 3.11+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Git](https://git-scm.com/) (pour cloner le dépôt)
- Une clé API Scopus valide (à insérer dans un fichier `.env`)

Pour installer les dépendances :
  ```bash
pip install -r requirements.txt
  ```
Pour cloner le dépôt :
```bash
  git clone https://github.com/Elazaarr/Scopus_PFE_app.git
  cd nom-du-repo
```
Pour lancer l'application Flask :
```bash
  python app.py
```

