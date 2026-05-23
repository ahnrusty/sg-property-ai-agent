"""Lease decay and CPF usage cap helpers.

Bala's Curve is the SLA reference for land value vs remaining lease.
Values approximate the published Bala's Table.
"""

from __future__ import annotations

# Approximation of Bala's Curve (SLA): years remaining -> retention factor of freehold.
BALAS_CURVE: dict[int, float] = {
    99: 0.96,
    95: 0.955,
    90: 0.94,
    85: 0.93,
    80: 0.92,
    75: 0.91,
    70: 0.90,
    65: 0.88,
    60: 0.86,
    55: 0.84,
    50: 0.81,
    45: 0.77,
    40: 0.73,
    35: 0.67,
    30: 0.60,
    25: 0.51,
    20: 0.41,
    15: 0.30,
    10: 0.18,
    5: 0.08,
    0: 0.00,
}


def lease_decay_factor(years_remaining: float) -> float:
    """Interpolate Bala's Curve factor for given years remaining.

    Args:
        years_remaining: Remaining lease in years (can be fractional).

    Returns:
        Retention factor as decimal (0.0 to ~0.96).
    """
    if years_remaining <= 0:
        return 0.0
    if years_remaining >= 99:
        return BALAS_CURVE[99]

    sorted_keys = sorted(BALAS_CURVE.keys())
    for i in range(len(sorted_keys) - 1):
        lo, hi = sorted_keys[i], sorted_keys[i + 1]
        if lo <= years_remaining <= hi:
            frac = (years_remaining - lo) / (hi - lo)
            return BALAS_CURVE[lo] + frac * (BALAS_CURVE[hi] - BALAS_CURVE[lo])

    return 0.0


def lease_decay_value(freehold_equivalent_value: float, years_remaining: float) -> dict:
    """Estimate value of a leasehold property given a freehold benchmark.

    Args:
        freehold_equivalent_value: Hypothetical value if freehold (SGD).
        years_remaining: Remaining lease years.

    Returns:
        dict with factor, estimated_value, notes.
    """
    if freehold_equivalent_value <= 0:
        raise ValueError("freehold_equivalent_value must be > 0")

    factor = lease_decay_factor(years_remaining)
    estimated = freehold_equivalent_value * factor

    return {
        "years_remaining": years_remaining,
        "balas_factor": round(factor, 4),
        "freehold_equivalent_value": freehold_equivalent_value,
        "estimated_leasehold_value": round(estimated, 2),
        "notes": [
            f"At {years_remaining:.1f} years remaining, Bala's Curve factor ≈ "
            f"{factor:.0%} of freehold value.",
            "Bala's Curve is the SLA reference for land-value retention vs "
            "remaining lease.",
            "Actual market price also depends on location, condition, and "
            "buyer pool, not just curve.",
        ],
    }


def cpf_usage_limit(
    valuation_limit: float,
    years_remaining: float,
    youngest_buyer_age: int,
) -> dict:
    """Compute CPF OA usage cap based on lease vs age-95 rule.

    Args:
        valuation_limit: The lower of purchase price or property valuation (SGD).
        years_remaining: Remaining lease years at time of purchase.
        youngest_buyer_age: Age of youngest co-owner.

    Returns:
        dict with cpf_cap, withdrawal_limit, pro_rate_factor, notes.
    """
    if valuation_limit <= 0:
        raise ValueError("valuation_limit must be > 0")
    if youngest_buyer_age < 0 or youngest_buyer_age > 100:
        raise ValueError("youngest_buyer_age must be 0–100")

    years_to_age_95 = max(0, 95 - youngest_buyer_age)
    years_to_age_65 = max(0, 65 - youngest_buyer_age)

    notes: list[str] = []

    if years_remaining < years_to_age_65:
        cpf_cap = 0.0
        factor = 0.0
        notes.append(
            "Remaining lease does NOT cover youngest buyer to age 65. "
            "No CPF can be used."
        )
    elif years_remaining >= years_to_age_95:
        cpf_cap = valuation_limit
        factor = 1.0
        notes.append(
            "Remaining lease covers youngest buyer to age 95 or beyond. "
            "Full Valuation Limit CPF use allowed."
        )
    else:
        factor = years_remaining / years_to_age_95 if years_to_age_95 > 0 else 1.0
        cpf_cap = valuation_limit * factor
        notes.append(
            f"Remaining lease ({years_remaining:.1f} yrs) does not cover "
            f"youngest buyer to age 95. CPF use is pro-rated to "
            f"{factor:.0%} of Valuation Limit."
        )

    withdrawal_limit = valuation_limit * 1.20 * factor
    notes.extend(
        [
            f"Valuation Limit: {valuation_limit:,.0f}",
            f"Pro-rate factor: {factor:.2%}",
            f"CPF cap (initial): {cpf_cap:,.0f}",
            f"Withdrawal Limit (120%): {withdrawal_limit:,.0f} (subject to BRS rules above age 55).",
            "Verify on CPF Home Calculators before transacting.",
        ]
    )

    return {
        "valuation_limit": valuation_limit,
        "years_remaining": years_remaining,
        "youngest_buyer_age": youngest_buyer_age,
        "pro_rate_factor": round(factor, 4),
        "cpf_cap": round(cpf_cap, 2),
        "withdrawal_limit": round(withdrawal_limit, 2),
        "notes": notes,
    }
