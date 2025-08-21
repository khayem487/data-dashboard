# Dashboard Data Achats

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

## Screenshots

*(à venir)*

## Auteur

Khayem Ben Ghorbel — github.com/khayem487
