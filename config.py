import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    """Configuration de l'application avec sécurisation des clés API"""
    
    # Clé API Scopus depuis les variables d'environnement
    SCOPUS_API_KEY = os.getenv('SCOPUS_API_KEY')
    
    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configuration de l'application
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # URLs de base pour les APIs
    SCOPUS_BASE_URL = "https://api.elsevier.com/content"
    
    @staticmethod
    def validate_config():
        """Valide que toutes les configurations requises sont présentes"""
        if not Config.SCOPUS_API_KEY:
            raise ValueError(
                "SCOPUS_API_KEY non trouvée. "
                "Veuillez définir votre clé API Scopus dans le fichier .env ou les variables d'environnement."
            )
        
        print("✅ Configuration validée avec succès")
        return True

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    TESTING = False
    
    # En production, utilisez des secrets plus forts
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    @staticmethod
    def validate_production_config():
        """Validations supplémentaires pour la production"""
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY doit être définie en production")
        
        if Config.SCOPUS_API_KEY == 'votre_cle_api_scopus_ici':
            raise ValueError("Veuillez changer la clé API par défaut en production")

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
