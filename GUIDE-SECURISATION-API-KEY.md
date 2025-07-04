# Guide de Sécurisation de l'API Key Scopus

## 🔐 Pourquoi sécuriser l'API Key ?

### **Risques sans sécurisation :**
- ❌ **Exposition publique** : Clé visible dans le code source
- ❌ **Abus potentiel** : Utilisation non autorisée de votre quota
- ❌ **Coûts inattendus** : Dépassement des limites d'utilisation
- ❌ **Révocation forcée** : Elsevier peut révoquer la clé exposée

### **Avantages de la sécurisation :**
- ✅ **Protection** : Clé cachée du code source
- ✅ **Contrôle** : Gestion centralisée des accès
- ✅ **Flexibilité** : Différentes clés pour dev/prod
- ✅ **Conformité** : Respect des bonnes pratiques

## 🛠️ Méthodes de Sécurisation Implémentées

### **1. Variables d'environnement (.env)**

#### **Fichier .env créé :**
```bash
# Configuration des clés API
SCOPUS_API_KEY=votre_cle_api_scopus_ici

# Configuration de l'application
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=votre_secret_key_flask_ici
```

#### **Avantages :**
- ✅ **Séparation** : Clés séparées du code
- ✅ **Environnements** : Différentes clés dev/prod
- ✅ **Sécurité** : Fichier exclu du contrôle de version

### **2. Configuration centralisée (config.py)**

#### **Classe Config créée :**
```python
class Config:
    SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    @staticmethod
    def validate_config():
        if not Config.SCOPUS_API_KEY:
            raise ValueError("SCOPUS_API_KEY non trouvée")
```

#### **Avantages :**
- ✅ **Validation** : Vérification automatique des clés
- ✅ **Centralisation** : Toute la config en un endroit
- ✅ **Flexibilité** : Configs différentes par environnement

### **3. Protection Git (.gitignore)**

#### **Fichiers protégés :**
```bash
# Fichiers de configuration sensibles
.env
.env.local
.env.production
*.key
secrets.json
```

#### **Avantages :**
- ✅ **Exclusion** : Fichiers sensibles non versionnés
- ✅ **Sécurité** : Pas d'exposition accidentelle
- ✅ **Équipe** : Protection pour tous les développeurs

## 📋 Instructions d'Installation

### **Étape 1 : Installer les dépendances**
```bash
pip install python-dotenv
```

### **Étape 2 : Configurer le fichier .env**
1. Copiez votre clé API Scopus
2. Modifiez le fichier `.env` :
```bash
SCOPUS_API_KEY=votre_vraie_cle_api_ici
SECRET_KEY=votre_secret_flask_unique_ici
```

### **Étape 3 : Vérifier la configuration**
```bash
python app.py
```

**Résultat attendu :**
```
🔐 Configuration sécurisée chargée avec succès
✅ Configuration validée avec succès
```

## 🚨 Que faire si vous avez déjà exposé votre clé ?

### **Actions immédiates :**
1. **Révoquer la clé** sur le portail Elsevier
2. **Générer une nouvelle clé** API
3. **Mettre à jour** le fichier .env
4. **Vérifier les logs** d'utilisation sur Scopus

### **Prévention future :**
- ✅ Utiliser cette méthode de sécurisation
- ✅ Vérifier .gitignore avant chaque commit
- ✅ Scanner le code pour les clés exposées
- ✅ Utiliser des outils de détection de secrets

## 🔧 Configuration Avancée

### **Variables d'environnement système (Production)**

#### **Windows :**
```cmd
setx SCOPUS_API_KEY "votre_cle_api"
setx SECRET_KEY "votre_secret_key"
```

#### **Linux/Mac :**
```bash
export SCOPUS_API_KEY="votre_cle_api"
export SECRET_KEY="votre_secret_key"
```

### **Configuration Docker**
```dockerfile
# Dockerfile
ENV SCOPUS_API_KEY=""
ENV SECRET_KEY=""

# docker-compose.yml
environment:
  - SCOPUS_API_KEY=${SCOPUS_API_KEY}
  - SECRET_KEY=${SECRET_KEY}
```

### **Configuration Cloud (Heroku, AWS, etc.)**
```bash
# Heroku
heroku config:set SCOPUS_API_KEY=votre_cle_api

# AWS Lambda
aws lambda update-function-configuration \
  --function-name votre-fonction \
  --environment Variables='{SCOPUS_API_KEY=votre_cle_api}'
```

## 🛡️ Sécurité Supplémentaire

### **1. Rotation des clés**
- 🔄 **Changez régulièrement** votre clé API
- 📅 **Planifiez** une rotation tous les 6 mois
- 🔍 **Surveillez** l'utilisation de votre quota

### **2. Limitation d'accès**
- 🌐 **IP whitelisting** : Limitez aux IPs autorisées
- ⏰ **Horaires** : Restreignez les heures d'utilisation
- 📊 **Monitoring** : Surveillez les appels API

### **3. Chiffrement**
```python
# Optionnel : Chiffrement de la clé
from cryptography.fernet import Fernet

def encrypt_api_key(key):
    f = Fernet(Fernet.generate_key())
    encrypted_key = f.encrypt(key.encode())
    return encrypted_key
```

## ✅ Checklist de Sécurisation

### **Configuration de base :**
- [x] Fichier .env créé avec la clé API
- [x] python-dotenv installé
- [x] config.py configuré
- [x] .gitignore mis à jour
- [x] app.py modifié pour utiliser la config

### **Vérifications :**
- [ ] Clé API réelle ajoutée dans .env
- [ ] Application démarre sans erreur
- [ ] Fichier .env exclu de Git
- [ ] Tests de fonctionnement OK

### **Sécurité avancée :**
- [ ] Variables d'environnement système (production)
- [ ] Monitoring des appels API
- [ ] Plan de rotation des clés
- [ ] Documentation équipe mise à jour

## 🚀 Utilisation

### **Développement local :**
1. Modifiez `.env` avec votre clé
2. Lancez `python app.py`
3. L'application utilise automatiquement la clé sécurisée

### **Production :**
1. Définissez les variables d'environnement système
2. Utilisez `ProductionConfig`
3. Surveillez les logs et l'utilisation

### **Équipe :**
1. Chaque développeur a son propre `.env`
2. Clés de développement séparées de la production
3. Documentation partagée des bonnes pratiques

## 🎯 Résultat Final

Votre API Key Scopus est maintenant :
- ✅ **Sécurisée** : Cachée du code source
- ✅ **Flexible** : Différente par environnement
- ✅ **Protégée** : Exclue du contrôle de version
- ✅ **Validée** : Vérification automatique au démarrage
- ✅ **Maintenable** : Configuration centralisée

**Votre application est maintenant conforme aux bonnes pratiques de sécurité !** 🔐
