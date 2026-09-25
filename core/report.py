from .calculations import real_rate, withdrawal_rate

def portfolio_text(profile, assets, macro):
    lines = []
    if profile:
        lines.append(f"Patrimônio informado: R$ {profile['initial_patrimony']:,.2f}")
        lines.append(f"Renda mensal desejada: R$ {profile['desired_monthly_income']:,.2f}")
        lines.append(f"Taxa de retirada anual: {withdrawal_rate(profile['desired_monthly_income'], profile['initial_patrimony']):.2%}")
    if macro:
        rr = real_rate(macro["selic"], macro["ipca_12m"])
        lines.append(f"Juro real aproximado: {rr:.2%}")
    lines.append(f"Ativos cadastrados: {len(assets)}")
    return "\n".join(lines)
