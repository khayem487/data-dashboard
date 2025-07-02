from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

DATA_PATH = Path("data") / "achats.csv"
BUDGET_INITIAL = 500_000
CATEGORIES_ORDER = [
    "Matières premières",
    "Composants",
    "Outillage",
    "Logistique",
    "Services",
]


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Fichier data/achats.csv introuvable. Exécutez d'abord: python generate_data.py"
        )

    df = pd.read_csv(DATA_PATH)
    expected_cols = {"date", "fournisseur", "categorie", "montant", "statut"}
    if not expected_cols.issubset(df.columns):
        raise ValueError("Le CSV ne contient pas toutes les colonnes attendues.")

    df["montant"] = pd.to_numeric(df["montant"], errors="coerce").fillna(0.0)
    df["date"] = df["date"].astype(str)
    return df


df_achats = load_data()


def validated_df() -> pd.DataFrame:
    return df_achats[df_achats["statut"] == "Validé"].copy()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/kpis")
def api_kpis():
    valides = validated_df()

    total_achats = float(valides["montant"].sum())
    nb_commandes = int(len(valides))
    nb_fournisseurs = int(df_achats["fournisseur"].nunique())
    taux_validation = round((len(valides) / len(df_achats)) * 100, 1) if len(df_achats) else 0.0

    return jsonify(
        {
            "total_achats": total_achats,
            "nb_commandes": nb_commandes,
            "nb_fournisseurs": nb_fournisseurs,
            "taux_validation": taux_validation,
        }
    )


@app.route("/api/par_mois")
def api_par_mois():
    valides = validated_df()
    series = (
        valides.groupby("date", as_index=False)["montant"]
        .sum()
        .sort_values("date", ascending=True)
    )

    data = [
        {"mois": str(row["date"]), "total": round(float(row["montant"]), 2)}
        for _, row in series.iterrows()
    ]
    return jsonify(data)


@app.route("/api/par_categorie")
def api_par_categorie():
    valides = validated_df()
    series = (
        valides.groupby("categorie", as_index=False)["montant"]
        .sum()
        .sort_values("montant", ascending=False)
    )

    data = [
        {"categorie": str(row["categorie"]), "total": round(float(row["montant"]), 2)}
        for _, row in series.iterrows()
    ]
    return jsonify(data)


@app.route("/api/par_fournisseur")
def api_par_fournisseur():
    valides = validated_df()
    series = (
        valides.groupby("fournisseur", as_index=False)["montant"]
        .sum()
        .sort_values("montant", ascending=False)
        .head(5)
    )

    data = [
        {
            "fournisseur": str(row["fournisseur"]),
            "total": round(float(row["montant"]), 2),
        }
        for _, row in series.iterrows()
    ]
    return jsonify(data)


@app.route("/api/cascade_budget")
def api_cascade_budget():
    valides = validated_df()
    by_cat = valides.groupby("categorie")["montant"].sum().to_dict()

    waterfall = [{"label": "Budget initial", "value": BUDGET_INITIAL, "type": "total"}]

    total_spent = 0.0
    for cat in CATEGORIES_ORDER:
        cat_total = float(by_cat.get(cat, 0.0))
        total_spent += cat_total
        waterfall.append(
            {"label": cat, "value": round(-cat_total, 2), "type": "negative"}
        )

    remaining = BUDGET_INITIAL - total_spent
    waterfall.append(
        {"label": "Solde restant", "value": round(float(remaining), 2), "type": "total"}
    )

    return jsonify(waterfall)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
