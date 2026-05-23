"""Listing scorecard and comparison helpers."""

from __future__ import annotations

from typing import Any


def score_listing(
    listing: dict[str, Any],
    criteria: dict[str, Any],
) -> dict:
    """Score a listing against user-defined weighted criteria.

    Args:
        listing: dict with keys like price, psf, beds, baths, sqft, mrt_min,
            tenure_years_left, year_built, maintenance_fee_monthly.
        criteria: dict with weights and targets, e.g.
            {
                "max_price": 2_000_000,
                "min_beds": 3,
                "max_mrt_min": 10,
                "min_sqft": 900,
                "min_tenure_years_left": 60,
                "weights": {
                    "price": 0.3,
                    "beds": 0.1,
                    "mrt": 0.2,
                    "sqft": 0.2,
                    "tenure": 0.2
                }
            }

    Returns:
        dict with score (0–100), per-dimension scores, fit summary, notes.
    """
    weights = criteria.get(
        "weights",
        {"price": 0.25, "beds": 0.15, "mrt": 0.20, "sqft": 0.20, "tenure": 0.20},
    )

    scores: dict[str, float] = {}
    notes: list[str] = []

    # Price (lower = better up to max_price)
    if "max_price" in criteria and "price" in listing:
        if listing["price"] <= criteria["max_price"]:
            ratio = listing["price"] / criteria["max_price"]
            scores["price"] = 100 * (1 - 0.5 * ratio)
        else:
            scores["price"] = max(
                0.0, 100 * (1 - (listing["price"] / criteria["max_price"] - 1) * 2)
            )
        notes.append(
            f"Price {listing['price']:,.0f} vs max {criteria['max_price']:,.0f}: "
            f"{scores['price']:.0f}/100"
        )

    # Beds
    if "min_beds" in criteria and "beds" in listing:
        scores["beds"] = 100.0 if listing["beds"] >= criteria["min_beds"] else 0.0
        notes.append(
            f"Beds {listing['beds']} vs min {criteria['min_beds']}: {scores['beds']:.0f}/100"
        )

    # MRT walking minutes (lower = better)
    if "max_mrt_min" in criteria and "mrt_min" in listing:
        if listing["mrt_min"] <= criteria["max_mrt_min"]:
            scores["mrt"] = 100 * (
                1 - 0.5 * listing["mrt_min"] / criteria["max_mrt_min"]
            )
        else:
            scores["mrt"] = max(
                0.0, 100 * (1 - (listing["mrt_min"] / criteria["max_mrt_min"] - 1) * 2)
            )
        notes.append(
            f"MRT {listing['mrt_min']} min vs max {criteria['max_mrt_min']}: "
            f"{scores['mrt']:.0f}/100"
        )

    # Size
    if "min_sqft" in criteria and "sqft" in listing:
        if listing["sqft"] >= criteria["min_sqft"]:
            ratio = min(listing["sqft"] / criteria["min_sqft"], 2.0)
            scores["sqft"] = 50 + 50 * (ratio - 1)
        else:
            scores["sqft"] = max(0.0, 100 * listing["sqft"] / criteria["min_sqft"])
        notes.append(
            f"Size {listing['sqft']} sqft vs min {criteria['min_sqft']}: "
            f"{scores['sqft']:.0f}/100"
        )

    # Tenure
    if "min_tenure_years_left" in criteria and "tenure_years_left" in listing:
        if listing["tenure_years_left"] >= criteria["min_tenure_years_left"]:
            scores["tenure"] = 100.0
        else:
            scores["tenure"] = max(
                0.0,
                100 * listing["tenure_years_left"] / criteria["min_tenure_years_left"],
            )
        notes.append(
            f"Tenure {listing['tenure_years_left']} yrs vs min "
            f"{criteria['min_tenure_years_left']}: {scores['tenure']:.0f}/100"
        )

    weighted_sum = 0.0
    weight_total = 0.0
    for k, w in weights.items():
        if k in scores:
            weighted_sum += scores[k] * w
            weight_total += w

    fit_score = (weighted_sum / weight_total) if weight_total > 0 else 0.0

    return {
        "fit_score": round(fit_score, 1),
        "dimension_scores": {k: round(v, 1) for k, v in scores.items()},
        "weights_used": {k: weights[k] for k in scores if k in weights},
        "notes": notes,
    }


def compare_listings(
    listings: list[dict[str, Any]],
    criteria: dict[str, Any],
) -> dict:
    """Compare multiple listings using the same criteria.

    Args:
        listings: list of listing dicts; each should include a "name" key
            for identification in output.
        criteria: same shape as score_listing.

    Returns:
        dict with ranked list and recommendation.
    """
    if not listings:
        raise ValueError("listings must not be empty")

    results = []
    for listing in listings:
        name = listing.get("name", "Unnamed listing")
        score_result = score_listing(listing, criteria)
        results.append(
            {
                "name": name,
                "fit_score": score_result["fit_score"],
                "dimension_scores": score_result["dimension_scores"],
                "listing": listing,
            }
        )

    results.sort(key=lambda x: x["fit_score"], reverse=True)

    return {
        "ranked": results,
        "top_pick": results[0]["name"],
        "top_pick_score": results[0]["fit_score"],
        "notes": [
            f"Evaluated {len(results)} listings.",
            f"Top pick: {results[0]['name']} (score {results[0]['fit_score']:.1f}/100).",
            "Scores are indicative; non-quantifiable factors (facing, MCST quality, neighbour) require viewing.",
        ],
    }


def psf_calc(
    price: float | None = None,
    sqft: float | None = None,
    psf: float | None = None,
    sqm: float | None = None,
) -> dict:
    """Convert between price, size, and per-square-foot/metre.

    Supply any two of (price, sqft, psf) and the third is computed.
    sqm can be supplied as an alternative to sqft.

    Returns:
        dict with price, sqft, sqm, psf, psm.
    """
    if sqm is not None and sqft is None:
        sqft = sqm * 10.7639
    if sqft is not None and sqm is None:
        sqm = sqft / 10.7639

    if price is None and sqft is not None and psf is not None:
        price = sqft * psf
    elif sqft is None and price is not None and psf is not None:
        sqft = price / psf
        sqm = sqft / 10.7639
    elif psf is None and price is not None and sqft is not None:
        psf = price / sqft

    if price is None or sqft is None or psf is None:
        raise ValueError(
            "Provide any two of price, sqft (or sqm), psf to compute the third."
        )

    psm = price / sqm if sqm else None

    return {
        "price": round(price, 2),
        "sqft": round(sqft, 2),
        "sqm": round(sqm, 2) if sqm else None,
        "psf": round(psf, 2),
        "psm": round(psm, 2) if psm else None,
    }
