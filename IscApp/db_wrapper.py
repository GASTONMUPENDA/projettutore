import pyorient
from pyorientdb import OrientDB
import requests
import json


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "gmk144996")
client.db_create("IscAppDB", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)

db = DatabaseWrapper()

client.db_open("IscAppDB", "root", "gmk144996")

client.command("CREATE CLASS Utilisateur EXTENDS V")
client.command("CREATE PROPERTY Utilisateur.nom STRING")
client.command("CREATE PROPERTY Utilisateur.prenom STRING")
client.command("CREATE PROPERTY Utilisateur.postnom STRING")
client.command("CREATE PROPERTY Utilisateur.adresse_physique STRING")
client.command("CREATE PROPERTY Utilisateur.telephone STRING")
client.command("CREATE PROPERTY Utilisateur.email STRING")
client.command("CREATE PROPERTY Utilisateur.mot_de_passe STRING")

# Création de la classe Etudiant
client.command("CREATE CLASS Etudiant EXTENDS Utilisateur")
client.command("CREATE PROPERTY Etudiant.matricule STRING")
client.command("CREATE PROPERTY Etudiant.promotion STRING")
client.command("CREATE PROPERTY Etudiant.section STRING")

# Création de la classe Enseignant
client.command("CREATE CLASS Enseignant EXTENDS Utilisateur")
client.command("CREATE PROPERTY Enseignant.numero_d_ordre STRING")
client.command("CREATE PROPERTY Enseignant.cours EMBEDDEDLIST STRING")
client.command("CREATE PROPERTY Enseignant.promotion STRING")
client.command("CREATE PROPERTY Enseignant.section STRING")

# Création de la classe Résultat
client.command("CREATE CLASS Resultat EXTENDS V")
client.command("CREATE PROPERTY Resultat.moyenne FLOAT")
client.command("CREATE PROPERTY Resultat.mention STRING")
client.command("CREATE PROPERTY Resultat.etudiant LINK Etudiant")
client.command("CREATE PROPERTY Resultat.cours LINK Cours")
client.command("CREATE PROPERTY Resultat.promotion STRING")

# Création de la classe Cours
client.command("CREATE CLASS Cours EXTENDS V")
client.command("CREATE PROPERTY Cours.nom STRING")
client.command("CREATE PROPERTY Cours.description STRING")
client.command("CREATE PROPERTY Cours.code STRING")
client.command("CREATE PROPERTY Cours.enseignant LINK Enseignant")


class DatabaseWrapper:
    def __init__(self, host, port, user, password):
        self.base_url = f"http://{host}:{port}/"
        self.auth = (user, password)
        self.db_name = "IscAppDB"

    def save_utilisateur(self, nom, prenom, postnom, adresse_physique, telephone, email, motdepasse):
          url = f"{self.base_url}command/{self.db_name}/sql"
          headers = {
            'Content-Type': 'application/json'
        }
          data = {
            "command": f"INSERT INTO Utilisateur SET nom='{nom}', prenom='{prenom}', postnom='{postnom}', adressephysique='{adressephysique}', telephone='{telephone}', email='{email}', motdepasse='{motdepasse}'"
        }
          response = requests.post(url, headers=headers, data=json.dumps(data), auth=self.auth)
          return response.json()

    def connect(self):
        # L'API HTTP ne nécessite pas de connexion explicite
        pass

    def close(self):
        # L'API HTTP ne nécessite pas de déconnexion explicite
        pass