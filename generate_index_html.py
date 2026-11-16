import os

html_content = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Gestion MT">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0c0d0e">
<title>Gestion MT Coffrage — Inventaire, Cages Dynamiques & Mobile</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
<style>
/* ── PALETTE OFFICIELLE : NOIR, BLANC & ORANGE ──────────────── */
:root {
  --noir-pur: #000000;
  --noir-fond: #0c0d0e;
  --noir-card: #18191b;
  --noir-elevated: #242528;
  --blanc: #ffffff;
  --gris-clair: #f4f4f5;
  --gris-bordure: #2d2e32;
  --orange: #ff6200;
  --orange-hover: #e55800;
  --orange-subtil: rgba(255, 98, 0, 0.15);
  --rouge-alerte: #ef4444;
  --vert-ok: #22c55e;
  --bleu-location: #38bdf8;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}

* {
  box-sizing: border-box;
}

body {
  background-color: var(--noir-fond);
  color: #f4f4f5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  -webkit-tap-highlight-color: transparent;
  padding-bottom: calc(75px + var(--safe-bottom));
}

@media (min-width: 992px) {
  body {
    padding-bottom: 20px;
  }
}

/* ── Navbar Desktop & Top Bar Mobile ────────────────────────── */
.navbar {
  background-color: var(--noir-pur) !important;
  border-bottom: 2px solid var(--orange);
  padding-top: 0.7rem;
  padding-bottom: 0.7rem;
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 900;
  letter-spacing: 0.04em;
  color: var(--blanc);
  text-transform: uppercase;
}

.brand-badge {
  background-color: var(--orange);
  color: var(--noir-pur);
  font-weight: 800;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.navbar .nav-link {
  color: #a1a1aa !important;
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.5rem 0.8rem !important;
  border-radius: 6px;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.navbar .nav-link:hover {
  color: var(--blanc) !important;
  background-color: rgba(255, 255, 255, 0.06);
}

.navbar .nav-link.active-page {
  color: var(--orange) !important;
  background-color: var(--orange-subtil);
}

/* ── Mobile Bottom Navigation Bar (Dock Tactile au Pouce) ───── */
.mobile-bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: calc(64px + var(--safe-bottom));
  padding-bottom: var(--safe-bottom);
  background-color: rgba(12, 13, 14, 0.96);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1.5px solid var(--gris-bordure);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1040;
}

.mobile-nav-btn {
  background: transparent;
  border: none;
  color: #8e8e93;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  flex: 1;
  height: 100%;
  padding: 4px 0;
  cursor: pointer;
  transition: all 0.15s ease;
  text-decoration: none;
}

.mobile-nav-btn i {
  font-size: 1.35rem;
  line-height: 1.1;
  margin-bottom: 2px;
}

.mobile-nav-btn:active {
  transform: scale(0.92);
}

.mobile-nav-btn.active-page {
  color: var(--orange) !important;
}

.mobile-nav-btn.active-page i {
  transform: translateY(-1px);
}

/* ── Floating Action Button (FAB) Mobile ────────────────────── */
.mobile-fab {
  position: fixed;
  bottom: calc(76px + var(--safe-bottom));
  right: 18px;
  z-index: 1030;
}

.fab-btn {
  width: 56px;
  height: 56px;
  border-radius: 50% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 18px rgba(255, 98, 0, 0.45) !important;
  border: 2px solid #ffffff !important;
}

.fab-btn:active {
  transform: scale(0.92);
}

/* ── Cartes métriques ─────────────────────────────────────── */
.card-stat {
  background-color: var(--noir-card);
  border: 1px solid var(--gris-bordure);
  border-radius: 12px;
  padding: 1.1rem 1.25rem;
  height: 100%;
}

.card-stat .stat-value {
  font-size: 2.1rem;
  font-weight: 900;
  line-height: 1;
  color: var(--blanc);
  letter-spacing: -0.02em;
}

.card-stat .stat-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #a1a1aa;
  margin-top: 0.45rem;
}

/* ── Cartes Cages Panneaux ─────────────────────────────────── */
.card-cage {
  background-color: var(--blanc);
  color: var(--noir-pur);
  border: 1.5px solid #e4e4e7;
  border-radius: 14px;
  padding: 1.25rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
  position: relative;
  transition: border-color 0.15s ease, transform 0.1s ease;
}

.card-cage:hover {
  border-color: var(--orange);
}

.cage-color-stripe {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.badge-cage-color {
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

/* ── Cartes Mobile pour Tableaux ───────────────────────────── */
.mobile-item-card {
  background-color: var(--blanc);
  color: var(--noir-pur);
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 0.85rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* ── Boutons Tactiles Orange & Noir ────────────────────────── */
.btn-orange {
  background-color: var(--orange);
  border-color: var(--orange);
  color: var(--noir-pur);
  font-weight: 800;
  letter-spacing: 0.02em;
}

.btn-orange:hover, .btn-orange:active, .btn-orange:focus {
  background-color: var(--orange-hover);
  border-color: var(--orange-hover);
  color: var(--noir-pur);
}

.btn-outline-orange {
  border: 1.5px solid var(--orange);
  color: var(--orange);
  background: transparent;
  font-weight: 700;
}

.btn-outline-orange:hover {
  background-color: var(--orange);
  color: var(--noir-pur);
}

.btn-dark-pro {
  background-color: #27272a;
  border-color: #3f3f46;
  color: var(--blanc);
  font-weight: 700;
}

.btn-dark-pro:hover {
  background-color: #3f3f46;
  color: var(--blanc);
}

.btn-stepper {
  width: 52px;
  height: 52px;
  font-size: 1.5rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.card-custom {
  background-color: var(--blanc);
  color: var(--noir-pur);
  border: 1px solid #e4e4e7;
  border-radius: 12px;
}

.table-pro {
  width: 100%;
  margin-bottom: 0;
  color: #18181b;
}

.table-pro th {
  background-color: #f4f4f5;
  color: #52525b;
  font-weight: 800;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.85rem 1rem;
  border-bottom: 2px solid #e4e4e7;
}

.table-pro td {
  padding: 0.85rem 1rem;
  vertical-align: middle;
  border-bottom: 1px solid #f4f4f5;
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1.5px solid #d4d4d8;
  font-weight: 500;
  font-size: 16px; /* Empêche le zoom auto iOS */
  min-height: 46px;
}

.form-control:focus, .form-select:focus {
  border-color: var(--orange);
  box-shadow: 0 0 0 3px var(--orange-subtil);
}

/* Horizontal scroll chips for mobile */
.scroll-chips {
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  gap: 0.5rem;
}
.scroll-chips::-webkit-scrollbar {
  display: none;
}
</style>
</head>
<body>

<!-- ── TOP NAVBAR ───────────────────────────────────────────── -->
<nav class="navbar navbar-expand-lg sticky-top shadow-sm">
  <div class="container-fluid px-3 px-md-4">
    <a class="navbar-brand d-flex align-items-center gap-2 text-decoration-none" href="#" onclick="navigateTo('cages')">
      <span class="brand-title">Gestion MT</span>
      <span class="brand-badge">Coffrage</span>
    </a>

    <!-- Actions Mobile Rapides Header -->
    <div class="d-flex align-items-center gap-2 d-lg-none">
      <button class="btn btn-sm btn-outline-orange px-2 py-1 fw-bold" onclick="openAjusterModalSansArticle()" title="Ajuster Répartition">
        ⚙️ Ajuster
      </button>
      <button class="btn btn-sm btn-orange px-2 py-1 fw-bold" onclick="navigateTo('database')" title="Base & Sauvegardes">
        <i class="bi bi-database"></i>
      </button>
      <button class="navbar-toggler border-0 text-white" type="button" data-bs-toggle="collapse" data-bs-target="#navMain">
        <i class="bi bi-list fs-3"></i>
      </button>
    </div>

    <!-- Menu Déroulant Desktop & Tablette -->
    <div class="collapse navbar-collapse" id="navMain">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
        <li class="nav-item">
          <a class="nav-link active-page" href="#" id="nav-cages" onclick="navigateTo('cages')">
            <i class="bi bi-grid-3x3-gap-fill me-1"></i> Cages Panneaux (21 pcs)
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" id="nav-location" onclick="navigateTo('location')">
            <i class="bi bi-truck me-1"></i> Section Location
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" id="nav-sections" onclick="navigateTo('sections')">
            <i class="bi bi-folder2-open me-1"></i> Sections d'inventaire
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" id="nav-dashboard" onclick="navigateTo('dashboard')">
            <i class="bi bi-list-check me-1"></i> Tout le matériel
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" id="nav-mouvements" onclick="navigateTo('mouvements')">
            <i class="bi bi-clock-history me-1"></i> Historique
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" id="nav-database" onclick="navigateTo('database')">
            <i class="bi bi-database-fill-gear me-1"></i> Base & Sauvegardes
          </a>
        </li>
      </ul>
      <div class="d-none d-lg-flex gap-2">
        <button class="btn btn-outline-orange btn-sm px-3 fw-bold" onclick="openSortieLocationModal()">
          + Sortie Location
        </button>
        <button class="btn btn-outline-orange btn-sm px-3 fw-bold" onclick="openNouvelleSectionModal()">
          + Nouvelle Section
        </button>
        <button class="btn btn-orange btn-sm px-3 fw-bold" onclick="navigateTo('article-form')">
          + Nouvel item
        </button>
      </div>
    </div>
  </div>
</nav>

<!-- ── BOTTOM NAVIGATION DOCK (MOBILE DÉDIÉ AU POUCE) ──────── -->
<nav class="mobile-bottom-nav d-lg-none" id="mobile-dock">
  <button class="mobile-nav-btn active-page" id="mob-cages" onclick="navigateTo('cages')">
    <i class="bi bi-grid-3x3-gap-fill"></i>
    <span>Cages</span>
  </button>
  <button class="mobile-nav-btn" id="mob-location" onclick="navigateTo('location')">
    <i class="bi bi-truck"></i>
    <span>Location</span>
  </button>
  <button class="mobile-nav-btn" id="mob-sections" onclick="navigateTo('sections')">
    <i class="bi bi-folder2-open"></i>
    <span>Sections</span>
  </button>
  <button class="mobile-nav-btn" id="mob-dashboard" onclick="navigateTo('dashboard')">
    <i class="bi bi-list-check"></i>
    <span>Stock</span>
  </button>
  <button class="mobile-nav-btn" id="mob-database" onclick="navigateTo('database')">
    <i class="bi bi-database-fill-gear"></i>
    <span>Base/Sync</span>
  </button>
</nav>

<!-- ── BOUTON FLOTTANT D'ACTION RAPIDE (FAB MOBILE) ────────── -->
<div class="mobile-fab d-lg-none dropdown">
  <button class="btn btn-orange fab-btn" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    <i class="bi bi-plus-lg fs-3"></i>
  </button>
  <ul class="dropdown-menu dropdown-menu-end shadow-lg border-0 p-2" style="background-color: #18191b; border: 1px solid var(--gris-bordure) !important;">
    <li><a class="dropdown-item text-white py-2 fw-bold" href="#" onclick="openAjusterModalSansArticle()"><i class="bi bi-sliders text-warning me-2"></i> Ajuster répartition</a></li>
    <li><a class="dropdown-item text-white py-2 fw-bold" href="#" onclick="openSortieLocationModal()"><i class="bi bi-truck text-info me-2"></i> Louer du matériel</a></li>
    <li><a class="dropdown-item text-white py-2 fw-bold" href="#" onclick="openNewCageModal()"><i class="bi bi-grid-3x3 text-primary me-2"></i> Ajouter des cages</a></li>
    <li><a class="dropdown-item text-white py-2 fw-bold" href="#" onclick="navigateTo('article-form')"><i class="bi bi-plus-circle text-success me-2"></i> Nouvel item</a></li>
    <li><hr class="dropdown-divider border-secondary"></li>
    <li><a class="dropdown-item text-white py-2 fw-bold" href="#" onclick="navigateTo('database')"><i class="bi bi-cloud-arrow-down text-warning me-2"></i> Sauvegarde / Excel</a></li>
  </ul>
</div>

<!-- ── CONTENU PRINCIPAL ────────────────────────────────────── -->
<main class="container-fluid px-2 px-md-4 py-3 py-md-4">
  <div id="flash-container"></div>
  <div id="app"></div>
</main>

<!-- ==============================================================
     MODALS DU SYSTÈME
     ============================================================== -->

<!-- ── MODAL A : AJUSTER LA RÉPARTITION DU STOCK ──────────────── -->
<div class="modal fade" id="modalAjusterRepartitionCage" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <div>
          <h5 class="modal-title fs-6 fw-bold text-uppercase mb-0" style="letter-spacing: 0.05em;">
            Ajuster la répartition du stock (Cour / Chantier / Location)
          </h5>
          <div class="small" style="color: #a1a1aa;" id="ajust-cage-subtitle">
            Panneaux de coffrage &bull; 1 Cage = 21 Panneaux
          </div>
        </div>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitAjusterRepartition(event)">
        <input type="hidden" id="ajust-article-id">
        <div class="modal-body p-3 p-md-4">
          
          <div class="mb-3" id="ajust-select-article-box" style="display: none;">
            <label class="form-label fw-bold small text-uppercase text-muted">Sélectionner la grandeur et la couleur</label>
            <select id="ajust-article-select" class="form-select form-select-lg" onchange="onArticleSelectChange(this.value)">
            </select>
          </div>

                    <!-- Capacité personnalisable de cette cage -->
          <div class="p-2 mb-3 rounded-3 d-flex justify-content-between align-items-center flex-wrap gap-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div>
              <span class="small fw-bold text-uppercase text-dark d-block">
                <i class="bi bi-box-seam me-1 text-primary"></i> Capacité de la Cage :
              </span>
              <span class="small text-muted">Nombre de panneaux par cage pour cet article</span>
            </div>
            <div class="d-flex align-items-center gap-1">
              <button type="button" class="btn btn-sm btn-outline-secondary fw-bold px-2 py-1" onclick="stepAjustCapaciteArticle(-1)">−</button>
              <input type="number" id="ajust-panneaux-par-cage" class="form-control form-control-sm text-center fw-bold fs-5 text-primary" style="width: 75px;" value="21" min="1" max="150" oninput="onAjustCapaciteChanged()">
              <button type="button" class="btn btn-sm btn-outline-secondary fw-bold px-2 py-1" onclick="stepAjustCapaciteArticle(1)">+</button>
              <span class="small fw-bold text-muted ms-1">pcs/cage</span>
            </div>
          </div>

          <!-- 1. Stock Total -->
          <div class="p-3 mb-3 rounded-3" style="background-color: #0c0d0e; color: #fff; border: 1.5px solid var(--orange);">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="fw-bold small text-uppercase text-warning">1. Inventaire Total (Parc Complet)</span>
              <span class="badge bg-secondary">21 panneaux / cage</span>
            </div>
            <div class="row align-items-center g-2">
              <div class="col-7 col-md-8">
                <div class="input-group">
                  <button type="button" class="btn btn-secondary btn-stepper" onclick="stepAjustCages('ajust-cages-total', -1)">−</button>
                  <input type="number" id="ajust-cages-total" class="form-control text-center fw-bold fs-3 bg-dark text-white border-secondary" 
                         value="15" min="0" required oninput="calcAjustementFromTotal()">
                  <button type="button" class="btn btn-secondary btn-stepper" onclick="stepAjustCages('ajust-cages-total', 1)">+</button>
                </div>
              </div>
              <div class="col-5 col-md-4 text-end">
                <div class="fs-4 fw-bold text-white"><span id="ajust-panneaux-total">315</span> <span class="fs-6 fw-normal text-muted">pcs</span></div>
                <div class="small text-muted">panneaux au total</div>
              </div>
            </div>
          </div>

          <div class="fw-bold small text-uppercase text-muted mb-2">2. Répartition dans les 3 emplacements</div>

          <div class="row g-3">
            <!-- Cour -->
            <div class="col-12 col-md-4">
              <div class="p-3 rounded-3 h-100" style="background-color: #f0fdf4; border: 1.5px solid #bbf7d0;">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <strong class="text-success text-uppercase small">Dans la Cour</strong>
                  <span class="badge bg-success">Disponible</span>
                </div>
                <div class="input-group mb-2">
                  <button type="button" class="btn btn-outline-success btn-stepper" onclick="stepAjustCages('ajust-cages-cour', -1)">−</button>
                  <input type="number" id="ajust-cages-cour" class="form-control text-center fw-bold fs-4 text-success" 
                         value="10" min="0" required oninput="onRepartitionInputChanged()">
                  <button type="button" class="btn btn-outline-success btn-stepper" onclick="stepAjustCages('ajust-cages-cour', 1)">+</button>
                </div>
                <div class="small fw-bold text-success mb-2 text-center">
                  = <span id="ajust-panneaux-cour">210</span> panneaux
                </div>
                <label class="form-label small text-muted text-uppercase mb-1">Emplacement en cour :</label>
                <input type="text" id="ajust-emplacement-cour" class="form-control form-control-sm" placeholder="Ex: Cour A, Rack 1">
              </div>
            </div>

            <!-- Chantier -->
            <div class="col-12 col-md-4">
              <div class="p-3 rounded-3 h-100" style="background-color: #fff7ed; border: 1.5px solid #fed7aa;">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <strong style="color: var(--orange);" class="text-uppercase small">Sur Chantier</strong>
                  <span class="badge text-white" style="background-color: var(--orange);">En service</span>
                </div>
                <div class="input-group mb-2">
                  <button type="button" class="btn btn-outline-warning btn-stepper" onclick="stepAjustCages('ajust-cages-chantier', -1)">−</button>
                  <input type="number" id="ajust-cages-chantier" class="form-control text-center fw-bold fs-4" style="color: var(--orange);" 
                         value="3" min="0" required oninput="onRepartitionInputChanged()">
                  <button type="button" class="btn btn-outline-warning btn-stepper" onclick="stepAjustCages('ajust-cages-chantier', 1)">+</button>
                </div>
                <div class="small fw-bold text-center mb-2" style="color: var(--orange);">
                  = <span id="ajust-panneaux-chantier">63</span> panneaux
                </div>
                <label class="form-label small text-muted text-uppercase mb-1">Nom du chantier :</label>
                <input type="text" id="ajust-nom-chantier" class="form-control form-control-sm" placeholder="Ex: Tour Horizon">
              </div>
            </div>

            <!-- Location -->
            <div class="col-12 col-md-4">
              <div class="p-3 rounded-3 h-100" style="background-color: #f0f9ff; border: 1.5px solid #bae6fd;">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <strong class="text-primary text-uppercase small">Sur Location</strong>
                  <span class="badge bg-primary">Loué</span>
                </div>
                <div class="input-group mb-2">
                  <button type="button" class="btn btn-outline-primary btn-stepper" onclick="stepAjustCages('ajust-cages-location', -1)">−</button>
                  <input type="number" id="ajust-cages-location" class="form-control text-center fw-bold fs-4 text-primary" 
                         value="2" min="0" required oninput="onRepartitionInputChanged()">
                  <button type="button" class="btn btn-outline-primary btn-stepper" onclick="stepAjustCages('ajust-cages-location', 1)">+</button>
                </div>
                <div class="small fw-bold text-primary text-center mb-2">
                  = <span id="ajust-panneaux-location">42</span> panneaux
                </div>
                <label class="form-label small text-muted text-uppercase mb-1">Client locataire :</label>
                <input type="text" id="ajust-nom-client" class="form-control form-control-sm" placeholder="Ex: Coffrage Boréal">
              </div>
            </div>
          </div>

          <!-- Indicateur d'équilibre -->
          <div class="p-3 mt-3 rounded-2" id="ajust-balance-box" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
              <div id="ajust-balance-text" class="fw-bold small"></div>
              <div class="d-flex gap-1" id="ajust-balance-actions"></div>
            </div>
          </div>

          <div class="mt-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Note / Motif de l'ajustement</label>
            <input type="text" id="ajust-note" class="form-control" placeholder="Ex: Inventaire physique de la cour, retour...">
          </div>

        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-orange px-4 fw-bold">
            Enregistrer la nouvelle répartition
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL B : SORTIE VERS UN CHANTIER ───────────────────── -->
<div class="modal fade" id="modalSortieCage" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Sortie de Cages vers un chantier
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitSortieCage(event)">
        <input type="hidden" id="sortie-article-id">
        <div class="modal-body p-3 p-md-4">
          <div class="p-3 mb-3 rounded-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div class="fw-bold fs-6" id="sortie-cage-title">Panneau 10 pieds — Rose</div>
            <div class="small text-muted mt-1">
              Disponible en cour : <strong class="text-success fs-6" id="sortie-cage-dispo-txt">0 cage(s)</strong>
              <span id="sortie-cage-panneaux-txt" class="ms-1 text-muted">(0 panneaux)</span>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nombre de Cages à envoyer *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCageSortie(-1)">−</button>
              <input type="number" id="sortie-nb-cages" class="form-control text-center fw-bold fs-4" value="1" min="1" required oninput="calcPanneauxSortie()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCageSortie(1)">+</button>
            </div>
            <div class="form-text small fw-bold text-primary mt-1 text-center">
              = <span id="sortie-calc-panneaux">21</span> panneaux envoyés au chantier (21 pcs/cage)
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nom du chantier de destination *</label>
            <input type="text" id="sortie-chantier-nom" class="form-control form-control-lg" required placeholder="Ex : Tour Bell, Pont Sud, Résidence St-Laurent…">
          </div>

          <div class="mb-2">
            <label class="form-label fw-bold small text-uppercase text-muted">Note / Référence transporteur</label>
            <input type="text" id="sortie-note" class="form-control" placeholder="Ex: Camion 3, chauffeur Jean…">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-orange px-4 fw-bold">
            Valider la sortie de cage(s)
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL C : RETOUR DE CHANTIER ────────────────────────── -->
<div class="modal fade" id="modalRetourCage" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--vert-ok);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Retour de Cages du chantier vers la cour
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitRetourCage(event)">
        <input type="hidden" id="retour-article-id">
        <div class="modal-body p-3 p-md-4">
          <div class="p-3 mb-3 rounded-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div class="fw-bold fs-6" id="retour-cage-title">Panneau 10 pieds — Rose</div>
            <div class="small text-muted mt-1">
              Actuellement sur chantier : <strong style="color: var(--orange);" class="fs-6" id="retour-cage-chantier-txt">0 cage(s)</strong>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nombre de Cages qui reviennent en cour *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCageRetour(-1)">−</button>
              <input type="number" id="retour-nb-cages" class="form-control text-center fw-bold fs-4" value="1" min="1" required oninput="calcPanneauxRetour()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCageRetour(1)">+</button>
            </div>
            <div class="form-text small fw-bold text-success mt-1 text-center">
              = <span id="retour-calc-panneaux">21</span> panneaux réintégrés dans la cour (21 pcs/cage)
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label fw-bold small text-uppercase text-muted">Chantier d'origine</label>
            <input type="text" id="retour-chantier-nom" class="form-control" placeholder="Nom du chantier">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-success px-4 fw-bold">
            Réintégrer en cour
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL D : SORTIE EN LOCATION ────────────────────────── -->
<div class="modal fade" id="modalSortieLocation" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--bleu-location);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Sortie en Location de Matériel
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitSortieLocation(event)">
        <input type="hidden" id="loc-article-id">
        <div class="modal-body p-3 p-md-4">
          <div class="mb-3" id="loc-select-article-container">
            <label class="form-label fw-bold small text-uppercase text-muted">Article à mettre en location *</label>
            <select id="loc-article-select" class="form-select form-select-lg" required onchange="onLocArticleChange(this.value)">
            </select>
          </div>

          <div class="p-3 mb-3 rounded-2" id="loc-info-box" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div class="fw-bold fs-6" id="loc-info-title">Panneau 10 pieds — Rose</div>
            <div class="small text-muted mt-1">
              Disponible en cour : <strong class="text-success fs-6" id="loc-dispo-txt">0 disponible(s)</strong>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted" id="loc-quantite-label">Nombre de Cages à louer *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepLocQuantite(-1)">−</button>
              <input type="number" id="loc-quantite" class="form-control text-center fw-bold fs-4 text-primary" value="1" min="1" required oninput="calcPanneauxLocation()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepLocQuantite(1)">+</button>
            </div>
            <div class="form-text small fw-bold text-primary mt-1 text-center" id="loc-panneaux-equiv-box">
              = <span id="loc-calc-panneaux">21</span> panneaux loués (21 pcs/cage)
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Client / Entreprise locataire *</label>
            <input type="text" id="loc-client-nom" class="form-control form-control-lg" required placeholder="Ex : Coffrage Boréal, Construction Apex, Groupe BTP...">
          </div>

          <div class="row g-2 mb-3">
            <div class="col-6">
              <label class="form-label fw-bold small text-uppercase text-muted">Date de début</label>
              <input type="date" id="loc-date-debut" class="form-control">
            </div>
            <div class="col-6">
              <label class="form-label fw-bold small text-uppercase text-muted">Date retour prévue</label>
              <input type="date" id="loc-date-fin" class="form-control">
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label fw-bold small text-uppercase text-muted">N° Bon de location / Note</label>
            <input type="text" id="loc-note" class="form-control" placeholder="Ex: Contrat LOC-2026-04, Chauffeur...">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-primary px-4 fw-bold">
            Valider la sortie en location
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL E : RETOUR DE LOCATION ────────────────────────── -->
<div class="modal fade" id="modalRetourLocation" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--vert-ok);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Retour de Location vers la cour
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitRetourLocation(event)">
        <input type="hidden" id="retloc-article-id">
        <div class="modal-body p-3 p-md-4">
          <div class="p-3 mb-3 rounded-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <div class="fw-bold fs-6" id="retloc-title">Panneau 10 pieds — Rose</div>
            <div class="small text-muted mt-1">
              Locataire actuel : <strong class="text-dark" id="retloc-client-txt">—</strong> &bull; 
              En location : <strong class="text-primary fs-6" id="retloc-actuel-txt">0 cage(s)</strong>
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted" id="retloc-quantite-label">Nombre de Cages retournées en cour *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepRetLocQuantite(-1)">−</button>
              <input type="number" id="retloc-quantite" class="form-control text-center fw-bold fs-4 text-success" value="1" min="1" required oninput="calcPanneauxRetLoc()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepRetLocQuantite(1)">+</button>
            </div>
            <div class="form-text small fw-bold text-success mt-1 text-center" id="retloc-panneaux-equiv-box">
              = <span id="retloc-calc-panneaux">21</span> panneaux réintégrés dans la cour
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label fw-bold small text-uppercase text-muted">Note / État du matériel retourné</label>
            <input type="text" id="retloc-note" class="form-control" placeholder="Ex: Matériel vérifié, complet et nettoyé">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-success px-4 fw-bold">
            Réintégrer dans la cour
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL F : AJOUTER UNE NOUVELLE GRANDEUR / COULEUR CAGE ── -->
<div class="modal fade" id="modalConfigCage" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Ajouter une grandeur / couleur de Cages
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitConfigCage(event)">
        <div class="modal-body p-3 p-md-4">
          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Grandeur des panneaux *</label>
            <select id="cfg-grandeur" class="form-select form-select-lg" required>
              <option value="10 pieds">10 pieds</option>
              <option value="8 pieds" selected>8 pieds</option>
              <option value="7 pieds">7 pieds</option>
              <option value="5 pieds">5 pieds</option>
              <option value="4 pieds">4 pieds</option>
              <option value="2 pieds">2 pieds</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Couleur *</label>
            <select id="cfg-couleur" class="form-select form-select-lg" required>
              <option value="Rose">Rose</option>
              <option value="Vert">Vert</option>
              <option value="Bleu">Bleu</option>
              <option value="Rouge">Rouge</option>
              <option value="Blanc">Blanc</option>
              <option value="Jaune">Jaune</option>
              <option value="Orange">Orange</option>
              <option value="Noir">Noir</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nombre de panneaux par cage (capacité) *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCfgCapaciteCage(-1)">−</button>
              <input type="number" id="cfg-panneaux-par-cage" class="form-control text-center fw-bold fs-4 text-primary" value="21" min="1" max="150" required oninput="calcCfgPanneaux()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCfgCapaciteCage(1)">+</button>
            </div>
            <div class="form-text small mt-1">Vous pouvez personnaliser le nombre de panneaux par cage pour ce lot.</div>
          </div>

          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nombre total de Cages *</label>
            <div class="input-group">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCfgCages(-1)">−</button>
              <input type="number" id="cfg-nb-cages" class="form-control text-center fw-bold fs-4" value="15" min="0" required oninput="calcCfgPanneaux()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCfgCages(1)">+</button>
            </div>
            <div class="p-2 mt-2 rounded bg-light text-center fw-bold" style="border: 1px solid #e4e4e7;">
              Total : <span class="fs-5 text-primary" id="cfg-calc-panneaux">315</span> panneaux (21 panneaux &times; cages)
            </div>
          </div>

          <div class="mb-2">
            <label class="form-label fw-bold small text-uppercase text-muted">Emplacement dans la cour</label>
            <input type="text" id="cfg-emplacement" class="form-control" placeholder="Ex: Cour A, Rack 1">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-orange px-4 fw-bold">
            Enregistrer ce lot de cages
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL G : NOUVELLE SECTION D'INVENTAIRE ───────────────── -->
<div class="modal fade" id="modalNouvelleSection" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase" style="letter-spacing: 0.05em;">
          Créer une Section d'inventaire
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitNouvelleSection(event)">
        <input type="hidden" id="edit-section-id" value="">
        <div class="modal-body p-3 p-md-4">
          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nom de la section *</label>
            <input type="text" id="sec-nom" class="form-control form-control-lg" required 
                   placeholder="Ex: Quincaillerie, Étais, Poutrelles H20, Consommables…">
          </div>
          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Description (optionnelle)</label>
            <input type="text" id="sec-desc" class="form-control" 
                   placeholder="Ex: Tirants, écrous papillon, coins de serrage…">
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-orange px-4 fw-bold" id="btn-save-section">
            Créer la section
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── MODAL H : IMPORTATION BACKUP JSON ───────────────────── -->
<div class="modal fade" id="modalImportBackup" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase">
          Restaurer une sauvegarde d'inventaire
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body p-4">
        <p class="small text-muted mb-3">
          Sélectionnez un fichier de sauvegarde <code>.json</code> exporté précédemment depuis l'application Gestion MT.
        </p>
        <div class="mb-3">
          <input type="file" id="backup-file-input" class="form-control" accept=".json">
        </div>
        <div class="alert alert-warning small fw-bold mb-0">
          <i class="bi bi-exclamation-triangle-fill me-1"></i> La restauration mettra à jour votre base locale avec les données du fichier.
        </div>
      </div>
      <div class="modal-footer p-3 bg-light">
        <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
        <button type="button" class="btn btn-orange px-4 fw-bold" onclick="processImportFile()">
          Restaurer maintenant
        </button>
      </div>
    </div>
  </div>
</div>

<!-- ── MODAL I : CONFIGURATION CAPACITÉ GLOBALE DES CAGES ──── -->
<div class="modal fade" id="modalCapaciteCageGlobale" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg" style="background-color: var(--blanc); color: var(--noir-pur);">
      <div class="modal-header" style="background-color: var(--noir-pur); color: var(--blanc); border-bottom: 2px solid var(--orange);">
        <h5 class="modal-title fs-6 fw-bold text-uppercase">
          <i class="bi bi-gear-fill text-warning me-2"></i> Capacité des Cages de Panneaux
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <form onsubmit="submitConfigCapaciteGlobale(event)">
        <div class="modal-body p-4">
          <p class="small text-muted mb-3">
            Définissez le nombre de panneaux contenus par défaut dans une cage pour le calcul automatique de votre inventaire.
          </p>
          <div class="mb-3">
            <label class="form-label fw-bold small text-uppercase text-muted">Nombre de panneaux par cage (standard) *</label>
            <div class="input-group input-group-lg">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCapaciteGlobale(-1)">−</button>
              <input type="number" id="cfg-capacite-globale-input" class="form-control text-center fw-bold fs-3 text-primary" value="21" min="1" max="150" required oninput="updateCapacitePreviewTxt()">
              <button type="button" class="btn btn-outline-secondary btn-stepper" onclick="stepCapaciteGlobale(1)">+</button>
            </div>
            <div class="form-text small mt-2">
              Chaque cage sera calculée sur cette base (1 cage = <span id="cfg-capacite-preview-txt" class="fw-bold text-primary">21</span> panneaux).
            </div>
          </div>
          <div class="form-check p-3 rounded-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
            <input class="form-check-input ms-0 me-2" type="checkbox" id="cfg-apply-all-checkbox" checked>
            <label class="form-check-label small fw-bold" for="cfg-apply-all-checkbox">
              Mettre à jour tous les panneaux existants avec cette nouvelle capacité
            </label>
          </div>
        </div>
        <div class="modal-footer p-3 bg-light">
          <button type="button" class="btn btn-outline-secondary px-3" data-bs-dismiss="modal">Annuler</button>
          <button type="submit" class="btn btn-orange px-4 fw-bold">
            Enregistrer la capacité
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ── FOOTER OFFICIEL EXIGÉ : créé par Ô ───────────────────── -->
<footer class="text-center py-4 small" style="color: #71717a; border-top: 1px solid var(--gris-bordure);">
  créé par Ô
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dexie@4.0.11/dist/dexie.min.js"></script>

<script>
/* ================================================================
   BASE DE DONNÉES LOCALE INDEXEDDB (v7 PRÊTE À L'EMPLOI)
   ================================================================ */
const db = new Dexie("GestionMTCoffrage_DB_v7");
db.version(1).stores({
  sections:   "++id, nom",
  types:      "++id, nom",
  articles:   "++id, section_id, type_id, couleur, etat, chantier_actuel, client_location",
  mouvements: "++id, article_id, type_mouvement, date_mouvement, chantier, client",
  locations:  "++id, article_id, client, date_debut, statut"
});

/* ================================================================
   GESTION DYNAMIQUE DU NOMBRE DE PANNEAUX PAR CAGE
   ================================================================ */
function getGlobalPanneauxParCage() {
  return parseInt(localStorage.getItem("MT_PANNEAUX_PAR_CAGE")) || 21;
}

function setGlobalPanneauxParCage(val) {
  const num = parseInt(val) || 21;
  localStorage.setItem("MT_PANNEAUX_PAR_CAGE", num);
  PANNEAUX_PAR_CAGE = num;
  return num;
}

// Variable globale — initialisée depuis localStorage, mise à jour par setGlobalPanneauxParCage()
let PANNEAUX_PAR_CAGE = getGlobalPanneauxParCage();

function getCapaciteCage(article) {
  if (article && article.panneaux_par_cage && parseInt(article.panneaux_par_cage) > 0) {
    return parseInt(article.panneaux_par_cage);
  }
  return getGlobalPanneauxParCage();
}

function openModalCapaciteCageGlobale() {
  const current = getGlobalPanneauxParCage();
  document.getElementById("cfg-capacite-globale-input").value = current;
  updateCapacitePreviewTxt();
  new bootstrap.Modal(document.getElementById("modalCapaciteCageGlobale")).show();
}

function stepCapaciteGlobale(delta) {
  const el = document.getElementById("cfg-capacite-globale-input");
  let v = (parseInt(el.value) || 21) + delta;
  if (v < 1) v = 1;
  el.value = v;
  updateCapacitePreviewTxt();
}

function updateCapacitePreviewTxt() {
  const v = document.getElementById("cfg-capacite-globale-input").value || 21;
  document.getElementById("cfg-capacite-preview-txt").textContent = v;
}

async function submitConfigCapaciteGlobale(e) {
  e.preventDefault();
  const val = parseInt(document.getElementById("cfg-capacite-globale-input").value) || 21;
  setGlobalPanneauxParCage(val);

  const applyAll = document.getElementById("cfg-apply-all-checkbox").checked;
  if (applyAll) {
    const types = await db.types.toArray();
    const typePanneau = types.find(t => t.nom === "Panneau de coffrage");
    if (typePanneau) {
      const articles = await db.articles.where("type_id").equals(typePanneau.id).toArray();
      for (const a of articles) {
        await db.articles.update(a.id, { panneaux_par_cage: val });
      }
    }
  }

  bootstrap.Modal.getInstance(document.getElementById("modalCapaciteCageGlobale"))?.hide();
  flash(`Capacité des cages mise à jour : ${val} panneaux par cage.`, "success");
  // Re-render all relevant pages so displays update immediately
  if (currentPage === "cages") renderCages();
  else if (currentPage === "location") renderLocation();
  else if (currentPage === "database") renderDatabase();
  else if (currentPage === "inventory") renderInventory();
  else navigateTo(currentPage); // force refresh for any other page
}

function stepAjustCapaciteArticle(delta) {
  const el = document.getElementById("ajust-panneaux-par-cage");
  let v = (parseInt(el.value) || 21) + delta;
  if (v < 1) v = 1;
  el.value = v;
  onAjustCapaciteChanged();
}

function onAjustCapaciteChanged() {
  const cap = parseInt(document.getElementById("ajust-panneaux-par-cage").value) || 21;
  calcAjustementFromTotal();
}

function stepCfgCapaciteCage(delta) {
  const el = document.getElementById("cfg-panneaux-par-cage");
  let v = (parseInt(el.value) || 21) + delta;
  if (v < 1) v = 1;
  el.value = v;
  calcCfgPanneaux();
}


const COULEUR_HEX = {
  "Rose":   "#ec4899",
  "Vert":   "#16a34a",
  "Bleu":   "#2563eb",
  "Rouge":  "#dc2626",
  "Blanc":  "#e4e4e7",
  "Jaune":  "#eab308",
  "Orange": "#ff6200",
  "Noir":   "#0a0a0c"
};

const SECTIONS_CATALOGUE = [
  { nom: "Coffrage & Panneaux (Cages)", description: "Panneaux métalliques calculés en cages de 21, fillers et cages de coin" },
  { nom: "Étaiement & Poutrelles", description: "Étais télescopiques réglables, trépieds, fourches et poutrelles H20" },
  { nom: "Quincaillerie & Attaches", description: "Tirants (tie-rods), écrous papillon, coins de serrage, verrous et barres" },
  { nom: "Sécurité & Outillage", description: "Potelets de garde-corps, passerelles de bétonnage, échelles d'accès chantier" }
];

const TYPES_CATALOGUE = [
  {
    nom: "Panneau de coffrage",
    description: "Panneaux métalliques calculés en cages de 21 panneaux",
    champs: [
      { nom: "Grandeur", type: "select", options: ["2 pieds", "4 pieds", "5 pieds", "7 pieds", "8 pieds", "10 pieds"], requis: true },
      { nom: "Couleur", type: "select", options: ["Rose", "Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Orange", "Noir"], requis: true }
    ]
  },
  {
    nom: "Filler",
    description: "Pièces de remplissage de coffrage",
    champs: [
      { nom: "Largeur", type: "select", options: ["1 po", "2 po", "3 po", "4 po", "6 po", "8 po"], requis: true },
      { nom: "Hauteur", type: "select", options: ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], requis: true }
    ]
  },
  {
    nom: "Cage de coin",
    description: "Cages d'angle intérieur et extérieur",
    champs: [
      { nom: "Type de coin", type: "select", options: ["Coin intérieur", "Coin extérieur"], requis: true },
      { nom: "Hauteur", type: "select", options: ["4 pieds", "5 pieds", "8 pieds", "10 pieds"], requis: true }
    ]
  },
  {
    nom: "Cage de braise",
    description: "Cages de braise et maintien",
    champs: [{ nom: "Modèle", type: "text", options: [], requis: true }]
  },
  {
    nom: "Étais",
    description: "Étais métalliques télescopiques",
    champs: [
      { nom: "Plage de hauteur", type: "select", options: ["1.50m - 2.50m", "2.00m - 3.50m", "2.50m - 4.00m", "3.00m - 5.00m"], requis: true }
    ]
  },
  {
    nom: "Poutrelles",
    description: "Poutrelles H20 et profilés",
    champs: [
      { nom: "Type", type: "select", options: ["H20 Bois", "Aluminium"], requis: true },
      { nom: "Longueur", type: "select", options: ["2.45 m", "2.90 m", "3.90 m", "4.90 m"], requis: true }
    ]
  },
  {
    nom: "Quincaillerie",
    description: "Tirants, écrous et pièces d'assemblage",
    champs: [{ nom: "Dimension", type: "text", options: [], requis: false }]
  },
  {
    nom: "Sécurité & Chantier",
    description: "Garde-corps, passerelles et échelles",
    champs: [{ nom: "Type", type: "text", options: [], requis: false }]
  }
];

/* ── CHARGEMENT DE LA BASE MODÈLE COMPLÈTE (42 ARTICLES) ───── */
async function loadReadyToUseCatalogue(forceReset = false) {
  if (forceReset) {
    await db.articles.clear();
    await db.mouvements.clear();
    await db.types.clear();
    await db.sections.clear();
  }

  const countSec = await db.sections.count();
  if (countSec === 0) {
    await db.sections.bulkAdd(SECTIONS_CATALOGUE);
  }

  const countTypes = await db.types.count();
  if (countTypes === 0) {
    await db.types.bulkAdd(TYPES_CATALOGUE);
  }

  const artCount = await db.articles.count();
  if (artCount === 0) {
    const sections = await db.sections.toArray();
    const types = await db.types.toArray();

    const secCoffrage = sections.find(s => s.nom.includes("Coffrage"))?.id || sections[0].id;
    const secEtais = sections.find(s => s.nom.includes("Étaiement"))?.id || sections[1].id;
    const secQuinc = sections.find(s => s.nom.includes("Quincaillerie"))?.id || sections[2].id;
    const secSecu = sections.find(s => s.nom.includes("Sécurité"))?.id || sections[3].id;

    const tPanneau = types.find(t => t.nom === "Panneau de coffrage")?.id || 1;
    const tFiller = types.find(t => t.nom === "Filler")?.id || 2;
    const tCoin = types.find(t => t.nom === "Cage de coin")?.id || 3;
    const tEtais = types.find(t => t.nom === "Étais")?.id || 5;
    const tPoutre = types.find(t => t.nom === "Poutrelles")?.id || 6;
    const tQuinc = types.find(t => t.nom === "Quincaillerie")?.id || 7;
    const tSecu = types.find(t => t.nom.includes("Sécurité"))?.id || 8;

    const now = Date.now();

    // 1. PANNEAUX DE COFFRAGE (1 CAGE = 21 PANNEAUX)
    const PANNEAUX_PRESETS = [
      // 10 pieds
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Rose", tot: 20, chant: 5, loc: 3, chantNom: "Chantier Tour Horizon", client: "Coffrage Boréal", emp: "Cour A - Rack 1" },
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Bleu", tot: 16, chant: 4, loc: 0, chantNom: "Complexe Desjardins", client: "", emp: "Cour A - Rack 2" },
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Vert", tot: 14, chant: 3, loc: 2, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Cour A - Rack 3" },
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Blanc", tot: 10, chant: 2, loc: 1, chantNom: "Hôpital St-Luc", client: "Groupe BTP Québec", emp: "Cour A - Rack 4" },
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Orange", tot: 8, chant: 2, loc: 0, chantNom: "Hangar 5", client: "", emp: "Cour A - Rack 5" },
      { dim: "Panneau 10 pieds", gr: "10 pieds", clr: "Jaune", tot: 6, chant: 0, loc: 0, chantNom: "", client: "", emp: "Cour A - Rack 6" },
      // 8 pieds
      { dim: "Panneau 8 pieds", gr: "8 pieds", clr: "Vert", tot: 25, chant: 8, loc: 4, chantNom: "Chantier Pont Champlain", client: "Construction Apex", emp: "Cour B - Rack 1" },
      { dim: "Panneau 8 pieds", gr: "8 pieds", clr: "Rose", tot: 18, chant: 4, loc: 2, chantNom: "Tour Bell", client: "Coffrages Modernes Inc.", emp: "Cour B - Rack 2" },
      { dim: "Panneau 8 pieds", gr: "8 pieds", clr: "Rouge", tot: 15, chant: 3, loc: 0, chantNom: "Centre Logistique Dorval", client: "", emp: "Cour B - Rack 3" },
      { dim: "Panneau 8 pieds", gr: "8 pieds", clr: "Bleu", tot: 12, chant: 2, loc: 1, chantNom: "Résidence St-Laurent", client: "BTP Prestige", emp: "Cour B - Rack 4" },
      { dim: "Panneau 8 pieds", gr: "8 pieds", clr: "Noir", tot: 8, chant: 0, loc: 0, chantNom: "", client: "", emp: "Cour B - Rack 5" },
      // 7 pieds
      { dim: "Panneau 7 pieds", gr: "7 pieds", clr: "Orange", tot: 12, chant: 3, loc: 2, chantNom: "Hangar 5", client: "Groupe BTP Québec", emp: "Cour B - Rack 6" },
      { dim: "Panneau 7 pieds", gr: "7 pieds", clr: "Blanc", tot: 10, chant: 2, loc: 0, chantNom: "Tour Bell", client: "", emp: "Cour B - Rack 7" },
      // 5 pieds
      { dim: "Panneau 5 pieds", gr: "5 pieds", clr: "Jaune", tot: 10, chant: 2, loc: 1, chantNom: "Pont Champlain", client: "Coffrage Boréal", emp: "Cour C - Rack 1" },
      { dim: "Panneau 5 pieds", gr: "5 pieds", clr: "Bleu", tot: 8, chant: 1, loc: 0, chantNom: "Tour Horizon", client: "", emp: "Cour C - Rack 2" },
      // 4 pieds
      { dim: "Panneau 4 pieds", gr: "4 pieds", clr: "Rouge", tot: 10, chant: 2, loc: 0, chantNom: "Résidence St-Laurent", client: "", emp: "Cour C - Rack 3" },
      { dim: "Panneau 4 pieds", gr: "4 pieds", clr: "Vert", tot: 8, chant: 1, loc: 1, chantNom: "Tour Bell", client: "Construction Apex", emp: "Cour C - Rack 4" },
      // 2 pieds
      { dim: "Panneau 2 pieds", gr: "2 pieds", clr: "Blanc", tot: 6, chant: 1, loc: 0, chantNom: "Complexe Desjardins", client: "", emp: "Cour C - Rack 5" },
      { dim: "Panneau 2 pieds", gr: "2 pieds", clr: "Noir", tot: 6, chant: 0, loc: 0, chantNom: "", client: "", emp: "Cour C - Rack 6" }
    ];

    for (const p of PANNEAUX_PRESETS) {
      const totP = p.tot * PANNEAUX_PAR_CAGE;
      const chantP = p.chant * PANNEAUX_PAR_CAGE;
      const locP = p.loc * PANNEAUX_PAR_CAGE;

      const artId = await db.articles.add({
        section_id: secCoffrage,
        type_id: tPanneau,
        dimension_modele: p.dim,
        couleur: p.clr,
        quantite_totale: totP,
        quantite_en_chantier: chantP,
        quantite_en_location: locP,
        quantite_en_reparation: 0,
        seuil_alerte: 2 * PANNEAUX_PAR_CAGE,
        chantier_actuel: p.chantNom,
        client_location: p.client,
        etat: "Bon",
        emplacement: p.emp,
        panneaux_par_cage: getGlobalPanneauxParCage(),
        champs_valeurs: { "Grandeur": p.gr, "Couleur": p.clr }
      });

      if (p.chant > 0) {
        await db.mouvements.add({
          article_id: artId,
          type_mouvement: "Sortie chantier",
          quantite: chantP,
          chantier: p.chantNom,
          client: "",
          note: `${p.chant} cages (${chantP} panneaux) envoyées au ${p.chantNom}`,
          date_mouvement: new Date(now - 172800000).toISOString()
        });
      }

      if (p.loc > 0) {
        await db.mouvements.add({
          article_id: artId,
          type_mouvement: "Sortie location",
          quantite: locP,
          chantier: "",
          client: p.client,
          note: `Location de ${p.loc} cages (${locP} panneaux) à ${p.client}`,
          date_mouvement: new Date(now - 86400000).toISOString()
        });
      }
    }

    // 2. FILLERS
    const FILLERS = [
      { dim: "Filler 2 po x 8 pieds", tot: 60, chant: 20, loc: 0, chantNom: "Tour Horizon", emp: "Cour D - Rack 1" },
      { dim: "Filler 4 po x 8 pieds", tot: 50, chant: 15, loc: 5, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Cour D - Rack 1" },
      { dim: "Filler 6 po x 8 pieds", tot: 40, chant: 10, loc: 0, chantNom: "Tour Bell", emp: "Cour D - Rack 1" },
      { dim: "Filler 2 po x 10 pieds", tot: 40, chant: 12, loc: 4, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Cour D - Rack 2" },
      { dim: "Filler 4 po x 10 pieds", tot: 35, chant: 10, loc: 0, chantNom: "Complexe Desjardins", emp: "Cour D - Rack 2" }
    ];
    for (const f of FILLERS) {
      await db.articles.add({
        section_id: secCoffrage,
        type_id: tFiller,
        dimension_modele: f.dim,
        couleur: "",
        quantite_totale: f.tot,
        quantite_en_chantier: f.chant,
        quantite_en_location: f.loc || 0,
        quantite_en_reparation: 0,
        seuil_alerte: 10,
        chantier_actuel: f.chantNom || "",
        client_location: f.client || "",
        etat: "Bon",
        emplacement: f.emp,
        champs_valeurs: {}
      });
    }

    // 3. CAGES DE COIN
    const COINS = [
      { dim: "Coin intérieur 8 pieds", tot: 24, chant: 8, loc: 2, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Cour D - Rack 3" },
      { dim: "Coin extérieur 8 pieds", tot: 20, chant: 6, loc: 2, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Cour D - Rack 3" },
      { dim: "Coin intérieur 10 pieds", tot: 18, chant: 6, loc: 3, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Cour D - Rack 4" },
      { dim: "Coin extérieur 10 pieds", tot: 16, chant: 4, loc: 2, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Cour D - Rack 4" }
    ];
    for (const c of COINS) {
      await db.articles.add({
        section_id: secCoffrage,
        type_id: tCoin,
        dimension_modele: c.dim,
        couleur: "",
        quantite_totale: c.tot,
        quantite_en_chantier: c.chant,
        quantite_en_location: c.loc,
        quantite_en_reparation: 0,
        seuil_alerte: 4,
        chantier_actuel: c.chantNom,
        client_location: c.client,
        etat: "Bon",
        emplacement: c.emp,
        champs_valeurs: {}
      });
    }

    // 4. ÉTAIS
    const ETAIS = [
      { dim: "Étai télescopique 2.00m - 3.50m", tot: 200, chant: 70, loc: 30, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Râtelier Étais 1" },
      { dim: "Étai télescopique 2.50m - 4.00m", tot: 150, chant: 50, loc: 20, chantNom: "Complexe Desjardins", client: "Groupe BTP Québec", emp: "Râtelier Étais 2" },
      { dim: "Étai haute capacité 3.00m - 5.00m", tot: 80, chant: 30, loc: 10, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Râtelier Étais 3" }
    ];
    for (const et of ETAIS) {
      await db.articles.add({
        section_id: secEtais,
        type_id: tEtais,
        dimension_modele: et.dim,
        couleur: "",
        quantite_totale: et.tot,
        quantite_en_chantier: et.chant,
        quantite_en_location: et.loc,
        quantite_en_reparation: 0,
        seuil_alerte: 25,
        chantier_actuel: et.chantNom,
        client_location: et.client,
        etat: "Bon",
        emplacement: et.emp,
        champs_valeurs: {}
      });
    }

    // 5. POUTRELLES H20
    const POUTRES = [
      { dim: "Poutrelle H20 Bois 2.90m", tot: 120, chant: 40, loc: 20, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Allée P1" },
      { dim: "Poutrelle H20 Bois 3.90m", tot: 100, chant: 35, loc: 15, chantNom: "Complexe Desjardins", client: "Construction Apex", emp: "Allée P2" },
      { dim: "Poutrelle H20 Bois 4.90m", tot: 80, chant: 25, loc: 10, chantNom: "Pont Champlain", client: "Groupe BTP Québec", emp: "Allée P3" }
    ];
    for (const pt of POUTRES) {
      await db.articles.add({
        section_id: secEtais,
        type_id: tPoutre,
        dimension_modele: pt.dim,
        couleur: "",
        quantite_totale: pt.tot,
        quantite_en_chantier: pt.chant,
        quantite_en_location: pt.loc,
        quantite_en_reparation: 0,
        seuil_alerte: 20,
        chantier_actuel: pt.chantNom,
        client_location: pt.client,
        etat: "Bon",
        emplacement: pt.emp,
        champs_valeurs: {}
      });
    }

    // 6. QUINCAILLERIE & ATTACHES
    const QUINCS = [
      { dim: "Tirants (Tie-rods) 24 po", tot: 800, chant: 250, loc: 100, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Bac Q1" },
      { dim: "Tirants (Tie-rods) 36 po", tot: 400, chant: 120, loc: 50, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Bac Q2" },
      { dim: "Écrous papillon (Wing nuts) 15mm", tot: 1200, chant: 400, loc: 150, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Bac Q3" },
      { dim: "Coins de serrage (Wedges)", tot: 1000, chant: 300, loc: 100, chantNom: "Pont Champlain", client: "Groupe BTP Québec", emp: "Bac Q4" },
      { dim: "Clamps d'alignement rapide", tot: 250, chant: 80, loc: 30, chantNom: "Complexe Desjardins", client: "Coffrage Boréal", emp: "Bac Q5" }
    ];
    for (const q of QUINCS) {
      await db.articles.add({
        section_id: secQuinc,
        type_id: tQuinc,
        dimension_modele: q.dim,
        couleur: "",
        quantite_totale: q.tot,
        quantite_en_chantier: q.chant,
        quantite_en_location: q.loc,
        quantite_en_reparation: 0,
        seuil_alerte: 100,
        chantier_actuel: q.chantNom,
        client_location: q.client,
        etat: "Bon",
        emplacement: q.emp,
        champs_valeurs: {}
      });
    }

    // 7. SÉCURITÉ & CHANTIER
    const SECUS = [
      { dim: "Potelets de garde-corps acier", tot: 120, chant: 45, loc: 15, chantNom: "Tour Horizon", client: "Coffrage Boréal", emp: "Zone S1" },
      { dim: "Passerelles de travail bétonnage 2.50m", tot: 30, chant: 10, loc: 4, chantNom: "Pont Champlain", client: "Construction Apex", emp: "Zone S2" },
      { dim: "Échelles d'accès sécurisées aluminium", tot: 20, chant: 8, loc: 2, chantNom: "Complexe Desjardins", client: "Groupe BTP Québec", emp: "Zone S3" }
    ];
    for (const s of SECUS) {
      await db.articles.add({
        section_id: secSecu,
        type_id: tSecu,
        dimension_modele: s.dim,
        couleur: "",
        quantite_totale: s.tot,
        quantite_en_chantier: s.chant,
        quantite_en_location: s.loc,
        quantite_en_reparation: 0,
        seuil_alerte: 5,
        chantier_actuel: s.chantNom,
        client_location: s.client,
        etat: "Bon",
        emplacement: s.emp,
        champs_valeurs: {}
      });
    }
  }
}

/* ================================================================
   UTILITAIRES DE CALCUL & NAVIGATION
   ================================================================ */
const app = () => document.getElementById("app");

function flash(message, category = "success") {
  const container = document.getElementById("flash-container");
  const id = "flash-" + Date.now();
  const bg = category === "success" 
    ? "background-color: #dcfce7; color: #15803d; border: 1.5px solid #bbf7d0;" 
    : "background-color: #fee2e2; color: #b91c1c; border: 1.5px solid #fecaca;";
  container.insertAdjacentHTML("beforeend", `
    <div id="${id}" class="alert alert-dismissible fade show p-3 mb-3 fw-bold small shadow-sm rounded-3" style="${bg}" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `);
  setTimeout(() => { document.getElementById(id)?.remove(); }, 3500);
}

// Règle fondamentale : La cour (disponible) = Totale - Chantier - Location - Réparation
function getDispo(a) {
  const tot = parseInt(a.quantite_totale) || 0;
  const chant = parseInt(a.quantite_en_chantier) || 0;
  const loc = parseInt(a.quantite_en_location) || 0;
  const rep = parseInt(a.quantite_en_reparation) || 0;
  return Math.max(0, tot - chant - loc - rep);
}

function setActiveNav(page) {
  // Desktop navbar links
  document.querySelectorAll(".navbar .nav-link").forEach(el => el.classList.remove("active-page"));
  const navEl = document.getElementById("nav-" + page);
  if (navEl) navEl.classList.add("active-page");

  // Mobile bottom dock buttons
  document.querySelectorAll(".mobile-nav-btn").forEach(el => el.classList.remove("active-page"));
  const mobEl = document.getElementById("mob-" + page);
  if (mobEl) mobEl.classList.add("active-page");
}

let currentPage = "cages";
function navigateTo(page, params = {}) {
  currentPage = page;
  setActiveNav(page);
  window.scrollTo({ top: 0, behavior: "smooth" });
  switch (page) {
    case "cages": renderCages(); break;
    case "location": renderLocation(); break;
    case "sections": renderSections(); break;
    case "dashboard": renderDashboard(); break;
    case "mouvements": renderMouvements(); break;
    case "database": renderDatabase(); break;
    case "types": renderTypes(); break;
    case "article-form": renderArticleForm(params.id, params.sectionId); break;
    case "type-form": renderTypeForm(params.id); break;
  }
}

/* ================================================================
   VUE 1 : GESTION DES CAGES DE PANNEAUX (COUR / CHANTIER / LOCATION)
   ================================================================ */
async function renderCages() {
  const types = await db.types.toArray();
  const typePanneau = types.find(t => t.nom === "Panneau de coffrage");
  let panneauxArticles = [];
  if (typePanneau) {
    panneauxArticles = await db.articles.where("type_id").equals(typePanneau.id).toArray();
  }

  let totalCagesStock = 0;
  let totalCagesDispo = 0;
  let totalCagesChantier = 0;
  let totalCagesLocation = 0;

  let totalPanneauxStock = 0;
  let totalPanneauxDispo = 0;
  let totalPanneauxChantier = 0;
  let totalPanneauxLocation = 0;

  panneauxArticles.forEach(a => {
    const cap = getCapaciteCage(a);
    const tot = parseInt(a.quantite_totale) || 0;
    const disp = getDispo(a);
    const chant = parseInt(a.quantite_en_chantier) || 0;
    const loc = parseInt(a.quantite_en_location) || 0;

    totalPanneauxStock += tot;
    totalPanneauxDispo += disp;
    totalPanneauxChantier += chant;
    totalPanneauxLocation += loc;

    totalCagesStock += Math.floor(tot / cap);
    totalCagesDispo += Math.floor(disp / cap);
    totalCagesChantier += Math.floor(chant / cap);
    totalCagesLocation += Math.floor(loc / cap);
  });

  app().innerHTML = `
    <!-- En-tête Cages Panneaux -->
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4 flex-wrap gap-2">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase" style="letter-spacing: 0.03em;">
          Cages de Panneaux (${PANNEAUX_PAR_CAGE} pcs)
        </h1>
        <span class="small" style="color: #a1a1aa;">
          1 Cage = <strong>${PANNEAUX_PAR_CAGE} Panneaux</strong> &bull; Répartition directe : <strong>Cour</strong> &bull; <strong>Chantier</strong> &bull; <strong>Location</strong>
        </span>
      </div>
      <div class="d-flex gap-2 flex-wrap">
        <button class="btn btn-outline-warning fw-bold px-3 py-2" onclick="openModalCapaciteCageGlobale()" title="Modifier le nombre de panneaux par cage">
          <i class="bi bi-gear-fill me-1"></i> Capacité : ${getGlobalPanneauxParCage()} pcs/cage
        </button>
        <button class="btn btn-outline-orange fw-bold px-3 py-2" onclick="openAjusterModalSansArticle()">
          ⚙️ Ajuster Répartition
        </button>
        <button class="btn btn-orange fw-bold px-3 py-2 shadow-sm" onclick="openNewCageModal()">
          + Configurer Cages
        </button>
      </div>
    </div>

    <!-- 4 Compteurs métriques principaux -->
    <div class="row g-2 g-md-3 mb-3 mb-md-4">
      <div class="col-6 col-lg-3">
        <div class="card-stat">
          <div class="stat-value">${totalCagesStock} <span class="fs-6 fw-normal text-muted">cages</span></div>
          <div class="stat-label">Parc Total (${totalPanneauxStock} panneaux)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--vert-ok);">
          <div class="stat-value text-success">${totalCagesDispo} <span class="fs-6 fw-normal text-muted">cages</span></div>
          <div class="stat-label">Dans la Cour (${totalPanneauxDispo} dispo)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--orange);">
          <div class="stat-value" style="color: var(--orange);">${totalCagesChantier} <span class="fs-6 fw-normal text-muted">cages</span></div>
          <div class="stat-label">Sur Chantiers (${totalPanneauxChantier} panneaux)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--bleu-location);">
          <div class="stat-value text-primary">${totalCagesLocation} <span class="fs-6 fw-normal text-muted">cages</span></div>
          <div class="stat-label">Sur Location (${totalPanneauxLocation} panneaux)</div>
        </div>
      </div>
    </div>

    <!-- Barre de filtres par couleur et grandeur (Tactile au pouce) -->
    <div class="p-2 p-md-3 mb-3 mb-md-4 rounded-3 d-flex flex-wrap gap-2 align-items-center justify-content-between" style="background-color: var(--noir-card); border: 1px solid var(--gris-bordure);">
      <div class="scroll-chips w-100 pb-1">
        <button class="btn btn-sm btn-dark-pro px-3" onclick="filterCagesByColor('')">Toutes les couleurs</button>
        ${["Rose", "Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Orange", "Noir"].map(c => `
          <button class="btn btn-sm" style="background-color: #27272a; color: #fff; border: 1px solid #3f3f46;" onclick="filterCagesByColor('${c}')">
            <span class="d-inline-block rounded-circle me-1" style="width: 10px; height: 10px; background-color: ${COULEUR_HEX[c] || '#fff'};"></span> ${c}
          </button>
        `).join("")}
      </div>
    </div>

    <!-- Grille des Cartes Cages -->
    <div class="row g-3" id="cages-grid">
      ${panneauxArticles.length === 0 ? `
        <div class="col-12">
          <div class="p-5 text-center text-muted bg-dark rounded-3 border border-secondary">
            <h5>Aucune cage enregistrée pour le moment.</h5>
            <p>Chargez le catalogue prêt à l'emploi ou configurez vos premières cages.</p>
            <button class="btn btn-orange fw-bold px-4 py-2 mt-2" onclick="loadReadyToUseCatalogue(true).then(() => renderCages())">
              Recharger la base complète modèle
            </button>
          </div>
        </div>
      ` : panneauxArticles.map(a => {
        const dispoP = getDispo(a);
        const chantP = parseInt(a.quantite_en_chantier) || 0;
        const locP = parseInt(a.quantite_en_location) || 0;
        const totP = parseInt(a.quantite_totale) || 0;

        const cap = getCapaciteCage(a);
        const cagesDispo = Math.floor(dispoP / cap);
        const cagesChantier = Math.floor(chantP / cap);
        const cagesLocation = Math.floor(locP / cap);
        const cagesTotal = Math.floor(totP / cap);

        const hexColor = COULEUR_HEX[a.couleur] || "#ff6200";

        return `
        <div class="col-12 col-md-6 col-lg-4 cage-item-card" data-couleur="${a.couleur || ''}">
          <div class="card-cage h-100 d-flex flex-column justify-content-between">
            <div class="cage-color-stripe" style="background-color: ${hexColor};"></div>

            <div>
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge-cage-color" style="background-color: ${hexColor}; color: ${a.couleur === 'Blanc' || a.couleur === 'Jaune' ? '#000' : '#fff'};">
                  ${a.couleur || 'Standard'}
                </span>
                <span class="badge bg-light text-dark border fw-bold" title="Cliquer pour ajuster" style="cursor: pointer;" onclick="openAjusterRepartitionModal(${a.id})">${cap} pcs / cage</span>
              </div>

              <div class="d-flex justify-content-between align-items-baseline mb-1">
                <h2 class="h5 fw-bold mb-0">${a.dimension_modele}</h2>
                <span class="fs-6 fw-bold text-muted">${cagesTotal} cages tot.</span>
              </div>
              
              <div class="small text-muted mb-3">
                ${a.emplacement ? `Cour : <strong>${a.emplacement}</strong>` : 'Cour principale'}
                &bull; <span class="fw-bold">${totP}</span> panneaux totaux
              </div>

              <!-- Bloc 3 Répartitions : Cour / Chantier / Location -->
              <div class="p-2 rounded-3 mb-3" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
                <!-- 1. Cour -->
                <div class="d-flex justify-content-between align-items-center p-2 rounded mb-1" style="background-color: #ffffff; border-left: 4px solid var(--vert-ok);">
                  <div>
                    <span class="small fw-bold text-success text-uppercase">Dans la cour :</span>
                  </div>
                  <div class="text-end">
                    <span class="fs-4 fw-bold text-success">${cagesDispo}</span>
                    <span class="fw-bold">cages</span>
                    <span class="small text-muted">(${dispoP} pcs)</span>
                  </div>
                </div>

                <!-- 2. Chantier -->
                <div class="d-flex justify-content-between align-items-center p-2 rounded mb-1" style="background-color: #ffffff; border-left: 4px solid var(--orange);">
                  <div>
                    <span class="small fw-bold text-uppercase" style="color: var(--orange);">Sur chantier :</span>
                    ${a.chantier_actuel && cagesChantier > 0 ? `<div class="small text-muted text-truncate" style="max-width: 140px;">${a.chantier_actuel}</div>` : ''}
                  </div>
                  <div class="text-end">
                    <span class="fs-5 fw-bold" style="color: var(--orange);">${cagesChantier}</span>
                    <span class="small fw-bold">cages</span>
                    <span class="small text-muted">(${chantP} pcs)</span>
                  </div>
                </div>

                <!-- 3. Location -->
                <div class="d-flex justify-content-between align-items-center p-2 rounded" style="background-color: #ffffff; border-left: 4px solid var(--bleu-location);">
                  <div>
                    <span class="small fw-bold text-primary text-uppercase">Sur location :</span>
                    ${a.client_location && cagesLocation > 0 ? `<div class="small text-muted text-truncate" style="max-width: 140px;">${a.client_location}</div>` : ''}
                  </div>
                  <div class="text-end">
                    <span class="fs-5 fw-bold text-primary">${cagesLocation}</span>
                    <span class="small fw-bold">cages</span>
                    <span class="small text-muted">(${locP} pcs)</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Actions Rapides -->
            <div class="d-flex flex-column gap-2 pt-2 border-top">
              <button class="btn btn-outline-dark fw-bold py-2 w-100 shadow-sm"
                      onclick="openAjusterRepartitionModal(${a.id})">
                ⚙️ Ajuster Répartition (Cour / Chantier / Location)
              </button>

              <div class="row g-1">
                <div class="col-6">
                  <button class="btn btn-orange btn-sm w-100 fw-bold py-2"
                          onclick="openSortieCageModal(${a.id}, '${a.dimension_modele}', '${a.couleur}', ${cagesDispo}, ${dispoP})">
                    − Chantier
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-primary btn-sm w-100 fw-bold py-2 text-white"
                          onclick="openSortieLocationPourArticle(${a.id})">
                    − Louer
                  </button>
                </div>
              </div>

              <div class="d-flex gap-1 justify-content-between">
                ${cagesChantier > 0 ? `
                  <button class="btn btn-sm btn-outline-warning fw-bold flex-grow-1"
                          onclick="openRetourCageModal(${a.id}, '${a.dimension_modele}', '${a.couleur}', ${cagesChantier}, '${(a.chantier_actuel || '').replace(/'/g, "\\'")}')">
                    + Retour Chantier (${cagesChantier})
                  </button>
                ` : ''}
                ${cagesLocation > 0 ? `
                  <button class="btn btn-sm btn-outline-primary fw-bold flex-grow-1"
                          onclick="openRetourLocationPourArticle(${a.id})">
                    + Retour Location (${cagesLocation})
                  </button>
                ` : ''}
              </div>
            </div>

          </div>
        </div>`;
      }).join("")}
    </div>
  `;
}

function filterCagesByColor(couleur) {
  document.querySelectorAll("#cages-grid .cage-item-card").forEach(el => {
    if (!couleur || el.dataset.couleur === couleur) {
      el.style.display = "";
    } else {
      el.style.display = "none";
    }
  });
}

/* ================================================================
   LOGIQUE MODAL AJUSTEMENT RÉPARTITION
   ================================================================ */
let articleEnAjustement = null;

async function openAjusterModalSansArticle() {
  const types = await db.types.toArray();
  const typePanneau = types.find(t => t.nom === "Panneau de coffrage");
  if (!typePanneau) return;
  const articles = await db.articles.where("type_id").equals(typePanneau.id).toArray();
  if (articles.length === 0) {
    openNewCageModal();
    return;
  }
  const selectBox = document.getElementById("ajust-select-article-box");
  const selectEl = document.getElementById("ajust-article-select");
  selectBox.style.display = "block";
  selectEl.innerHTML = articles.map(a => `<option value="${a.id}">${a.dimension_modele} — ${a.couleur || 'Sans couleur'}</option>`).join("");
  openAjusterRepartitionModal(articles[0].id);
}

async function onArticleSelectChange(articleId) {
  if (articleId) openAjusterRepartitionModal(parseInt(articleId));
}

async function openAjusterRepartitionModal(articleId) {
  const article = await db.articles.get(articleId);
  if (!article) return;
  articleEnAjustement = article;

  document.getElementById("ajust-article-id").value = article.id;
  const capArticle = getCapaciteCage(article);
  document.getElementById("ajust-panneaux-par-cage").value = capArticle;
  document.getElementById("ajust-cage-subtitle").innerHTML = `
    <strong>${article.dimension_modele} — ${article.couleur}</strong> &bull; 1 Cage = <strong>${capArticle} Panneaux</strong>
  `;

  const selectEl = document.getElementById("ajust-article-select");
  if (selectEl) selectEl.value = article.id;

  const totP = parseInt(article.quantite_totale) || 0;
  const chantP = parseInt(article.quantite_en_chantier) || 0;
  const locP = parseInt(article.quantite_en_location) || 0;
  const dispoP = getDispo(article);

  const capArticle = getCapaciteCage(article);
  const cagesTot = Math.floor(totP / capArticle);
  const cagesChant = Math.floor(chantP / capArticle);
  const cagesLoc = Math.floor(locP / capArticle);
  const cagesCour = Math.floor(dispoP / capArticle);

  document.getElementById("ajust-cages-total").value = cagesTot;
  document.getElementById("ajust-panneaux-total").textContent = totP;

  document.getElementById("ajust-cages-cour").value = cagesCour;
  document.getElementById("ajust-panneaux-cour").textContent = dispoP;
  document.getElementById("ajust-emplacement-cour").value = article.emplacement || "";

  document.getElementById("ajust-cages-chantier").value = cagesChant;
  document.getElementById("ajust-panneaux-chantier").textContent = chantP;
  document.getElementById("ajust-nom-chantier").value = article.chantier_actuel || "";

  document.getElementById("ajust-cages-location").value = cagesLoc;
  document.getElementById("ajust-panneaux-location").textContent = locP;
  document.getElementById("ajust-nom-client").value = article.client_location || "";

  document.getElementById("ajust-note").value = "";

  updateBalanceDisplay();
  new bootstrap.Modal(document.getElementById("modalAjusterRepartitionCage")).show();
}

function stepAjustCages(inputId, delta) {
  const el = document.getElementById(inputId);
  let v = (parseInt(el.value) || 0) + delta;
  if (v < 0) v = 0;
  el.value = v;

  if (inputId === "ajust-cages-total") {
    calcAjustementFromTotal();
  } else {
    onRepartitionInputChanged();
  }
}

function calcAjustementFromTotal() {
  const cap = parseInt(document.getElementById("ajust-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  const totCages = parseInt(document.getElementById("ajust-cages-total").value) || 0;
  document.getElementById("ajust-panneaux-total").textContent = totCages * cap;
  
  const chant = parseInt(document.getElementById("ajust-cages-chantier").value) || 0;
  const loc = parseInt(document.getElementById("ajust-cages-location").value) || 0;
  const nouvCour = Math.max(0, totCages - chant - loc);
  document.getElementById("ajust-cages-cour").value = nouvCour;
  
  updateBalanceDisplay();
}

function onRepartitionInputChanged() {
  const cap = parseInt(document.getElementById("ajust-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  const cour = parseInt(document.getElementById("ajust-cages-cour").value) || 0;
  const chant = parseInt(document.getElementById("ajust-cages-chantier").value) || 0;
  const loc = parseInt(document.getElementById("ajust-cages-location").value) || 0;

  document.getElementById("ajust-panneaux-cour").textContent = cour * cap;
  document.getElementById("ajust-panneaux-chantier").textContent = chant * cap;
  document.getElementById("ajust-panneaux-location").textContent = loc * cap;

  updateBalanceDisplay();
}

function updateBalanceDisplay() {
  const total = parseInt(document.getElementById("ajust-cages-total").value) || 0;
  const cour = parseInt(document.getElementById("ajust-cages-cour").value) || 0;
  const chant = parseInt(document.getElementById("ajust-cages-chantier").value) || 0;
  const loc = parseInt(document.getElementById("ajust-cages-location").value) || 0;
  const somme = cour + chant + loc;

  const textEl = document.getElementById("ajust-balance-text");
  const actionsEl = document.getElementById("ajust-balance-actions");
  const boxEl = document.getElementById("ajust-balance-box");

  if (somme === total) {
    boxEl.style.backgroundColor = "#f0fdf4";
    boxEl.style.borderColor = "#bbf7d0";
    textEl.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill me-1"></i> Équilibre : Cour (${cour}) + Chantier (${chant}) + Location (${loc}) = ${total} cages.</span>`;
    actionsEl.innerHTML = "";
  } else {
    boxEl.style.backgroundColor = "#fffbeb";
    boxEl.style.borderColor = "#fef08a";
    const diff = total - somme;
    textEl.innerHTML = `
      <span class="text-warning-emphasis">
        <i class="bi bi-exclamation-triangle-fill me-1"></i> Somme (${somme}) &ne; Total (${total}). Écart : <strong>${diff > 0 ? '+' : ''}${diff} cages</strong>.
      </span>
    `;
    actionsEl.innerHTML = `
      <button type="button" class="btn btn-sm btn-outline-success fw-bold" onclick="autoAjustCour(${Math.max(0, total - chant - loc)})">
        Cour = ${Math.max(0, total - chant - loc)} cages
      </button>
      <button type="button" class="btn btn-sm btn-outline-dark fw-bold" onclick="autoAjustTotal(${somme})">
        Total = ${somme} cages
      </button>
    `;
  }
}

function autoAjustCour(nouvCour) {
  document.getElementById("ajust-cages-cour").value = nouvCour;
  onRepartitionInputChanged();
}

function autoAjustTotal(nouvTot) {
  const cap = parseInt(document.getElementById("ajust-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  document.getElementById("ajust-cages-total").value = nouvTot;
  document.getElementById("ajust-panneaux-total").textContent = nouvTot * cap;
  updateBalanceDisplay();
}

async function submitAjusterRepartition(e) {
  e.preventDefault();
  const articleId = parseInt(document.getElementById("ajust-article-id").value);
  const cap = parseInt(document.getElementById("ajust-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  const totalCages = parseInt(document.getElementById("ajust-cages-total").value) || 0;
  const courCages = parseInt(document.getElementById("ajust-cages-cour").value) || 0;
  const chantCages = parseInt(document.getElementById("ajust-cages-chantier").value) || 0;
  const locCages = parseInt(document.getElementById("ajust-cages-location").value) || 0;

  const totalPanneaux = totalCages * cap;
  const chantPanneaux = chantCages * cap;
  const locPanneaux = locCages * cap;

  const nomChantier = document.getElementById("ajust-nom-chantier").value.trim();
  const nomClient = document.getElementById("ajust-nom-client").value.trim();
  const emplacementCour = document.getElementById("ajust-emplacement-cour").value.trim();
  const note = document.getElementById("ajust-note").value.trim();

  await db.articles.update(articleId, {
    panneaux_par_cage: cap,
    quantite_totale: totalPanneaux,
    quantite_en_chantier: chantPanneaux,
    quantite_en_location: locPanneaux,
    chantier_actuel: chantCages > 0 ? nomChantier : "",
    client_location: locCages > 0 ? nomClient : "",
    emplacement: emplacementCour
  });

  await db.mouvements.add({
    article_id: articleId,
    type_mouvement: "Ajustement répartition",
    quantite: totalPanneaux,
    chantier: nomChantier,
    client: nomClient,
    note: `Répartition mise à jour : Cour ${courCages} c. (${courCages*21}p), Chantier ${chantCages} c. (${chantPanneaux}p), Location ${locCages} c. (${locPanneaux}p)${note ? ' - ' + note : ''}`,
    date_mouvement: new Date().toISOString()
  });

  bootstrap.Modal.getInstance(document.getElementById("modalAjusterRepartitionCage"))?.hide();
  flash(`Répartition enregistrée : ${totalCages} cages à ${cap} pcs/cage (Cour: ${courCages}, Chantier: ${chantCages}, Location: ${locCages})`, "success");
  if (currentPage === "cages") renderCages();
  else if (currentPage === "location") renderLocation();
  else if (currentPage === "sections") renderSections();
  else renderDashboard();
}

/* ================================================================
   VUE 2 : SECTION LOCATION DE MATÉRIEL
   ================================================================ */
async function renderLocation() {
  const articles = await db.articles.toArray();
  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);

  const articlesEnLocation = articles.filter(a => (parseInt(a.quantite_en_location) || 0) > 0);

  let totalCagesLoc = 0;
  let totalPanneauxLoc = 0;
  let totalAutresItemsLoc = 0;
  const clientsUniques = new Set();

  articles.forEach(a => {
    const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
    const loc = parseInt(a.quantite_en_location) || 0;
    if (loc > 0) {
      if (a.client_location) clientsUniques.add(a.client_location);
      if (isPanneau) {
        totalPanneauxLoc += loc;
        totalCagesLoc += Math.floor(loc / PANNEAUX_PAR_CAGE);
      } else {
        totalAutresItemsLoc += loc;
      }
    }
  });

  const mvtsLoc = await db.mouvements.where("type_mouvement").equals("Sortie location")
    .or("type_mouvement").equals("Retour location")
    .reverse().sortBy("date_mouvement");

  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4 flex-wrap gap-2">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase" style="letter-spacing: 0.03em;">
          Section Location de Matériel
        </h1>
        <span class="small" style="color: #a1a1aa;">
          Suivi des cages de coffrage et matériels loués &bull; Gestion des contrats et retours
        </span>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-orange fw-bold px-3 py-2" onclick="navigateTo('cages')">
          &larr; Vue Cages
        </button>
        <button class="btn btn-primary fw-bold px-3 py-2 shadow-sm text-white" onclick="openSortieLocationModal()">
          + Sortie Location
        </button>
      </div>
    </div>

    <!-- Compteurs Location -->
    <div class="row g-2 g-md-3 mb-3 mb-md-4">
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--bleu-location);">
          <div class="stat-value text-primary">${totalCagesLoc} <span class="fs-6 fw-normal text-muted">cages</span></div>
          <div class="stat-label">Cages Louées (${totalPanneauxLoc} pcs)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat">
          <div class="stat-value">${totalAutresItemsLoc} <span class="fs-6 fw-normal text-muted">unités</span></div>
          <div class="stat-label">Autres matériels loués (étais, attaches...)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--orange);">
          <div class="stat-value" style="color: var(--orange);">${clientsUniques.size}</div>
          <div class="stat-label">Clients locataires actifs</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--vert-ok);">
          <div class="stat-value text-success">${articlesEnLocation.length}</div>
          <div class="stat-label">Contrats / Lignes actives</div>
        </div>
      </div>
    </div>

    <!-- Cartes Mobile / Tableau Desktop -->
    <div class="card-custom mb-4 overflow-hidden shadow-sm">
      <div class="p-3 bg-dark text-white d-flex justify-content-between align-items-center" style="border-bottom: 2px solid var(--bleu-location);">
        <h2 class="h6 mb-0 fw-bold text-uppercase" style="letter-spacing: 0.04em;">
          <i class="bi bi-box-arrow-right me-1 text-info"></i> Matériels actuellement en location
        </h2>
        <span class="badge bg-primary text-white">${articlesEnLocation.length} contrat(s)</span>
      </div>

      <!-- Version Mobile : Cartes tactiles -->
      <div class="d-md-none p-2">
        ${articlesEnLocation.length === 0 ? `
          <div class="text-center py-4 text-muted">
            <p>Aucun équipement en location.</p>
            <button class="btn btn-primary btn-sm fw-bold text-white" onclick="openSortieLocationModal()">+ Louer du matériel</button>
          </div>
        ` : articlesEnLocation.map(a => {
          const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
          const qLoc = parseInt(a.quantite_en_location) || 0;
          const cagesLoc = isPanneau ? Math.floor(qLoc / PANNEAUX_PAR_CAGE) : qLoc;
          return `
          <div class="mobile-item-card">
            <div class="d-flex justify-content-between align-items-center mb-1">
              <strong class="fs-6 text-dark">${a.client_location || 'Client'}</strong>
              <span class="badge bg-primary text-white">${isPanneau ? cagesLoc + ' cages' : qLoc + ' unités'}</span>
            </div>
            <div class="fw-bold">${a.dimension_modele} ${a.couleur ? '— ' + a.couleur : ''}</div>
            <div class="small text-muted mb-2">${isPanneau ? `(${qLoc} panneaux au total)` : ''} &bull; Emplacement : ${a.emplacement || 'Cour'}</div>
            <div class="d-flex gap-2">
              <button class="btn btn-sm btn-success fw-bold flex-grow-1 py-2" onclick="openRetourLocationPourArticle(${a.id})">
                + Retour en cour
              </button>
              <button class="btn btn-sm btn-outline-dark fw-bold px-3 py-2" onclick="openAjusterRepartitionModal(${a.id})">
                ⚙️
              </button>
            </div>
          </div>`;
        }).join("")}
      </div>

      <!-- Version Desktop : Tableau complet -->
      <div class="table-responsive d-none d-md-block">
        <table class="table-pro">
          <thead>
            <tr>
              <th>Client / Entreprise</th>
              <th>Matériel & Spécification</th>
              <th>Type</th>
              <th>Couleur</th>
              <th class="text-center">Cages louées</th>
              <th class="text-center">Quantité totale</th>
              <th>Origine</th>
              <th class="text-end">Actions rapides</th>
            </tr>
          </thead>
          <tbody>
            ${articlesEnLocation.length === 0 ? `
              <tr>
                <td colspan="8" class="text-center py-5 text-muted">
                  <h5>Aucun équipement n'est actuellement en location.</h5>
                  <button class="btn btn-primary btn-sm fw-bold px-3 py-2 mt-2 text-white" onclick="openSortieLocationModal()">
                    + Enregistrer une sortie en location
                  </button>
                </td>
              </tr>
            ` : articlesEnLocation.map(a => {
              const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
              const qLoc = parseInt(a.quantite_en_location) || 0;
              const cagesLoc = isPanneau ? Math.floor(qLoc / PANNEAUX_PAR_CAGE) : '—';
              return `
              <tr>
                <td><strong class="text-dark">${a.client_location || 'Client non spécifié'}</strong></td>
                <td class="fw-bold">${a.dimension_modele}</td>
                <td><span class="badge bg-dark text-white fw-bold">${typeMap[a.type_id] || 'Standard'}</span></td>
                <td>${a.couleur ? `<span class="badge bg-light text-dark border">${a.couleur}</span>` : '<span class="text-muted">—</span>'}</td>
                <td class="text-center">${isPanneau ? `<span class="fs-5 fw-bold text-primary">${cagesLoc}</span> <span class="small fw-bold">cages</span>` : '—'}</td>
                <td class="text-center"><span class="fs-5 fw-bold text-primary">${qLoc}</span> <span class="small text-muted">pcs</span></td>
                <td>${a.emplacement || 'Cour principale'}</td>
                <td class="text-end text-nowrap">
                  <button class="btn btn-sm btn-success fw-bold px-3 py-1 me-1 shadow-sm" onclick="openRetourLocationPourArticle(${a.id})">
                    + Retour en cour
                  </button>
                  <button class="btn btn-sm btn-outline-dark fw-bold px-2 py-1" onclick="openAjusterRepartitionModal(${a.id})">
                    ⚙️
                  </button>
                </td>
              </tr>`;
            }).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

/* ================================================================
   LOGIQUE MODAL SORTIE EN LOCATION & RETOUR DE LOCATION
   ================================================================ */
async function openSortieLocationModal() {
  const articles = await db.articles.toArray();
  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);

  const selectEl = document.getElementById("loc-article-select");
  selectEl.innerHTML = articles.map(a => {
    const dispo = getDispo(a);
    const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
    const cagesTxt = isPanneau ? ` (${Math.floor(dispo / PANNEAUX_PAR_CAGE)} cages dispo)` : ` (${dispo} dispo)`;
    return `<option value="${a.id}">${a.dimension_modele} ${a.couleur ? '— ' + a.couleur : ''}${cagesTxt}</option>`;
  }).join("");

  document.getElementById("loc-select-article-container").style.display = "block";
  document.getElementById("loc-date-debut").value = new Date().toISOString().split("T")[0];
  document.getElementById("loc-date-fin").value = "";
  document.getElementById("loc-client-nom").value = "";
  document.getElementById("loc-note").value = "";

  if (articles.length > 0) {
    onLocArticleChange(articles[0].id);
  }
  new bootstrap.Modal(document.getElementById("modalSortieLocation")).show();
}

async function openSortieLocationPourArticle(articleId) {
  await openSortieLocationModal();
  const selectEl = document.getElementById("loc-article-select");
  selectEl.value = articleId;
  onLocArticleChange(articleId);
}

let locArticleActuel = null;
async function onLocArticleChange(articleId) {
  const a = await db.articles.get(parseInt(articleId));
  if (!a) return;
  locArticleActuel = a;

  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');

  const dispo = getDispo(a);
  const cagesDispo = Math.floor(dispo / PANNEAUX_PAR_CAGE);

  document.getElementById("loc-article-id").value = a.id;
  document.getElementById("loc-info-title").textContent = `${a.dimension_modele} ${a.couleur ? '— ' + a.couleur : ''}`;
  
  if (isPanneau) {
    document.getElementById("loc-dispo-txt").textContent = `${cagesDispo} cage(s) (${dispo} panneaux)`;
    document.getElementById("loc-quantite-label").textContent = "Nombre de Cages à louer *";
    document.getElementById("loc-panneaux-equiv-box").style.display = "block";
    document.getElementById("loc-quantite").value = 1;
    calcPanneauxLocation();
  } else {
    document.getElementById("loc-dispo-txt").textContent = `${dispo} unité(s)`;
    document.getElementById("loc-quantite-label").textContent = "Quantité d'unités à louer *";
    document.getElementById("loc-panneaux-equiv-box").style.display = "none";
    document.getElementById("loc-quantite").value = 1;
  }
}

function stepLocQuantite(delta) {
  const el = document.getElementById("loc-quantite");
  let v = (parseInt(el.value) || 1) + delta;
  if (v < 1) v = 1;
  el.value = v;
  calcPanneauxLocation();
}

function calcPanneauxLocation() {
  const types_isPanneau = locArticleActuel && (locArticleActuel.dimension_modele || '').includes('Panneau');
  const nb = parseInt(document.getElementById("loc-quantite").value) || 0;
  if (types_isPanneau) {
    const cap = getCapaciteCage(locArticleActuel);
    document.getElementById("loc-calc-panneaux").textContent = nb * cap;
  }
}

async function submitSortieLocation(e) {
  e.preventDefault();
  const articleId = parseInt(document.getElementById("loc-article-id").value);
  const article = await db.articles.get(articleId);
  if (!article) return;

  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const isPanneau = (typeMap[article.type_id] || '').includes('Panneau');

  const inputQ = parseInt(document.getElementById("loc-quantite").value) || 1;
  const cap = getCapaciteCage(article);
  const quantitePanneaux = isPanneau ? inputQ * cap : inputQ;
  const dispo = getDispo(article);

  if (quantitePanneaux > dispo) {
    alert(`Stock insuffisant en cour : seulement ${isPanneau ? Math.floor(dispo/21) + ' cage(s)' : dispo + ' unité(s)'} disponibles.`);
    return;
  }

  const client = document.getElementById("loc-client-nom").value.trim();
  const dateDebut = document.getElementById("loc-date-debut").value;
  const note = document.getElementById("loc-note").value.trim();

  const nouvLoc = (parseInt(article.quantite_en_location) || 0) + quantitePanneaux;
  await db.articles.update(articleId, {
    quantite_en_location: nouvLoc,
    client_location: client
  });

  await db.mouvements.add({
    article_id: articleId,
    type_mouvement: "Sortie location",
    quantite: quantitePanneaux,
    client: client,
    note: isPanneau ? `Sortie location de ${inputQ} cage(s) (${quantitePanneaux} panneaux) vers « ${client} »${note ? ' - ' + note : ''}` : `Sortie location de ${inputQ} unités vers « ${client} »${note ? ' - ' + note : ''}`,
    date_mouvement: dateDebut ? new Date(dateDebut).toISOString() : new Date().toISOString()
  });

  bootstrap.Modal.getInstance(document.getElementById("modalSortieLocation"))?.hide();
  flash(`Succès : ${isPanneau ? inputQ + ' cage(s)' : inputQ + ' unité(s)'} mise(s) en location pour « ${client} ».`, "success");
  
  if (currentPage === "location") renderLocation();
  else if (currentPage === "cages") renderCages();
  else if (currentPage === "sections") renderSections();
  else renderDashboard();
}

async function openRetourLocationPourArticle(articleId) {
  const article = await db.articles.get(articleId);
  if (!article) return;

  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const isPanneau = (typeMap[article.type_id] || '').includes('Panneau');

  const qLoc = parseInt(article.quantite_en_location) || 0;
  const cagesLoc = isPanneau ? Math.floor(qLoc / PANNEAUX_PAR_CAGE) : qLoc;

  document.getElementById("retloc-article-id").value = article.id;
  document.getElementById("retloc-title").textContent = `${article.dimension_modele} ${article.couleur ? '— ' + article.couleur : ''}`;
  document.getElementById("retloc-client-txt").textContent = article.client_location || 'Client';
  document.getElementById("retloc-actuel-txt").textContent = isPanneau ? `${cagesLoc} cage(s) (${qLoc} panneaux)` : `${qLoc} unité(s)`;

  if (isPanneau) {
    document.getElementById("retloc-quantite-label").textContent = "Nombre de Cages retournées en cour *";
    document.getElementById("retloc-panneaux-equiv-box").style.display = "block";
    document.getElementById("retloc-quantite").value = Math.min(1, cagesLoc);
    document.getElementById("retloc-quantite").max = cagesLoc;
    calcPanneauxRetLoc();
  } else {
    document.getElementById("retloc-quantite-label").textContent = "Quantité d'unités retournées en cour *";
    document.getElementById("retloc-panneaux-equiv-box").style.display = "none";
    document.getElementById("retloc-quantite").value = Math.min(1, qLoc);
    document.getElementById("retloc-quantite").max = qLoc;
  }

  document.getElementById("retloc-note").value = "";
  new bootstrap.Modal(document.getElementById("modalRetourLocation")).show();
}

function stepRetLocQuantite(delta) {
  const el = document.getElementById("retloc-quantite");
  let v = (parseInt(el.value) || 1) + delta;
  if (v < 1) v = 1;
  el.value = v;
  calcPanneauxRetLoc();
}

function calcPanneauxRetLoc() {
  const nb = parseInt(document.getElementById("retloc-quantite").value) || 0;
  const artId = parseInt(document.getElementById("retloc-article-id").value);
  db.articles.get(artId).then(a => {
    const cap = getCapaciteCage(a);
    document.getElementById("retloc-calc-panneaux").textContent = nb * cap;
  });
}

async function submitRetourLocation(e) {
  e.preventDefault();
  const articleId = parseInt(document.getElementById("retloc-article-id").value);
  const article = await db.articles.get(articleId);
  if (!article) return;

  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const isPanneau = (typeMap[article.type_id] || '').includes('Panneau');

  const inputQ = parseInt(document.getElementById("retloc-quantite").value) || 1;
  const cap = getCapaciteCage(article);
  const quantitePanneaux = isPanneau ? inputQ * cap : inputQ;
  const qLocActuelle = parseInt(article.quantite_en_location) || 0;

  const nouvLoc = Math.max(0, qLocActuelle - quantitePanneaux);
  const client = article.client_location || "";
  const note = document.getElementById("retloc-note").value.trim();

  await db.articles.update(articleId, {
    quantite_en_location: nouvLoc,
    client_location: nouvLoc === 0 ? "" : client
  });

  await db.mouvements.add({
    article_id: articleId,
    type_mouvement: "Retour location",
    quantite: quantitePanneaux,
    client: client,
    note: isPanneau ? `Retour de location de ${inputQ} cage(s) (${quantitePanneaux} panneaux) réintégrées en cour${note ? ' - ' + note : ''}` : `Retour de location de ${inputQ} unités${note ? ' - ' + note : ''}`,
    date_mouvement: new Date().toISOString()
  });

  bootstrap.Modal.getInstance(document.getElementById("modalRetourLocation"))?.hide();
  flash(`Succès : ${isPanneau ? inputQ + ' cage(s)' : inputQ + ' unité(s)'} réintégrée(s) dans la cour.`, "success");

  if (currentPage === "location") renderLocation();
  else if (currentPage === "cages") renderCages();
  else if (currentPage === "sections") renderSections();
  else renderDashboard();
}

/* ================================================================
   MOUVEMENTS DE CHANTIER (SORTIE & RETOUR)
   ================================================================ */
function openSortieCageModal(articleId, nom, couleur, cagesDispo, dispoPanneaux) {
  document.getElementById("sortie-article-id").value = articleId;
  document.getElementById("sortie-cage-title").textContent = `${nom} — ${couleur}`;
  document.getElementById("sortie-cage-dispo-txt").textContent = `${cagesDispo} cage(s)`;
  document.getElementById("sortie-cage-panneaux-txt").textContent = `(${dispoPanneaux} panneaux)`;
  document.getElementById("sortie-nb-cages").value = 1;
  document.getElementById("sortie-nb-cages").max = cagesDispo;
  document.getElementById("sortie-chantier-nom").value = "";
  document.getElementById("sortie-note").value = "";
  calcPanneauxSortie();
  new bootstrap.Modal(document.getElementById("modalSortieCage")).show();
}

function stepCageSortie(delta) {
  const el = document.getElementById("sortie-nb-cages");
  let v = (parseInt(el.value) || 1) + delta;
  if (v < 1) v = 1;
  el.value = v;
  calcPanneauxSortie();
}

function calcPanneauxSortie() {
  const nb = parseInt(document.getElementById("sortie-nb-cages").value) || 0;
  const artId = parseInt(document.getElementById("sortie-article-id").value);
  db.articles.get(artId).then(a => {
    const cap = getCapaciteCage(a);
    document.getElementById("sortie-calc-panneaux").textContent = nb * cap;
  });
}

async function submitSortieCage(e) {
  e.preventDefault();
  const articleId = parseInt(document.getElementById("sortie-article-id").value);
  const nbCages = parseInt(document.getElementById("sortie-nb-cages").value) || 1;
  const chantier = document.getElementById("sortie-chantier-nom").value.trim();
  const note = document.getElementById("sortie-note").value.trim();

  const article = await db.articles.get(articleId);
  if (!article) return;

  const cap = getCapaciteCage(article);
  const panneauxSortie = nbCages * cap;
  const dispoActuel = getDispo(article);

  if (panneauxSortie > dispoActuel) {
    alert(`Stock insuffisant en cour : seulement ${Math.floor(dispoActuel / 21)} cage(s) disponibles.`);
    return;
  }

  const qChantier = (parseInt(article.quantite_en_chantier) || 0) + panneauxSortie;

  await db.articles.update(articleId, {
    quantite_en_chantier: qChantier,
    chantier_actuel: chantier
  });

  await db.mouvements.add({
    article_id: articleId,
    type_mouvement: "Sortie chantier",
    quantite: panneauxSortie,
    chantier: chantier,
    note: note ? `${nbCages} cage(s) (${panneauxSortie} panneaux) - ${note}` : `${nbCages} cage(s) (${panneauxSortie} panneaux)`,
    date_mouvement: new Date().toISOString()
  });

  bootstrap.Modal.getInstance(document.getElementById("modalSortieCage"))?.hide();
  flash(`Succès : ${nbCages} cage(s) (${panneauxSortie} panneaux) envoyée(s) au chantier « ${chantier} ».`, "success");
  renderCages();
}

function openRetourCageModal(articleId, nom, couleur, cagesChantier, chantierActuel) {
  document.getElementById("retour-article-id").value = articleId;
  document.getElementById("retour-cage-title").textContent = `${nom} — ${couleur}`;
  document.getElementById("retour-cage-chantier-txt").textContent = `${cagesChantier} cage(s) en chantier`;
  document.getElementById("retour-nb-cages").value = 1;
  document.getElementById("retour-nb-cages").max = cagesChantier;
  document.getElementById("retour-chantier-nom").value = chantierActuel || "";
  calcPanneauxRetour();
  new bootstrap.Modal(document.getElementById("modalRetourCage")).show();
}

function stepCageRetour(delta) {
  const el = document.getElementById("retour-nb-cages");
  let v = (parseInt(el.value) || 1) + delta;
  if (v < 1) v = 1;
  el.value = v;
  calcPanneauxRetour();
}

function calcPanneauxRetour() {
  const nb = parseInt(document.getElementById("retour-nb-cages").value) || 0;
  const artId = parseInt(document.getElementById("retour-article-id").value);
  db.articles.get(artId).then(a => {
    const cap = getCapaciteCage(a);
    document.getElementById("retour-calc-panneaux").textContent = nb * cap;
  });
}

async function submitRetourCage(e) {
  e.preventDefault();
  const articleId = parseInt(document.getElementById("retour-article-id").value);
  const nbCages = parseInt(document.getElementById("retour-nb-cages").value) || 1;
  const chantier = document.getElementById("retour-chantier-nom").value.trim();

  const article = await db.articles.get(articleId);
  if (!article) return;

  const cap = getCapaciteCage(article);
  const panneauxRetour = nbCages * cap;
  let qChantier = Math.max(0, (parseInt(article.quantite_en_chantier) || 0) - panneauxRetour);
  let chantActuel = article.chantier_actuel;
  if (qChantier === 0) chantActuel = "";

  await db.articles.update(articleId, {
    quantite_en_chantier: qChantier,
    chantier_actuel: chantActuel
  });

  await db.mouvements.add({
    article_id: articleId,
    type_mouvement: "Retour chantier",
    quantite: panneauxRetour,
    chantier: chantier,
    note: `Retour de ${nbCages} cage(s) (${panneauxRetour} panneaux) dans la cour`,
    date_mouvement: new Date().toISOString()
  });

  bootstrap.Modal.getInstance(document.getElementById("modalRetourCage"))?.hide();
  flash(`Succès : ${nbCages} cage(s) réintégrée(s) dans la cour.`, "success");
  renderCages();
}

/* ================================================================
   AJOUT CONFIGURATION CAGES (GRANDEUR + COULEUR)
   ================================================================ */
function openNewCageModal() {
  document.getElementById("cfg-nb-cages").value = 15;
  document.getElementById("cfg-panneaux-par-cage").value = getGlobalPanneauxParCage();
  document.getElementById("cfg-emplacement").value = "Cour A";
  calcCfgPanneaux();
  new bootstrap.Modal(document.getElementById("modalConfigCage")).show();
}

function stepCfgCages(delta) {
  const el = document.getElementById("cfg-nb-cages");
  let v = (parseInt(el.value) || 0) + delta;
  if (v < 0) v = 0;
  el.value = v;
  calcCfgPanneaux();
}

function calcCfgPanneaux() {
  const nb = parseInt(document.getElementById("cfg-nb-cages").value) || 0;
  const cap = parseInt(document.getElementById("cfg-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  document.getElementById("cfg-calc-panneaux").textContent = nb * cap;
}

async function submitConfigCage(e) {
  e.preventDefault();
  const grandeur = document.getElementById("cfg-grandeur").value;
  const couleur = document.getElementById("cfg-couleur").value;
  const nbCages = parseInt(document.getElementById("cfg-nb-cages").value) || 0;
  const cap = parseInt(document.getElementById("cfg-panneaux-par-cage")?.value) || getGlobalPanneauxParCage();
  const emplacement = document.getElementById("cfg-emplacement").value.trim();

  const types = await db.types.toArray();
  const typePanneau = types.find(t => t.nom === "Panneau de coffrage");
  if (!typePanneau) return;

  const sections = await db.sections.toArray();
  const secCoffrage = sections.find(s => s.nom.includes("Coffrage")) || sections[0];

  const totalPanneaux = nbCages * cap;
  const dimensionNom = `Panneau ${grandeur}`;

  const existing = await db.articles.where("type_id").equals(typePanneau.id).toArray();
  const found = existing.find(a => a.dimension_modele === dimensionNom && a.couleur === couleur);

  if (found) {
    await db.articles.update(found.id, {
      panneaux_par_cage: cap,
      quantite_totale: totalPanneaux,
      emplacement: emplacement || found.emplacement,
      section_id: found.section_id || (secCoffrage ? secCoffrage.id : 0)
    });
    flash(`Mise à jour : ${dimensionNom} ${couleur} ajusté à ${nbCages} cages (${totalPanneaux} panneaux).`, "success");
  } else {
    await db.articles.add({
      section_id: secCoffrage ? secCoffrage.id : 0,
      type_id: typePanneau.id,
      dimension_modele: dimensionNom,
      couleur: couleur,
      panneaux_par_cage: cap,
      quantite_totale: totalPanneaux,
      quantite_en_chantier: 0,
      quantite_en_location: 0,
      quantite_en_reparation: 0,
      seuil_alerte: 2 * PANNEAUX_PAR_CAGE,
      chantier_actuel: "",
      client_location: "",
      etat: "Bon",
      emplacement: emplacement,
      champs_valeurs: { "Grandeur": grandeur, "Couleur": couleur }
    });
    flash(`Ajouté : ${nbCages} cages de ${dimensionNom} (${couleur}) = ${totalPanneaux} panneaux.`, "success");
  }

  bootstrap.Modal.getInstance(document.getElementById("modalConfigCage"))?.hide();
  renderCages();
}

/* ================================================================
   VUE 3 : SECTIONS D'INVENTAIRE & ITEMS LIÉS
   ================================================================ */
async function renderSections() {
  const sections = await db.sections.toArray();
  const articles = await db.articles.toArray();
  const types = await db.types.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);

  const articlesParSection = {};
  sections.forEach(s => articlesParSection[s.id] = []);
  const articlesSansSection = [];

  articles.forEach(a => {
    if (a.section_id && articlesParSection[a.section_id]) {
      articlesParSection[a.section_id].push(a);
    } else {
      articlesSansSection.push(a);
    }
  });

  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4 flex-wrap gap-2">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase" style="letter-spacing: 0.03em;">
          Sections d'inventaire
        </h1>
        <span class="small" style="color: #a1a1aa;">
          Organisation méthodique du parc par catégories &bull; Équipements rattachés
        </span>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-orange btn-sm px-3 fw-bold" onclick="openNouvelleSectionModal()">
          + Nouvelle Section
        </button>
        <button class="btn btn-orange btn-sm px-3 fw-bold" onclick="navigateTo('article-form')">
          + Nouvel Item
        </button>
      </div>
    </div>

    <div id="sections-container">
      ${sections.map(sec => {
        const secItems = articlesParSection[sec.id] || [];
        const totalPieces = secItems.reduce((acc, it) => acc + (parseInt(it.quantite_totale) || 0), 0);
        const dispoPieces = secItems.reduce((acc, it) => acc + getDispo(it), 0);
        const chantierPieces = secItems.reduce((acc, it) => acc + (parseInt(it.quantite_en_chantier) || 0), 0);
        const locationPieces = secItems.reduce((acc, it) => acc + (parseInt(it.quantite_en_location) || 0), 0);

        return `
        <div class="card-custom mb-4 overflow-hidden shadow-sm">
          <div class="p-3 bg-dark text-white d-flex justify-content-between align-items-center flex-wrap gap-2" style="border-bottom: 2px solid var(--orange);">
            <div>
              <div class="d-flex align-items-center gap-2">
                <h2 class="h5 mb-0 fw-bold text-white text-uppercase" style="letter-spacing: 0.04em;">
                  ${sec.nom}
                </h2>
                <span class="badge bg-secondary text-white small">${secItems.length} réf.</span>
              </div>
              ${sec.description ? `<div class="small text-muted mt-1">${sec.description}</div>` : ''}
            </div>

            <div class="d-flex align-items-center gap-2">
              <span class="small text-muted d-none d-lg-inline me-2">
                Total: <strong>${totalPieces}</strong> &bull; Cour: <strong class="text-success">${dispoPieces}</strong> &bull; Chantier: <strong style="color: var(--orange);">${chantierPieces}</strong> &bull; Loc: <strong class="text-primary">${locationPieces}</strong>
              </span>
              <button class="btn btn-orange btn-sm fw-bold px-3" onclick="navigateTo('article-form', { sectionId: ${sec.id} })">
                + Item
              </button>
              <button class="btn btn-sm btn-dark-pro px-2 py-1" onclick="openEditSectionModal(${sec.id}, '${sec.nom.replace(/'/g, "\\'")}', '${(sec.description || '').replace(/'/g, "\\'")}')" title="Modifier">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger px-2 py-1" onclick="deleteSection(${sec.id}, '${sec.nom.replace(/'/g, "\\'")}')" title="Supprimer">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>

          <!-- Version Mobile : Cartes -->
          <div class="d-md-none p-2">
            ${secItems.length === 0 ? '<div class="text-center py-3 text-muted">Section vide.</div>' : secItems.map(it => {
              const dispo = getDispo(it);
              const isPanneau = (typeMap[it.type_id] || '').includes('Panneau');
              const cagesTxt = isPanneau ? ` (${Math.floor(dispo / 21)} cages)` : '';
              return `
              <div class="mobile-item-card">
                <div class="d-flex justify-content-between align-items-baseline mb-1">
                  <strong class="fs-6 text-dark">${it.dimension_modele}</strong>
                  ${it.couleur ? `<span class="badge bg-light text-dark border">${it.couleur}</span>` : ''}
                </div>
                <div class="small text-muted mb-2">${typeMap[it.type_id] || 'Standard'} &bull; ${it.emplacement || 'Cour'}</div>
                <div class="d-flex justify-content-between text-center p-2 rounded mb-2" style="background-color: var(--gris-clair);">
                  <div><span class="small text-muted d-block">TOTAL</span><strong>${it.quantite_totale}</strong></div>
                  <div><span class="small text-success d-block">COUR</span><strong class="text-success">${dispo}${cagesTxt}</strong></div>
                  <div><span class="small d-block" style="color: var(--orange);">CHANT.</span><strong style="color: var(--orange);">${it.quantite_en_chantier || 0}</strong></div>
                  <div><span class="small text-primary d-block">LOC.</span><strong class="text-primary">${it.quantite_en_location || 0}</strong></div>
                </div>
                <div class="d-flex gap-1 justify-content-end">
                  <button class="btn btn-sm btn-outline-dark px-2" onclick="openAjusterRepartitionModal(${it.id})">⚙️ Ajuster</button>
                  <button class="btn btn-sm btn-outline-secondary px-2" onclick="navigateTo('article-form', { id: ${it.id} })">Modifier</button>
                </div>
              </div>`;
            }).join("")}
          </div>

          <!-- Version Desktop : Tableau -->
          <div class="table-responsive d-none d-md-block">
            <table class="table-pro">
              <thead>
                <tr>
                  <th>Désignation / Modèle</th>
                  <th>Type</th>
                  <th>Couleur</th>
                  <th class="text-center">Total</th>
                  <th class="text-center text-success">Cour</th>
                  <th class="text-center" style="color: var(--orange);">Chantier</th>
                  <th class="text-center text-primary">Location</th>
                  <th>Affectation</th>
                  <th>Emplacement</th>
                  <th class="text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                ${secItems.map(it => {
                  const dispo = getDispo(it);
                  const isPanneau = (typeMap[it.type_id] || '').includes('Panneau');
                  const cagesCour = isPanneau ? `<span class="badge bg-light text-dark border ms-1">${Math.floor(dispo / 21)} c.</span>` : '';
                  return `
                  <tr>
                    <td class="fw-bold">${it.dimension_modele}</td>
                    <td><span class="badge bg-dark text-white fw-bold" style="font-size: 0.72rem;">${typeMap[it.type_id] || 'Standard'}</span></td>
                    <td>${it.couleur ? `<span class="badge bg-light text-dark border">${it.couleur}</span>` : '<span class="text-muted">—</span>'}</td>
                    <td class="text-center fw-bold">${it.quantite_totale}</td>
                    <td class="text-center fw-bold text-success fs-6">${dispo} ${cagesCour}</td>
                    <td class="text-center fw-bold" style="color: var(--orange);">${it.quantite_en_chantier || 0}</td>
                    <td class="text-center fw-bold text-primary">${it.quantite_en_location || 0}</td>
                    <td>
                      ${it.chantier_actuel ? `<div><span class="badge bg-warning text-dark me-1">Chantier</span>${it.chantier_actuel}</div>` : ''}
                      ${it.client_location ? `<div><span class="badge bg-info text-dark me-1">Loc</span>${it.client_location}</div>` : ''}
                      ${!it.chantier_actuel && !it.client_location ? '<span class="text-muted">Entrepôt</span>' : ''}
                    </td>
                    <td>${it.emplacement || '<span class="text-muted">—</span>'}</td>
                    <td class="text-end text-nowrap">
                      <button class="btn btn-sm btn-outline-dark px-2 py-1 me-1" onclick="openAjusterRepartitionModal(${it.id})" title="Ajuster">⚙️</button>
                      <button class="btn btn-sm btn-outline-secondary px-2 py-1" onclick="navigateTo('article-form', { id: ${it.id} })">Modifier</button>
                      <button class="btn btn-sm btn-outline-danger px-2 py-1 ms-1" onclick="deleteArticleFromSection(${it.id})">✕</button>
                    </td>
                  </tr>`;
                }).join("")}
              </tbody>
            </table>
          </div>
        </div>`;
      }).join("")}
    </div>
  `;
}

function openNouvelleSectionModal() {
  document.getElementById("edit-section-id").value = "";
  document.getElementById("sec-nom").value = "";
  document.getElementById("sec-desc").value = "";
  document.getElementById("btn-save-section").textContent = "Créer la section";
  new bootstrap.Modal(document.getElementById("modalNouvelleSection")).show();
}

function openEditSectionModal(id, nom, desc) {
  document.getElementById("edit-section-id").value = id;
  document.getElementById("sec-nom").value = nom;
  document.getElementById("sec-desc").value = desc;
  document.getElementById("btn-save-section").textContent = "Enregistrer les modifications";
  new bootstrap.Modal(document.getElementById("modalNouvelleSection")).show();
}

async function submitNouvelleSection(e) {
  e.preventDefault();
  const idStr = document.getElementById("edit-section-id").value;
  const nom = document.getElementById("sec-nom").value.trim();
  const desc = document.getElementById("sec-desc").value.trim();

  if (!nom) return;

  if (idStr) {
    const id = parseInt(idStr);
    await db.sections.update(id, { nom, description: desc });
    flash(`Section « ${nom} » mise à jour avec succès !`, "success");
  } else {
    await db.sections.add({ nom, description: desc, date_creation: new Date().toISOString() });
    flash(`Nouvelle section « ${nom} » créée !`, "success");
  }

  bootstrap.Modal.getInstance(document.getElementById("modalNouvelleSection"))?.hide();
  renderSections();
}

async function deleteSection(id, nom) {
  if (!confirm(`Supprimer la section d'inventaire « ${nom} » ?`)) return;
  const articlesInSec = await db.articles.where("section_id").equals(id).toArray();
  for (const a of articlesInSec) {
    await db.articles.update(a.id, { section_id: 0 });
  }
  await db.sections.delete(id);
  flash(`Section « ${nom} » supprimée.`, "warning");
  renderSections();
}

async function deleteArticleFromSection(id) {
  if (!confirm("Supprimer cet item ?")) return;
  await db.articles.delete(id);
  flash("Item supprimé.", "warning");
  renderSections();
}

/* ================================================================
   VUE 4 : TOUT LE MATÉRIEL (TABLEAU & MOBILE CARDS)
   ================================================================ */
async function renderDashboard() {
  const articles = await db.articles.toArray();
  const types = await db.types.toArray();
  const sections = await db.sections.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const secMap = {};
  sections.forEach(s => secMap[s.id] = s.nom);

  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4 flex-wrap gap-2">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase">Tout le parc de matériel</h1>
        <span class="small" style="color: #a1a1aa;">Vue globale des ${articles.length} items &bull; Cour, Chantier, Location</span>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-light btn-sm px-3" onclick="exportInventoryCSV()">
          <i class="bi bi-file-earmark-spreadsheet me-1"></i> Excel/CSV
        </button>
        <button class="btn btn-orange btn-sm px-3" onclick="navigateTo('article-form')">
          + Nouvel item
        </button>
      </div>
    </div>

    <!-- Version Mobile : Cartes tactiles -->
    <div class="d-md-none">
      ${articles.map(a => {
        const dispo = getDispo(a);
        const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
        const cagesDispo = isPanneau ? ` (${Math.floor(dispo / 21)} cages)` : '';
        return `
        <div class="mobile-item-card">
          <div class="d-flex justify-content-between align-items-baseline mb-1">
            <strong class="fs-6 text-dark">${a.dimension_modele}</strong>
            ${a.couleur ? `<span class="badge bg-light text-dark border">${a.couleur}</span>` : ''}
          </div>
          <div class="small text-muted mb-2">
            ${typeMap[a.type_id] || 'Standard'} &bull; ${secMap[a.section_id] || 'Section'}
          </div>
          <div class="d-flex justify-content-between text-center p-2 rounded mb-2" style="background-color: var(--gris-clair);">
            <div><span class="small text-muted d-block">TOTAL</span><strong>${a.quantite_totale}</strong></div>
            <div><span class="small text-success d-block">COUR</span><strong class="text-success">${dispo}${cagesDispo}</strong></div>
            <div><span class="small d-block" style="color: var(--orange);">CHANT.</span><strong style="color: var(--orange);">${a.quantite_en_chantier || 0}</strong></div>
            <div><span class="small text-primary d-block">LOC.</span><strong class="text-primary">${a.quantite_en_location || 0}</strong></div>
          </div>
          <div class="d-flex gap-1 justify-content-end">
            <button class="btn btn-sm btn-outline-dark px-2" onclick="openAjusterRepartitionModal(${a.id})">⚙️ Ajuster</button>
            <button class="btn btn-sm btn-outline-secondary px-2" onclick="navigateTo('article-form',{id:${a.id}})">Modifier</button>
            <button class="btn btn-sm btn-outline-danger px-2" onclick="deleteArticle(${a.id})">✕</button>
          </div>
        </div>`;
      }).join("")}
    </div>

    <!-- Version Desktop : Tableau complet -->
    <div class="card-custom overflow-hidden shadow-sm d-none d-md-block">
      <div class="table-responsive">
        <table class="table-pro">
          <thead>
            <tr>
              <th>Désignation</th>
              <th>Section</th>
              <th>Type</th>
              <th>Couleur</th>
              <th class="text-center">Total</th>
              <th class="text-center text-success">Cour</th>
              <th class="text-center" style="color: var(--orange);">Chantier</th>
              <th class="text-center text-primary">Location</th>
              <th>Affectation</th>
              <th>État</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            ${articles.map(a => {
              const typeName = typeMap[a.type_id] || '—';
              const secName = secMap[a.section_id] || '<span class="text-muted">Non classé</span>';
              const dispo = getDispo(a);
              return `
              <tr>
                <td class="fw-bold">${a.dimension_modele}</td>
                <td><span class="badge bg-light text-dark border">${secName}</span></td>
                <td><span class="badge bg-dark text-white fw-bold" style="font-size: 0.72rem;">${typeName}</span></td>
                <td>${a.couleur ? `<span class="badge bg-light text-dark border">${a.couleur}</span>` : '—'}</td>
                <td class="text-center fw-bold">${a.quantite_totale}</td>
                <td class="text-center fw-bold text-success fs-6">${dispo}</td>
                <td class="text-center fw-bold" style="color: var(--orange);">${a.quantite_en_chantier || 0}</td>
                <td class="text-center fw-bold text-primary">${a.quantite_en_location || 0}</td>
                <td>
                  ${a.chantier_actuel ? `<div><span class="badge bg-warning text-dark me-1">Chantier</span>${a.chantier_actuel}</div>` : ''}
                  ${a.client_location ? `<div><span class="badge bg-info text-dark me-1">Client</span>${a.client_location}</div>` : ''}
                  ${!a.chantier_actuel && !a.client_location ? '<span class="text-muted">Entrepôt</span>' : ''}
                </td>
                <td><span class="badge bg-light text-dark border">${a.etat || 'Bon'}</span></td>
                <td class="text-end text-nowrap">
                  <button class="btn btn-sm btn-outline-dark px-2 py-1 me-1" onclick="openAjusterRepartitionModal(${a.id})" title="Ajuster">⚙️</button>
                  <button class="btn btn-sm btn-outline-secondary px-2 py-1" onclick="navigateTo('article-form',{id:${a.id}})">Modifier</button>
                  <button class="btn btn-sm btn-outline-danger px-2 py-1" onclick="deleteArticle(${a.id})">✕</button>
                </td>
              </tr>`;
            }).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

/* ================================================================
   VUE 5 : HISTORIQUE COMPLET DES MOUVEMENTS
   ================================================================ */
async function renderMouvements() {
  const mvts = await db.mouvements.orderBy("date_mouvement").reverse().toArray();
  const articles = await db.articles.toArray();
  const artMap = {};
  articles.forEach(a => artMap[a.id] = a.dimension_modele);

  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase">Historique des mouvements</h1>
        <span class="small" style="color: #a1a1aa;">Traçabilité complète : Sorties, Retours, Chantiers et Locations</span>
      </div>
    </div>

    <!-- Mobile list -->
    <div class="d-md-none">
      ${mvts.map(m => `
        <div class="mobile-item-card">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="badge ${m.type_mouvement.includes('Sortie') ? 'bg-warning text-dark' : 'bg-success text-white'} fw-bold">${m.type_mouvement}</span>
            <span class="small text-muted font-monospace">${new Date(m.date_mouvement).toLocaleDateString()}</span>
          </div>
          <div class="fw-bold fs-6">${artMap[m.article_id] || 'Article'}</div>
          <div class="text-dark small my-1">Quantité : <strong>${m.quantite} pcs</strong> ${m.chantier ? '&bull; Chantier: <strong>' + m.chantier + '</strong>' : ''} ${m.client ? '&bull; Client: <strong>' + m.client + '</strong>' : ''}</div>
          <div class="small text-muted">${m.note || ''}</div>
        </div>
      `).join("")}
    </div>

    <!-- Desktop table -->
    <div class="card-custom overflow-hidden shadow-sm d-none d-md-block">
      <div class="table-responsive">
        <table class="table-pro">
          <thead>
            <tr>
              <th>Date & Heure</th>
              <th>Opération</th>
              <th>Article</th>
              <th class="text-center">Quantité</th>
              <th>Chantier / Client</th>
              <th>Détail / Note</th>
            </tr>
          </thead>
          <tbody>
            ${mvts.map(m => `
              <tr>
                <td class="small text-muted font-monospace">${new Date(m.date_mouvement).toLocaleString()}</td>
                <td><span class="badge ${m.type_mouvement.includes('Sortie') ? 'bg-warning text-dark' : 'bg-success text-white'} fw-bold">${m.type_mouvement}</span></td>
                <td class="fw-bold">${artMap[m.article_id] || 'Article'}</td>
                <td class="text-center fw-bold fs-6">${m.quantite} pcs</td>
                <td>${m.chantier ? '<strong>Chantier: ' + m.chantier + '</strong>' : ''} ${m.client ? '<strong>Client: ' + m.client + '</strong>' : ''} ${!m.chantier && !m.client ? '—' : ''}</td>
                <td class="small text-muted">${m.note || '—'}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

/* ================================================================
   VUE 6 : BASE DE DONNÉES, SAUVEGARDES & SYNCHRONISATION
   ================================================================ */
async function renderDatabase() {
  const countArticles = await db.articles.count();
  const countMouvements = await db.mouvements.count();
  const countSections = await db.sections.count();
  const countTypes = await db.types.count();

  const articles = await db.articles.toArray();
  const totalPanneaux = articles.reduce((acc, a) => acc + (parseInt(a.quantite_totale) || 0), 0);
  const totalCages = Math.floor(totalPanneaux / PANNEAUX_PAR_CAGE);

  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4 flex-wrap gap-2">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase" style="letter-spacing: 0.03em;">
          Base de Données & Sauvegardes
        </h1>
        <span class="small" style="color: #a1a1aa;">
          Gestion complète &bull; Export JSON / Excel &bull; Sauvegarde et Restauration
        </span>
      </div>
    </div>

    <!-- Métriques de la base -->
    <div class="row g-2 g-md-3 mb-4">
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--vert-ok);">
          <div class="stat-value text-success">${countArticles}</div>
          <div class="stat-label">Références en base</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--orange);">
          <div class="stat-value" style="color: var(--orange);">${totalCages}</div>
          <div class="stat-label">Cages calculées (${totalPanneaux} panneaux)</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat">
          <div class="stat-value">${countMouvements}</div>
          <div class="stat-label">Mouvements archivés</div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card-stat" style="border-top: 3px solid var(--bleu-location);">
          <div class="stat-value text-primary">100%</div>
          <div class="stat-label">Fonctionnement Hors-Ligne</div>
        </div>
      </div>
    </div>

    <!-- Outils de Sauvegarde et d'Exportation -->
    <div class="row g-3">
      <!-- 0. Paramètre Capacité des Cages -->
      <div class="col-12 col-md-6">
        <div class="card-custom p-4 h-100 shadow-sm d-flex flex-column justify-content-between" style="border-left: 4px solid var(--orange);">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <i class="bi bi-gear-wide-connected text-warning fs-3"></i>
              <h2 class="h5 fw-bold mb-0 text-uppercase">Capacité des Cages</h2>
            </div>
            <p class="small text-muted">
              Nombre de panneaux par cage standard : <strong class="fs-6 text-primary">${getGlobalPanneauxParCage()} panneaux / cage</strong>. Modifiable pour l'ensemble du parc ou par référence.
            </p>
          </div>
          <div class="mt-3">
            <button class="btn btn-outline-warning fw-bold w-100 py-2 text-dark" onclick="openModalCapaciteCageGlobale()">
              <i class="bi bi-sliders me-1"></i> Changer la capacité par défaut (${getGlobalPanneauxParCage()} pcs)
            </button>
          </div>
        </div>
      </div>
      <!-- 1. Sauvegarde Complète JSON -->
      <div class="col-12 col-md-6">
        <div class="card-custom p-4 h-100 shadow-sm d-flex flex-column justify-content-between">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <i class="bi bi-cloud-arrow-down-fill text-warning fs-3"></i>
              <h2 class="h5 fw-bold mb-0 text-uppercase">Sauvegarde JSON</h2>
            </div>
            <p class="small text-muted">
              Exportez une copie intégrale de toutes vos données (sections, types, items, stocks dans la cour, chantiers, locations et mouvements). Ce fichier peut être sauvegardé sur votre téléphone ou transféré sur un autre ordinateur.
            </p>
          </div>
          <div class="d-flex gap-2 flex-wrap mt-3">
            <button class="btn btn-orange fw-bold flex-grow-1 py-2" onclick="exportBackupJSON()">
              <i class="bi bi-download me-1"></i> Télécharger la Sauvegarde (.json)
            </button>
            <button class="btn btn-outline-dark fw-bold px-3 py-2" onclick="openImportModal()">
              <i class="bi bi-upload me-1"></i> Restaurer
            </button>
          </div>
        </div>
      </div>

      <!-- 2. Exportation Tableur Excel / CSV -->
      <div class="col-12 col-md-6">
        <div class="card-custom p-4 h-100 shadow-sm d-flex flex-column justify-content-between">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <i class="bi bi-file-earmark-spreadsheet-fill text-success fs-3"></i>
              <h2 class="h5 fw-bold mb-0 text-uppercase">Tableur Excel / CSV</h2>
            </div>
            <p class="small text-muted">
              Téléchargez un tableau prêt à être ouvert dans Excel ou Google Sheets avec toutes les colonnes : Désignation, Grandeur, Couleur, Nombre de cages, Stock Cour, Chantier, Location, et Emplacement.
            </p>
          </div>
          <div class="mt-3">
            <button class="btn btn-success fw-bold w-100 py-2 text-white" onclick="exportInventoryCSV()">
              <i class="bi bi-file-earmark-spreadsheet me-1"></i> Télécharger le Tableur Excel (.csv)
            </button>
          </div>
        </div>
      </div>

      <!-- 3. Base Modèle Prête à l'Emploi -->
      <div class="col-12 col-md-6">
        <div class="card-custom p-4 h-100 shadow-sm d-flex flex-column justify-content-between">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <i class="bi bi-box-seam-fill text-primary fs-3"></i>
              <h2 class="h5 fw-bold mb-0 text-uppercase">Base Modèle Prête à l'Emploi</h2>
            </div>
            <p class="small text-muted">
              Recharge instantanément le catalogue complet de coffrage : 42 références couvrant toutes les grandeurs de panneaux (2pi à 10pi), toutes les couleurs, fillers, cages de coin, étais et quincaillerie, avec des mouvements réalistes.
            </p>
          </div>
          <div class="mt-3">
            <button class="btn btn-primary fw-bold w-100 py-2 text-white" onclick="rechargeCatalogueModele()">
              <i class="bi bi-arrow-repeat me-1"></i> Recharger la Base Modèle (42 items)
            </button>
          </div>
        </div>
      </div>

      <!-- 4. Remise à Zéro Complète -->
      <div class="col-12 col-md-6">
        <div class="card-custom p-4 h-100 shadow-sm d-flex flex-column justify-content-between border-danger">
          <div>
            <div class="d-flex align-items-center gap-2 mb-2">
              <i class="bi bi-trash-fill text-danger fs-3"></i>
              <h2 class="h5 fw-bold mb-0 text-uppercase text-danger">Zone de Nettoyage</h2>
            </div>
            <p class="small text-muted">
              Permet de vider intégralement la base de données locale si vous souhaitez repartir de zéro et saisir votre inventaire officiel en atelier.
            </p>
          </div>
          <div class="mt-3">
            <button class="btn btn-outline-danger fw-bold w-100 py-2" onclick="viderBaseComplete()">
              <i class="bi bi-exclamation-triangle me-1"></i> Vider la base de données
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

/* ================================================================
   LOGIQUE DE SAUVEGARDE & EXPORT
   ================================================================ */
async function exportBackupJSON() {
  const sections = await db.sections.toArray();
  const types = await db.types.toArray();
  const articles = await db.articles.toArray();
  const mouvements = await db.mouvements.toArray();

  const backupData = {
    version: 7,
    date_export: new Date().toISOString(),
    societe: "Gestion MT Coffrage",
    sections,
    types,
    articles,
    mouvements
  };

  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(backupData, null, 2));
  const dlAnchor = document.createElement("a");
  const nowStr = new Date().toISOString().split("T")[0];
  dlAnchor.setAttribute("href", dataStr);
  dlAnchor.setAttribute("download", `inventaire_gestion_mt_${nowStr}.json`);
  document.body.appendChild(dlAnchor);
  dlAnchor.click();
  dlAnchor.remove();

  flash("Sauvegarde JSON téléchargée avec succès !", "success");
}

function openImportModal() {
  document.getElementById("backup-file-input").value = "";
  new bootstrap.Modal(document.getElementById("modalImportBackup")).show();
}

async function processImportFile() {
  const fileInput = document.getElementById("backup-file-input");
  if (!fileInput.files || fileInput.files.length === 0) {
    alert("Veuillez sélectionner un fichier .json");
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.onload = async function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (!data.articles || !Array.isArray(data.articles)) {
        alert("Fichier de sauvegarde invalide (aucun article trouvé).");
        return;
      }

      await db.articles.clear();
      await db.mouvements.clear();
      await db.sections.clear();
      await db.types.clear();

      if (data.sections && data.sections.length > 0) await db.sections.bulkAdd(data.sections);
      if (data.types && data.types.length > 0) await db.types.bulkAdd(data.types);
      if (data.articles && data.articles.length > 0) await db.articles.bulkAdd(data.articles);
      if (data.mouvements && data.mouvements.length > 0) await db.mouvements.bulkAdd(data.mouvements);

      bootstrap.Modal.getInstance(document.getElementById("modalImportBackup"))?.hide();
      flash(`Restauration terminée : ${data.articles.length} articles réintégrés !`, "success");
      renderDatabase();
    } catch (err) {
      alert("Erreur lors de la lecture du fichier : " + err.message);
    }
  };

  reader.readAsText(file);
}

async function exportInventoryCSV() {
  const articles = await db.articles.toArray();
  const types = await db.types.toArray();
  const sections = await db.sections.toArray();
  const typeMap = {};
  types.forEach(t => typeMap[t.id] = t.nom);
  const secMap = {};
  sections.forEach(s => secMap[s.id] = s.nom);

  let csvContent = "\uFEFFDésignation,Section,Type,Couleur,Total Pièces,Cages Totales,Cour (Dispo),Chantier,Location,Chantier Actuel,Client Location,Emplacement,État\n";

  articles.forEach(a => {
    const dispo = getDispo(a);
    const isPanneau = (typeMap[a.type_id] || '').includes('Panneau');
    const cages = isPanneau ? Math.floor((parseInt(a.quantite_totale)||0)/getCapaciteCage(a)) : 0;
    const row = [
      `"${a.dimension_modele || ''}"`,
      `"${secMap[a.section_id] || ''}"`,
      `"${typeMap[a.type_id] || ''}"`,
      `"${a.couleur || ''}"`,
      a.quantite_totale || 0,
      cages,
      dispo,
      a.quantite_en_chantier || 0,
      a.quantite_en_location || 0,
      `"${a.chantier_actuel || ''}"`,
      `"${a.client_location || ''}"`,
      `"${a.emplacement || ''}"`,
      `"${a.etat || 'Bon'}"`
    ];
    csvContent += row.join(",") + "\n";
  });

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const dlAnchor = document.createElement("a");
  const nowStr = new Date().toISOString().split("T")[0];
  dlAnchor.setAttribute("href", url);
  dlAnchor.setAttribute("download", `inventaire_gestion_mt_${nowStr}.csv`);
  document.body.appendChild(dlAnchor);
  dlAnchor.click();
  dlAnchor.remove();

  flash("Tableur CSV exporté pour Excel !", "success");
}

async function rechargeCatalogueModele() {
  if (!confirm("Recharger la base complète modèle (42 articles avec panneaux, cages et accessoires) ?")) return;
  await loadReadyToUseCatalogue(true);
  flash("Catalogue complet de 42 articles rechargé !", "success");
  renderDatabase();
}

async function viderBaseComplete() {
  if (!confirm("ATTENTION : Voulez-vous vraiment effacer tous les articles et mouvements de la base ?")) return;
  await db.articles.clear();
  await db.mouvements.clear();
  flash("Base d'articles remise à zéro.", "warning");
  renderDatabase();
}

/* ================================================================
   VUE 7 : TYPES & SCHÉMAS DYNAMIQUES
   ================================================================ */
async function renderTypes() {
  const types = await db.types.toArray();
  app().innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3 mb-md-4">
      <div>
        <h1 class="h4 mb-0 fw-bold text-white text-uppercase">Types d'équipements</h1>
        <span class="small" style="color: #a1a1aa;">Gestion des types et caractéristiques dynamiques</span>
      </div>
      <button class="btn btn-orange btn-sm px-3" onclick="navigateTo('type-form')">+ Nouveau type</button>
    </div>

    <div class="card-custom overflow-hidden shadow-sm">
      <div class="table-responsive">
        <table class="table-pro">
          <thead>
            <tr><th>Nom du type</th><th>Description</th><th>Champs spécifiques</th></tr>
          </thead>
          <tbody>
            ${types.map(t => `
              <tr>
                <td class="fw-bold fs-6">${t.nom}</td>
                <td class="text-muted small">${t.description || '—'}</td>
                <td>${(t.champs || []).map(ch => `<span class="badge bg-light text-dark border me-1">${ch.nom}</span>`).join("") || 'Standard'}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

/* ================================================================
   VUE 8 : FORMULAIRE D'ARTICLE / ITEM
   ================================================================ */
async function renderArticleForm(id = null, defaultSectionId = null) {
  const article = id ? await db.articles.get(id) : null;
  const sections = await db.sections.toArray();
  const types = await db.types.toArray();

  const selectedSectionId = article ? article.section_id : (defaultSectionId || (sections[0] ? sections[0].id : 0));

  app().innerHTML = `
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card-custom p-3 p-md-4 shadow-sm">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h2 class="h5 fw-bold text-uppercase mb-0">${id ? 'Modifier l\'' : 'Ajouter un '}item à l'inventaire</h2>
            <button class="btn btn-sm btn-outline-dark" onclick="openNouvelleSectionModal()">+ Section</button>
          </div>
          <form onsubmit="saveArticle(event, ${id || 'null'})">
            <div class="mb-3 p-3 rounded-2" style="background-color: var(--gris-clair); border: 1px solid #e4e4e7;">
              <label class="form-label fw-bold small text-uppercase text-muted">Section d'inventaire *</label>
              <select id="art-section-id" class="form-select form-select-lg" required>
                ${sections.map(s => `<option value="${s.id}" ${selectedSectionId == s.id ? 'selected' : ''}>${s.nom}</option>`).join("")}
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold small text-uppercase text-muted">Type d'équipement *</label>
              <select id="art-type-id" class="form-select" required>
                <option value="">— Choisir un type —</option>
                ${types.map(t => `<option value="${t.id}" ${article?.type_id == t.id ? 'selected' : ''}>${t.nom}</option>`).join("")}
              </select>
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold small text-uppercase text-muted">Désignation / Modèle *</label>
              <input type="text" id="art-modele" class="form-control form-control-lg" required 
                     value="${article?.dimension_modele || ''}" placeholder="Ex: Tirants 24 po, Étai 3m, Panneau 8 pieds…">
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold small text-uppercase text-muted">Couleur (optionnelle)</label>
              <select id="art-couleur" class="form-select">
                <option value="">— Sans couleur spécifique —</option>
                ${["Rose", "Vert", "Bleu", "Rouge", "Blanc", "Jaune", "Orange", "Noir"].map(c => `
                  <option value="${c}" ${article?.couleur === c ? 'selected' : ''}>${c}</option>
                `).join("")}
              </select>
            </div>

            <div class="row g-2 mb-3">
              <div class="col-6 col-md-3">
                <label class="form-label fw-bold small text-uppercase text-muted">Stock Total *</label>
                <input type="number" id="art-total" class="form-control fw-bold" min="0" required value="${article?.quantite_totale || 0}">
              </div>
              <div class="col-6 col-md-3">
                <label class="form-label fw-bold small text-uppercase text-muted">Sur chantier</label>
                <input type="number" id="art-chantier" class="form-control" min="0" value="${article?.quantite_en_chantier || 0}">
              </div>
              <div class="col-6 col-md-3">
                <label class="form-label fw-bold small text-uppercase text-muted">Sur location</label>
                <input type="number" id="art-location" class="form-control" min="0" value="${article?.quantite_en_location || 0}">
              </div>
              <div class="col-6 col-md-3">
                <label class="form-label fw-bold small text-uppercase text-muted">En réparation</label>
                <input type="number" id="art-reparation" class="form-control" min="0" value="${article?.quantite_en_reparation || 0}">
              </div>
            </div>

            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label fw-bold small text-uppercase text-muted">Chantier actuel</label>
                <input type="text" id="art-chantier-actuel" class="form-control" value="${article?.chantier_actuel || ''}" placeholder="Ex: Tour Horizon">
              </div>
              <div class="col-6">
                <label class="form-label fw-bold small text-uppercase text-muted">Client locataire</label>
                <input type="text" id="art-client-location" class="form-control" value="${article?.client_location || ''}" placeholder="Ex: Coffrage Boréal">
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold small text-uppercase text-muted">Emplacement en cour / entrepôt</label>
              <input type="text" id="art-emplacement" class="form-control" value="${article?.emplacement || ''}" placeholder="Ex: Cour A, Rack 3">
            </div>

            <div class="d-flex gap-2 mt-4">
              <button type="submit" class="btn btn-orange btn-lg flex-grow-1 fw-bold">Enregistrer l'item</button>
              <button type="button" class="btn btn-outline-secondary btn-lg" onclick="navigateTo('sections')">Annuler</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `;
}

async function saveArticle(e, id) {
  e.preventDefault();
  const data = {
    section_id: parseInt(document.getElementById("art-section-id").value) || 0,
    type_id: parseInt(document.getElementById("art-type-id").value) || 0,
    dimension_modele: document.getElementById("art-modele").value.trim(),
    couleur: document.getElementById("art-couleur").value,
    quantite_totale: parseInt(document.getElementById("art-total").value) || 0,
    quantite_en_chantier: parseInt(document.getElementById("art-chantier").value) || 0,
    quantite_en_location: parseInt(document.getElementById("art-location").value) || 0,
    quantite_en_reparation: parseInt(document.getElementById("art-reparation").value) || 0,
    seuil_alerte: 5,
    chantier_actuel: document.getElementById("art-chantier-actuel").value.trim(),
    client_location: document.getElementById("art-client-location").value.trim(),
    etat: "Bon",
    emplacement: document.getElementById("art-emplacement").value.trim()
  };
  if (id) {
    await db.articles.update(id, data);
    flash("Item mis à jour avec succès !", "success");
  } else {
    await db.articles.add(data);
    flash("Item ajouté et lié avec succès !", "success");
  }
  navigateTo("sections");
}

async function deleteArticle(id) {
  if (!confirm("Supprimer cet article ?")) return;
  await db.articles.delete(id);
  flash("Article supprimé.", "warning");
  renderDashboard();
}

// Initialisation au chargement
loadReadyToUseCatalogue().then(() => navigateTo("cages"));
</script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"index.html written successfully! File size: {len(html_content)} bytes")

