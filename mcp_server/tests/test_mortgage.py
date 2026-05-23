"""Tests for mortgage and affordability calculators."""

from __future__ import annotations

import pytest

from sg_property_mcp.tools.mortgage import (
    check_tdsr_msr,
    estimate_max_loan,
    estimate_mortgage,
    monthly_payment,
)


class TestMonthlyPayment:
    def test_known_value(self) -> None:
        # $1M, 2% p.a., 30 yrs ≈ $3,696.19/month
        p = monthly_payment(1_000_000, 0.02, 30)
        assert abs(p - 3696.19) < 0.05

    def test_high_rate(self) -> None:
        # $500k, 5% p.a., 25 yrs ≈ $2,922.95
        p = monthly_payment(500_000, 0.05, 25)
        assert abs(p - 2922.95) < 0.10

    def test_zero_rate(self) -> None:
        p = monthly_payment(1_000_000, 0.0, 25)
        assert abs(p - 1_000_000 / (25 * 12)) < 0.01

    def test_invalid_inputs(self) -> None:
        with pytest.raises(ValueError):
            monthly_payment(0, 0.02, 30)
        with pytest.raises(ValueError):
            monthly_payment(1_000_000, -0.01, 30)
        with pytest.raises(ValueError):
            monthly_payment(1_000_000, 0.02, 0)


class TestEstimateMortgage:
    def test_returns_all_fields(self) -> None:
        r = estimate_mortgage(1_000_000, 0.02, 30)
        assert r.monthly_payment > 0
        assert r.total_interest > 0
        assert r.total_paid > r.principal
        assert r.principal == 1_000_000
        assert r.rate == 0.02
        assert r.tenure_years == 30


class TestMaxLoan:
    def test_tdsr_only(self) -> None:
        # $12k income, no debt, 4% stress, 30 yrs, 55% TDSR.
        # Headroom = $6,600/month. PV at 4%/12 over 360 = roughly $1,383k
        r = estimate_max_loan(12_000, 0.0, 0.04, 30, 0.55, False)
        assert r["max_loan_tdsr"] > 1_300_000
        assert r["max_loan_tdsr"] < 1_500_000
        assert r["max_loan"] == r["max_loan_tdsr"]

    def test_with_msr(self) -> None:
        # MSR caps lower for typical HDB scenario; MSR should bind for high-income HDB upgrader.
        r = estimate_max_loan(15_000, 0.0, 0.03, 25, 0.55, True)
        assert r["max_loan_msr"] is not None
        assert r["max_loan"] == min(r["max_loan_tdsr"], r["max_loan_msr"])

    def test_debt_eats_headroom(self) -> None:
        # Income $8k, existing debt $5k → TDSR headroom -$600 ish, no loan possible
        r = estimate_max_loan(8_000, 5_000, 0.04, 30, 0.55, False)
        assert r["max_loan_tdsr"] == 0.0


class TestCheckTDSR:
    def test_pass(self) -> None:
        r = check_tdsr_msr(4_000, 12_000, 0.0, False)
        assert r["tdsr_ratio"] == pytest.approx(4000 / 12000, rel=1e-3)
        assert r["tdsr_pass"] is True
        assert r["passes"] is True

    def test_fail_tdsr(self) -> None:
        r = check_tdsr_msr(7_000, 12_000, 0.0, False)
        # 7000/12000 = 58.3% > 55%
        assert r["tdsr_pass"] is False

    def test_msr_check(self) -> None:
        # Mortgage 4500 / income 12000 = 37.5% > 30% MSR
        r = check_tdsr_msr(4_500, 12_000, 0.0, msr_applicable=True)
        assert r["msr_pass"] is False
        assert r["passes"] is False
