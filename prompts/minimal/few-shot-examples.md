# Few-Shot Examples (for small models)

Small models follow patterns better than abstract instructions. Include 2-3 of these in the system prompt before sending the user query. Each example shows the EXACT desired output format.

---

## Example 1: Basic stamp duty question

**User**: SC, first home, $1.2M condo. Compute stamp duty.

**Assistant**:
```
BSD on $1,200,000:
- 1% × 180,000 = $1,800
- 2% × 180,000 = $3,600
- 3% × 640,000 = $19,200
- 4% × 200,000 = $8,000
- Total BSD: $32,600

ABSD: SC first property = 0%. Total ABSD: $0.

Total stamp duty: $32,600.
Payable within 14 days of OTP signing. CPF OA can cover BSD.

Verify on IRAS: https://www.iras.gov.sg/quick-links/calculators
```

---

## Example 2: Sequencing question

**User**: SC married couple, own HDB worth $700k (loan $200k, CPF used $180k). Want to buy $1.6M condo. Sell first or buy first?

**Assistant**:
```
Two viable paths. Comparing:

PATH A: SELL HDB FIRST
- Sale net cash: ~$500k (after loan, commission, CPF refund)
- CPF refunded: ~$180k + accrued interest
- Move to interim rental: 2-3 months × $3k = ~$8k
- Buy condo as 1st property: 0% ABSD
- LTV: 75%; down payment $400k; min cash $80k
- BSD: $44,600

PATH B: BUY CONDO FIRST (with 6-month ABSD remission)
- Pay 20% ABSD upfront: $320,000 in cash (refundable)
- LTV: 45% (holding both); down payment $880,000
- BSD: $44,600
- Sell HDB within 6 months of condo legal completion → apply ABSD refund

RECOMMENDATION:
Path A unless you can comfortably float $320k ABSD for 6 months.

Path B fits if:
- Strong liquidity reserves
- Continuity of housing critical (school-age kids)
- Confident HDB sells in 3 months

Either way:
- Engage CEA agent + conveyancing lawyer
- Get bank IPA
- Plan completion timeline carefully

Verify: HDB MOP completion on HDB Resale Portal. ABSD remission rules on IRAS.
```

---

## Example 3: Listing comparison

**User**: Compare these two condos for a young SC couple, $2M budget, 3BR, near MRT:

Listing A: Parc Komo, 1,108 sqft, $1,950k, 99yr (95 left), MRT 9 min, TOP 2021
Listing B: Riverfront Residences, 1,184 sqft, $1,880k, 99yr (93 left), MRT 11 min, TOP 2022

**Assistant**:
```
Comparison:

| Field | Parc Komo | Riverfront |
|-------|-----------|------------|
| Price | $1,950,000 | $1,880,000 |
| $/psf | $1,760 | $1,588 |
| Size | 1,108 sqft | 1,184 sqft |
| MRT | 9 min | 11 min |
| Tenure left | 95 yrs | 93 yrs |
| TOP | 2021 | 2022 |
| Fit score | 82/100 | 86/100 |

TOP PICK: Riverfront Residences

PROS:
1. Better $/psf ($172 lower per sqft)
2. Larger unit (+76 sqft, ~7% more space)
3. Newer building (1 yr difference)

CONS:
1. MRT slightly further (2 min more)
2. Riverfront area can flood-risk; verify with PUB
3. Larger MCST development; verify management quality

VERIFY NEXT:
1. URA Realis last 6 months transactions same project/size
2. MCST minutes (last 2 AGM) for both
3. Walking route on OneMap (not aerial)
4. Future URA Master Plan for both areas

QUESTIONS FOR AGENT:
1. Why is the seller selling?
2. Any pending special levies in next 12 months?
3. Outstanding maintenance fees / property tax?
4. Stack-specific facing and noise?
5. Renovation permits on file?

Recommend viewing both, weekday morning + weekend afternoon.
Engage CEA agent and conveyancing lawyer before OTP.
```

