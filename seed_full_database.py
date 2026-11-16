"""
Script d'initialisation complet pour Gestion MT Coffrage
Peuple la base de données SQLite (inventaire.db) avec un catalogue complet et réaliste :
- Tous les panneaux (2pi, 4pi, 5pi, 7pi, 8pi, 10pi) et couleurs (Rose, Vert, Bleu, Rouge, Blanc, Jaune, Orange, Noir)
- Cages calculées (1 cage = 21 panneaux)
- Répartition : Cour (disponible), Chantiers réels, Locations réelles
- Fillers, Cages de coin, Cages de braise
- Étais télescopiques, Poutrelles H20
- Quincaillerie (Tirants, écrous papillon, coins)
- Sécurité (Garde-corps, passerelles)
- Historique des mouvements réalistes
"""
from datetime import datetime, timezone, timedelta
from app import create_app, db
from models import TypeArticle, Article, MouvementStock

app = create_app()

PANNEAUX_PAR_CAGE = 21

TYPES_DATA = [
    {
        "nom": "Panneau de coffrage",
        "description": "Panneaux métalliques calculés en cages de 21 panneaux",
        "champs_schema": [
            {"nom": "Grandeur", "type": "select", "options": ["2 pieds", "4 pieds", "5 pieds", "7 pieds", "8 pieds", "10 pieds"], "requis": True},
            {"nom": "Couleur", "type": "select", "options": ["Rose", "Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Orange", "Noir"], "requis": True}
        ]
    },
    {
        "nom": "Filler",
        "description": "Pièces de remplissage de coffrage",
        "champs_schema": [
            {"nom": "Largeur", "type": "select", "options": ["1 po", "2 po", "3 po", "4 po", "6 po", "8 po"], "requis": True},
            {"nom": "Hauteur", "type": "select", "options": ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], "requis": True}
        ]
    },
    {
        "nom": "Cage de coin",
        "description": "Cages d'angle intérieur et extérieur",
        "champs_schema": [
            {"nom": "Type de coin", "type": "select", "options": ["Coin intérieur", "Coin extérieur"], "requis": True},
            {"nom": "Hauteur", "type": "select", "options": ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], "requis": True}
        ]
    },
    {
        "nom": "Cage de braise",
        "description": "Cages de braise et maintien",
        "champs_schema": [
            {"nom": "Modèle", "type": "text", "options": [], "requis": True}
        ]
    },
    {
        "nom": "Étais",
        "description": "Étais métalliques télescopiques",
        "champs_schema": [
            {"nom": "Plage de hauteur", "type": "select", "options": ["1.50m - 2.50m", "2.00m - 3.50m", "2.50m - 4.00m", "3.00m - 5.00m"], "requis": True}
        ]
    },
    {
        "nom": "Poutrelles",
        "description": "Poutrelles H20 et profilés",
        "champs_schema": [
            {"nom": "Type", "type": "select", "options": ["H20 Bois", "Aluminium"], "requis": True},
            {"nom": "Longueur", "type": "select", "options": ["2.45 m", "2.90 m", "3.90 m", "4.90 m"], "requis": True}
        ]
    },
    {
        "nom": "Quincaillerie",
        "description": "Tirants, écrous et pièces d'assemblage",
        "champs_schema": [
            {"nom": "Dimension", "type": "text", "options": [], "requis": False}
        ]
    },
    {
        "nom": "Sécurité & Chantier",
        "description": "Garde-corps, passerelles et échelles",
        "champs_schema": [
            {"nom": "Type", "type": "text", "options": [], "requis": False}
        ]
    }
]

