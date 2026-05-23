# Decision Trees

Plain-text flowcharts for the most common scenarios. Useful as guard rails for small models that may otherwise drift.

---

## Tree 1: "I want to buy a property"

```
START
 │
 ├─ Are you SC, SPR, or Foreigner?
 │   ├─ Foreigner ──► Can you buy?
 │   │                  ├─ HDB: NO (except special schemes)
 │   │                  ├─ Condo: YES (60% ABSD)
 │   │                  └─ Landed: NO (Sentosa Cove only)
 │   ├─ SPR ──────────► Same as foreigner for landed (LDAU)
 │   │                  Condo: 5%/30%/35% ABSD by count
 │   │                  HDB: YES with SC spouse or PR family
 │   └─ SC ───────────► All types available
 │
 ├─ How many properties already owned?
 │   ├─ 0 ──► 1st-property ABSD rate
 │   ├─ 1 ──► 2nd-property ABSD rate (consider sequencing/decoupling)
 │   └─ 2+ ──► 3rd-property rate; high ABSD; consider trust/structures
 │
 └─ Compute:
     ├─ BSD: progressive bands on price
     ├─ ABSD: profile × count
     ├─ Down payment: 25% first / 55% second
     ├─ Min cash: 5% first / 25% second
     ├─ Loan: stress test TDSR 55%, MSR 30% (HDB/EC)
     └─ Return: total cash needed, total CPF needed, monthly cost
```

---

## Tree 2: "I want to upgrade from HDB to Condo"

```
START: SC married couple, HDB MOP done
 │
 ├─ Do you have liquidity for ABSD float ($200k-$500k)?
 │   ├─ NO ──► SELL FIRST PATH
 │   │           1. List HDB now
 │   │           2. Sell completes (8-12 weeks)
 │   │           3. Move to interim rental (2-3 months)
 │   │           4. OTP condo as first property (0% ABSD)
 │   │           5. Move to condo
 │   │           Pros: $0 ABSD, 75% LTV
 │   │           Cons: 2 moves, interim rental cost, market timing
 │   │
 │   └─ YES ──► BUY FIRST PATH (ABSD remission)
 │              1. OTP condo (pay 20% ABSD upfront)
 │              2. Immediately list HDB
 │              3. HDB sale completes within 6 months of condo completion
 │              4. Apply ABSD refund (automatic if conditions met)
 │              5. Single move
 │              Pros: No interim rental, continuity
 │              Cons: 6-month deadline (no extensions), 45% LTV, ABSD cash float
 │
 │   ELIGIBILITY for remission: SC married couple, both on both transactions only.
 │   Single SC, SPR, or SC+Foreigner couples: NOT eligible → use Sell First.
```

---

## Tree 3: "I want to keep condo and buy another property"

```
START: Joint-owned condo, want to buy 2nd property
 │
 ├─ Is current property HDB? ──YES──► CANNOT decouple HDB. Use sell first OR pay ABSD.
 │
 ├─ Is current property jointly owned by spouses?
 │   ├─ NO ──► Decoupling not possible. Pay ABSD on 2nd or sell current.
 │   │
 │   └─ YES ──► DECOUPLING CANDIDATE
 │               │
 │               ├─ Can remaining spouse qualify for loan in sole name?
 │               │   ├─ NO ──► STOP. Decoupling fails. Reconsider.
 │               │   └─ YES ──► Continue
 │               │
 │               ├─ Compute decoupling cost (BSD on transfer + legal):
 │               │   ~$25k for $1M property, ~$35k for $2M, ~$50k for $3M+
 │               │
 │               ├─ Compute ABSD savings (transferring spouse buys as 1st):
 │               │   SC: 20% of new property price
 │               │   SPR: 25% delta
 │               │
 │               └─ Decision:
 │                   Net benefit = ABSD saved - decoupling cost
 │                   Positive (typically yes for >$1M new): GO
 │                   Negative (rare): SKIP
 │
 │   Execute: 2 separate lawyers, market valuation, complete decoupling
 │   2-4 weeks BEFORE 2nd property OTP. Update wills, CPF nominations, insurance.
```

---

## Tree 4: "I want to downsize from condo to HDB"

```
START: Own private property, want HDB resale
 │
 ├─ Is your target a brand-new BTO?
 │   ├─ YES ──► 30-MONTH WAIT from private disposal
 │   └─ NO (resale) ──► Continue
 │
 ├─ Are both spouses (or single buyer) 55 or above?
 │   ├─ NO ──► 15-MONTH WAIT applies
 │   │           Plan interim housing (rental $3-5k/mo)
 │   │           Total cost: 15 × $3,500 ≈ $52,500
 │   │
 │   └─ YES ──► Continue
 │               │
 │               ├─ Buying 4-room or smaller resale (or 2-room Flexi, CCA)?
 │               │   ├─ YES ──► SENIOR EXEMPTION; NO WAIT
 │               │   │            Direct transition
 │               │   │            Possible Silver Housing Bonus (~$30k)
 │               │   └─ NO (5-room+) ──► 15-MONTH WAIT applies
 │
 ├─ Income check for HDB loan and grants:
 │   Family income ≤ $14k → eligible for HDB loan, grants
 │   Family income > $14k → bank loan only, no grants
 │
 └─ Have you appealed the wait-out? (~25% success rate)
     Mostly approved: documented pre-Sep-2022 OTP, or extenuating circumstances
     Don't bank on appeal; plan as if wait applies
```

---

## Tree 5: "I want to sell my property"

```
START
 │
 ├─ Have you held > 3 years? ──NO──► SSD applies (12/8/4% by year)
 │                                    Check if delay viable
 │
 ├─ Outstanding mortgage redemption notice period?
 │   Some banks: 3 months notice or pay penalty
 │   Plan completion timeline accordingly
 │
 ├─ CPF accrued interest projection
 │   Principal used + 2.5% compounded
 │   Use CPF Home Calculator for exact
 │
 ├─ Pricing strategy
 │   Above market: 90th+ percentile, willing to wait
 │   At market: 50-60th percentile, typical sale
 │   Below market: 30-40th percentile, fast sale
 │
 ├─ Agent commission: 2% (negotiable) + 9% GST; seller pays both sides typical
 │
 ├─ Net proceeds = Sale - Mortgage - CPF Refund - Commission - Legal - SSD
 │
 └─ Next home plan?
     Buying next: see Trees 1-4 for sequencing
     Renting: budget $3-6k/mo bridging rental
     Moving in with family: free; consider duration
```

---

## Tree 6: "Affordability quick check"

```
START
 │
 ├─ Gross monthly household income (after 30% haircut for variable)
 │
 ├─ Existing monthly debt (other loans, car, credit card 3% balance)
 │
 ├─ TDSR headroom = (Income × 0.55) − Existing debt
 │   If ≤ 0 → STOP. Cannot afford new loan.
 │
 ├─ At stress rate (4% residential / 3% HDB):
 │   Max loan = TDSR headroom × annuity factor (30yr ~ 209x; 25yr ~ 199x; 20yr ~ 175x)
 │
 ├─ For HDB / EC from developer: also check MSR
 │   MSR cap = Income × 0.30
 │   Binding = min(TDSR, MSR)
 │
 ├─ Max purchase = Max loan ÷ LTV (0.75 first / 0.45 second)
 │
 └─ Cash + CPF required:
     Down payment = Price − Loan
     Min cash = Price × 0.05 (first) or 0.25 (second)
     BSD + ABSD + Legal + Admin = compute via tools
     Buffer = 6 months mortgage + maintenance
```
