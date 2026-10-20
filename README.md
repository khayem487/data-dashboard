# Dashboard Data Achats

[![Démo en ligne](https://img.shields.io/badge/D%C3%A9mo-Vercel-295e94?logo=vercel)](https://khayem-data-dashboard.vercel.app/)

**[Ouvrir le tableau de bord](https://khayem-data-dashboard.vercel.app/)** — l'application Flask calcule les indicateurs avec Pandas et le navigateur les affiche avec Chart.js.

## Description

Ce projet est un **tableau de bord analytique** simulant le suivi des achats industriels pour une entreprise.
Il permet de visualiser rapidement les indicateurs clés (KPIs), les tendances mensuelles, la répartition des dépenses et une cascade budgétaire.

## Stack technique

- Python
- Flask
- Pandas
- NumPy
- Chart.js
- JavaScript (vanilla)

## Lancer le projet

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Générer les données :

```bash
python generate_data.py
```

3. Démarrer l'application Flask :

```bash
python app.py
```

4. Ouvrir dans le navigateur :

```text
http://localhost:5000
```

## API disponibles

- `GET /api/kpis`
- `GET /api/par_mois`
- `GET /api/par_categorie`
- `GET /api/par_fournisseur`
- `GET /api/cascade_budget`

## Déploiement et vérifications

Le projet utilise Python 3.12 sur Vercel. Le CSV de démonstration est inclus dans le déploiement ; les chemins de fichiers ne dépendent pas du dossier de lancement. Les assets sont servis depuis `public/static/`.

Les données sont **entièrement fictives**, générées avec une graine fixe : 200 achats sur 2023–2024. Cette démonstration n'est pas connectée au système d'information d'une entreprise. Elle ne requiert ni compte, ni base externe, ni identifiants.

Pour vérifier les cinq API contre un calcul indépendant à partir du CSV :

```bash
python tests/verify_dashboard.py
python tests/verify_dashboard.py https://khayem-data-dashboard.vercel.app
```

Le point de santé `GET /health` indique le statut et le nombre de lignes disponibles. Ce tableau de bord est en lecture seule ; aucun achat ne peut être modifié par un visiteur.

## Screenshots

*(à venir)*

## Auteur

Khayem Ben Ghorbel — github.com/khayem487
