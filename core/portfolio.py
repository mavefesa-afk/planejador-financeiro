from .database import get_connection
from .profile import get_profile

def money(v):
    return float(v or 0)

def recalc_percentages():
    conn = get_connection()
    total = conn.execute("SELECT COALESCE(SUM(total_value), 0) FROM assets").fetchone()[0]
    if total > 0:
        conn.execute(
            "UPDATE assets SET current_percent = (total_value / ?) * 100",
            (total,),
        )
    else:
        conn.execute("UPDATE assets SET current_percent = 0")
    conn.commit()
    conn.close()

def add_asset(data):
    conn = get_connection()
    conn.execute("""
        INSERT INTO assets
        (ticker, name, asset_class, quantity, unit_price, total_value,
         target_percent, current_percent, action, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
    """, (
        data["ticker"].upper().strip(),
        data["name"].strip(),
        data["asset_class"],
        money(data["quantity"]),
        money(data["unit_price"]),
        money(data["total_value"]),
        money(data["target_percent"]),
        data["action"],
        data["notes"],
    ))
    conn.commit()
    conn.close()
    recalc_percentages()

def delete_asset(asset_id):
    conn = get_connection()
    conn.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    conn.commit()
    conn.close()
    recalc_percentages()

def get_assets():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM assets ORDER BY total_value DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def portfolio_summary():
    profile = get_profile()
    assets = get_assets()
    total = sum(money(a["total_value"]) for a in assets)
    return {
        "total_value": total,
        "asset_count": len(assets),
        "class_count": len({a["asset_class"] for a in assets}),
        "profile": (profile or {}).get("risk_profile", "Não informado"),
    }
