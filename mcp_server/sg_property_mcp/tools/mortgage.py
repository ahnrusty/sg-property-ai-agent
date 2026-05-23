"""Mortgage payment and amortisation calculators."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MortgageResult:
    """Mortgage payment computation result."""

    monthly_payment: float
    total_interest: float
    total_paid: float
    principal: float
    rate: float
    tenure_years: int
    notes: list[str]


def monthly_payment(principal: float, annual_rate: float, tenure_years: int) -> float:
    """Standard PMT for fully amortising loan.

    Args:
        principal: Loan amount in SGD.
        annual_rate: Annual interest rate as decimal (e.g. 0.025 for 2.5%).
        tenure_years: Loan tenure in years.

    Returns:
        Monthly payment in SGD.
    """
    if principal <= 0:
        raise ValueError("principal must be > 0")
    if annual_rate < 0:
        raise ValueError("annual_rate must be >= 0")
    if tenure_years <= 0:
        raise ValueError("tenure_years must be > 0")

    n = tenure_years * 12
    r = annual_rate / 12

    if r == 0:
        return principal / n

    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def estimate_mortgage(
    principal: float, annual_rate: float, tenure_years: int
) -> MortgageResult:
    """Compute monthly payment and total interest for a given loan.

    Args:
        principal: Loan amount in SGD.
        annual_rate: Annual interest rate as decimal.
        tenure_years: Loan tenure in years.

    Returns:
        MortgageResult.
    """
    payment = monthly_payment(principal, annual_rate, tenure_years)
    total_paid = payment * tenure_years * 12
    total_interest = total_paid - principal

    return MortgageResult(
        monthly_payment=round(payment, 2),
        total_interest=round(total_interest, 2),
        total_paid=round(total_paid, 2),
        principal=principal,
        rate=annual_rate,
        tenure_years=tenure_years,
        notes=[
            f"Loan {principal:,.0f} at {annual_rate:.2%} over {tenure_years} years.",
            f"Monthly payment {payment:,.2f}.",
            f"Total interest paid {total_interest:,.2f} ({total_interest/principal:.0%} of principal).",
            "Indicative only. Actual rate depends on bank package and reset schedule.",
        ],
    )


def estimate_max_loan(
    gross_monthly_income: float,
    existing_monthly_debt: float,
    stress_rate: float = 0.04,
    tenure_years: int = 30,
    ratio: float = 0.55,
    msr_applicable: bool = False,
) -> dict:
    """Estimate max loan quantum given TDSR (and MSR if applicable).

    Args:
        gross_monthly_income: Gross monthly household income in SGD.
        existing_monthly_debt: Existing monthly debt obligations (other loans,
            credit cards min payments, car loans).
        stress_rate: Annual stress rate for affordability (default 4% for
            residential bank loan; use 3% for HDB loan).
        tenure_years: Loan tenure in years.
        ratio: 0.55 for TDSR (default), 0.30 if MSR-bound (HDB/EC).
        msr_applicable: If True, also check MSR (30%) and return the lower
            of TDSR / MSR result.

    Returns:
        dict with max_loan_tdsr, max_loan_msr (if applicable), max_loan, notes.
    """
    if gross_monthly_income <= 0:
        raise ValueError("gross_monthly_income must be > 0")
    if existing_monthly_debt < 0:
        raise ValueError("existing_monthly_debt must be >= 0")

    tdsr_headroom = gross_monthly_income * ratio - existing_monthly_debt
    if tdsr_headroom <= 0:
        return {
            "max_loan_tdsr": 0.0,
            "max_loan_msr": None,
            "max_loan": 0.0,
            "notes": [
                f"Existing debt {existing_monthly_debt:,.0f} already exceeds "
                f"TDSR headroom at {ratio:.0%} of {gross_monthly_income:,.0f} "
                f"= {gross_monthly_income * ratio:,.0f}.",
                "No room for new mortgage at this stress rate and tenure.",
            ],
        }

    n = tenure_years * 12
    r = stress_rate / 12
    if r == 0:
        max_loan_tdsr = tdsr_headroom * n
    else:
        max_loan_tdsr = tdsr_headroom * ((1 + r) ** n - 1) / (r * (1 + r) ** n)

    notes = [
        f"Gross monthly income: {gross_monthly_income:,.0f}",
        f"Existing debt: {existing_monthly_debt:,.0f}",
        f"TDSR headroom ({ratio:.0%}): {tdsr_headroom:,.0f}",
        f"Stress rate {stress_rate:.2%}, tenure {tenure_years} years.",
        f"Max loan (TDSR): {max_loan_tdsr:,.0f}",
    ]

    result: dict = {
        "max_loan_tdsr": round(max_loan_tdsr, 2),
        "max_loan_msr": None,
        "max_loan": round(max_loan_tdsr, 2),
        "notes": notes,
    }

    if msr_applicable:
        # MSR caps mortgage payment alone (no debt offset) at 30% of income.
        msr_headroom = gross_monthly_income * 0.30
        if r == 0:
            max_loan_msr = msr_headroom * n
        else:
            max_loan_msr = msr_headroom * ((1 + r) ** n - 1) / (r * (1 + r) ** n)

        result["max_loan_msr"] = round(max_loan_msr, 2)
        result["max_loan"] = round(min(max_loan_tdsr, max_loan_msr), 2)
        notes.extend(
            [
                f"MSR cap (30% of income): {msr_headroom:,.0f}",
                f"Max loan (MSR): {max_loan_msr:,.0f}",
                f"Binding constraint: {'MSR' if max_loan_msr < max_loan_tdsr else 'TDSR'}",
            ]
        )

    notes.append("Indicative only. Banks apply income haircuts on variable income.")
    return result


def check_tdsr_msr(
    proposed_monthly_payment: float,
    gross_monthly_income: float,
    existing_monthly_debt: float,
    msr_applicable: bool = False,
) -> dict:
    """Check whether a proposed mortgage payment passes TDSR (and MSR).

    Args:
        proposed_monthly_payment: New mortgage monthly payment at stress rate.
        gross_monthly_income: Gross monthly household income.
        existing_monthly_debt: Existing monthly debt obligations.
        msr_applicable: If True, also check MSR (30%).

    Returns:
        dict with tdsr_ratio, msr_ratio, passes, notes.
    """
    if gross_monthly_income <= 0:
        raise ValueError("gross_monthly_income must be > 0")

    tdsr_ratio = (
        proposed_monthly_payment + existing_monthly_debt
    ) / gross_monthly_income
    tdsr_pass = tdsr_ratio <= 0.55

    result: dict = {
        "tdsr_ratio": round(tdsr_ratio, 4),
        "tdsr_pass": tdsr_pass,
        "msr_ratio": None,
        "msr_pass": None,
        "passes": tdsr_pass,
        "notes": [
            f"TDSR = ({proposed_monthly_payment:,.0f} + {existing_monthly_debt:,.0f}) / "
            f"{gross_monthly_income:,.0f} = {tdsr_ratio:.2%} (cap 55%).",
        ],
    }

    if msr_applicable:
        msr_ratio = proposed_monthly_payment / gross_monthly_income
        msr_pass = msr_ratio <= 0.30
        result["msr_ratio"] = round(msr_ratio, 4)
        result["msr_pass"] = msr_pass
        result["passes"] = tdsr_pass and msr_pass
        result["notes"].append(
            f"MSR = {proposed_monthly_payment:,.0f} / {gross_monthly_income:,.0f} "
            f"= {msr_ratio:.2%} (cap 30%)."
        )

    result["notes"].append(
        "Both TDSR and MSR are computed at the stress rate, not actual borrowing rate."
    )
    return result
