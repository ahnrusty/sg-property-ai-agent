"""Tests for upgrade/downgrade path analysers."""

from __future__ import annotations

import pytest

from sg_property_mcp.tools.upgrade_paths import (
    analyze_upgrade_path,
    check_15_month_wait_out,
    compare_decoupling_vs_absd,
    estimate_cpf_refund_at_sale,
    estimate_decoupling_cost,
    estimate_transition_cash_flow,
)


class TestAnalyzeUpgradePath:
    def test_hdb_to_condo_sc_couple_returns_two_strategies(self) -> None:
        r = analyze_upgrade_path(
            current_property="HDB",
            target_property="CONDO",
            new_price=1_800_000,
            profile="SC",
            marital_status="MARRIED_SC_SC",
            properties_after_new_buy=1,  # HDB sold
        )
        assert r["path_label"] == "HDB → Condo"
        strategies = r["strategies"]
        assert len(strategies) == 2
        # Sell First should have 0 ABSD
        sell_first = [s for s in strategies if "Sell" in s["strategy"]][0]
        assert sell_first["absd_net"] == 0.0
        # Buy First should have refundable ABSD
        buy_first = [s for s in strategies if "Buy" in s["strategy"]][0]
        assert buy_first["eligible"] is True
        assert buy_first["absd_refundable"] > 0
        assert buy_first["absd_net"] == 0.0

    def test_hdb_to_condo_single_sc_no_remission(self) -> None:
        r = analyze_upgrade_path(
            current_property="HDB",
            target_property="CONDO",
            new_price=1_500_000,
            profile="SC",
            marital_status="SINGLE",
            properties_after_new_buy=1,
        )
        buy_first = [s for s in r["strategies"] if "Buy" in s["strategy"]][0]
        # Single SC not eligible for 6-month remission
        assert buy_first["eligible"] is False

    def test_condo_to_landed_decouple(self) -> None:
        r = analyze_upgrade_path(
            current_property="CONDO",
            target_property="LANDED",
            new_price=4_000_000,
            profile="SC",
            marital_status="MARRIED_SC_SC",
            properties_after_new_buy=2,  # keeping condo
            keep_existing=True,
        )
        # Should have decoupling strategy
        decouple = [s for s in r["strategies"] if "Decouple" in s["strategy"]]
        assert len(decouple) > 0
        assert decouple[0]["absd_net"] == 0.0  # First property for transferring spouse

    def test_condo_to_landed_foreigner_blocked(self) -> None:
        r = analyze_upgrade_path(
            current_property="CONDO",
            target_property="LANDED",
            new_price=4_000_000,
            profile="FOREIGNER",
            marital_status="MARRIED_OTHER",
        )
        # Foreigner blocked from mainland landed
        assert any(not s["eligible"] for s in r["strategies"])

    def test_condo_to_hdb_under_55_has_wait_out(self) -> None:
        r = analyze_upgrade_path(
            current_property="CONDO",
            target_property="HDB",
            new_price=700_000,
            profile="SC",
            marital_status="MARRIED_SC_SC",
            spouse_ages=[48, 46],
            hdb_flat_type_rooms=5,
        )
        strategy = r["strategies"][0]
        assert (
            "Wait 15" in strategy["strategy"]
            or "15 Month" in strategy["strategy"]
            or "15-month" in strategy["strategy"].lower()
            or "wait" in strategy["strategy"].lower()
        )

    def test_condo_to_hdb_senior_exempt(self) -> None:
        r = analyze_upgrade_path(
            current_property="CONDO",
            target_property="HDB",
            new_price=600_000,
            profile="SC",
            marital_status="MARRIED_SC_SC",
            spouse_ages=[58, 56],
            hdb_flat_type_rooms=4,
        )
        strategy = r["strategies"][0]
        assert (
            "senior" in strategy["strategy"].lower()
            or "Direct" in strategy["strategy"]
            or "no 15-month" in strategy["strategy"].lower()
        )

    def test_landed_to_condo_at_retirement(self) -> None:
        r = analyze_upgrade_path(
            current_property="LANDED",
            target_property="CONDO",
            new_price=2_800_000,
            profile="SC",
            marital_status="MARRIED_SC_SC",
            youngest_buyer_age=62,
        )
        # Should include retirement-specific strategy
        has_retirement = any(
            "RA" in s["strategy"]
            or "retirement" in s["strategy"].lower()
            or "CPF" in s["strategy"]
            for s in r["strategies"]
        )
        assert has_retirement


