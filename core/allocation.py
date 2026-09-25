def validate_allocation(targets: dict) -> tuple[bool, float]:
    total = sum(float(v or 0) for v in targets.values())
    return abs(total - 100.0) < 0.0001, total

def target_value(patrimony: float, target_percent: float) -> float:
    return patrimony * (target_percent / 100)
