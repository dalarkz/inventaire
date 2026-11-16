"""
Inventaire Coffrage MT — Application Flask (Version avancée)
"""

import json
from datetime import datetime, timezone
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from config import Config
from models import Article, MouvementStock, TypeArticle, db

# ── Schémas et types par défaut ──────────────────────────────
TYPES_INITIAUX = [
    {
        "nom": "Panneau de coffrage",
        "description": "Panneaux métalliques et contreplaqués",
        "champs": [
            {
                "nom": "Grandeur",
                "type": "select",
                "options": ["2 pieds", "4 pieds", "5 pieds", "7 pieds", "8 pieds", "10 pieds"],
                "requis": True,
            },
            {
                "nom": "Couleur",
                "type": "select",
                "options": ["Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Rose", "Orange", "Noir"],
                "requis": False,
            },
            {
                "nom": "Épaisseur / Matière",
                "type": "text",
                "options": [],
                "requis": False,
            },
        ],
    },
    {
        "nom": "Filler",
        "description": "Pièces de remplissage pour fermer les coffrages",
        "champs": [
            {
                "nom": "Largeur",
                "type": "select",
                "options": ['1 po', '2 po', '3 po', '4 po', '6 po', '8 po', '12 po'],
                "requis": True,
            },
            {
                "nom": "Hauteur",
                "type": "select",
                "options": ['4 pieds', '5 pieds', '8 pieds', '9 pieds', '10 pieds'],
                "requis": True,
            },
            {
                "nom": "Matière",
                "type": "select",
                "options": ["Acier", "Aluminium", "Bois"],
                "requis": False,
            },
        ],
    },
    {
        "nom": "Cage de coin",
        "description": "Cages d'angle intérieur et extérieur",
        "champs": [
            {
                "nom": "Type de coin",
                "type": "select",
                "options": ["Coin intérieur", "Coin extérieur", "Coin à charnière"],
                "requis": True,
            },
            {
                "nom": "Hauteur",
                "type": "select",
                "options": ["4 pieds", "5 pieds", "8 pieds", "10 pieds"],
                "requis": True,
            },
        ],
    },
    {
        "nom": "Cage de braise",
        "description": "Cages de braise et accessoires de maintien",
        "champs": [
            {
                "nom": "Modèle",
                "type": "text",
                "options": [],
                "requis": True,
            },
            {
                "nom": "Longueur",
                "type": "text",
                "options": [],
                "requis": False,
            },
        ],
    },
    {
        "nom": "Étais",
        "description": "Étais métalliques de soutènement télescopiques",
        "champs": [
            {
                "nom": "Plage de hauteur",
                "type": "select",
                "options": ["1.50m - 2.50m", "2.00m - 3.50m", "2.50m - 4.00m", "3.00m - 5.00m"],
                "requis": True,
            },
            {
                "nom": "Capacité max (kN)",
                "type": "number",
                "options": [],
                "requis": False,
            },
            {
                "nom": "Finition",
                "type": "select",
                "options": ["Galvanisé", "Peint", "Aluminium"],
                "requis": False,
            },
        ],
    },
    {
        "nom": "Poutrelles",
        "description": "Poutrelles H20 et profilés de répartition",
        "champs": [
            {
                "nom": "Type de profilé",
                "type": "select",
                "options": ["H20 Bois", "Aluminium", "Acier"],
                "requis": True,
            },
            {
                "nom": "Longueur",
                "type": "select",
                "options": ["1.90 m", "2.45 m", "2.90 m", "3.90 m", "4.90 m", "5.90 m"],
                "requis": True,
            },
        ],
    },
]


