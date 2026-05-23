"""Tests for lease decay and CPF usage cap."""

from __future__ import annotations

import pytest

from sg_property_mcp.tools.lease_decay import (
    cpf_usage_limit,
    lease_decay_factor,
    lease_decay_value,
)


class TestLeaseDecayFactor:
    def test_full_lease(self) -> None:
        assert lease_decay_factor(99) == pytest.approx(0.96, abs=0.001)

    def test_short_lease(self) -> None:
        assert lease_decay_factor(20) == pytest.approx(0.41, abs=0.001)

    def test_zero(self) -> None:
        assert lease_decay_factor(0) == 0.0

    def test_negative(self) -> None:
        assert lease_decay_factor(-5) == 0.0

    def test_interpolation_mid_value(self) -> None:
        # Between 60 (0.86) and 65 (0.88), at 62.5 should be ~0.87
        factor = lease_decay_factor(62.5)
        assert 0.86 < factor < 0.88

    def test_over_99(self) -> None:
        assert lease_decay_factor(120) == pytest.approx(0.96, abs=0.001)


class TestLeaseDecayValue:
    def test_basic(self) -> None:
        r = lease_decay_value(1_000_000, 50)
        assert r["estimated_leasehold_value"] == pytest.approx(810_000, rel=0.01)
        assert "balas_factor" in r
        assert "notes" in r

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            lease_decay_value(0, 50)


class TestCPFUsageLimit:
    def test_long_lease_full_cpf(self) -> None:
        # Young buyer (30), 99 yrs lease → covers to age 129, well beyond 95
        r = cpf_usage_limit(1_000_000, 99, 30)
        assert r["pro_rate_factor"] == 1.0
        assert r["cpf_cap"] == 1_000_000

    def test_pro_rated(self) -> None:
        # Buyer 40, 40 yrs remaining → covers to age 80, target age 95.
        # Years to age 95 = 55; factor = 40/55 ≈ 0.727
        r = cpf_usage_limit(1_000_000, 40, 40)
        assert 0.7 < r["pro_rate_factor"] < 0.75
        assert r["cpf_cap"] < 1_000_000

    def test_too_short_no_cpf(self) -> None:
        # Buyer 50, 10 yrs remaining → covers to age 60, < 65 → no CPF.
        r = cpf_usage_limit(1_000_000, 10, 50)
        assert r["pro_rate_factor"] == 0.0
        assert r["cpf_cap"] == 0.0

    def test_invalid_inputs(self) -> None:
        with pytest.raises(ValueError):
            cpf_usage_limit(0, 99, 30)
        with pytest.raises(ValueError):
            cpf_usage_limit(1_000_000, 50, -1)
        with pytest.raises(ValueError):
            cpf_usage_limit(1_000_000, 50, 105)
