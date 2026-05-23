"""Upgrade and downgrade path analysers.

Helpers for evaluating HDB->Condo, Condo->Landed, Landed->Condo, Condo->HDB
and related transitions. All policy figures are illustrative and current
as of 2026; verify with IRAS, HDB, MAS, and CPF Board before executing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from sg_property_mcp.tools.stamp_duty import calculate_absd, calculate_bsd

PropertyType = Literal["HDB", "EC", "CONDO", "LANDED"]
Profile = Literal["SC", "SPR", "FOREIGNER", "ENTITY", "TRUSTEE"]
MaritalStatus = Literal[
    "SINGLE",
    "MARRIED_SC_SC",
    "MARRIED_SC_SPR",
    "MARRIED_SC_FOREIGNER",
    "MARRIED_SPR_SPR",
    "MARRIED_OTHER",
]


@dataclass
class TransitionPlan:
    """Output of upgrade/downgrade path analyser."""

    path_label: str
    strategy: str
    eligible: bool
    absd_cash_upfront: float
    absd_refundable: float
    absd_net: float
    bsd: float
    ltv_cap: float
    estimated_min_cash: float
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    timeline_weeks: tuple[int, int] | None = None


def _absd_rate_for_count(profile: Profile, count_after: int) -> float:
    """Look up the ABSD rate for a buyer profile and post-purchase property count."""
    bucket = min(3, max(1, count_after))
    result = calculate_absd(1.0, profile, bucket)
    # rate = total / consideration
    return result.total


def _hdb_to_condo(
    new_price: float,
    profile: Profile,
    marital_status: MaritalStatus,
    properties_after_new_buy: int,
) -> list[TransitionPlan]:
    """Generate HDB→Condo strategies."""

    bsd = calculate_bsd(new_price).total
    plans: list[TransitionPlan] = []

    # --- Sell First ---
    absd_sf = calculate_absd(
        new_price, profile, max(1, properties_after_new_buy - 1)
    ).total
    plans.append(
        TransitionPlan(
            path_label="HDB → Condo",
            strategy="Sell HDB First (no ABSD overhang)",
            eligible=True,
            absd_cash_upfront=absd_sf,
            absd_refundable=0.0,
            absd_net=absd_sf,
            bsd=bsd,
            ltv_cap=0.75,
            estimated_min_cash=new_price * 0.05 + bsd + absd_sf + 5_000,
            pros=[
                "Zero ABSD if condo is first property after HDB sale",
                "Maximum 75% LTV on new condo",
                "Cash position known before committing to new purchase",
                "No 6-month deadline pressure",
            ],
            cons=[
                "2-3 months interim rental needed (~$10k-$20k)",
                "Two moves (HDB → rental → condo)",
                "Market risk: condo prices may rise during your wait",
                "HDB sale price uncertain at planning stage",
            ],
            notes=[
                "Recommended for tight liquidity or non-SC-married-couple profiles.",
                "Plan HDB sale 4-6 months before target condo OTP.",
            ],
            timeline_weeks=(16, 32),
        )
    )

    # --- Buy First with 6-Month Remission (SC married couple only) ---
    is_sc_couple = marital_status == "MARRIED_SC_SC"
    absd_bf = calculate_absd(
        new_price, profile, max(2, properties_after_new_buy + 1)
    ).total
    plans.append(
        TransitionPlan(
            path_label="HDB → Condo",
            strategy="Buy Condo First, Sell HDB Within 6 Months (ABSD Remission)",
            eligible=is_sc_couple,
            absd_cash_upfront=absd_bf,
            absd_refundable=absd_bf if is_sc_couple else 0.0,
            absd_net=0.0 if is_sc_couple else absd_bf,
            bsd=bsd,
            ltv_cap=0.45,
            estimated_min_cash=new_price * 0.05 + absd_bf + bsd + 5_000,
            pros=[
                "No interim rental, no double move",
                "Lock in condo at known price",
                "Continuity of housing",
            ],
            cons=[
                "Pay 20% ABSD UPFRONT in cash (refunded if sale completes in 6 months)",
                "LTV drops to 45% while holding both → 55% down payment",
                "HARD 6-month deadline; miss by 1 day = ABSD forfeited",
                "ABSD cash float of $200k-$500k for up to 6 months",
                "Bridging loan may be needed (4-6% pa)",
            ],
            notes=[
                "Eligibility: SC married couple, both on both transactions.",
                "6 months runs from condo legal completion (resale) or TOP/CSC (new launch).",
                "Plan to list HDB IMMEDIATELY on signing condo OTP.",
                "Not available to: SC singles, SPR couples, SC+Foreigner couples (except FTA citizens).",
            ],
            timeline_weeks=(20, 28),
        )
    )

    return plans


def _condo_to_landed(
    new_price: float,
    profile: Profile,
    marital_status: MaritalStatus,
    properties_after_new_buy: int,
    keep_existing_condo: bool = False,
) -> list[TransitionPlan]:
    """Generate Condo→Landed strategies."""

    plans: list[TransitionPlan] = []
    bsd = calculate_bsd(new_price).total

    # Landed eligibility check
    foreigner_blocked = profile in ("FOREIGNER", "SPR")
    if foreigner_blocked:
        plans.append(
            TransitionPlan(
                path_label="Condo → Landed",
                strategy="LDAU Approval Required (Foreigner / SPR)",
                eligible=False,
                absd_cash_upfront=0.0,
                absd_refundable=0.0,
                absd_net=0.0,
                bsd=0.0,
                ltv_cap=0.0,
                estimated_min_cash=0.0,
                pros=[],
                cons=[
                    "Foreigners and Singapore PRs cannot buy mainland landed without LDAU approval",
                    "LDAU approval is discretionary; granted rarely",
                    "Sentosa Cove is the sole exception for foreigners (one landed unit for own-occupation)",
                ],
                notes=[
                    "Apply to Land Dealings Approval Unit (SLA) before any purchase commitment.",
                    "Approval typically requires demonstrated economic contribution to Singapore.",
                ],
            )
        )
        return plans

    if not keep_existing_condo:
        # Standard sell-and-buy paths
        plans.extend(
            _hdb_to_condo(new_price, profile, marital_status, properties_after_new_buy)
        )
        for plan in plans:
            plan.path_label = "Condo → Landed"

    # --- Decoupling Play (Condo→Landed retaining condo) ---
    if keep_existing_condo and marital_status in (
        "MARRIED_SC_SC",
        "MARRIED_SC_SPR",
        "MARRIED_SPR_SPR",
    ):
        # Spouse A buys landed as first property after decoupling.
        absd_dc = calculate_absd(new_price, profile, 1).total
        plans.append(
            TransitionPlan(
                path_label="Condo → Landed (keep condo)",
                strategy="Decouple Condo, Then Buy Landed in Transferring Spouse's Name",
                eligible=True,
                absd_cash_upfront=absd_dc,
                absd_refundable=0.0,
                absd_net=absd_dc,
                bsd=bsd,
                ltv_cap=0.75,
                estimated_min_cash=new_price * 0.05 + bsd + absd_dc + 35_000 + 5_000,
                pros=[
                    "Retain condo for rental income or family use",
                    "ABSD on landed = 0% (transferring spouse buys as first property)",
                    "Maximum 75% LTV on landed",
                    "Massive ABSD savings vs paying full second-property ABSD",
                ],
                cons=[
                    "Decoupling cost ~$25k-$40k (BSD on transfer + legal + admin)",
                    "Remaining spouse must independently qualify for refinanced loan on condo",
                    "IRAS scrutiny risk if poorly executed",
                    "Wills, CPF nominations, insurance must be updated",
                    "Future divorce complications",
                ],
                notes=[
                    "Decoupling means transferring one spouse's share so they become 'property-free' for ABSD.",
                    "Two SEPARATE lawyers required (joint counsel is an IRAS red flag).",
                    "Complete decoupling fully BEFORE landed OTP. 2-4 week gap recommended.",
                    "See skills/decoupling-strategy.md for full mechanics.",
                ],
                timeline_weeks=(20, 32),
            )
        )

    return plans


def _landed_to_condo(
    new_price: float,
    profile: Profile,
    marital_status: MaritalStatus,
    properties_after_new_buy: int,
    youngest_buyer_age: int,
) -> list[TransitionPlan]:
    """Generate Landed→Condo strategies (mostly downsize / retirement)."""

    plans = _hdb_to_condo(new_price, profile, marital_status, properties_after_new_buy)
    for plan in plans:
        plan.path_label = "Landed → Condo"

    if youngest_buyer_age >= 55:
        plans.append(
            TransitionPlan(
                path_label="Landed → Condo (retirement downsize)",
                strategy="Sell Landed, Buy Condo; CPF Refund Tops Up RA",
                eligible=True,
                absd_cash_upfront=calculate_absd(
                    new_price, profile, max(1, properties_after_new_buy - 1)
                ).total,
                absd_refundable=0.0,
                absd_net=calculate_absd(
                    new_price, profile, max(1, properties_after_new_buy - 1)
                ).total,
                bsd=calculate_bsd(new_price).total,
                ltv_cap=0.75,  # Note: max loan tenure capped by age 75
                estimated_min_cash=new_price * 0.05 + 5_000,
                pros=[
                    "CPF refund first tops up Retirement Account to Full Retirement Sum",
                    "FRS 2026: $220,400; FRS 2027: $228,200 (higher monthly CPF LIFE for life)",
                    "Large liquid cash release from landed equity",
                    "Lower maintenance burden (pooled MCST)",
                    "Often condo facilities suit later life (lift, security, gym, pool)",
                ],
                cons=[
                    "Loan tenure capped by age 75 (e.g., age 62 → max ~13 years)",
                    "Property tax may shift depending on AV change",
                    "Estate planning needs update post-downsize",
                ],
                notes=[
                    "At 55+, the CPF refund mechanic transforms downsize into a retirement income booster.",
                    "Consider full-cash purchase for simplicity if liquidity allows.",
                ],
                timeline_weeks=(16, 28),
            )
        )

    return plans


def _condo_to_hdb(
    new_price: float,
    profile: Profile,
    marital_status: MaritalStatus,
    youngest_buyer_age: int,
    spouse_ages: tuple[int, int] | None,
    hdb_flat_type_rooms: int,
) -> list[TransitionPlan]:
    """Generate Condo→HDB strategies, factoring in 15-month wait-out and senior exemption."""

    plans: list[TransitionPlan] = []

    # Senior exemption: both spouses 55+, 4-room or smaller
    senior_exempt = (
        spouse_ages is not None
        and all(age >= 55 for age in spouse_ages)
        and hdb_flat_type_rooms <= 4
    ) or (spouse_ages is None and youngest_buyer_age >= 55 and hdb_flat_type_rooms <= 4)

    bsd = calculate_bsd(new_price).total

    if senior_exempt:
        plans.append(
            TransitionPlan(
                path_label="Condo → HDB (senior exemption)",
                strategy="Sell Condo, Buy HDB Directly (no 15-month wait)",
                eligible=True,
                absd_cash_upfront=0.0,
                absd_refundable=0.0,
                absd_net=0.0,
                bsd=bsd,
                ltv_cap=0.75,
                estimated_min_cash=new_price * 0.10 + bsd + 5_000,
                pros=[
                    "No 15-month wait-out (both spouses 55+, buying 4-room or smaller)",
                    "Direct transition; single move",
                    "CPF refund + sale proceeds boost retirement liquidity",
                    "Possible Silver Housing Bonus (~$30k) for senior downsizers",
                    "Lower monthly housing costs",
                ],
                cons=[
                    "Loan tenure capped by age (25 yrs max for HDB loan, capped at age 65 for HDB / age 75 for bank)",
                    "Income ceiling for HDB loan ($14k) and grants applies",
                    "If household income > $14k, must use bank loan, no grants",
                ],
                notes=[
                    "Senior exemption covers: 4-room or smaller resale, 2-room Flexi, or Community Care Apartment.",
                    "Both spouses must be 55+ at time of application.",
                    "Silver Housing Bonus eligibility depends on income and downsizing criteria.",
                ],
                timeline_weeks=(12, 24),
            )
        )
    else:
        plans.append(
            TransitionPlan(
                path_label="Condo → HDB (under 55 or 5-room+)",
                strategy="Sell Condo, Wait 15 Months, Buy HDB Resale",
                eligible=True,
                absd_cash_upfront=0.0,
                absd_refundable=0.0,
                absd_net=0.0,
                bsd=bsd,
                ltv_cap=0.75,
                estimated_min_cash=new_price * 0.10 + bsd + 50_000 + 5_000,
                pros=[
                    "No ABSD (HDB is first property after condo sale)",
                    "Lower long-term housing cost",
                    "Returned CPF + sale proceeds available during wait",
                ],
                cons=[
                    "15-month wait-out: cannot buy non-subsidised HDB resale immediately",
                    "Interim rental cost: 15 months × $3k-$5k/mo = $45k-$75k",
                    "Two moves (condo → rental → HDB)",
                    "Market risk: HDB resale prices may rise during wait",
                ],
                notes=[
                    "15-month wait-out applies since Sep 30, 2022 for private property owners and ex-owners.",
                    "Brand-new BTO has 30-month wait (vs 15 for resale).",
                    "Appeals possible but ~25% success rate; mostly for OTP-pre-Sep-2022 cases or extenuating circumstances.",
                ],
                timeline_weeks=(60, 110),  # ~15 months wait + transition
            )
        )

    return plans


def analyze_upgrade_path(
    current_property: PropertyType,
    target_property: PropertyType,
    new_price: float,
    profile: Profile,
    marital_status: MaritalStatus,
    properties_after_new_buy: int = 1,
    keep_existing: bool = False,
    youngest_buyer_age: int = 40,
    spouse_ages: tuple[int, int] | None = None,
    hdb_flat_type_rooms: int = 4,
) -> dict:
    """Return all viable strategies for the given residential transition.

    Args:
        current_property: HDB, EC, CONDO, or LANDED you currently own.
        target_property: HDB, EC, CONDO, or LANDED you want to acquire.
        new_price: Purchase price of target property in SGD.
        profile: SC, SPR, FOREIGNER, ENTITY, or TRUSTEE.
        marital_status: SINGLE, MARRIED_SC_SC, MARRIED_SC_SPR,
            MARRIED_SC_FOREIGNER, MARRIED_SPR_SPR, or MARRIED_OTHER.
        properties_after_new_buy: Total residential properties owned AFTER this
            purchase (including the new one and any retained existing).
        keep_existing: If True, you intend to keep the current property.
        youngest_buyer_age: Youngest co-owner's age (affects loan tenure, CPF).
        spouse_ages: (age_a, age_b) for couples; used for senior exemption.
        hdb_flat_type_rooms: 2, 3, 4, 5 for HDB target (senior exemption rule).

    Returns:
        dict with path_label, strategies (list of TransitionPlan dicts), and notes.
    """
    plans: list[TransitionPlan] = []

    path = (current_property, target_property)

    if path == ("HDB", "CONDO") or path == ("HDB", "EC"):
        plans = _hdb_to_condo(
            new_price, profile, marital_status, properties_after_new_buy
        )
    elif path == ("HDB", "LANDED"):
        # Same playbook as HDB→Condo for sequencing; landed eligibility check applies.
        if profile in ("FOREIGNER", "SPR"):
            return {
                "path_label": "HDB → Landed",
                "strategies": [],
                "blocking_issue": "Foreigners and SPRs cannot buy mainland landed without LDAU approval.",
                "notes": ["Apply to LDAU (SLA) before any purchase commitment."],
            }
        plans = _hdb_to_condo(
            new_price, profile, marital_status, properties_after_new_buy
        )
        for p in plans:
            p.path_label = "HDB → Landed"
    elif path == ("CONDO", "CONDO") or path == ("CONDO", "EC"):
        # Sell-first or 6-month remission paths
        plans = _hdb_to_condo(
            new_price, profile, marital_status, properties_after_new_buy
        )
        for p in plans:
            p.path_label = "Condo → Condo"
        # Plus decoupling if joint and keeping
        if keep_existing and marital_status in (
            "MARRIED_SC_SC",
            "MARRIED_SC_SPR",
            "MARRIED_SPR_SPR",
        ):
            absd_dc = calculate_absd(new_price, profile, 1).total
            plans.append(
                TransitionPlan(
                    path_label="Condo → Condo (decouple, keep existing)",
                    strategy="Decouple Existing, Buy New as First Property",
                    eligible=True,
                    absd_cash_upfront=absd_dc,
                    absd_refundable=0.0,
                    absd_net=absd_dc,
                    bsd=calculate_bsd(new_price).total,
                    ltv_cap=0.75,
                    estimated_min_cash=new_price * 0.05
                    + calculate_bsd(new_price).total
                    + 35_000,
                    pros=[
                        "Retain existing condo (typically for rental income)",
                        "ABSD on new condo = 0% (first property for transferring spouse)",
                        "75% LTV on new",
                    ],
                    cons=[
                        "Decoupling cost ~$25k-$50k depending on existing condo value",
                        "Remaining spouse must qualify for refinanced loan in sole name",
                        "IRAS scrutiny risk",
                    ],
                    notes=[
                        "See skills/decoupling-strategy.md for full mechanics.",
                    ],
                    timeline_weeks=(20, 32),
                )
            )
    elif path == ("CONDO", "LANDED"):
        plans = _condo_to_landed(
            new_price,
            profile,
            marital_status,
            properties_after_new_buy,
            keep_existing,
        )
    elif path == ("LANDED", "CONDO"):
        plans = _landed_to_condo(
            new_price,
            profile,
            marital_status,
            properties_after_new_buy,
            youngest_buyer_age,
        )
    elif path == ("LANDED", "LANDED"):
        plans = _condo_to_landed(
            new_price,
            profile,
            marital_status,
            properties_after_new_buy,
            keep_existing,
        )
        for p in plans:
            p.path_label = "Landed → Landed"
    elif path in (("CONDO", "HDB"), ("LANDED", "HDB"), ("EC", "HDB")):
        plans = _condo_to_hdb(
            new_price,
            profile,
            marital_status,
            youngest_buyer_age,
            spouse_ages,
            hdb_flat_type_rooms,
        )
        if path[0] == "LANDED":
            for p in plans:
                p.path_label = p.path_label.replace("Condo", "Landed")
    elif path == ("HDB", "HDB"):
        plans.append(
            TransitionPlan(
                path_label="HDB → HDB",
                strategy="Sell Current HDB, Buy Replacement HDB",
                eligible=True,
                absd_cash_upfront=0.0,
                absd_refundable=0.0,
                absd_net=0.0,
                bsd=calculate_bsd(new_price).total,
                ltv_cap=0.75,
                estimated_min_cash=new_price * 0.10 + calculate_bsd(new_price).total,
                pros=[
                    "No ABSD (HDB always first property in HDB ownership chain)",
                    "Can use HDB loan if eligible (income ≤ $14k family)",
                    "Resale levy may apply if previously took subsidy (3-room: $30k, 4-room: $40k, 5-room: $45k)",
                ],
                cons=[
                    "Must satisfy MOP on current flat before selling",
                    "Ethnic Integration Policy / SPR quota applies to new flat",
                    "Income ceiling for HDB loan and grants",
                ],
                notes=[
                    "Check current flat's MOP completion date on HDB Resale Portal.",
                    "Resale levy applies to second subsidised flat purchase.",
                ],
                timeline_weeks=(16, 28),
            )
        )
    else:
        return {
            "path_label": f"{current_property} → {target_property}",
            "strategies": [],
            "blocking_issue": f"Path {current_property} → {target_property} not directly modeled.",
            "notes": [
                "Consult skills/upgrade-downgrade-paths.md for general framework.",
                "Engage a CEA-registered agent and conveyancing lawyer for non-standard paths.",
            ],
        }

    return {
        "path_label": (
            plans[0].path_label if plans else f"{current_property} → {target_property}"
        ),
        "strategies": [
            {
                "strategy": p.strategy,
                "eligible": p.eligible,
                "absd_cash_upfront": p.absd_cash_upfront,
                "absd_refundable": p.absd_refundable,
                "absd_net": p.absd_net,
                "bsd": p.bsd,
                "ltv_cap": p.ltv_cap,
                "estimated_min_cash": round(p.estimated_min_cash, 2),
                "pros": p.pros,
                "cons": p.cons,
                "notes": p.notes,
                "timeline_weeks": p.timeline_weeks,
            }
            for p in plans
        ],
        "notes": [
            "All figures illustrative. Verify with IRAS, HDB, MAS, CPF Board.",
            "Engage CEA agent, conveyancing lawyer, and bank mortgage specialist.",
            "For complex paths (decoupling, trust structures): also engage tax adviser.",
        ],
    }


def check_15_month_wait_out(
    spouse_ages: tuple[int, int] | None,
    youngest_buyer_age: int,
    target_hdb_rooms: int,
    target_is_new_bto: bool = False,
    has_otp_before_sep_2022: bool = False,
) -> dict:
    """Check whether the 15-month wait-out applies for private-to-HDB downgrade.

    Args:
        spouse_ages: (age_a, age_b) for couples; None for single buyer.
        youngest_buyer_age: Single buyer's age, or youngest in joint application.
        target_hdb_rooms: Number of rooms in target HDB (2, 3, 4, 5).
        target_is_new_bto: If True, target is BTO (30-month wait); else resale (15-month).
        has_otp_before_sep_2022: If True, has documentary OTP/sale proof before Sep 30, 2022.

    Returns:
        dict with applies, wait_months, exemption_reason, appeal_advice.
    """
    if has_otp_before_sep_2022:
        return {
            "applies": False,
            "wait_months": 0,
            "exemption_reason": "OTP / sale committed before Sep 30, 2022 (policy date). Appeal-eligible.",
            "appeal_advice": (
                "File appeal with HDB providing documentary proof of OTP or sale "
                "commitment before Sep 30, 2022. About 50% of pre-policy appeals "
                "between Sep 2022 and Oct 2022 were favourably considered."
            ),
            "notes": [
                "Documentary proof required: option fee receipt or option exercise fee receipt dated before Sep 30, 2022.",
                "HDB will process appeal on a case-by-case basis.",
            ],
        }

    # Senior exemption check
    if spouse_ages is not None:
        both_55_plus = all(age >= 55 for age in spouse_ages)
    else:
        both_55_plus = youngest_buyer_age >= 55

    if both_55_plus and target_hdb_rooms <= 4 and not target_is_new_bto:
        return {
            "applies": False,
            "wait_months": 0,
            "exemption_reason": (
                "Senior exemption: both spouses (or single buyer) 55+ buying 4-room "
                "or smaller resale flat."
            ),
            "appeal_advice": None,
            "notes": [
                "Exemption also covers 2-room Flexi flats and Community Care Apartments.",
                "Direct transition possible; no wait-out required.",
                "Consider Silver Housing Bonus eligibility (~$30k for qualifying senior downsizers).",
            ],
        }

    # General case: wait-out applies
    wait_months = 30 if target_is_new_bto else 15
    notes = [
        f"15-month wait-out from disposal completion of private property "
        f"(introduced Sep 30, 2022).",
        "Appeals: ~25% approval rate; mostly for OTP-pre-Sep-2022 cases or extenuating "
        "circumstances (medical, elder care, no alternative housing).",
        "Plan for interim housing: rental $3k-$5k/mo typical for HDB-equivalent space.",
    ]
    if target_is_new_bto:
        notes.append(
            "Brand-new BTO has 30-month wait, not 15. Plus you must ballot like everyone."
        )

    return {
        "applies": True,
        "wait_months": wait_months,
        "exemption_reason": None,
        "appeal_advice": (
            "Appeal is possible but only ~25% success rate. Most successful appeals "
            "involve pre-Sep-2022 OTP/sale proof or genuine extenuating circumstances. "
            "General lifestyle downsize appeals rarely succeed."
        ),
        "notes": notes,
    }


def estimate_decoupling_cost(
    current_property_value: float,
    share_being_transferred: float = 0.50,
    legal_fees_per_lawyer: float = 2_500,
    refinancing_admin: float = 1_500,
    valuation_fee: float = 700,
) -> dict:
    """Estimate the cash cost of decoupling a jointly-owned private property.

    Args:
        current_property_value: Current market value of the joint property.
        share_being_transferred: Fraction being transferred (typically 0.50).
        legal_fees_per_lawyer: Per-lawyer fee; 2 lawyers required.
        refinancing_admin: Bank refinancing admin cost.
        valuation_fee: Independent valuation fee.

    Returns:
        dict with bsd_on_transfer, legal_total, total_cash_cost, notes.
    """
    if current_property_value <= 0:
        raise ValueError("current_property_value must be > 0")
    if not 0 < share_being_transferred <= 1:
        raise ValueError("share_being_transferred must be in (0, 1]")

    consideration = current_property_value * share_being_transferred
    bsd = calculate_bsd(consideration).total
    legal_total = legal_fees_per_lawyer * 2

    total = bsd + legal_total + refinancing_admin + valuation_fee

    return {
        "current_property_value": current_property_value,
        "share_being_transferred": share_being_transferred,
        "consideration": consideration,
        "bsd_on_transfer": bsd,
        "legal_total": legal_total,
        "refinancing_admin": refinancing_admin,
        "valuation_fee": valuation_fee,
        "total_cash_cost": round(total, 2),
        "notes": [
            f"Decoupling transfers {share_being_transferred:.0%} of the property at "
            f"market value ({consideration:,.0f} SGD).",
            f"BSD computed on the transferred share value: {bsd:,.2f}",
            "TWO separate lawyers required (one per spouse).",
            "CPF refund (transferring spouse) is a flow, not a cost — funds return to OA.",
            "Compare to ABSD savings on planned second property to validate ROI.",
            "IRAS scrutiny: ensure market valuation, separate counsel, time gap, and genuine substance.",
        ],
    }


def compare_decoupling_vs_absd(
    current_joint_property_value: float,
    new_property_price: float,
    profile: Profile,
    properties_after_new_buy: int,
) -> dict:
    """Compare decoupling cost vs paying ABSD on a planned second property purchase.

    Args:
        current_joint_property_value: Current value of joint property.
        new_property_price: Price of planned new property.
        profile: SC, SPR, etc.
        properties_after_new_buy: Property count after the new purchase.

    Returns:
        dict comparing the two paths with net benefit.
    """
    decouple_cost = estimate_decoupling_cost(current_joint_property_value)
    absd_without = calculate_absd(
        new_property_price, profile, properties_after_new_buy
    ).total
    absd_with = calculate_absd(new_property_price, profile, 1).total

    absd_savings = absd_without - absd_with
    net_benefit = absd_savings - decouple_cost["total_cash_cost"]

    return {
        "decoupling_cost": decouple_cost["total_cash_cost"],
        "absd_without_decoupling": absd_without,
        "absd_with_decoupling": absd_with,
        "absd_savings": round(absd_savings, 2),
        "net_benefit": round(net_benefit, 2),
        "recommend_decoupling": net_benefit > 0,
        "notes": [
            f"ABSD without decoupling: {absd_without:,.0f} ({profile} second/third property rate).",
            f"ABSD with decoupling (transferring spouse buys as first property): {absd_with:,.0f}.",
            f"Decoupling cost: {decouple_cost['total_cash_cost']:,.0f}.",
            f"Net benefit: {net_benefit:,.0f}.",
            "Decoupling only viable if remaining spouse can qualify for refinanced loan in sole name.",
            "HDB cannot be decoupled (except under divorce order).",
            "Verify with conveyancing lawyer and tax adviser before executing.",
        ],
    }


def estimate_cpf_refund_at_sale(
    cpf_principal_used: float,
    years_held: float,
    accrued_rate: float = 0.025,
) -> dict:
    """Estimate CPF refund (principal + accrued interest) on property sale.

    This is a simplified linear-withdrawal approximation. Actual CPF refund
    is computed by CPF Board based on detailed monthly contribution history.

    Args:
        cpf_principal_used: Total CPF OA principal used on the property over hold period.
        years_held: Years property has been held.
        accrued_rate: CPF accrued interest rate (default 2.5% p.a., OA rate).

    Returns:
        dict with principal, accrued_interest, total_refund, notes.
    """
    if cpf_principal_used < 0:
        raise ValueError("cpf_principal_used must be >= 0")
    if years_held < 0:
        raise ValueError("years_held must be >= 0")

    # Simplified: assume principal contributed mid-period for accrued interest calc.
    # Real CPF calc tracks each monthly contribution and compounds.
    avg_holding_years = years_held / 2
    # Compound: F = P * (1+r)^t
    total_with_interest = cpf_principal_used * ((1 + accrued_rate) ** avg_holding_years)
    accrued = total_with_interest - cpf_principal_used

    return {
        "cpf_principal_used": cpf_principal_used,
        "years_held": years_held,
        "accrued_interest_estimate": round(accrued, 2),
        "total_refund_estimate": round(total_with_interest, 2),
        "notes": [
            f"Estimated using simplified linear withdrawal assumption ({avg_holding_years:.1f} avg years).",
            f"Compounded at {accrued_rate:.1%} p.a. (OA rate).",
            "Actual CPF refund is computed by CPF Board from detailed monthly contribution history.",
            "Use CPF Home Calculators (https://www.cpf.gov.sg/member/tools-and-services/calculators) "
            "for precise figures.",
            "At age 55+, refund first tops up Retirement Account to Full Retirement Sum (FRS 2026: $220,400).",
            "Excess flows to OA, where it earns 2.5% p.a. and can fund next property purchase.",
        ],
    }


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
) -> dict:
    """End-to-end cashflow model for a sell + buy transition.

    Args:
        sell_price: Sale price of current property.
        sell_outstanding_loan: Outstanding mortgage to redeem.
        sell_cpf_refund_estimate: Estimated CPF refund (principal + accrued).
        sell_agent_commission_rate: Decimal (e.g., 0.02 for 2%); GST added at 9%.
        new_price: Purchase price of new property.
        new_ltv_cap: Max LTV (0.75 for first, 0.45 for second).
        new_min_cash_pct: Minimum cash component (0.05 first, 0.25 second).
        new_bsd: BSD on new property.
        new_absd_upfront: ABSD cash outlay (may be refundable).
        interim_months: Months of interim rental (0 if buy-first).
        interim_rental_monthly: Monthly interim rent.

    Returns:
        dict with sale_net_cash, cash_required, cash_position_after, notes.
    """
    # Sale side
    agent_comm = sell_price * sell_agent_commission_rate * 1.09  # incl 9% GST
    legal_sell = 3_000
    sell_net_before_cpf = sell_price - sell_outstanding_loan - agent_comm - legal_sell
    sell_net_cash = sell_net_before_cpf - sell_cpf_refund_estimate
    cpf_refunded_to_oa = sell_cpf_refund_estimate

    # New property side
    new_loan = new_price * new_ltv_cap
    new_down_payment = new_price - new_loan
    new_min_cash = new_price * new_min_cash_pct
    new_legal = 3_500
    new_admin = 1_000

    # Interim
    interim_total = interim_months * interim_rental_monthly

    # Total cash outflow
    total_cash_required = (
        new_min_cash
        + new_bsd
        + new_absd_upfront
        + new_legal
        + new_admin
        + interim_total
    )
    # Note: down payment beyond min_cash can be CPF; we don't double-count CPF here

    # Cash position after
    cash_position_after = sell_net_cash - total_cash_required

    return {
        "sell_net_cash": round(sell_net_cash, 2),
        "cpf_refunded_to_oa": round(cpf_refunded_to_oa, 2),
        "new_loan_amount": round(new_loan, 2),
        "new_down_payment": round(new_down_payment, 2),
        "new_min_cash_component": round(new_min_cash, 2),
        "interim_rental_total": round(interim_total, 2),
        "total_cash_required": round(total_cash_required, 2),
        "cash_position_after_transition": round(cash_position_after, 2),
        "notes": [
            f"Sale net cash (after loan, commission, legal, CPF refund): {sell_net_cash:,.0f}",
            f"CPF returned to OA (available for next property): {cpf_refunded_to_oa:,.0f}",
            f"New loan: {new_loan:,.0f} at {new_ltv_cap:.0%} LTV",
            f"Down payment: {new_down_payment:,.0f} ({new_min_cash:,.0f} min cash; rest CPF/cash)",
            f"BSD + ABSD upfront: {new_bsd + new_absd_upfront:,.0f}",
            f"Interim rental ({interim_months} months): {interim_total:,.0f}",
            f"Estimated cash position after transition: {cash_position_after:,.0f}",
            "Illustrative; confirm actual numbers with lawyer, bank, and CPF Board.",
        ],
    }
