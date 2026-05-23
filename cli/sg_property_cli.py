#!/usr/bin/env python3
"""SG Property Agent CLI — Ollama-backed conversation with Python calculators.

Wraps a local Ollama model with deterministic Python calculators so smaller
models don't have to do arithmetic in their head. Auto-detects keywords and
runs the relevant calculator, injecting results into the model's context.

Usage:
    sg_property_cli.py "I'm SC, first home, $1.8M condo. Compute stamp duties."
    sg_property_cli.py --model sg-property "Upgrade HDB to $2M condo, SC couple. Sell first or buy first?"
    sg_property_cli.py --interactive
    echo "BSD on $1.5M" | sg_property_cli.py

Requirements:
    - Ollama running at http://localhost:11434
    - A model built from one of the Modelfiles (default: sg-property)
    - sg-property-ai-agent installed (or PYTHONPATH set to mcp_server/)

The CLI does not require the FastMCP server to be running.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Any

try:
    from sg_property_mcp.tools import (
        lease_decay,
        mortgage,
        scorecard,
        stamp_duty,
        upgrade_paths,
    )
except ImportError:
    sys.stderr.write(
        "Error: sg_property_mcp not on PYTHONPATH.\n"
        "Run: PYTHONPATH=mcp_server python cli/sg_property_cli.py\n"
        "Or install: uv pip install -e .\n"
    )
    sys.exit(1)


OLLAMA_URL = "http://localhost:11434/api/generate"


# -------------- Keyword → calculator dispatcher --------------

# Require at least one digit, allow commas/decimals/k/m suffix
PRICE_RE = re.compile(r"\$?(\d[\d,]*(?:\.\d+)?)\s*([kKmM])?\b")


def parse_amount(text: str) -> float | None:
    """Extract first SGD amount from text. Supports $1.8M, 1,800,000, 720k, etc.

    Returns the first match that is plausibly a property amount (≥ $1,000).
    Ignores small numbers (likely ages, percentages, room counts).
    """
    for m in PRICE_RE.finditer(text):
        raw = m.group(1).replace(",", "")
        if not raw:
            continue
        try:
            n = float(raw)
        except ValueError:
            continue
        suffix = (m.group(2) or "").upper()
        if suffix == "K":
            n *= 1_000
        elif suffix == "M":
            n *= 1_000_000
        # Filter out small numbers (likely ages, room counts, percentages)
        if n >= 1_000:
            return n
    return None


def detect_profile(text: str) -> str:
    """Detect SC/SPR/FOREIGNER/ENTITY from query text."""
    t = text.upper()
    if "FOREIGNER" in t or "FOREIGN" in t:
        return "FOREIGNER"
    if " SPR" in t or "PERMANENT RESIDENT" in t or "PR " in t:
        return "SPR"
    if "ENTITY" in t or "COMPANY" in t or "TRUSTEE" in t:
        return "ENTITY"
    return "SC"


def detect_property_count(text: str) -> int:
    """Detect 1st/2nd/3rd property from query text."""
    t = text.lower()
    if "third" in t or "3rd" in t or "3 properties" in t:
        return 3
    if "second" in t or "2nd" in t or "investment" in t or "2 properties" in t:
        return 2
    return 1


def run_calculators(query: str) -> str:
    """Auto-detect intent and run relevant calculators. Return formatted result string."""
    parts: list[str] = []
    q = query.lower()

    amount = parse_amount(query)
    profile = detect_profile(query)
    count = detect_property_count(query)

    if amount and ("bsd" in q or "stamp dut" in q or "buyer" in q):
        bsd = stamp_duty.calculate_bsd(amount)
        parts.append(
            f"[BSD on ${amount:,.0f}: ${bsd.total:,.2f}]\n"
            + "\n".join(f"  - {n}" for n in bsd.notes)
        )

    if amount and ("absd" in q or "additional" in q):
        absd = stamp_duty.calculate_absd(amount, profile, count)
        parts.append(
            f"[ABSD on ${amount:,.0f} ({profile} property #{count}): "
            f"${absd.total:,.2f}]\n" + "\n".join(f"  - {n}" for n in absd.notes[:3])
        )

    if amount and ("ssd" in q or "seller" in q):
        # Default to 2 years if not specified
        months = 24
        m = re.search(r"(\d+)\s*(year|yr|month|mo)", q)
        if m:
            v = int(m.group(1))
            months = v * 12 if "y" in m.group(2) else v
        ssd = stamp_duty.calculate_ssd(amount, months)
        parts.append(
            f"[SSD on ${amount:,.0f} at {months} months held: ${ssd.total:,.2f}]"
        )

    if "mortgage" in q or "monthly payment" in q or "loan" in q:
        if amount:
            # Try to find rate and tenure
            rate_m = re.search(r"(\d+(?:\.\d+)?)\s*%", q)
            tenure_m = re.search(r"(\d+)\s*(yr|year)", q)
            rate = float(rate_m.group(1)) / 100 if rate_m else 0.025
            tenure = int(tenure_m.group(1)) if tenure_m else 30
            mt = mortgage.estimate_mortgage(amount, rate, tenure)
            parts.append(
                f"[Mortgage ${amount:,.0f} @ {rate:.2%} / {tenure}yr: "
                f"${mt.monthly_payment:,.2f}/mo, total interest ${mt.total_interest:,.0f}]"
            )

    if "max loan" in q or "affordab" in q or "tdsr" in q or "msr" in q:
        income_m = re.search(r"income[^\d]*([\d,]+)", q)
        if income_m:
            income = float(income_m.group(1).replace(",", ""))
            msr = "hdb" in q or "msr" in q
            stress = 0.03 if "hdb" in q else 0.04
            ml = mortgage.estimate_max_loan(
                gross_monthly_income=income,
                existing_monthly_debt=0,
                stress_rate=stress,
                tenure_years=30,
                msr_applicable=msr,
            )
            parts.append(
                f"[Max loan @ ${income:,.0f}/mo income, stress {stress:.0%}: "
                f"${ml['max_loan']:,.0f}]"
            )

    # Upgrade path detection
    if any(
        k in q
        for k in [
            "upgrade",
            "downgrade",
            "sell first",
            "buy first",
            "hdb to condo",
            "condo to landed",
            "condo to hdb",
        ]
    ):
        # Try to extract current and target
        current = None
        target = None
        if "hdb to condo" in q or ("hdb" in q and "condo" in q and "to condo" in q):
            current, target = "HDB", "CONDO"
        elif "condo to landed" in q or (
            "condo" in q and "landed" in q and "to landed" in q
        ):
            current, target = "CONDO", "LANDED"
        elif "condo to hdb" in q or ("condo" in q and "hdb" in q and "downgrade" in q):
            current, target = "CONDO", "HDB"
        elif "landed to condo" in q or "downsize" in q:
            current, target = "LANDED", "CONDO"

        if current and target and amount:
            marital = (
                "MARRIED_SC_SC"
                if ("married" in q or "couple" in q) and profile == "SC"
                else "SINGLE"
            )
            result = upgrade_paths.analyze_upgrade_path(
                current_property=current,
                target_property=target,
                new_price=amount,
                profile=profile,
                marital_status=marital,
                properties_after_new_buy=count,
            )
            parts.append(f"[Upgrade analysis {current} → {target} at ${amount:,.0f}]")
            for s in result["strategies"]:
                parts.append(
                    f"  Strategy: {s['strategy']}"
                    f"\n    Eligible: {s['eligible']}; ABSD net: ${s['absd_net']:,.0f}; "
                    f"LTV cap: {s['ltv_cap']:.0%}"
                )

    # 15-month wait check
    if "15 month" in q or "wait" in q or ("condo" in q and "hdb" in q):
        age_m = re.findall(r"(\d{2})\s*(?:and|,)?\s*(\d{2})?", q)
        if age_m:
            spouse_ages = None
            youngest = None
            for ages in age_m:
                if ages[0] and ages[1]:
                    try:
                        a, b = int(ages[0]), int(ages[1])
                        if 18 <= a <= 99 and 18 <= b <= 99:
                            spouse_ages = (a, b)
                            youngest = min(a, b)
                            break
                    except ValueError:
                        pass
            # Default to 4-room if not specified
            rooms_m = re.search(r"(\d)-?room", q)
            rooms = int(rooms_m.group(1)) if rooms_m else 4
            if spouse_ages:
                wo = upgrade_paths.check_15_month_wait_out(
                    target_hdb_rooms=rooms,
                    spouse_ages=spouse_ages,
                    youngest_buyer_age=youngest,
                )
                parts.append(
                    f"[15-month wait check: ages {spouse_ages[0]}/{spouse_ages[1]}, "
                    f"{rooms}-room target]"
                    f"\n  Applies: {wo['applies']}; "
                    f"Wait: {wo['wait_months']} months"
                )
                if wo["exemption_reason"]:
                    parts.append(f"  Reason: {wo['exemption_reason']}")

    return "\n\n".join(parts) if parts else ""


def ollama_chat(model: str, prompt: str, num_ctx: int = 16384) -> str:
    """Send a prompt to Ollama and return the response text."""
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_ctx": num_ctx},
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            return data.get("response", "(no response)")
    except urllib.error.URLError as e:
        sys.stderr.write(
            f"Error: cannot reach Ollama at {OLLAMA_URL}.\n"
            f"Is `ollama serve` running?\n"
            f"Underlying: {e}\n"
        )
        sys.exit(2)


def build_prompt(user_query: str, calculator_output: str = "") -> str:
    """Augment the user query with calculator results if any."""
    if calculator_output:
        return (
            f"User query: {user_query}\n\n"
            f"Calculator results (use these exact figures, do not recompute):\n"
            f"{calculator_output}\n\n"
            f"Respond to the user. Use the calculator results above. "
            f"Add any context, caveats, and next steps."
        )
    return user_query


def run_query(
    model: str, user_query: str, num_ctx: int = 16384, verbose: bool = False
) -> str:
    """Run a single query against the agent."""
    calc_output = run_calculators(user_query)
    if verbose and calc_output:
        sys.stderr.write(f"\n[Calculator pre-pass]\n{calc_output}\n\n")
    prompt = build_prompt(user_query, calc_output)
    return ollama_chat(model, prompt, num_ctx)


def interactive_loop(model: str, num_ctx: int, verbose: bool) -> None:
    """Simple REPL for the agent."""
    print(f"SG Property Agent (model: {model}). Ctrl-C to exit.\n")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not line:
            continue
        if line.lower() in ("exit", "quit", "bye"):
            return
        response = run_query(model, line, num_ctx, verbose)
        print(f"\n{response}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SG Property Agent CLI (Ollama-backed)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Single query to process. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--model",
        default="sg-property",
        help="Ollama model name (default: sg-property)",
    )
    parser.add_argument(
        "--num-ctx",
        type=int,
        default=16384,
        help="Context window size (default: 16384; reduce for low-RAM)",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive REPL",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show calculator pre-pass output",
    )
    args = parser.parse_args()

    if args.interactive:
        interactive_loop(args.model, args.num_ctx, args.verbose)
        return

    if args.query:
        query = args.query
    elif not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    else:
        parser.error("Provide a query, use --interactive, or pipe via stdin.")

    response = run_query(args.model, query, args.num_ctx, args.verbose)
    print(response)


if __name__ == "__main__":
    main()
