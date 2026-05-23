# Example 5: Affordability Check (Quick Triage)

## Scenario

User asks: "Combined household income $20,000/month. Want to buy a $2.5M condo. Can I afford it?"

## Step 1: Quick model with MCP tools

Agent calls `estimate_max_loan(20_000, 0, 0.04, 30, 0.55, False)`:

> Max loan (TDSR, no debt): ≈ **$2,302,000**

For $2.5M condo at 75% LTV, required loan = $1.875M. Within TDSR headroom. ✓

## Step 2: Compute upfront

Agent calls `calculate_bsd(2_500_000)`:
> BSD = 1%×180 + 2%×180 + 3%×640 + 4%×500 + 5%×1,000 = 1,800 + 3,600 + 19,200 + 20,000 + 50,000 = **$94,600**

Agent asks: "Is this first or second property? Profile (SC/SPR/foreigner)?"

User: "First property, both SC."

Agent calls `calculate_absd(2_500_000, "SC", 1)`:
> ABSD = $0

## Step 3: Cash and CPF requirements

| Item | Amount | Source |
|------|--------|--------|
| Down payment 25% on $2.5M | $625,000 | 5% min cash ($125k) + CPF + cash for the rest |
| BSD | $94,600 | CPF OA or cash |
| Legal fees | $3,500 | Cash |
| Valuation fee | $500 | Cash |
| **Total upfront** | **$723,600** | |

Of which **minimum cash needed**: ~$125,000 (5% LTV cash) + $4,000 (legal/admin) = **~$129,000**.

Rest can be CPF + cash mix.

## Step 4: Monthly cost

Agent calls `estimate_mortgage(1_875_000, 0.02, 30)`:
> Monthly mortgage = ~$6,929 at 2% over 30 yrs

Add:
- Maintenance fee ~$450/mo
- Property tax (AV ~$45k, owner-occupied): annual ~$1,800, monthly ~$150
- Fire insurance ~$50/mo
- **Total monthly cost**: ~$7,580

Agent calls `check_tdsr_msr(6929, 20_000, 0, False)`:
> TDSR = 34.6%. Within 55% cap. ✓

## Step 5: Stress test scenarios

> Agent: Let's stress test:
>
> **Scenario A: rates rise to 4% (current stress floor)**
> Monthly payment at 4% over 30 yrs: $8,948. TDSR = 44.7%. Still within cap.
>
> **Scenario B: one income drops 30% (variable component)**
> Income = $14,000. TDSR at current 2% rate: $6,929/$14,000 = 49.5%. Tight but OK.
>
> **Scenario C: both stress + income drop**
> $8,948/$14,000 = 63.9%. Fail TDSR. Would need to reduce loan quantum or accept tighter cashflow.

## Step 6: Buffer recommendation

> Recommend: keep cash buffer of **6 months of mortgage + maintenance** = ~$45,000 in liquid savings post-completion.
>
> Plus: renovation budget if needed ($30k-$150k depending on scope and unit condition).

## Step 7: Summary

```
At $2.5M condo, first property, both SC, no existing debt:

✓ TDSR: 34.6% (cap 55%) - PASS
✓ LTV: 75% bank loan possible
✓ Stress at 4%: 44.7% TDSR - PASS

Upfront cash: ~$129k minimum
Upfront CPF + cash: ~$724k
Monthly: ~$7,580 (mortgage + maintenance + tax + insurance)

Buffer recommended: $45k+ liquid post-completion
Renovation budget: separate, $30k-$150k depending on scope

Verdict: Affordable. Watch:
- Rate normalisation risk (stress test passes)
- Variable income haircut (stress test tight)
- Renovation cashflow
```

## Step 8: Caveats and escalation

> Agent: "Illustrative only. Get bank IPA based on actual income documents (3 months payslips, 12 months bank statements, NOA). Income haircut on variable / commission components may reduce max loan. Compare 2-3 banks for best package. Engage independent mortgage broker for shortlist if you want neutral comparison."
>
> Recommended next steps:
> 1. Get IPA from 2-3 banks (no obligation)
> 2. Engage conveyancing lawyer to review OTP terms before signing
> 3. Confirm CPF accrued interest projection on CPF Home Calculators
