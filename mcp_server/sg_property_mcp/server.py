"""FastMCP server exposing Singapore property calculators as MCP tools.

Run: python -m sg_property_mcp
Or:  sg-property-mcp (after pip install)
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from sg_property_mcp.tools import lease_decay, mortgage, scorecard, stamp_duty

mcp = FastMCP(
    name="sg-property",
    instructions=(
        "Singapore residential property calculators. All policy figures are "
        "illustrative and were correct at time of writing. Always re-verify "
        "against IRAS, HDB, URA, MAS, and CPF Board before any transaction. "
        "This server does not provide legal, tax, or financial advice."
    ),
)


# ---------- Stamp duty tools ----------


@mcp.tool()
def calculate_bsd(
    consideration: float, property_type: str = "residential"
) -> dict[str, Any]:
    """Compute Buyer's Stamp Duty on the higher of price or market value.

    Args:
        consideration: Purchase price or market value (SGD), whichever is higher.
        property_type: "residential" or "non_residential".
    """
    r = stamp_duty.calculate_bsd(consideration, property_type)
    return {"total": r.total, "breakdown": r.breakdown, "notes": r.notes}


@mcp.tool()
def calculate_absd(
    consideration: float,
    profile: str,
    property_count_after_purchase: int,
) -> dict[str, Any]:
    """Compute Additional Buyer's Stamp Duty.

    Args:
        consideration: Purchase price or market value (SGD), whichever is higher.
        profile: One of SC, SPR, FOREIGNER, ENTITY, TRUSTEE.
        property_count_after_purchase: Total residential properties owned
            after this purchase (this purchase = property #N).
    """
    r = stamp_duty.calculate_absd(consideration, profile, property_count_after_purchase)
    return {"total": r.total, "breakdown": r.breakdown, "notes": r.notes}


@mcp.tool()
def calculate_ssd(consideration: float, holding_period_months: int) -> dict[str, Any]:
    """Compute Seller's Stamp Duty on residential disposal.

    Args:
        consideration: Sale price or market value (SGD), whichever is higher.
        holding_period_months: Months elapsed between purchase OTP and sale OTP.
    """
    r = stamp_duty.calculate_ssd(consideration, holding_period_months)
    return {"total": r.total, "breakdown": r.breakdown, "notes": r.notes}


# ---------- Mortgage / affordability tools ----------


@mcp.tool()
def estimate_mortgage(
    principal: float, annual_rate: float, tenure_years: int
) -> dict[str, Any]:
    """Estimate monthly mortgage payment and total interest.

    Args:
        principal: Loan amount in SGD.
        annual_rate: Annual interest rate as decimal (e.g. 0.025 for 2.5%).
        tenure_years: Loan tenure in years.
    """
    r = mortgage.estimate_mortgage(principal, annual_rate, tenure_years)
    return {
        "monthly_payment": r.monthly_payment,
        "total_interest": r.total_interest,
        "total_paid": r.total_paid,
        "principal": r.principal,
        "annual_rate": r.rate,
        "tenure_years": r.tenure_years,
        "notes": r.notes,
    }


@mcp.tool()
def estimate_max_loan(
    gross_monthly_income: float,
    existing_monthly_debt: float = 0.0,
    stress_rate: float = 0.04,
    tenure_years: int = 30,
    ratio: float = 0.55,
    msr_applicable: bool = False,
) -> dict[str, Any]:
    """Estimate max loan quantum given TDSR (and MSR if HDB/EC).

    Args:
        gross_monthly_income: Gross monthly household income in SGD.
        existing_monthly_debt: Other monthly debt obligations.
        stress_rate: Annual stress rate (default 0.04 residential bank; use 0.03 for HDB loan).
        tenure_years: Loan tenure.
        ratio: TDSR ratio (default 0.55).
        msr_applicable: Set True for HDB and EC from developer.
    """
    return mortgage.estimate_max_loan(
        gross_monthly_income,
        existing_monthly_debt,
        stress_rate,
        tenure_years,
        ratio,
        msr_applicable,
    )


@mcp.tool()
def check_tdsr_msr(
    proposed_monthly_payment: float,
    gross_monthly_income: float,
    existing_monthly_debt: float = 0.0,
    msr_applicable: bool = False,
) -> dict[str, Any]:
    """Check whether a proposed mortgage payment passes TDSR (and MSR).

    Args:
        proposed_monthly_payment: New mortgage monthly payment at stress rate.
        gross_monthly_income: Gross monthly household income.
        existing_monthly_debt: Existing monthly debt obligations.
        msr_applicable: Set True for HDB and EC from developer.
    """
    return mortgage.check_tdsr_msr(
        proposed_monthly_payment,
        gross_monthly_income,
        existing_monthly_debt,
        msr_applicable,
    )


# ---------- Lease decay / CPF tools ----------


@mcp.tool()
def lease_decay_value(
    freehold_equivalent_value: float, years_remaining: float
) -> dict[str, Any]:
    """Estimate leasehold value using Bala's Curve.

    Args:
        freehold_equivalent_value: Hypothetical price if freehold (SGD).
        years_remaining: Remaining lease years at point of valuation.
    """
    return lease_decay.lease_decay_value(freehold_equivalent_value, years_remaining)


@mcp.tool()
def cpf_usage_limit(
    valuation_limit: float,
    years_remaining: float,
    youngest_buyer_age: int,
) -> dict[str, Any]:
    """Compute CPF OA usage cap based on lease-to-age-95 rule.

    Args:
        valuation_limit: Lower of price or property valuation (SGD).
        years_remaining: Remaining lease years at purchase.
        youngest_buyer_age: Age of youngest co-owner.
    """
    return lease_decay.cpf_usage_limit(
        valuation_limit, years_remaining, youngest_buyer_age
    )


# ---------- Listing comparison ----------


@mcp.tool()
def score_listing(listing: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
    """Score a single listing against weighted criteria.

    Args:
        listing: dict with keys like price, beds, baths, sqft, mrt_min, tenure_years_left.
        criteria: dict with max_price, min_beds, max_mrt_min, min_sqft,
            min_tenure_years_left, and optional weights dict.
    """
    return scorecard.score_listing(listing, criteria)


@mcp.tool()
def compare_listings(
    listings: list[dict[str, Any]], criteria: dict[str, Any]
) -> dict[str, Any]:
    """Rank multiple listings against the same criteria.

    Args:
        listings: list of listing dicts; each should include a "name" key.
        criteria: same shape as score_listing criteria.
    """
    return scorecard.compare_listings(listings, criteria)


@mcp.tool()
def psf_calc(
    price: float | None = None,
    sqft: float | None = None,
    psf: float | None = None,
    sqm: float | None = None,
) -> dict[str, Any]:
    """Convert between price, size, and $/psf.

    Supply any two of (price, sqft or sqm, psf) and the third is computed.
    """
    return scorecard.psf_calc(price=price, sqft=sqft, psf=psf, sqm=sqm)


def main() -> None:
    """Entrypoint for `python -m sg_property_mcp` and the console script."""
    mcp.run()


if __name__ == "__main__":
    main()
