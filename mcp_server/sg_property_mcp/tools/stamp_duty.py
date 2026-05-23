"""Stamp duty calculators: BSD, ABSD, SSD.

All rates valid as of 2026. Always re-verify against IRAS before use:
https://www.iras.gov.sg/taxes/stamp-duty
"""

from __future__ import annotations

from dataclasses import dataclass

# Buyer's Stamp Duty bands (residential, from 14 Feb 2023).
# Each tuple: (upper bound of band in SGD, marginal rate as decimal).
# Final tuple uses None for upper bound (open-ended top band).
BSD_RESIDENTIAL_BANDS: list[tuple[float | None, float]] = [
    (180_000, 0.01),
    (360_000, 0.02),
    (1_000_000, 0.03),
    (1_500_000, 0.04),
    (3_000_000, 0.05),
    (None, 0.06),
]

BSD_NON_RESIDENTIAL_BANDS: list[tuple[float | None, float]] = [
    (180_000, 0.01),
    (360_000, 0.02),
    (1_000_000, 0.03),
    (1_500_000, 0.04),
    (None, 0.05),
]

# ABSD rates from 27 Apr 2023. Keyed by (profile, property_count_bucket).
# property_count_bucket: 1 = first, 2 = second, 3 = third or more.
ABSD_RATES: dict[tuple[str, int], float] = {
    ("SC", 1): 0.00,
    ("SC", 2): 0.20,
    ("SC", 3): 0.30,
    ("SPR", 1): 0.05,
    ("SPR", 2): 0.30,
    ("SPR", 3): 0.35,
    ("FOREIGNER", 1): 0.60,
    ("FOREIGNER", 2): 0.60,
    ("FOREIGNER", 3): 0.60,
    ("ENTITY", 1): 0.65,
    ("ENTITY", 2): 0.65,
    ("ENTITY", 3): 0.65,
    ("TRUSTEE", 1): 0.65,
    ("TRUSTEE", 2): 0.65,
    ("TRUSTEE", 3): 0.65,
}

VALID_PROFILES = {"SC", "SPR", "FOREIGNER", "ENTITY", "TRUSTEE"}

# Seller's Stamp Duty (residential, since 11 Mar 2017).
SSD_RESIDENTIAL: list[tuple[int, float]] = [
    (12, 0.12),  # held <= 12 months
    (24, 0.08),
    (36, 0.04),
]


@dataclass
class StampDutyResult:
    """Stamp duty computation result."""

    total: float
    breakdown: list[dict]
    notes: list[str]


def calculate_bsd(
    consideration: float,
    property_type: str = "residential",
) -> StampDutyResult:
    """Compute Buyer's Stamp Duty on the higher of price or market value.

    Args:
        consideration: Purchase price or market value, whichever is higher (SGD).
        property_type: "residential" or "non_residential".

    Returns:
        StampDutyResult with total BSD, band breakdown, and notes.
    """
    if consideration <= 0:
        raise ValueError("consideration must be > 0")

    bands = (
        BSD_RESIDENTIAL_BANDS
        if property_type == "residential"
        else BSD_NON_RESIDENTIAL_BANDS
    )

    breakdown: list[dict] = []
    remaining = consideration
    lower = 0.0
    total = 0.0

    for upper, rate in bands:
        band_top = upper if upper is not None else consideration
        band_size = max(0.0, min(band_top, consideration) - lower)
        if band_size <= 0:
            break
        band_duty = band_size * rate
        total += band_duty
        breakdown.append(
            {
                "from": lower,
                "to": band_top if upper is not None else None,
                "rate": rate,
                "band_amount": band_size,
                "duty": round(band_duty, 2),
            }
        )
        lower = band_top
        if upper is None or consideration <= upper:
            break

    return StampDutyResult(
        total=round(total, 2),
        breakdown=breakdown,
        notes=[
            f"BSD computed on SGD {consideration:,.0f}.",
            "Computed on the higher of purchase price or market value.",
            "Verify against IRAS Stamp Duty calculator before payment.",
        ],
    )


def calculate_absd(
    consideration: float,
    profile: str,
    property_count_after_purchase: int,
) -> StampDutyResult:
    """Compute Additional Buyer's Stamp Duty.

    Args:
        consideration: Purchase price or market value, whichever is higher (SGD).
        profile: One of SC, SPR, FOREIGNER, ENTITY, TRUSTEE.
        property_count_after_purchase: Total residential properties owned
            after this purchase (this purchase = property #N).

    Returns:
        StampDutyResult with total ABSD and notes.
    """
    profile = profile.upper().strip()
    if profile not in VALID_PROFILES:
        raise ValueError(
            f"profile must be one of {sorted(VALID_PROFILES)}, got {profile!r}"
        )
    if consideration <= 0:
        raise ValueError("consideration must be > 0")
    if property_count_after_purchase < 1:
        raise ValueError("property_count_after_purchase must be >= 1")

    bucket = min(3, property_count_after_purchase)
    rate = ABSD_RATES[(profile, bucket)]
    total = consideration * rate

    notes = [
        f"ABSD rate {rate:.0%} for {profile} purchasing property #{bucket}"
        + (" or more" if bucket == 3 else "")
        + ".",
        "Computed on the higher of purchase price or market value.",
        "Payable within 14 days of OTP signing in Singapore (30 days if overseas).",
        "Married couples (with at least one SC) may apply for ABSD remission "
        "if they dispose of the existing property within 6 months "
        "(OTP for resale, NVP for new launch).",
        "Verify on IRAS before payment.",
    ]
    if profile == "FOREIGNER":
        notes.append(
            "Citizens of Iceland, Liechtenstein, Norway, Switzerland, and USA "
            "may qualify for ABSD parity with Singapore Citizens under FTAs."
        )

    return StampDutyResult(
        total=round(total, 2),
        breakdown=[
            {
                "profile": profile,
                "property_count": bucket,
                "rate": rate,
                "consideration": consideration,
            }
        ],
        notes=notes,
    )


def calculate_ssd(
    consideration: float,
    holding_period_months: int,
    property_type: str = "residential",
) -> StampDutyResult:
    """Compute Seller's Stamp Duty.

    Args:
        consideration: Sale price or market value, whichever is higher (SGD).
        holding_period_months: Months elapsed between purchase OTP date
            and sale OTP date.
        property_type: Currently only "residential" supported.

    Returns:
        StampDutyResult with total SSD and notes.
    """
    if property_type != "residential":
        raise NotImplementedError(
            "Only residential SSD implemented. Industrial SSD has a separate "
            "schedule on IRAS."
        )
    if consideration <= 0:
        raise ValueError("consideration must be > 0")
    if holding_period_months < 0:
        raise ValueError("holding_period_months must be >= 0")

    rate = 0.0
    matched_band = None
    for max_months, band_rate in SSD_RESIDENTIAL:
        if holding_period_months <= max_months:
            rate = band_rate
            matched_band = max_months
            break

    total = consideration * rate
    notes = [
        f"Holding period {holding_period_months} months.",
        f"SSD rate {rate:.0%}.",
    ]
    if rate == 0.0:
        notes.append("Held > 3 years; no SSD payable on residential disposal.")
    else:
        notes.append(
            f"Sale within {matched_band} months of purchase triggers "
            f"{rate:.0%} SSD on the higher of sale price or market value."
        )
    notes.append("Verify on IRAS before sale.")

    return StampDutyResult(
        total=round(total, 2),
        breakdown=[
            {
                "holding_period_months": holding_period_months,
                "rate": rate,
                "consideration": consideration,
            }
        ],
        notes=notes,
    )
