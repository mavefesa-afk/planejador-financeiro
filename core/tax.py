def fixed_income_ir_rate(days: int) -> float:
    if days <= 180:
        return 0.225
    if days <= 360:
        return 0.20
    if days <= 720:
        return 0.175
    return 0.15

def net_return_rate(gross_return: float, ir_rate: float) -> float:
    return gross_return * (1 - ir_rate)
