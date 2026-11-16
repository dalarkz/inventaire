import json
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TypeArticle(db.Model):
    __tablename__ = "type_article"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), default="")
    # champs_schema stocke la liste des champs personnalisés pour ce type :
    # [
    #   {"nom": "Grandeur", "type": "select", "options": ["2 pieds", "4 pieds", ...], "requis": True},
    #   {"nom": "Capacité charge", "type": "text", "options": [], "requis": False}
    # ]
    champs_schema = db.Column(db.JSON, default=list)
    cree_le = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    articles = db.relationship(
        "Article", backref="type_article", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<TypeArticle {self.nom}>"


class Article(db.Model):
    __tablename__ = "article"

    ETATS = ["Bon", "Usé", "À réparer"]
    COULEURS = ["Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Rose", "Orange", "Noir"]

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(
        db.Integer, db.ForeignKey("type_article.id"), nullable=False
    )
    dimension_modele = db.Column(db.String(100), nullable=False)
    couleur = db.Column(db.String(30), default="")
    quantite_totale = db.Column(db.Integer, nullable=False, default=0)
    quantite_en_chantier = db.Column(db.Integer, nullable=False, default=0)
    quantite_en_location = db.Column(db.Integer, nullable=False, default=0)
    quantite_en_reparation = db.Column(db.Integer, nullable=False, default=0)
    seuil_alerte = db.Column(db.Integer, nullable=False, default=5)
    chantier_actuel = db.Column(db.String(150), default="")
    client_location = db.Column(db.String(150), default="")
    etat = db.Column(db.String(20), nullable=False, default="Bon")
    emplacement = db.Column(db.String(150), default="")
    notes = db.Column(db.Text, default="")
    # champs_valeurs stocke les valeurs dynamiques des champs définis par le type :
    # {"Capacité charge": "20 kN", "Filetage": "Acier galvanisé"}
    champs_valeurs = db.Column(db.JSON, default=dict)
    cree_le = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    modifie_le = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    mouvements = db.relationship(
        "MouvementStock", backref="article", lazy=True, cascade="all, delete-orphan",
        order_by="desc(MouvementStock.date_mouvement)"
    )

    @property
    def quantite_disponible(self):
        """Calculée automatiquement : totale - en chantier - en location - en réparation (dans la cour)."""
        return max(0, self.quantite_totale - self.quantite_en_chantier - self.quantite_en_location - self.quantite_en_reparation)

    @property
    def est_en_alerte(self):
        """Indique si la quantité disponible est inférieure ou égale au seuil défini."""
        return self.quantite_disponible <= self.seuil_alerte

    @property
    def nombre_cages_disponibles(self):
        """Nombre de cages de 21 panneaux disponibles dans la cour."""
        return self.quantite_disponible // 21

    @property
    def nombre_cages_totales(self):
        """Nombre total de cages de 21 panneaux."""
        return self.quantite_totale // 21

    @property
    def nombre_cages_en_chantier(self):
        """Nombre de cages de 21 panneaux sur les chantiers."""
        return self.quantite_en_chantier // 21

    @property
    def nombre_cages_en_location(self):
        """Nombre de cages de 21 panneaux en location."""
        return self.quantite_en_location // 21

    def __repr__(self):
        return f"<Article {self.dimension_modele}>"


class MouvementStock(db.Model):
    __tablename__ = "mouvement_stock"

    TYPES_MOUVEMENT = [
        "Sortie chantier",
        "Retour chantier",
        "Sortie location",
        "Retour location",
        "Envoi réparation",
        "Retour réparation",
        "Perte / Rebut",
        "Ajustement répartition",
        "Ajustement stock",
    ]

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(
        db.Integer, db.ForeignKey("article.id"), nullable=False
    )
    type_mouvement = db.Column(db.String(50), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=1)
    chantier = db.Column(db.String(150), default="")
    client = db.Column(db.String(150), default="")
    date_mouvement = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    note = db.Column(db.Text, default="")
    cree_le = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Mouvement {self.type_mouvement} - Article {self.article_id} : {self.quantite}>"
