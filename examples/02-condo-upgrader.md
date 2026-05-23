# Example 2: HDB Upgrader to Private Condo

## Scenario

**Profile**: Married couple, both SC, 42 yrs old, 2 kids. Currently own a 5-room HDB in Bukit Panjang (bought 2016 for $480k, MOP done). Outstanding HDB loan $180k. CPF used on flat (with accrued interest): ~$220k. Combined income $18,500/month. No car loan, $300/month credit card minimum.

**Goal**: Sell HDB, buy a 4-bedroom RCR/OCR condo for the family. Budget $2.2M – $2.5M.

## Step 1: Intake and sequence planning

> Agent: Couple in their 40s, upgrader path. Two big decisions:
> 1. Sell first, then buy — or buy first, then sell?
> 2. ABSD timing matters: buying a second residential property triggers 20% ABSD unless you sell HDB within 6 months and apply for remission.
>
> Quick model:

### Sell first, then buy
- HDB sells. Net proceeds (~$300k cash to you, plus $220k back to CPF after returning principal + accrued interest)
- 2-3 months bridging rental
- Buy condo with no ABSD overhang
- Cleaner, but two moves and rental cost

### Buy first, sell within 6 months
- Pay 20% ABSD upfront (~$440k–$500k on $2.2M-$2.5M)
- Sell HDB within 6 months of OTP for resale (or NVP for new launch)
- Apply for ABSD refund (married couple, both SC, with at least one SC)
- Faster move, but huge cash float and refund timing risk

### Decoupling alternative (for second property)
- Not applicable here since you're not keeping the HDB.

> Recommend: buy first if confident on selling HDB quickly (it's a desirable 5-room in BP, probably under 3 months DOM). Have backup plan if it doesn't sell.

## Step 2: Compute ABSD exposure

Agent calls `calculate_absd(2_300_000, "SC", 2)`:

> ABSD on second property at $2.3M = 20% × $2.3M = **$460,000**.
>
> Plus BSD: `calculate_bsd(2_300_000)` = 1%×180k + 2%×180k + 3%×640k + 4%×500k + 5%×800k = 1,800 + 3,600 + 19,200 + 20,000 + 40,000 = **$84,600**.
>
> If sold and remission granted within 6 months: refund $460,000. Net = $84,600 BSD only.

## Step 3: Affordability

> Agent calls `estimate_max_loan(18_500, 300, 0.04, 30, 0.55, False)`:
> Max bank loan (TDSR) ≈ $1.97M.
>
> But you already have $180k HDB loan outstanding. After selling HDB, that's cleared. For new condo purchase IPA, this is treated as outstanding until clearance.
>
> Plan: get IPA based on post-sale position (bank may grant conditional IPA subject to HDB sale completing).
>
> At $2.3M purchase, 75% LTV = $1.725M loan. Within max. Headroom for cushion.

## Step 4: Cashflow model (buy-first scenario, $2.3M condo)

| Item | Amount | Source |
|------|--------|--------|
| Booking fee (new launch) or option fee (resale) | ~$115k (5%) or ~$23k (1%) | Cash |
| Exercise top-up to 25% | $460k | Cash + CPF |
| BSD | $84,600 | CPF OA + Cash |
| ABSD | $460,000 | **Cash** (refund later if remission granted) |
| Legal fees | $3,500 | Cash |
| Stamp duty admin | $500 | Cash |
| **Estimated upfront cash** | **~$1,025,000** | (mix CPF + cash) |

Of which strict cash component:
- ABSD: $460k (refundable)
- Legal + admin: $4k
- Cash portion of down payment (5% min): $115k
- Stamp duty admin: $500
- **Hard cash needed**: ~$580k

From HDB sale: net cash to you ~$300k + bank loan $1.725M + CPF $300k+ (post-grant). Need bridging financing for the ABSD overhang.

## Step 5: Risk flagging

> Agent: Three risks to flag clearly:
>
> 1. **ABSD refund timing**: If HDB sale slips past 6 months from condo OTP, ABSD refund denied. Plan HDB sale aggressively.
> 2. **CPF accrued interest**: On HDB sale, you return ~$220k to CPF. This continues to earn 2.5%, then can be used for new condo. But it's CPF, not cash.
> 3. **Cashflow mid-transaction**: You're temporarily holding 2 properties. Bridging loan from bank possible but adds interest cost.

## Step 6: Condo shortlist criteria

- 4 bedrooms (or 3-bed dual key)
- Min 1,200 sqft internal
- 99-year or freehold; minimum 75 yrs remaining for 99
- RCR or OCR with good schools in catchment (you have 2 kids)
- ≤ 10 min walk to MRT
- New launch or resale built ≤ 15 yrs

## Step 7: Sample comparison

| Listing | Project | Type | Size | Price | $/psf | MRT min | Tenure left | Fit |
|---------|---------|------|------|-------|-------|---------|-------------|-----|
| A | Treasure At Tampines | 4BR | 1,302 sqft | $2.25M | $1,728 | 12 | 96 | 78 |
| B | Bayshore | 4BR | 1,378 sqft | $2.45M | $1,778 | 7 | 99 (new launch) | 86 |
| C | Coastline Residences | 4BR | 1,302 sqft | $2.18M | $1,674 | 10 | freehold | 84 |

Top pick: B (Bayshore) for new launch, best MRT, full lease. Cost premium covered by upgrader cash.

## Step 8: Action sequence

1. List HDB now (or in parallel with condo search)
2. Engage condo agent and conveyancing lawyer
3. Obtain bank IPA for $1.725M (subject to HDB sale)
4. Shortlist 5 condos, view in next 3 weekends
5. Negotiate OTP on top pick (target 1% option fee, 14-day option)
6. Time HDB OTP to sit within 4-5 months of condo OTP (buffer for completion)
7. Apply for ABSD remission immediately on HDB sale completion

## Step 9: Escalation

- CEA agent for condo (separate from HDB agent for cleaner conflicts)
- Conveyancing lawyer (one firm for both transactions can simplify)
- Bank mortgage specialist (compare 3 banks for IPA)
- Tax adviser if any ambiguity on ABSD remission

End: "All figures illustrative. Confirm IPA, ABSD refund eligibility, and CPF refund computations with bank, IRAS, and CPF Board respectively."
