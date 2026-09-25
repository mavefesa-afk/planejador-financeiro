from .database import get_connection

def save_profile(data):
    conn = get_connection()
    conn.execute("""
    INSERT INTO profile
    (id, age, horizon_years, situation, initial_patrimony,
     monthly_contribution, desired_monthly_income, minimum_monthly_income,
     risk_profile, liquidity_months, other_monthly_income, notes)
    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        age=excluded.age,
        horizon_years=excluded.horizon_years,
        situation=excluded.situation,
        initial_patrimony=excluded.initial_patrimony,
        monthly_contribution=excluded.monthly_contribution,
        desired_monthly_income=excluded.desired_monthly_income,
        minimum_monthly_income=excluded.minimum_monthly_income,
        risk_profile=excluded.risk_profile,
        liquidity_months=excluded.liquidity_months,
        other_monthly_income=excluded.other_monthly_income,
        notes=excluded.notes
    """, (
        data["age"], data["horizon_years"], data["situation"],
        data["initial_patrimony"], data["monthly_contribution"],
        data["desired_monthly_income"], data["minimum_monthly_income"],
        data["risk_profile"], data["liquidity_months"],
        data["other_monthly_income"], data["notes"]
    ))
    conn.commit()
    conn.close()

def get_profile():
    conn = get_connection()
    row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
    conn.close()
    return dict(row) if row else None
