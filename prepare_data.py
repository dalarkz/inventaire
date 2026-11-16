import json

# Full dataset definitions matching seed_full_database.py
SEED_SECTIONS = [
  {
    "nom": "Coffrage & Panneaux (Cages)",
    "description": "Panneaux métalliques calculés en cages de 21, fillers et cages de coin"
  },
  {
    "nom": "Étaiement & Poutrelles",
    "description": "Étais télescopiques réglables, trépieds, fourches et poutrelles H20"
  },
  {
    "nom": "Quincaillerie & Attaches",
    "description": "Tirants (tie-rods), écrous papillon, coins de serrage, verrous et barres"
  },
  {
    "nom": "Sécurité & Outillage",
    "description": "Potelets de garde-corps, passerelles de bétonnage, échelles d'accès chantier"
  }
]

SEED_TYPES = [
  {
    "nom": "Panneau de coffrage",
    "description": "Panneaux métalliques calculés en cages de 21 panneaux",
    "champs": [
      { "nom": "Grandeur", "type": "select", "options": ["2 pieds", "4 pieds", "5 pieds", "7 pieds", "8 pieds", "10 pieds"], "requis": True },
      { "nom": "Couleur", "type": "select", "options": ["Rose", "Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Orange", "Noir"], "requis": True }
    ]
  },
  {
    "nom": "Filler",
    "description": "Pièces de remplissage de coffrage",
    "champs": [
      { "nom": "Largeur", "type": "select", "options": ["1 po", "2 po", "3 po", "4 po", "6 po", "8 po"], "requis": True },
      { "nom": "Hauteur", "type": "select", "options": ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], "requis": True }
    ]
  },
  {
    "nom": "Cage de coin",
    "description": "Cages d'angle intérieur et extérieur",
    "champs": [
      { "nom": "Type de coin", "type": "select", "options": ["Coin intérieur", "Coin extérieur"], "requis": True },
      { "nom": "Hauteur", "type": "select", "options": ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], "requis": True }
    ]
  },
  {
    "nom": "Cage de braise",
    "description": "Cages de braise et maintien",
    "champs": [{ "nom": "Modèle", "type": "text", "options": [], "requis": True }]
  },
  {
    "nom": "Étais",
    "description": "Étais métalliques télescopiques",
    "champs": [
      { "nom": "Plage de hauteur", "type": "select", "options": ["1.50m - 2.50m", "2.00m - 3.50m", "2.50m - 4.00m", "3.00m - 5.00m"], "requis": True }
    ]
  },
  {
    "nom": "Poutrelles",
    "description": "Poutrelles H20 et profilés",
    "champs": [
      { "nom": "Type", "type": "select", "options": ["H20 Bois", "Aluminium"], "requis": True },
      { "nom": "Longueur", "type": "select", "options": ["2.45 m", "2.90 m", "3.90 m", "4.90 m"], "requis": True }
    ]
  },
  {
    "nom": "Quincaillerie",
    "description": "Tirants, écrous et pièces d'assemblage",
    "champs": [
      { "nom": "Dimension", "type": "text", "options": [], "requis": False }
    ]
  },
  {
    "nom": "Sécurité & Chantier",
    "description": "Garde-corps, passerelles et échelles",
    "champs": [
      { "nom": "Type", "type": "text", "options": [], "requis": False }
    ]
  }
]

print("Definitions valid, sections:", len(SEED_SECTIONS), "types:", len(SEED_TYPES))

