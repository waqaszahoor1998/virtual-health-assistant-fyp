import csv
from pathlib import Path

import click
from flask import current_app
from flask.cli import with_appcontext

from app import db
from app.models.disease import Disease
from app.models.symptom import Symptom


def _repo_root() -> Path:
    # backend/app/cli/catalog.py -> parents[3] == repository root
    return Path(__file__).resolve().parents[3]


def _read_unique_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    out: list[str] = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            val = line.strip()
            if val:
                out.append(val)
    return out


def _read_symptom_disease_mapping(path: Path) -> tuple[set[str], set[str]]:
    """
    Parse data/processed/symptom_disease_mapping.csv.
    Expected header includes: symptom,disease,...
    """
    symptoms: set[str] = set()
    diseases: set[str] = set()
    if not path.exists():
        return symptoms, diseases
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = (row.get("symptom") or "").strip()
            d = (row.get("disease") or "").strip()
            if s:
                symptoms.add(s)
            if d:
                diseases.add(d)
    return symptoms, diseases


@click.command("build-catalog")
@click.option("--limit", type=int, default=0, help="Optional cap (0 = no cap).")
@with_appcontext
def build_catalog_command(limit: int):
    """
    Populate Symptom and Disease catalog tables (idempotent).

    Sources (in priority order):
      - Diseases: ml_models/models/unique_diseases.txt (if present)
      - Symptoms/diseases fallback: data/processed/symptom_disease_mapping.csv (if present)
    """
    db.create_all()

    repo_root = _repo_root()
    models_dir = Path(current_app.config.get("ML_MODELS_DIR", repo_root / "ml_models" / "models"))
    data_dir = Path(current_app.config.get("DATA_DIR", repo_root / "data"))

    diseases_txt = models_dir / "unique_diseases.txt"
    mapping_csv = data_dir / "processed" / "symptom_disease_mapping.csv"

    mapping_symptoms, mapping_diseases = _read_symptom_disease_mapping(mapping_csv)
    diseases_from_txt = _read_unique_lines(diseases_txt)

    disease_names: list[str] = diseases_from_txt or sorted(mapping_diseases)
    symptom_names: list[str] = sorted(mapping_symptoms)

    if limit and limit > 0:
        disease_names = disease_names[:limit]
        symptom_names = symptom_names[:limit]

    created_d = 0
    created_s = 0

    existing_d = {d.name for d in Disease.query.with_entities(Disease.name).all()}
    existing_s = {s.name for s in Symptom.query.with_entities(Symptom.name).all()}

    for name in disease_names:
        name = str(name).strip()
        if not name or name in existing_d:
            continue
        db.session.add(Disease(name=name))
        created_d += 1

    for name in symptom_names:
        name = str(name).strip()
        if not name or name in existing_s:
            continue
        db.session.add(Symptom(name=name))
        created_s += 1

    db.session.commit()

    click.echo("Catalog build complete.")
    click.echo(f"- diseases created: {created_d} (total now: {Disease.query.count()})")
    click.echo(f"- symptoms created: {created_s} (total now: {Symptom.query.count()})")

