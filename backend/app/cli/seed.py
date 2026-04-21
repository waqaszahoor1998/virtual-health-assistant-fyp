import json
from datetime import datetime, timedelta, timezone

import click
from flask.cli import with_appcontext

from app import db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.diagnosis import Diagnosis
from app.models.prescription import Prescription


DEMO_PASSWORD = "demo123"


def _get_or_create_user(email: str, role: str) -> tuple[User, bool]:
    user = User.query.filter_by(email=email).first()
    if user:
        return user, False
    user = User(email=email, role=role)
    user.set_password(DEMO_PASSWORD)
    db.session.add(user)
    db.session.flush()
    return user, True


def _get_or_create_doctor_for_user(user: User) -> tuple[Doctor, bool]:
    doctor = Doctor.query.filter_by(user_id=user.id).first()
    if doctor:
        return doctor, False
    doctor = Doctor(
        user_id=user.id,
        first_name="Rehan",
        last_name="Khan",
        specialization="General Medicine",
        license_number="DEMO-LIC-1001",
        phone="0300-0000000",
        hospital_clinic="Demo Clinic",
        address="123 Demo Street",
    )
    db.session.add(doctor)
    db.session.flush()
    return doctor, True


def _get_or_create_patient_for_user(user: User, first_name: str, last_name: str, phone: str) -> tuple[Patient, bool]:
    patient = Patient.query.filter_by(user_id=user.id).first()
    if patient:
        return patient, False
    patient = Patient(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        gender=None,
        address="Demo Address",
        blood_type="O+",
        allergies=json.dumps(["Penicillin"]),
        medical_history=json.dumps({"past_conditions": ["Hypertension"]}),
    )
    db.session.add(patient)
    db.session.flush()
    return patient, True


def _ensure_demo_appointments(doctor: Doctor, patients: list[Patient]) -> int:
    created = 0
    now = datetime.now(timezone.utc)
    for idx, patient in enumerate(patients[:2]):
        existing = Appointment.query.filter_by(patient_id=patient.id, doctor_id=doctor.id).first()
        if existing:
            continue
        appt = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=(now + timedelta(days=idx + 1)).replace(microsecond=0).replace(tzinfo=None),
            status="scheduled",
            reason="Demo checkup",
            notes="Seeded appointment for demo",
        )
        db.session.add(appt)
        created += 1
    return created


def _ensure_demo_diagnoses(doctor: Doctor, patients: list[Patient]) -> int:
    created = 0
    seed_cases: list[tuple[list[str], str, str]] = [
        (["fever", "cough", "sore throat"], "Influenza", "Likely viral infection; rest and hydration."),
        (["headache", "nausea", "sensitivity to light"], "Migraine", "Classic migraine pattern; avoid triggers."),
    ]
    for patient, (symptoms, confirmed, notes) in zip(patients, seed_cases, strict=False):
        existing = Diagnosis.query.filter_by(patient_id=patient.id, doctor_id=doctor.id).first()
        if existing:
            continue
        predicted = [
            {"disease": confirmed, "confidence": 0.82},
            {"disease": "Common Cold", "confidence": 0.41},
            {"disease": "Sinusitis", "confidence": 0.22},
        ]
        diag = Diagnosis(
            patient_id=patient.id,
            doctor_id=doctor.id,
            symptoms=json.dumps(symptoms),
            predicted_diseases=json.dumps(predicted),
            confirmed_disease=confirmed,
            notes=notes,
        )
        db.session.add(diag)
        db.session.flush()
        created += 1
    return created


def _ensure_demo_prescription(doctor: Doctor, patient: Patient) -> int:
    diagnosis = Diagnosis.query.filter_by(patient_id=patient.id, doctor_id=doctor.id).first()
    if not diagnosis:
        return 0
    existing = Prescription.query.filter_by(diagnosis_id=diagnosis.id).first()
    if existing:
        return 0
    rx = Prescription(
        diagnosis_id=diagnosis.id,
        patient_id=patient.id,
        doctor_id=doctor.id,
        drugbank_id="DB00945",
        drug_name="Aspirin",
        dosage="500mg",
        frequency="Twice daily",
        duration="3 days",
        instructions="Take with food",
    )
    db.session.add(rx)
    return 1


@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Seed the database with deterministic demo data."""
    created_counts = {
        "users": 0,
        "doctor_profiles": 0,
        "patient_profiles": 0,
        "appointments": 0,
        "diagnoses": 0,
        "prescriptions": 0,
    }

    # Ensure tables exist (works with SQLite demo mode + create_all in dev).
    db.create_all()

    doctor_user, created = _get_or_create_user("doctor1@demo.com", "doctor")
    created_counts["users"] += int(created)
    doctor, created = _get_or_create_doctor_for_user(doctor_user)
    created_counts["doctor_profiles"] += int(created)

    patient_specs = [
        ("patient1@demo.com", "Ayesha", "Ali", "0301-1111111"),
        ("patient2@demo.com", "Bilal", "Hussain", "0302-2222222"),
        ("patient3@demo.com", "Sara", "Khan", "0303-3333333"),
    ]
    patients: list[Patient] = []
    for email, first, last, phone in patient_specs:
        u, created = _get_or_create_user(email, "patient")
        created_counts["users"] += int(created)
        p, created = _get_or_create_patient_for_user(u, first, last, phone)
        created_counts["patient_profiles"] += int(created)
        patients.append(p)

    created_counts["appointments"] += _ensure_demo_appointments(doctor, patients)
    created_counts["diagnoses"] += _ensure_demo_diagnoses(doctor, patients)
    created_counts["prescriptions"] += _ensure_demo_prescription(doctor, patients[0])

    db.session.commit()

    click.echo("Seed complete.")
    for k, v in created_counts.items():
        click.echo(f"- {k}: {v}")