class TestCheck15MonthWaitOut:
    def test_under_55_5_room_applies(self) -> None:
        r = check_15_month_wait_out(
            spouse_ages=(48, 46),
            youngest_buyer_age=46,
            target_hdb_rooms=5,
        )
        assert r["applies"] is True
        assert r["wait_months"] == 15

    def test_senior_couple_4_room_exempt(self) -> None:
        r = check_15_month_wait_out(
            spouse_ages=(58, 56),
            youngest_buyer_age=56,
            target_hdb_rooms=4,
        )
        assert r["applies"] is False
        assert "Senior" in r["exemption_reason"]

    def test_senior_couple_5_room_still_applies(self) -> None:
        # Senior exemption only for 4-room or smaller
        r = check_15_month_wait_out(
            spouse_ages=(58, 56),
            youngest_buyer_age=56,
            target_hdb_rooms=5,
        )
        assert r["applies"] is True

    def test_one_spouse_only_55_others_younger(self) -> None:
        # One 55, other 53 → not both 55+
        r = check_15_month_wait_out(
            spouse_ages=(55, 53),
            youngest_buyer_age=53,
            target_hdb_rooms=4,
        )
        assert r["applies"] is True

    def test_pre_sep_2022_exempt(self) -> None:
        r = check_15_month_wait_out(
            spouse_ages=(48, 46),
            youngest_buyer_age=46,
            target_hdb_rooms=5,
            has_otp_before_sep_2022=True,
        )
        assert r["applies"] is False
        assert "before Sep 30, 2022" in r["exemption_reason"]

    def test_new_bto_30_month_wait(self) -> None:
        r = check_15_month_wait_out(
            spouse_ages=(48, 46),
            youngest_buyer_age=46,
            target_hdb_rooms=4,
            target_is_new_bto=True,
        )
        assert r["wait_months"] == 30


class TestEstimateDecouplingCost:
    def test_basic_calculation(self) -> None:
        r = estimate_decoupling_cost(current_property_value=1_800_000)
        # Transferring 50% = $900k. BSD on $900k = 1,800 + 3,600 + 16,200 = 21,600
        assert r["bsd_on_transfer"] == 21_600.0
        assert r["legal_total"] == 5_000  # 2 × $2,500
        assert r["total_cash_cost"] > 25_000

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            estimate_decoupling_cost(current_property_value=0)
        with pytest.raises(ValueError):
            estimate_decoupling_cost(
                current_property_value=1_000_000, share_being_transferred=1.5
            )


class TestCompareDecouplingVsAbsd:
    def test_decoupling_wins_for_high_absd(self) -> None:
        r = compare_decoupling_vs_absd(
            current_joint_property_value=2_000_000,
            new_property_price=2_500_000,
            profile="SC",
            properties_after_new_buy=2,  # second property without decoupling
        )
        assert r["absd_without_decoupling"] == 500_000  # 20% of $2.5M
        assert r["absd_with_decoupling"] == 0  # First property for transferring spouse
        assert r["recommend_decoupling"] is True
        assert r["net_benefit"] > 400_000  # Significant savings


class TestEstimateCPFRefund:
    def test_basic(self) -> None:
        r = estimate_cpf_refund_at_sale(cpf_principal_used=300_000, years_held=10)
        assert r["accrued_interest_estimate"] > 0
        assert r["total_refund_estimate"] > 300_000
        # 5 years avg, 2.5% compound: 300k * 1.025^5 ≈ 339k. Accrued ≈ 39k.
        assert 30_000 < r["accrued_interest_estimate"] < 50_000

    def test_invalid(self) -> None:
        with pytest.raises(ValueError):
            estimate_cpf_refund_at_sale(cpf_principal_used=-1, years_held=10)


class TestEstimateTransitionCashFlow:
    def test_sell_first_scenario(self) -> None:
        r = estimate_transition_cash_flow(
            sell_price=1_500_000,
            sell_outstanding_loan=400_000,
            sell_cpf_refund_estimate=250_000,
            sell_agent_commission_rate=0.02,
            new_price=2_000_000,
            new_ltv_cap=0.75,
            new_min_cash_pct=0.05,
            new_bsd=69_600,
            new_absd_upfront=0,
            interim_months=2,
            interim_rental_monthly=4_000,
        )
        assert r["sell_net_cash"] > 0
        assert r["cpf_refunded_to_oa"] == 250_000
        assert r["new_loan_amount"] == 1_500_000
        assert r["interim_rental_total"] == 8_000

    def test_buy_first_scenario(self) -> None:
        r = estimate_transition_cash_flow(
            sell_price=1_500_000,
            sell_outstanding_loan=400_000,
            sell_cpf_refund_estimate=250_000,
            sell_agent_commission_rate=0.02,
            new_price=2_000_000,
            new_ltv_cap=0.45,  # Holding both
            new_min_cash_pct=0.25,
            new_bsd=69_600,
            new_absd_upfront=400_000,  # 20% on $2M
            interim_months=0,
            interim_rental_monthly=0,
        )
        # Higher cash requirement due to ABSD float
        assert r["total_cash_required"] > 400_000
