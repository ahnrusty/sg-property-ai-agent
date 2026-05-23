# Example 1: HDB Resale Buyer (Young Family, First Home)

## Scenario

**Profile**: Married couple, both SC, 32 yrs old, 1 toddler. First-time HDB buyer (have not taken any HDB grant). Combined gross income $11,000/month. Combined CPF OA $80,000. No existing debt.

**Goal**: Buy a 4-room HDB resale in Tampines or Bedok, near MRT, within 12 weeks.

**Budget**: Up to $750,000.

## Conversation flow

### Step 1: Intake confirmation

> User: We're looking at HDB resale 4-room in Tampines or Bedok. Budget $700k-$750k. We have $80k CPF and around $50k cash. Income is $11k combined. No debt.

> Agent: Got it. Couple, both SC, first HDB, no grant taken yet. Combined income $11k, no debt. 4-room resale, Tampines or Bedok. $700-750k budget, $50k cash + $80k CPF on hand.
>
> Quick eligibility check:
> - Public Scheme (married SC couple): qualify
> - Income ceiling for HDB loan: $14k family — you pass
> - First-timer for grants: yes, eligible for Enhanced CPF Housing Grant (EHG)
>
> You qualify for:
> - EHG: up to $80,000 (full grant at ≤ $9k household; at $11k household, around $50,000-$60,000)
> - Family Grant (Resale): up to $50,000 (households ≤ $14k income, buying 3-room or larger)
> - Proximity Housing Grant: $20,000 to live with parents or $30,000 to live near (within 4km) — does this apply?
>
> Tell me about parent proximity and any preferred blocks or sub-areas. Then I'll model affordability.

### Step 2: Affordability with MCP tools

User says parents are in Bedok Reservoir, so PHG (proximity) of $30k applies.

> Agent (calls `estimate_max_loan` with income $11,000, debt $0, stress_rate 0.03 [HDB loan floor], tenure 25 yrs, MSR applicable):
>
> Result: Max HDB loan ≈ $696,000 (MSR-bound at 30%).
>
> Translates to: max purchase ~$928,000 with HDB loan at 75% LTV (since cash + CPF cover the rest).
>
> Your $750k cap is well within affordability. Healthy.
>
> Grants:
> - EHG (at $11k household): ~$55,000 (estimate; check HDB calculator)
> - Family Grant Resale: $50,000
> - PHG (near parents 4km): $30,000
> - **Total grants ≈ $135,000** (goes into CPF OA on completion)
>
> This effectively brings your acquisition cost down significantly.

### Step 3: Cash + CPF outlay at $720k purchase

> Agent calls `calculate_bsd(720000)`:
> BSD = 1% × 180k + 2% × 180k + 3% × 360k = 1,800 + 3,600 + 10,800 = **$16,200**
>
> Agent calls `calculate_absd(720000, "SC", 1)`:
> ABSD = $0 (first property, SC)
>
> Down payment: at 75% LTV (HDB loan), loan = $540,000. Down payment = $180,000.
> - 5% min cash: $9,000
> - Remaining $171,000: CPF OA + Grants OK
> - Available CPF + grants: $80k existing + $135k grants = $215k → covers the $171k down payment with room left
>
> Stamp duty:
> - BSD $16,200: cash or CPF
> - Legal fees ~$2,500 (HDB-approved law firm)
> - Valuation fee ~$120
>
> **Estimated cash at completion: ~$9,000 + $2,500 + $120 = ~$12,000**
>
> Monthly cost at $540k HDB loan, 2.6% interest, 25 yrs:
> Agent calls `estimate_mortgage(540000, 0.026, 25)`:
> ~$2,449/month
>
> Plus conservancy ~$80/month, property tax ~$70/month (owner-occupied), total **~$2,600/month**.
>
> MSR check: $2,449 / $11,000 = 22.3%. Well below 30% cap. Healthy.

### Step 4: Shortlist criteria

> Agent: Define filters for your shortlist:
> - 4-room (≥ 90 sqm typical)
> - Tampines or Bedok planning area
> - Within 8 min walk to MRT (Tampines, Tampines East, Tampines West, Bedok, Tanah Merah, Bedok Reservoir)
> - At least 70 years remaining lease (so CPF and bank loan unconstrained for your age)
> - Ideally not on low floor facing main road
> - Ethnic Integration Policy check on shortlisted blocks
>
> Should I draft a search brief with these filters that you can give your HDB agent?

### Step 5: Comparison output

After viewings, user pastes 3 listings. Agent uses `compare_listings`:

| Listing | Block | Floor | Sqft | Price | $/psf | MRT min | Lease left | Fit score |
|---------|-------|-------|------|-------|-------|---------|------------|-----------|
| A | Blk 412 Tampines St 41 | 14 | 1,001 | $698,000 | $697 | 6 | 70 | 88 |
| B | Blk 729 Bedok Reservoir Rd | 8 | 990 | $720,000 | $727 | 9 | 64 | 76 |
| C | Blk 261 Tampines St 23 | 19 | 1,001 | $735,000 | $734 | 4 | 68 | 82 |

Top pick: A (best $/psf, longest lease, MRT close, mid floor).

### Step 6: Verify next

- Pull last 12 months transacted prices for these blocks on HDB Resale Statistics
- Check EIP / SPR quota for each block on HDB Resale Portal
- Confirm no major renovations done without permit
- Note Blk 729 Bedok Reservoir is the oldest — verify CPF and loan tenure implications

### Step 7: Questions for the agent

1. Why is the seller selling?
2. Any renovation permits on file?
3. Any HDB outstanding charges?
4. Recent (12 months) transactions in the same block?
5. EIP and SPR quota status for buyers from <your ethnicity>?
6. Earliest completion date the seller can accommodate?

### Step 8: Escalation

- CEA-registered HDB agent for viewings and OTP
- Conveyancing lawyer (~$2,500 to $3,000 for HDB resale)
- Bank for IPA (compare HDB loan vs bank loan after IPA)

End with: "Illustrative only. Confirm grants and loan eligibility on HDB Resale Portal and with your bank."
