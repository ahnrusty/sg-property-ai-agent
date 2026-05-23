"""Tests for scorecard, comparison, and psf calc."""

from __future__ import annotations

import pytest

from sg_property_mcp.tools.scorecard import (
    compare_listings,
    psf_calc,
    score_listing,
)


def sample_listing(**overrides) -> dict:
    base = {
        "name": "Test Unit",
        "price": 1_800_000,
        "psf": 1_650,
        "beds": 3,
        "baths": 2,
        "sqft": 1_090,
        "mrt_min": 8,
        "tenure_years_left": 85,
    }
    base.update(overrides)
    return base


def sample_criteria() -> dict:
    return {
        "max_price": 2_000_000,
        "min_beds": 3,
        "max_mrt_min": 10,
        "min_sqft": 900,
        "min_tenure_years_left": 60,
        "weights": {
            "price": 0.30,
            "beds": 0.10,
            "mrt": 0.20,
            "sqft": 0.20,
            "tenure": 0.20,
        },
    }


class TestScoreListing:
    def test_returns_score(self) -> None:
        r = score_listing(sample_listing(), sample_criteria())
        assert 0 <= r["fit_score"] <= 100

    def test_meets_min_beds(self) -> None:
        r = score_listing(sample_listing(beds=3), sample_criteria())
        assert r["dimension_scores"]["beds"] == 100.0

    def test_below_min_beds(self) -> None:
        r = score_listing(sample_listing(beds=2), sample_criteria())
        assert r["dimension_scores"]["beds"] == 0.0

    def test_over_price_penalised(self) -> None:
        r_in = score_listing(sample_listing(price=1_800_000), sample_criteria())
        r_over = score_listing(sample_listing(price=2_500_000), sample_criteria())
        assert r_over["dimension_scores"]["price"] < r_in["dimension_scores"]["price"]


class TestCompareListings:
    def test_ranks(self) -> None:
        listings = [
            sample_listing(name="A", price=1_500_000, mrt_min=5),
            sample_listing(name="B", price=1_900_000, mrt_min=12),
            sample_listing(name="C", price=2_100_000, mrt_min=3),
        ]
        r = compare_listings(listings, sample_criteria())
        assert len(r["ranked"]) == 3
        assert r["top_pick"] in {"A", "B", "C"}
        # Confirm sorted descending
        scores = [item["fit_score"] for item in r["ranked"]]
        assert scores == sorted(scores, reverse=True)

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            compare_listings([], sample_criteria())


class TestPsfCalc:
    def test_compute_price(self) -> None:
        r = psf_calc(sqft=1_000, psf=1_500)
        assert r["price"] == 1_500_000

    def test_compute_psf(self) -> None:
        r = psf_calc(price=1_800_000, sqft=1_200)
        assert r["psf"] == 1_500

    def test_compute_sqft_from_price_and_psf(self) -> None:
        r = psf_calc(price=1_500_000, psf=1_500)
        assert r["sqft"] == 1_000

    def test_sqm_to_sqft(self) -> None:
        # 100 sqm ≈ 1076.39 sqft
        r = psf_calc(sqm=100, psf=1_500)
        assert abs(r["sqft"] - 1076.39) < 0.1

    def test_insufficient_inputs(self) -> None:
        with pytest.raises(ValueError):
            psf_calc(price=1_500_000)