---

## Example 4: Downgrade with wait-out

**User**: Couple 48 and 46, both SC. Own $1.8M condo. Want to buy 5-room HDB resale. Can I?

**Assistant**:
```
Yes, but 15-MONTH WAIT-OUT applies.

WHY: You are private property owners moving to non-subsidised HDB resale.
The wait-out was introduced 30 Sep 2022.

SENIOR EXEMPTION CHECK:
- Both spouses 55+: NO (you are 48 and 46)
- Buying 4-room or smaller: NO (5-room)
→ Exemption does not apply. Full 15 months.

YOUR PATH:
1. Sell condo (8-16 weeks typical)
2. Move to interim rental (HDB-equivalent: $3-5k/mo)
3. WAIT 15 months from condo sale completion
4. Apply for HDB resale; OTP, exercise, complete (~8 weeks)
5. Total transition: ~20-22 months

INTERIM COSTS:
- Rental: 15 × $3,500 ≈ $52,500
- Two moves: ~$2,500
- Total: ~$55,000

APPEAL OPTION:
- File appeal with HDB if you have extenuating circumstances
- Approval rate ~25%; mostly for pre-Sep-2022 OTP or medical/elder care
- General lifestyle downsize appeals rarely succeed

ALTERNATIVE:
Wait 7 years until you're 55 and 53 → still doesn't qualify.
Wait 9 years until 57 and 55 → SENIOR EXEMPTION applies if you buy 4-room or smaller.

If you can wait 9 years AND accept a 4-room: no wait-out, direct transition.
Most people just plan around the 15 months.

Verify on HDB Resale Portal: eligibility checker.
```

---

## Example 5: Decoupling math

**User**: Joint $1.5M condo. Want to buy $1.8M second condo as investment. Both SC married.

**Assistant**:
```
DECOUPLING ANALYSIS:

Option A: Pay ABSD on second condo
- 20% × $1,800,000 = $360,000 ABSD
- LTV drops to 45%; down payment $990,000
- Min cash 25% = $450,000

Option B: Decouple first, then buy second
- Decoupling cost on $1.5M condo, transferring 50% ($750k):
  - BSD: 1%×180 + 2%×180 + 3%×390 = $17,100
  - Legal (2 lawyers): $5,000
  - Refinancing admin: $1,500
  - Valuation: $700
  - TOTAL: ~$24,300
- Spouse A now property-free; buys second condo as FIRST property
- ABSD on $1.8M: 0%
- LTV: 75%; down payment $450,000
- Min cash 5% = $90,000

NET COMPARISON:
- ABSD saved: $360,000
- Decoupling cost: $24,300
- Net benefit: $335,700
- Plus: avoid $540,000 extra down payment burden from 45% LTV cap

RECOMMENDATION: DECOUPLE.

CHECKLIST:
1. Confirm remaining spouse can qualify for refinanced loan in sole name
2. Engage 2 SEPARATE lawyers (joint counsel = IRAS red flag)
3. Independent valuation of $1.5M condo
4. Execute decoupling fully (BSD paid, refinancing done) BEFORE second OTP
5. Leave 2-4 weeks between decoupling completion and second OTP
6. Update wills, CPF nominations, insurance

RISKS:
- Loan rejection in sole name → pre-qualify first
- IRAS scrutiny → keep market-value transfer + paper trail
- Future divorce complications → consult family lawyer

Engage tax adviser before executing for any unusual structuring.
```

---

## How to use these examples

1. Paste the system prompt (tiny or compact)
2. Paste 1-3 relevant examples above (skip irrelevant ones to save tokens)
3. Then send the user query

The agent will mirror the format of the examples.

For small local models (Gemma 4 26B, Qwen 8B), this few-shot scaffolding makes a big quality difference. For larger frontier models, the system prompt alone is sufficient.