def seed_full():
    with app.app_context():
        print("Réinitialisation des tables SQLite...")
        db.drop_all()
        db.create_all()

        type_map = {}
        for td in TYPES_DATA:
            t = TypeArticle(
                nom=td["nom"],
                description=td["description"],
                champs_schema=td["champs_schema"]
            )
            db.session.add(t)
            db.session.flush()
            type_map[td["nom"]] = t.id

        print(f"Types créés : {len(type_map)}")

        articles_to_create = []
        mouvements_to_create = []
        now = datetime.now(timezone.utc)

        # 1. PANNEAUX DE COFFRAGE (1 CAGE = 21 PANNEAUX)
        panneaux_definitions = [
            # 10 pieds
            {"grandeur": "10 pieds", "couleur": "Rose", "cages_tot": 20, "cages_chant": 5, "cages_loc": 3, "chantier": "Chantier Tour Horizon", "client": "Coffrage Boréal", "emplacement": "Cour A - Allée 1"},
            {"grandeur": "10 pieds", "couleur": "Bleu", "cages_tot": 16, "cages_chant": 4, "cages_loc": 0, "chantier": "Complexe Desjardins", "client": "", "emplacement": "Cour A - Allée 2"},
            {"grandeur": "10 pieds", "couleur": "Vert", "cages_tot": 14, "cages_chant": 3, "cages_loc": 2, "chantier": "Pont Champlain", "client": "Construction Apex", "emplacement": "Cour A - Allée 3"},
            {"grandeur": "10 pieds", "couleur": "Blanc", "cages_tot": 10, "cages_chant": 2, "cages_loc": 1, "chantier": "Hôpital St-Luc", "client": "Groupe BTP Québec", "emplacement": "Cour A - Allée 4"},
            {"grandeur": "10 pieds", "couleur": "Orange", "cages_tot": 8, "cages_chant": 2, "cages_loc": 0, "chantier": "Hangar 5", "client": "", "emplacement": "Cour A - Allée 5"},
            {"grandeur": "10 pieds", "couleur": "Jaune", "cages_tot": 6, "cages_chant": 0, "cages_loc": 0, "chantier": "", "client": "", "emplacement": "Cour A - Allée 6"},

            # 8 pieds
            {"grandeur": "8 pieds", "couleur": "Vert", "cages_tot": 25, "cages_chant": 8, "cages_loc": 4, "chantier": "Chantier Pont Champlain", "client": "Construction Apex", "emplacement": "Cour B - Allée 1"},
            {"grandeur": "8 pieds", "couleur": "Rose", "cages_tot": 18, "cages_chant": 4, "cages_loc": 2, "chantier": "Tour Bell", "client": "Coffrages Modernes Inc.", "emplacement": "Cour B - Allée 2"},
            {"grandeur": "8 pieds", "couleur": "Rouge", "cages_tot": 15, "cages_chant": 3, "cages_loc": 0, "chantier": "Centre Logistique Dorval", "client": "", "emplacement": "Cour B - Allée 3"},
            {"grandeur": "8 pieds", "couleur": "Bleu", "cages_tot": 12, "cages_chant": 2, "cages_loc": 1, "chantier": "Résidence St-Laurent", "client": "BTP Prestige", "emplacement": "Cour B - Allée 4"},
            {"grandeur": "8 pieds", "couleur": "Noir", "cages_tot": 8, "cages_chant": 0, "cages_loc": 0, "chantier": "", "client": "", "emplacement": "Cour B - Allée 5"},

            # 7 pieds
            {"grandeur": "7 pieds", "couleur": "Orange", "cages_tot": 12, "cages_chant": 3, "cages_loc": 2, "chantier": "Hangar 5", "client": "Groupe BTP Québec", "emplacement": "Cour B - Allée 6"},
            {"grandeur": "7 pieds", "couleur": "Blanc", "cages_tot": 10, "cages_chant": 2, "cages_loc": 0, "chantier": "Tour Bell", "client": "", "emplacement": "Cour B - Allée 7"},

            # 5 pieds
            {"grandeur": "5 pieds", "couleur": "Jaune", "cages_tot": 10, "cages_chant": 2, "cages_loc": 1, "chantier": "Pont Champlain", "client": "Coffrage Boréal", "emplacement": "Cour C - Allée 1"},
            {"grandeur": "5 pieds", "couleur": "Bleu", "cages_tot": 8, "cages_chant": 1, "cages_loc": 0, "chantier": "Tour Horizon", "client": "", "emplacement": "Cour C - Allée 2"},

            # 4 pieds
            {"grandeur": "4 pieds", "couleur": "Rouge", "cages_tot": 10, "cages_chant": 2, "cages_loc": 0, "chantier": "Résidence St-Laurent", "client": "", "emplacement": "Cour C - Allée 3"},
            {"grandeur": "4 pieds", "couleur": "Vert", "cages_tot": 8, "cages_chant": 1, "cages_loc": 1, "chantier": "Tour Bell", "client": "Construction Apex", "emplacement": "Cour C - Allée 4"},

            # 2 pieds
            {"grandeur": "2 pieds", "couleur": "Blanc", "cages_tot": 6, "cages_chant": 1, "cages_loc": 0, "chantier": "Complexe Desjardins", "client": "", "emplacement": "Cour C - Allée 5"},
            {"grandeur": "2 pieds", "couleur": "Noir", "cages_tot": 6, "cages_chant": 0, "cages_loc": 0, "chantier": "", "client": "", "emplacement": "Cour C - Allée 6"}
        ]

        t_panneau_id = type_map["Panneau de coffrage"]
        for p in panneaux_definitions:
            tot_p = p["cages_tot"] * PANNEAUX_PAR_CAGE
            chant_p = p["cages_chant"] * PANNEAUX_PAR_CAGE
            loc_p = p["cages_loc"] * PANNEAUX_PAR_CAGE

            art = Article(
                type_id=t_panneau_id,
                dimension_modele=f"Panneau {p['grandeur']}",
                couleur=p["couleur"],
                quantite_totale=tot_p,
                quantite_en_chantier=chant_p,
                quantite_en_location=loc_p,
                quantite_en_reparation=0,
                seuil_alerte=2 * PANNEAUX_PAR_CAGE,
                chantier_actuel=p["chantier"],
                client_location=p["client"],
                etat="Bon",
                emplacement=p["emplacement"],
                notes=f"Calculé en cages de 21 panneaux. {p['cages_tot']} cages totales.",
                champs_valeurs={"Grandeur": p["grandeur"], "Couleur": p["couleur"]}
            )
            db.session.add(art)
            db.session.flush()

            # Mouvement chantier si actif
            if p["cages_chant"] > 0:
                m1 = MouvementStock(
                    article_id=art.id,
                    type_mouvement="Sortie chantier",
                    quantite=chant_p,
                    chantier=p["chantier"],
                    client="",
                    note=f"{p['cages_chant']} cages ({chant_p} panneaux) envoyées au chantier {p['chantier']}",
                    date_mouvement=now - timedelta(days=2)
                )
                db.session.add(m1)

            # Mouvement location si actif
            if p["cages_loc"] > 0:
                m2 = MouvementStock(
                    article_id=art.id,
                    type_mouvement="Sortie location",
                    quantite=loc_p,
                    chantier="",
                    client=p["client"],
                    note=f"Location de {p['cages_loc']} cages ({loc_p} panneaux) à {p['client']}",
                    date_mouvement=now - timedelta(days=1)
                )
                db.session.add(m2)

        # 2. FILLERS
        t_filler_id = type_map["Filler"]
        fillers_data = [
            {"dim": "Filler 2 po x 8 pieds", "larg": "2 po", "haut": "8 pieds", "tot": 60, "chant": 20, "loc": 0, "chantier": "Chantier Tour Horizon", "emp": "Cour D - Rack 1"},
            {"dim": "Filler 4 po x 8 pieds", "larg": "4 po", "haut": "8 pieds", "tot": 50, "chant": 15, "loc": 5, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Cour D - Rack 1"},
            {"dim": "Filler 6 po x 8 pieds", "larg": "6 po", "haut": "8 pieds", "tot": 40, "chant": 10, "loc": 0, "chantier": "Tour Bell", "emp": "Cour D - Rack 1"},
            {"dim": "Filler 2 po x 10 pieds", "larg": "2 po", "haut": "10 pieds", "tot": 40, "chant": 12, "loc": 4, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Cour D - Rack 2"},
            {"dim": "Filler 4 po x 10 pieds", "larg": "4 po", "haut": "10 pieds", "tot": 35, "chant": 10, "loc": 0, "chantier": "Complexe Desjardins", "emp": "Cour D - Rack 2"}
        ]
        for f in fillers_data:
            art = Article(
                type_id=t_filler_id,
                dimension_modele=f["dim"],
                couleur="",
                quantite_totale=f["tot"],
                quantite_en_chantier=f["chant"],
                quantite_en_location=f.get("loc", 0),
                quantite_en_reparation=0,
                seuil_alerte=10,
                chantier_actuel=f.get("chantier", ""),
                client_location=f.get("client", ""),
                etat="Bon",
                emplacement=f["emp"],
                champs_valeurs={"Largeur": f["larg"], "Hauteur": f["haut"]}
            )
            db.session.add(art)

        # 3. CAGES DE COIN
        t_coin_id = type_map["Cage de coin"]
        coins_data = [
            {"dim": "Coin intérieur 8 pieds", "type_c": "Coin intérieur", "haut": "8 pieds", "tot": 24, "chant": 8, "loc": 2, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Cour D - Rack 3"},
            {"dim": "Coin extérieur 8 pieds", "type_c": "Coin extérieur", "haut": "8 pieds", "tot": 20, "chant": 6, "loc": 2, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Cour D - Rack 3"},
            {"dim": "Coin intérieur 10 pieds", "type_c": "Coin intérieur", "haut": "10 pieds", "tot": 18, "chant": 6, "loc": 3, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Cour D - Rack 4"},
            {"dim": "Coin extérieur 10 pieds", "type_c": "Coin extérieur", "haut": "10 pieds", "tot": 16, "chant": 4, "loc": 2, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Cour D - Rack 4"}
        ]
        for c in coins_data:
            art = Article(
                type_id=t_coin_id,
                dimension_modele=c["dim"],
                couleur="",
                quantite_totale=c["tot"],
                quantite_en_chantier=c["chant"],
                quantite_en_location=c["loc"],
                quantite_en_reparation=0,
                seuil_alerte=4,
                chantier_actuel=c["chantier"],
                client_location=c["client"],
                etat="Bon",
                emplacement=c["emp"],
                champs_valeurs={"Type de coin": c["type_c"], "Hauteur": c["haut"]}
            )
            db.session.add(art)

        # 4. ÉTAIS
        t_etais_id = type_map["Étais"]
        etais_data = [
            {"dim": "Étai télescopique 2.00m - 3.50m", "plage": "2.00m - 3.50m", "tot": 200, "chant": 70, "loc": 30, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Râtelier Étais 1"},
            {"dim": "Étai télescopique 2.50m - 4.00m", "plage": "2.50m - 4.00m", "tot": 150, "chant": 50, "loc": 20, "chantier": "Complexe Desjardins", "client": "Groupe BTP Québec", "emp": "Râtelier Étais 2"},
            {"dim": "Étai haute capacité 3.00m - 5.00m", "plage": "3.00m - 5.00m", "tot": 80, "chant": 30, "loc": 10, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Râtelier Étais 3"}
        ]
        for et in etais_data:
            art = Article(
                type_id=t_etais_id,
                dimension_modele=et["dim"],
                couleur="",
                quantite_totale=et["tot"],
                quantite_en_chantier=et["chant"],
                quantite_en_location=et["loc"],
                quantite_en_reparation=0,
                seuil_alerte=25,
                chantier_actuel=et["chantier"],
                client_location=et["client"],
                etat="Bon",
                emplacement=et["emp"],
                champs_valeurs={"Plage de hauteur": et["plage"]}
            )
            db.session.add(art)

        # 5. POUTRELLES H20
        t_poutre_id = type_map["Poutrelles"]
        poutres_data = [
            {"dim": "Poutrelle H20 Bois 2.90m", "type_p": "H20 Bois", "long": "2.90 m", "tot": 120, "chant": 40, "loc": 20, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Cour Extérieure - Rack P1"},
            {"dim": "Poutrelle H20 Bois 3.90m", "type_p": "H20 Bois", "long": "3.90 m", "tot": 100, "chant": 35, "loc": 15, "chantier": "Complexe Desjardins", "client": "Construction Apex", "emp": "Cour Extérieure - Rack P2"},
            {"dim": "Poutrelle H20 Bois 4.90m", "type_p": "H20 Bois", "long": "4.90 m", "tot": 80, "chant": 25, "loc": 10, "chantier": "Pont Champlain", "client": "Groupe BTP Québec", "emp": "Cour Extérieure - Rack P3"}
        ]
        for pt in poutres_data:
            art = Article(
                type_id=t_poutre_id,
                dimension_modele=pt["dim"],
                couleur="",
                quantite_totale=pt["tot"],
                quantite_en_chantier=pt["chant"],
                quantite_en_location=pt["loc"],
                quantite_en_reparation=0,
                seuil_alerte=20,
                chantier_actuel=pt["chantier"],
                client_location=pt["client"],
                etat="Bon",
                emplacement=pt["emp"],
                champs_valeurs={"Type": pt["type_p"], "Longueur": pt["long"]}
            )
            db.session.add(art)

        # 6. QUINCAILLERIE & ATTACHES
        t_quinc_id = type_map["Quincaillerie"]
        quinc_data = [
            {"dim": "Tirants (Tie-rods) 24 po", "tot": 800, "chant": 250, "loc": 100, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Bac Quincaillerie 1"},
            {"dim": "Tirants (Tie-rods) 36 po", "tot": 400, "chant": 120, "loc": 50, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Bac Quincaillerie 2"},
            {"dim": "Écrous papillon (Wing nuts) 15mm", "tot": 1200, "chant": 400, "loc": 150, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Bac Quincaillerie 3"},
            {"dim": "Coins de serrage (Wedges)", "tot": 1000, "chant": 300, "loc": 100, "chantier": "Pont Champlain", "client": "Groupe BTP Québec", "emp": "Bac Quincaillerie 4"},
            {"dim": "Clamps d'alignement rapide", "tot": 250, "chant": 80, "loc": 30, "chantier": "Complexe Desjardins", "client": "Coffrage Boréal", "emp": "Bac Quincaillerie 5"}
        ]
        for q in quinc_data:
            art = Article(
                type_id=t_quinc_id,
                dimension_modele=q["dim"],
                couleur="",
                quantite_totale=q["tot"],
                quantite_en_chantier=q["chant"],
                quantite_en_location=q["loc"],
                quantite_en_reparation=0,
                seuil_alerte=100,
                chantier_actuel=q["chantier"],
                client_location=q["client"],
                etat="Bon",
                emplacement=q["emp"],
                champs_valeurs={"Dimension": q["dim"]}
            )
            db.session.add(art)

        # 7. SÉCURITÉ & CHANTIER
        t_sec_id = type_map["Sécurité & Chantier"]
        sec_data = [
            {"dim": "Potelets de garde-corps acier", "tot": 120, "chant": 45, "loc": 15, "chantier": "Tour Horizon", "client": "Coffrage Boréal", "emp": "Allée Sécurité S1"},
            {"dim": "Passerelles de travail bétonnage 2.50m", "tot": 30, "chant": 10, "loc": 4, "chantier": "Pont Champlain", "client": "Construction Apex", "emp": "Allée Sécurité S2"},
            {"dim": "Échelles d'accès sécurisées aluminium", "tot": 20, "chant": 8, "loc": 2, "chantier": "Complexe Desjardins", "client": "Groupe BTP Québec", "emp": "Allée Sécurité S3"}
        ]
        for s in sec_data:
            art = Article(
                type_id=t_sec_id,
                dimension_modele=s["dim"],
                couleur="",
                quantite_totale=s["tot"],
                quantite_en_chantier=s["chant"],
                quantite_en_location=s["loc"],
                quantite_en_reparation=0,
                seuil_alerte=5,
                chantier_actuel=s["chantier"],
                client_location=s["client"],
                etat="Bon",
                emplacement=s["emp"],
                champs_valeurs={"Type": s["dim"]}
            )
            db.session.add(art)

        db.session.commit()
        print("Base SQLite peuplée avec succès !")
        total_arts = Article.query.count()
        total_mvts = MouvementStock.query.count()
        print(f"Total articles : {total_arts}")
        print(f"Total mouvements : {total_mvts}")

if __name__ == "__main__":
    seed_full()

