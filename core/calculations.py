from math import pow

def real_rate(nominal_rate: float, inflation: float) -> float:
    return ((1 + nominal_rate) / (1 + inflation)) - 1

def withdrawal_rate(monthly_income: float, patrimony: float) -> float:
    if patrimony <= 0:
        return 0.0
    return (monthly_income * 12) / patrimony

def future_value(initial: float, monthly_contribution: float,
                 annual_return: float, years: int) -> float:
    months = years * 12
    monthly_rate = pow(1 + annual_return, 1/12) - 1
    if monthly_rate == 0:
        return initial + monthly_contribution * months
    return (
        initial * pow(1 + monthly_rate, months)
        + monthly_contribution * ((pow(1 + monthly_rate, months) - 1) / monthly_rate)
    )

def future_real_value(nominal_value: float, inflation: float, years: int) -> float:
    return nominal_value / pow(1 + inflation, years)
