"""FastMCP server exposing Singapore property calculators as MCP tools.

Run: python -m sg_property_mcp
Or:  sg-property-mcp (after pip install)
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from sg_property_mcp.tools import (
    lease_decay,
    mortgage,
    scorecard,
    stamp_duty,
    upgrade_paths,
)

# Optional: RAG search over 2025-2027 insights. Lives at the repo root.
try:
    from rag.search import list_topics as _rag_list_topics
    from rag.search import search_insights as _rag_search

    _RAG_AVAILABLE = True
except ImportError:
    import sys
    from pathlib import Path

    _repo_root = Path(__file__).resolve().parents[2]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
    try:
        from rag.search import list_topics as _rag_list_topics
        from rag.search import search_insights as _rag_search

        _RAG_AVAILABLE = True
    except ImportError:
        _RAG_AVAILABLE = False

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


# ---------- Upgrade / downgrade path tools ----------


@mcp.tool()
def analyze_upgrade_path(
    current_property: str,
    target_property: str,
    new_price: float,
    profile: str,
    marital_status: str,
    properties_after_new_buy: int = 1,
    keep_existing: bool = False,
    youngest_buyer_age: int = 40,
    spouse_ages: list[int] | None = None,
    hdb_flat_type_rooms: int = 4,
) -> dict[str, Any]:
    """Analyse residential upgrade/downgrade paths and return viable strategies.

    Args:
        current_property: HDB, EC, CONDO, or LANDED.
        target_property: HDB, EC, CONDO, or LANDED.
        new_price: Purchase price of target property in SGD.
        profile: SC, SPR, FOREIGNER, ENTITY, TRUSTEE.
        marital_status: SINGLE, MARRIED_SC_SC, MARRIED_SC_SPR,
            MARRIED_SC_FOREIGNER, MARRIED_SPR_SPR, MARRIED_OTHER.
        properties_after_new_buy: Total properties owned after this purchase.
        keep_existing: If True, plan to retain current property (triggers decoupling option).
        youngest_buyer_age: Youngest co-owner age.
        spouse_ages: [age_a, age_b] list for couples; for senior exemption checks.
        hdb_flat_type_rooms: 2, 3, 4, 5 for HDB target (senior exemption applies to <= 4).
    """
    spouse_tuple = tuple(spouse_ages) if spouse_ages else None
    return upgrade_paths.analyze_upgrade_path(
        current_property=current_property,
        target_property=target_property,
        new_price=new_price,
        profile=profile,
        marital_status=marital_status,
        properties_after_new_buy=properties_after_new_buy,
        keep_existing=keep_existing,
        youngest_buyer_age=youngest_buyer_age,
        spouse_ages=spouse_tuple,
        hdb_flat_type_rooms=hdb_flat_type_rooms,
    )


@mcp.tool()
def check_15_month_wait_out(
    target_hdb_rooms: int,
    youngest_buyer_age: int | None = None,
    spouse_ages: list[int] | None = None,
    target_is_new_bto: bool = False,
    has_otp_before_sep_2022: bool = False,
) -> dict[str, Any]:
    """Check whether the 15-month wait-out applies for private-to-HDB downgrade.

    Args:
        target_hdb_rooms: Number of rooms in target HDB (2-5).
        youngest_buyer_age: Single buyer's age or youngest co-buyer's age.
            If omitted, inferred from spouse_ages (min of the two).
        spouse_ages: [age_a, age_b] for couples; needed for senior exemption.
        target_is_new_bto: True for BTO (30-month wait), False for resale (15-month).
        has_otp_before_sep_2022: Documentary proof of OTP/sale before policy date.
    """
    spouse_tuple = tuple(spouse_ages) if spouse_ages else None
    return upgrade_paths.check_15_month_wait_out(
        target_hdb_rooms=target_hdb_rooms,
        spouse_ages=spouse_tuple,
        youngest_buyer_age=youngest_buyer_age,
        target_is_new_bto=target_is_new_bto,
        has_otp_before_sep_2022=has_otp_before_sep_2022,
    )


@mcp.tool()
def estimate_decoupling_cost(
    current_property_value: float,
    share_being_transferred: float = 0.50,
) -> dict[str, Any]:
    """Estimate cash cost of decoupling a jointly-owned private property.

    Args:
        current_property_value: Current market value (SGD).
        share_being_transferred: Fraction transferred (0.50 typical for spousal joint).
    """
    return upgrade_paths.estimate_decoupling_cost(
        current_property_value, share_being_transferred
    )


@mcp.tool()
def compare_decoupling_vs_absd(
    current_joint_property_value: float,
    new_property_price: float,
    profile: str,
    properties_after_new_buy: int,
) -> dict[str, Any]:
    """Compare decoupling cost vs paying ABSD on a planned second property.

    Args:
        current_joint_property_value: Current value of joint property.
        new_property_price: Planned new property price.
        profile: SC, SPR, FOREIGNER.
        properties_after_new_buy: Total properties owned after new purchase
            (used to determine ABSD rate if NOT decoupling).
    """
    return upgrade_paths.compare_decoupling_vs_absd(
        current_joint_property_value,
        new_property_price,
        profile,
        properties_after_new_buy,
    )


@mcp.tool()
def estimate_cpf_refund_at_sale(
    cpf_principal_used: float,
    years_held: float,
    accrued_rate: float = 0.025,
) -> dict[str, Any]:
    """Estimate CPF refund (principal + accrued interest) on property sale.

    Simplified linear-withdrawal approximation. For precise figures use CPF Home Calculator.

    Args:
        cpf_principal_used: Total CPF OA principal used on property.
        years_held: Years property has been held.
        accrued_rate: CPF accrued interest rate (default 0.025 = 2.5% p.a., OA rate).
    """
    return upgrade_paths.estimate_cpf_refund_at_sale(
        cpf_principal_used, years_held, accrued_rate
    )


@mcp.tool()
def estimate_transition_cash_flow(
    sell_price: float,
    sell_outstanding_loan: float,
    sell_cpf_refund_estimate: float,
    sell_agent_commission_rate: float,
    new_price: float,
    new_ltv_cap: float,
    new_min_cash_pct: float,
    new_bsd: float,
    new_absd_upfront: float,
    interim_months: int = 0,
    interim_rental_monthly: float = 0.0,
) -> dict[str, Any]:
    """End-to-end cashflow model for a sell + buy transition.

    Args:
        sell_price: Sale price of current property.
        sell_outstanding_loan: Outstanding mortgage to redeem.
        sell_cpf_refund_estimate: Estimated CPF refund.
        sell_agent_commission_rate: Decimal (e.g. 0.02). GST 9% added.
        new_price: New property purchase price.
        new_ltv_cap: Max LTV (0.75 first, 0.45 second).
        new_min_cash_pct: Min cash component (0.05 first, 0.25 second).
        new_bsd: BSD on new property.
        new_absd_upfront: ABSD cash outlay.
        interim_months: Months of interim rental.
        interim_rental_monthly: Monthly interim rent.
    """
    return upgrade_paths.estimate_transition_cash_flow(
        sell_price=sell_price,
        sell_outstanding_loan=sell_outstanding_loan,
        sell_cpf_refund_estimate=sell_cpf_refund_estimate,
        sell_agent_commission_rate=sell_agent_commission_rate,
        new_price=new_price,
        new_ltv_cap=new_ltv_cap,
        new_min_cash_pct=new_min_cash_pct,
        new_bsd=new_bsd,
        new_absd_upfront=new_absd_upfront,
        interim_months=interim_months,
        interim_rental_monthly=interim_rental_monthly,
    )


# ---------- RAG insights search (optional) ----------


if _RAG_AVAILABLE:

    @mcp.tool()
    def search_insights(
        query: str,
        top_k: int = 5,
        backend: str = "bm25",
        year_filter: int | None = None,
        segment_filter: str | None = None,
        tag_filter: str | None = None,
    ) -> dict[str, Any]:
        """Search the local 2025-2027 SG property insights corpus.

        Returns ranked passages with sources for grounded responses.

        Args:
            query: Free-text query (e.g. "2026 SORA forecast", "HDB MOP wave 2027").
            top_k: Number of results to return (default 5).
            backend: "bm25" (zero-dep) or "embeddings" (requires Ollama nomic-embed-text).
            year_filter: Optional year filter (2024-2027).
            segment_filter: Optional segment filter (private, hdb, ec, landed, rental).
            tag_filter: Optional tag filter (e.g. "absd", "mop", "gls", "sora").
        """
        return _rag_search(
            query=query,
            top_k=top_k,
            backend=backend,
            year_filter=year_filter,
            segment_filter=segment_filter,
            tag_filter=tag_filter,
        )

    @mcp.tool()
    def list_insight_topics() -> dict[str, Any]:
        """List all topics in the SG property insights corpus."""
        return _rag_list_topics()


def main() -> None:
    """Entrypoint for `python -m sg_property_mcp` and the console script."""
    mcp.run()


if __name__ == "__main__":
    main()
