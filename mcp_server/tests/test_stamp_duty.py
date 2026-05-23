"""Tests for stamp duty calculators."""

from __future__ import annotations

import pytest

from sg_property_mcp.tools.stamp_duty import (
    calculate_absd,
    calculate_bsd,
    calculate_ssd,
)


class TestBSD:
    def test_known_values(self) -> None:
        # $1M residential: 1% × 180k + 2% × 180k + 3% × 640k = 1,800 + 3,600 + 19,200 = 24,600
        assert calculate_bsd(1_000_000).total == 24_600.0
        # $1.5M: + 4% × 500k = 24,600 + 20,000 = 44,600
        assert calculate_bsd(1_500_000).total == 44_600.0
        # $2M: + 5% × 500k = 44,600 + 25,000 = 69,600
        assert calculate_bsd(2_000_000).total == 69_600.0
        # $3M: + 5% × 1M = 44,600 + 75,000 = 119,600
        assert calculate_bsd(3_000_000).total == 119_600.0
        # $4M: + 6% × 1M above $3M = 119,600 + 60,000 = 179,600
        assert calculate_bsd(4_000_000).total == 179_600.0

    def test_small_amount(self) -> None:
        # $100k: 1% × 100k = 1,000
        assert calculate_bsd(100_000).total == 1_000.0

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            calculate_bsd(0)
        with pytest.raises(ValueError):
            calculate_bsd(-1)

    def test_non_residential_caps_at_5(self) -> None:
        # $2M non-residential: 1% × 180 + 2% × 180 + 3% × 640 + 4% × 500 + 5% × 500
        # = 1,800 + 3,600 + 19,200 + 20,000 + 25,000 = 69,600
        assert calculate_bsd(2_000_000, "non_residential").total == 69_600.0
        # $5M non-residential: + 5% × 3.5M cap at 5% = 69,600 + 175,000 - but cap is 5% above $1.5M.
        # Bands: 180+180+640+500=1.5M done. Above 1.5M: 5%.
        # = 1,800 + 3,600 + 19,200 + 20,000 + (5,000,000-1,500,000)*0.05
        # = 44,600 + 175,000 = 219,600
        assert calculate_bsd(5_000_000, "non_residential").total == 219_600.0


class TestABSD:
    def test_sc_first(self) -> None:
        r = calculate_absd(1_000_000, "SC", 1)
        assert r.total == 0.0

    def test_sc_second(self) -> None:
        r = calculate_absd(1_000_000, "SC", 2)
        assert r.total == 200_000.0

    def test_sc_third(self) -> None:
        r = calculate_absd(1_000_000, "SC", 3)
        assert r.total == 300_000.0

    def test_sc_fourth_treated_as_third(self) -> None:
        r = calculate_absd(1_000_000, "SC", 5)
        assert r.total == 300_000.0

    def test_spr_first(self) -> None:
        r = calculate_absd(1_000_000, "SPR", 1)
        assert r.total == 50_000.0

    def test_spr_second(self) -> None:
        r = calculate_absd(1_000_000, "SPR", 2)
        assert r.total == 300_000.0

    def test_spr_third(self) -> None:
        r = calculate_absd(1_000_000, "SPR", 3)
        assert r.total == 350_000.0

    def test_foreigner_any(self) -> None:
        assert calculate_absd(1_000_000, "FOREIGNER", 1).total == 600_000.0
        assert calculate_absd(1_000_000, "FOREIGNER", 2).total == 600_000.0
        assert calculate_absd(1_000_000, "FOREIGNER", 3).total == 600_000.0

    def test_entity(self) -> None:
        assert calculate_absd(1_000_000, "ENTITY", 1).total == 650_000.0

    def test_trustee(self) -> None:
        assert calculate_absd(1_000_000, "TRUSTEE", 1).total == 650_000.0

    def test_invalid_profile(self) -> None:
        with pytest.raises(ValueError):
            calculate_absd(1_000_000, "OTHER", 1)

    def test_invalid_count(self) -> None:
        with pytest.raises(ValueError):
            calculate_absd(1_000_000, "SC", 0)

    def test_case_insensitive_profile(self) -> None:
        assert calculate_absd(1_000_000, "sc", 2).total == 200_000.0
        assert calculate_absd(1_000_000, "foreigner", 1).total == 600_000.0


class TestSSD:
    def test_within_1yr(self) -> None:
        r = calculate_ssd(1_000_000, 6)
        assert r.total == 120_000.0

    def test_at_1yr_boundary(self) -> None:
        r = calculate_ssd(1_000_000, 12)
        assert r.total == 120_000.0

    def test_2nd_yr(self) -> None:
        r = calculate_ssd(1_000_000, 18)
        assert r.total == 80_000.0

    def test_3rd_yr(self) -> None:
        r = calculate_ssd(1_000_000, 30)
        assert r.total == 40_000.0

    def test_after_3yr(self) -> None:
        r = calculate_ssd(1_000_000, 37)
        assert r.total == 0.0

    def test_well_after_3yr(self) -> None:
        r = calculate_ssd(1_000_000, 120)
        assert r.total == 0.0
