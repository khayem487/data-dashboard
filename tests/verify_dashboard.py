"""Check every deployed aggregate against the original CSV with an independent reader.

Run without arguments for Flask's local test client, or pass a deployment origin.
No requests modify application data.
"""

import csv
import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def expected():
    with (ROOT / "data" / "achats.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    approved = [row for row in rows if row["statut"] == "Validé"]
    grouped = {}
    for field in ("date", "categorie", "fournisseur"):
        sums = defaultdict(Decimal)
        for row in approved:
            sums[row[field]] += Decimal(row["montant"])
        grouped[field] = sums
    total = sum((Decimal(row["montant"]) for row in approved), Decimal(0))
    result = {
        "/api/kpis": {
            "total_achats": float(total),
            "nb_commandes": len(approved),
            "nb_fournisseurs": len({row["fournisseur"] for row in rows}),
            "taux_validation": round(len(approved) / len(rows) * 100, 1),
        },
        "/api/par_mois": [
            {"mois": key, "total": float(value)}
            for key, value in sorted(grouped["date"].items())
        ],
        "/api/par_categorie": [
            {"categorie": key, "total": float(value)}
            for key, value in sorted(grouped["categorie"].items(), key=lambda item: item[1], reverse=True)
        ],
        "/api/par_fournisseur": [
            {"fournisseur": key, "total": float(value)}
            for key, value in sorted(grouped["fournisseur"].items(), key=lambda item: item[1], reverse=True)[:5]
        ],
    }
    categories = ("Matières premières", "Composants", "Outillage", "Logistique", "Services")
    result["/api/cascade_budget"] = (
        [{"label": "Budget initial", "value": 500_000, "type": "total"}]
        + [{"label": category, "value": float(-grouped["categorie"][category]), "type": "negative"} for category in categories]
        + [{"label": "Solde restant", "value": float(Decimal(500_000) - total), "type": "total"}]
    )
    return rows, result


def normalized(value):
    if isinstance(value, float):
        return round(value, 2)
    if isinstance(value, dict):
        return {key: normalized(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalized(item) for item in value]
    return value


def main():
    origin = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else None
    if origin:
        def get(path):
            with urlopen(origin + path, timeout=60) as response:
                assert response.status == 200, (path, response.status)
                return response.read()
    else:
        from app import app
        client = app.test_client()

        def get(path):
            response = client.get(path)
            assert response.status_code == 200, (path, response.status_code)
            return response.data

    rows, aggregates = expected()
    for path, target in aggregates.items():
        actual = json.loads(get(path))
        assert normalized(actual) == normalized(target), (path, actual, target)
        print("PASS", path)
    health = json.loads(get("/health"))
    assert health == {"status": "ok", "rows": len(rows), "dataset": "synthetic-demo"}, health
    assert b"--primary" in get("/static/style.css")
    page = get("/").decode("utf-8")
    assert page.count("<canvas ") == 4
    assert "données fictives" in page
    print("PASS /health, stylesheet, page and four chart containers")
    print(json.dumps({"origin": origin or "local-test-client", "rows": len(rows), "kpis": aggregates["/api/kpis"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