def appliquer_mouvement_stock(article, type_mouvement, quantite, chantier="", note=""):
    """Met à jour les compteurs de l'article et enregistre le mouvement dans l'historique."""
    quantite = int(quantite)
    if quantite <= 0:
        raise ValueError("La quantité doit être supérieure à 0.")

    if type_mouvement == "Sortie chantier":
        article.quantite_en_chantier += quantite
        if chantier:
            article.chantier_actuel = chantier
    elif type_mouvement == "Retour chantier":
        article.quantite_en_chantier = max(0, article.quantite_en_chantier - quantite)
        if article.quantite_en_chantier == 0:
            article.chantier_actuel = ""
    elif type_mouvement == "Envoi réparation":
        article.quantite_en_reparation += quantite
        article.etat = "À réparer"
    elif type_mouvement == "Retour réparation":
        article.quantite_en_reparation = max(0, article.quantite_en_reparation - quantite)
        if article.quantite_en_reparation == 0:
            article.etat = "Bon"
    elif type_mouvement == "Perte / Rebut":
        if article.quantite_en_chantier >= quantite:
            article.quantite_en_chantier -= quantite
        article.quantite_totale = max(0, article.quantite_totale - quantite)
    elif type_mouvement == "Ajustement stock":
        article.quantite_totale += quantite

    article.modifie_le = datetime.now(timezone.utc)

    mvt = MouvementStock(
        article_id=article.id,
        type_mouvement=type_mouvement,
        quantite=quantite,
        chantier=chantier.strip(),
        note=note.strip(),
        date_mouvement=datetime.now(timezone.utc),
    )
    db.session.add(mvt)
    return mvt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        _seed_types()

    @app.context_processor
    def inject_global_data():
        return {
            "now": datetime.now(timezone.utc),
            "TYPES_MOUVEMENT": MouvementStock.TYPES_MOUVEMENT,
            "ETATS": Article.ETATS,
            "COULEURS": Article.COULEURS,
        }

    # ──────────────────────────────────────────────────────────
    #  TABLEAU DE BORD UNIFIÉ & MOBILE
    # ──────────────────────────────────────────────────────────
    @app.route("/")
    def dashboard():
        articles = Article.query.join(TypeArticle).order_by(
            TypeArticle.nom, Article.dimension_modele
        ).all()
        types = TypeArticle.query.order_by(TypeArticle.nom).all()

        total_qte = sum(a.quantite_totale for a in articles)
        total_dispo = sum(a.quantite_disponible for a in articles)
        total_chantier = sum(a.quantite_en_chantier for a in articles)
        total_reparation = sum(a.quantite_en_reparation for a in articles)
        
        articles_alerte = [a for a in articles if a.est_en_alerte]
        nb_alertes = len(articles_alerte)

        # Liste de tous les chantiers actifs distincts
        chantiers_actifs = sorted(
            {a.chantier_actuel for a in articles if a.chantier_actuel}
        )
        emplacements = sorted(
            {a.emplacement for a in articles if a.emplacement}
        )

        # Derniers mouvements récents (5)
        derniers_mouvements = (
            MouvementStock.query.order_by(MouvementStock.date_mouvement.desc())
            .limit(6)
            .all()
        )

        stats = {
            "total": total_qte,
            "disponible": total_dispo,
            "en_chantier": total_chantier,
            "en_reparation": total_reparation,
            "nb_alertes": nb_alertes,
        }

        return render_template(
            "dashboard.html",
            articles=articles,
            types=types,
            stats=stats,
            articles_alerte=articles_alerte,
            chantiers=chantiers_actifs,
            emplacements=emplacements,
            derniers_mouvements=derniers_mouvements,
        )

    # ──────────────────────────────────────────────────────────
    #  ARTICLES — LISTE & GESTION
    # ──────────────────────────────────────────────────────────
    @app.route("/articles")
    def liste_articles():
        articles = Article.query.join(TypeArticle).order_by(
            TypeArticle.nom, Article.dimension_modele
        ).all()
        types = TypeArticle.query.order_by(TypeArticle.nom).all()
        chantiers = sorted({a.chantier_actuel for a in articles if a.chantier_actuel})
        emplacements = sorted({a.emplacement for a in articles if a.emplacement})

        return render_template(
            "articles/liste.html",
            articles=articles,
            types=types,
            chantiers=chantiers,
            emplacements=emplacements,
        )

    @app.route("/articles/ajouter", methods=["GET", "POST"])
    def ajouter_article():
        types = TypeArticle.query.order_by(TypeArticle.nom).all()
        if request.method == "POST":
            type_id = int(request.form["type_id"])
            type_obj = TypeArticle.query.get_or_404(type_id)

            # Extraction des valeurs dynamiques des champs définis par le type
            champs_valeurs = {}
            for ch in (type_obj.champs_schema or []):
                nom_champ = ch["nom"]
                field_key = f"dyn_{nom_champ}"
                champs_valeurs[nom_champ] = request.form.get(field_key, "").strip()

            couleur = champs_valeurs.get("Couleur", request.form.get("couleur", "")).strip()

            article = Article(
                type_id=type_id,
                dimension_modele=request.form["dimension_modele"].strip(),
                couleur=couleur,
                quantite_totale=int(request.form.get("quantite_totale", 0)),
                quantite_en_chantier=int(request.form.get("quantite_en_chantier", 0)),
                quantite_en_reparation=int(request.form.get("quantite_en_reparation", 0)),
                seuil_alerte=int(request.form.get("seuil_alerte", 5)),
                chantier_actuel=request.form.get("chantier_actuel", "").strip(),
                etat=request.form.get("etat", "Bon"),
                emplacement=request.form.get("emplacement", "").strip(),
                notes=request.form.get("notes", "").strip(),
                champs_valeurs=champs_valeurs,
            )
            db.session.add(article)
            db.session.commit()

            # Enregistrer le mouvement initial si qté > 0
            if article.quantite_totale > 0:
                appliquer_mouvement_stock(
                    article,
                    "Ajustement stock",
                    article.quantite_totale,
                    note="Stock initial enregistré",
                )
                db.session.commit()

            flash(f"Article « {article.dimension_modele} » ajouté avec succès.", "success")
            return redirect(url_for("dashboard"))

        return render_template(
            "articles/formulaire.html",
            article=None,
            types=types,
        )

    @app.route("/articles/<int:id>/modifier", methods=["GET", "POST"])
    def modifier_article(id):
        article = Article.query.get_or_404(id)
        types = TypeArticle.query.order_by(TypeArticle.nom).all()

        if request.method == "POST":
            type_id = int(request.form["type_id"])
            type_obj = TypeArticle.query.get_or_404(type_id)

            champs_valeurs = {}
            for ch in (type_obj.champs_schema or []):
                nom_champ = ch["nom"]
                field_key = f"dyn_{nom_champ}"
                champs_valeurs[nom_champ] = request.form.get(field_key, "").strip()

            couleur = champs_valeurs.get("Couleur", request.form.get("couleur", "")).strip()

            article.type_id = type_id
            article.dimension_modele = request.form["dimension_modele"].strip()
            article.couleur = couleur
            article.quantite_totale = int(request.form.get("quantite_totale", 0))
            article.quantite_en_chantier = int(request.form.get("quantite_en_chantier", 0))
            article.quantite_en_reparation = int(request.form.get("quantite_en_reparation", 0))
            article.seuil_alerte = int(request.form.get("seuil_alerte", 5))
            article.chantier_actuel = request.form.get("chantier_actuel", "").strip()
            article.etat = request.form.get("etat", "Bon")
            article.emplacement = request.form.get("emplacement", "").strip()
            article.notes = request.form.get("notes", "").strip()
            article.champs_valeurs = champs_valeurs
            article.modifie_le = datetime.now(timezone.utc)

            db.session.commit()
            flash("Article mis à jour.", "success")
            return redirect(url_for("dashboard"))

        return render_template(
            "articles/formulaire.html",
            article=article,
            types=types,
        )

    @app.route("/articles/<int:id>/supprimer", methods=["POST"])
    def supprimer_article(id):
        article = Article.query.get_or_404(id)
        nom = article.dimension_modele
        db.session.delete(article)
        db.session.commit()
        flash(f"Article « {nom} » supprimé.", "warning")
        return redirect(url_for("dashboard"))

    # ──────────────────────────────────────────────────────────
    #  MOUVEMENTS DE STOCK
    # ──────────────────────────────────────────────────────────
    @app.route("/mouvements")
    def liste_mouvements():
        mouvements = (
            MouvementStock.query.join(Article)
            .join(TypeArticle)
            .order_by(MouvementStock.date_mouvement.desc())
            .all()
        )
        chantiers = sorted({m.chantier for m in mouvements if m.chantier})
        return render_template(
            "mouvements/liste.html",
            mouvements=mouvements,
            chantiers=chantiers,
        )

    @app.route("/mouvements/nouveau", methods=["GET", "POST"])
    def nouveau_mouvement():
        articles = Article.query.join(TypeArticle).order_by(
            TypeArticle.nom, Article.dimension_modele
        ).all()
        article_preselect_id = request.args.get("article_id", type=int)

        if request.method == "POST":
            article_id = int(request.form["article_id"])
            type_mouvement = request.form["type_mouvement"]
            quantite = int(request.form["quantite"])
            chantier = request.form.get("chantier", "")
            note = request.form.get("note", "")

            article = Article.query.get_or_404(article_id)
            try:
                appliquer_mouvement_stock(
                    article, type_mouvement, quantite, chantier, note
                )
                db.session.commit()
                flash(
                    f"Mouvement enregistré : {type_mouvement} de {quantite} unité(s) pour « {article.dimension_modele} ».",
                    "success",
                )
                return redirect(url_for("dashboard"))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template(
            "mouvements/nouveau.html",
            articles=articles,
            article_preselect_id=article_preselect_id,
        )

    @app.route("/api/mouvements/rapide", methods=["POST"])
    def mouvement_rapide():
        """Endpoint AJAX pour enregistrer un mouvement depuis le modal tactile mobile."""
        data = request.form
        article_id = int(data.get("article_id", 0))
        type_mouvement = data.get("type_mouvement")
        quantite = int(data.get("quantite", 0))
        chantier = data.get("chantier", "").strip()
        note = data.get("note", "").strip()

        article = Article.query.get(article_id)
        if not article:
            return jsonify({"success": False, "message": "Article introuvable"}), 404

        try:
            mvt = appliquer_mouvement_stock(article, type_mouvement, quantite, chantier, note)
            db.session.commit()
            return jsonify({
                "success": True,
                "disponible": article.quantite_disponible,
                "en_chantier": article.quantite_en_chantier,
                "en_reparation": article.quantite_en_reparation,
                "est_en_alerte": article.est_en_alerte,
                "message": f"{type_mouvement} ({quantite}) enregistré pour {article.dimension_modele}."
            })
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 400

    # ──────────────────────────────────────────────────────────
    #  TYPES D'ARTICLES DYNAMIQUES & CHAMPS PERSONNALISÉS
    # ──────────────────────────────────────────────────────────
    @app.route("/types")
    def liste_types():
        types = TypeArticle.query.order_by(TypeArticle.nom).all()
        return render_template("types/liste.html", types=types)

    @app.route("/types/ajouter", methods=["POST"])
    def ajouter_type():
        nom = request.form.get("nom", "").strip()
        description = request.form.get("description", "").strip()
        champs_json_raw = request.form.get("champs_schema_json", "[]")

        if not nom:
            flash("Le nom du type est obligatoire.", "danger")
            return redirect(url_for("liste_types"))

        if TypeArticle.query.filter_by(nom=nom).first():
            flash(f"Le type « {nom} » existe déjà.", "danger")
            return redirect(url_for("liste_types"))

        try:
            champs_schema = json.loads(champs_json_raw) if champs_json_raw else []
        except Exception:
            champs_schema = []

        t = TypeArticle(nom=nom, description=description, champs_schema=champs_schema)
        db.session.add(t)
        db.session.commit()
        flash(f"Type « {nom} » créé avec ses champs personnalisés.", "success")
        return redirect(url_for("liste_types"))

    @app.route("/types/<int:id>/modifier", methods=["GET", "POST"])
    def modifier_type(id):
        type_article = TypeArticle.query.get_or_404(id)
        if request.method == "POST":
            nom = request.form.get("nom", "").strip()
            if not nom:
                flash("Le nom est obligatoire.", "danger")
                return redirect(url_for("modifier_type", id=id))

            existing = TypeArticle.query.filter_by(nom=nom).first()
            if existing and existing.id != id:
                flash(f"Le type « {nom} » existe déjà.", "danger")
                return redirect(url_for("modifier_type", id=id))

            champs_json_raw = request.form.get("champs_schema_json", "[]")
            try:
                champs_schema = json.loads(champs_json_raw) if champs_json_raw else []
            except Exception:
                champs_schema = type_article.champs_schema or []

            type_article.nom = nom
            type_article.description = request.form.get("description", "").strip()
            type_article.champs_schema = champs_schema
            db.session.commit()
            flash(f"Type « {nom} » mis à jour avec ses champs personnalisés.", "success")
            return redirect(url_for("liste_types"))

        return render_template("types/modifier.html", type_article=type_article)

    @app.route("/types/<int:id>/supprimer", methods=["POST"])
    def supprimer_type(id):
        type_article = TypeArticle.query.get_or_404(id)
        if type_article.articles:
            flash("Impossible de supprimer : des articles utilisent ce type.", "danger")
            return redirect(url_for("liste_types"))
        nom = type_article.nom
        db.session.delete(type_article)
        db.session.commit()
        flash(f"Type « {nom} » supprimé.", "warning")
        return redirect(url_for("liste_types"))

    @app.route("/api/types/<int:id>/schema")
    def api_type_schema(id):
        type_obj = TypeArticle.query.get_or_404(id)
        return jsonify({
            "id": type_obj.id,
            "nom": type_obj.nom,
            "champs": type_obj.champs_schema or []
        })

    return app


def _seed_types():
    """Pré-charge les types initiaux avec leurs schémas de champs s'ils n'existent pas."""
    if TypeArticle.query.count() == 0:
        for t_info in TYPES_INITIAUX:
            db.session.add(
                TypeArticle(
                    nom=t_info["nom"],
                    description=t_info["description"],
                    champs_schema=t_info["champs"],
                )
            )
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
