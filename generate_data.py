import os
from pathlib import Path

import numpy as np
import pandas as pd


def generate_achats_csv(output_path: Path, n_rows: int = 200) -> None:
    np.random.seed(42)

    months = pd.period_range("2023-01", "2024-12", freq="M").astype(str)

    fournisseurs = [f"Fournisseur {chr(65 + i)}" for i in range(10)]
    categories = [
        "Matières premières",
        "Composants",
        "Outillage",
        "Logistique",
        "Services",
    ]
    statuts = ["Validé", "En cours", "Annulé"]

    # Distribution réaliste: beaucoup de montants moyens, quelques élevés
    base = np.random.lognormal(mean=9.2, sigma=0.6, size=n_rows)
    montants = np.clip(base, 1000, 50000).round(2)

    df = pd.DataFrame(
        {
            "date": np.random.choice(months, size=n_rows),
            "fournisseur": np.random.choice(fournisseurs, size=n_rows),
            "categorie": np.random.choice(
                categories, size=n_rows, p=[0.28, 0.24, 0.14, 0.18, 0.16]
            ),
            "montant": montants,
            "statut": np.random.choice(statuts, size=n_rows, p=[0.7, 0.2, 0.1]),
        }
    )

    # Tri pour une lecture plus naturelle
    df = df.sort_values(by=["date", "fournisseur"]).reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    out = Path("data") / "achats.csv"
    generate_achats_csv(out)
    print(f"CSV généré: {os.path.abspath(out)}")
