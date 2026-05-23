# Example 6: Condo to Landed (Upgrader with Decoupling)

## Scenario

**Profile**: Married couple, both SC, mid-40s, 2 teenage kids. Own a $2.5M condo in Bukit Timah jointly (bought 2018, fully amortising). Outstanding loan $600k. CPF used + accrued interest combined ~$450k. Combined gross income $35,000/month. Want to buy a $4M freehold semi-detached in Frankel area.

**Goal**: Get into landed without paying $800,000 ABSD. Retain condo for rental income.

## Step 1: Triage

> Agent: Strong upgrade scenario. Three paths to consider:
>
> **Path A**: Sell condo first, buy landed (0% ABSD, simplest)
> - Saves $800k ABSD
> - But: forfeits ongoing rental income from condo (~$5,500/mo ≈ $66k/yr)
> - Lose option to hold appreciating Bukit Timah condo long-term
>
> **Path B**: Buy landed first, sell condo within 6 months (ABSD remission)
> - Refunds $800k ABSD after sale
> - LTV drops to 45% on landed → need $2.2M down payment
> - 6-month deadline pressure
> - Still forfeit rental income from condo
>
> **Path C**: Decouple condo, then buy landed in transferring spouse's name
> - Spouse A transfers 50% share to Spouse B → Spouse B sole owner of condo
> - Spouse A buys landed as first property at 0% ABSD
> - Retain condo for rental
> - Cost: ~$35k for decoupling
>
> **Recommendation**: Path C if loan qualifies in sole name. Let me model it.

## Step 2: Decoupling feasibility check

Agent calls helper:
> Joint condo at $2.5M; transferring 50% = $1.25M consideration.
> `calculate_bsd(1_250_000)` = 1%×180 + 2%×180 + 3%×640 + 4%×250 = 1,800 + 3,600 + 19,200 + 10,000 = **$34,600**.
>
> Add legal fees (2 lawyers): $5,000
> Mortgage refinancing: $2,000
> Valuation: $700
> **Total decoupling cost: ~$42,000**

Loan qualification in Spouse B's sole name:
> Spouse B income: assume $18,000 (out of $35k combined).
> Outstanding loan after decoupling: $600k mortgage continues, plus Spouse A's CPF refund creates change in cashflow.
>
> `estimate_max_loan(18000, 0, 0.04, 25, 0.55)`: max bank loan ~$1.66M.
>
> Existing $600k well within capacity. ✓ Loan qualifies in sole name.

CPF refund to Spouse A:
> Assume Spouse A's share of CPF used + interest: ~$225k (half of $450k).
> Returns to Spouse A's OA. Available for landed down payment.

## Step 3: Landed purchase math (Spouse A as first-time buyer)

Agent calls:
- `calculate_bsd(4_000_000)`: 1%×180 + 2%×180 + 3%×640 + 4%×500 + 5%×1,500 + 6%×1,000 = 1,800 + 3,600 + 19,200 + 20,000 + 75,000 + 60,000 = **$179,600**
- `calculate_absd(4_000_000, "SC", 1)`: **$0** (Spouse A first property)

Down payment at 75% LTV (first property):
- Loan: $3M
- Down payment: $1M (5% min cash = $200k + balance CPF/cash)

Spouse A's loan eligibility:
- `estimate_max_loan(17000, 0, 0.04, 30, 0.55)`: max ~$2.96M.
- Close to $3M needed. May need joint borrower (Spouse B as guarantor only) — but that may complicate the ABSD position. Verify with bank if joint borrower (not joint owner) affects ABSD classification.
- Alternative: increase LTV via reducing loan to $2.9M, top up cash.

## Step 4: Cash + CPF assembly

| Item | Amount | Source |
|------|--------|--------|
| Decoupling: BSD on transfer | $34,600 | Cash |
| Decoupling: Legal + admin | $7,700 | Cash |
| Spouse A CPF refunded to OA | +$225,000 | Available for landed |
| Landed: 5% cash deposit on OTP | $200,000 | Cash |
| Landed: Balance down payment 20% | $800,000 | CPF + Cash |
| Landed: BSD | $179,600 | CPF or Cash |
| Landed: Legal | $5,000 | Cash |
| Landed: Stamp duty admin + valuation | $1,500 | Cash |

**Hard cash needed (decoupling + landed cash portion)**: $34,600 + $7,700 + $200,000 + $5,000 + $1,500 = **~$249,000** (plus any cash top-up beyond CPF for down payment and BSD).

**ABSD saved**: $800,000.
**Net benefit vs paying ABSD**: ~**$758,000**.

Plus retained rental income from condo: ~$66k/yr × hold period.

## Step 5: Risk flagging

> Agent calls out:
>
> 1. **Loan qualification**: Spouse A's max loan ~$2.96M vs $3M needed. Tight. Pre-confirm with bank.
> 2. **Timing**: Complete decoupling fully **before** OTP on landed (recommend 2-4 weeks gap to avoid IRAS reassessment risk).
> 3. **Separate counsel**: 2 lawyers, separate engagement letters.
> 4. **Valuation**: get independent professional valuation for the condo decoupling.
> 5. **Insurance**: Spouse B's HPS / MRTA reissue in sole name.
> 6. **CPF nomination**: update both spouses' CPF nominations post-decoupling.
> 7. **Will and estate**: refresh wills given ownership change.
> 8. **Property tax**: condo now in Spouse B's sole name; AV may need re-declaration.
> 9. **Rental management**: who handles condo rental (Spouse B as sole owner, but day-to-day decisions joint).
> 10. **Divorce contingency**: decoupled property is sole-owned. Discuss with family lawyer.

## Step 6: Sequencing timeline

| Week | Action |
|------|--------|
| W1 | Engage 2 lawyers, brief on decoupling |
| W1-W2 | Bank pre-qualification for Spouse B sole-name refinancing |
| W2-W3 | Valuation of condo; agree internal transfer price |
| W3-W4 | OTP and exercise on decoupling (Spouse A → Spouse B) |
| W5 | Pay BSD on transfer ($34,600) |
| W5-W8 | Refinancing in Spouse B sole name completes |
| W8-W10 | CPF refund to Spouse A OA processed |
| W10-W12 | Bank IPA for Spouse A landed purchase |
| W12-W14 | Search and viewings for landed |
| W14-W16 | OTP on landed (Spouse A as buyer) |
| W16-W18 | Pay BSD on landed ($179,600); ABSD $0 |
| W18-W30 | Landed completion (typically 8-12 weeks for resale) |

Total: **~7 months** to land in the new property with condo retained and ABSD avoided.

## Step 7: Verify and document

- [ ] IRAS-defensible documentation: separate lawyers, market-value transfer, time gap
- [ ] Bank loan confirmations (refinancing and new purchase)
- [ ] CPF refund completion notice
- [ ] Wills updated, CPF nominations refreshed
- [ ] Insurance restructured
- [ ] Landed due diligence checklist (plot ratio, soil, conservation, setbacks, drainage)

## Step 8: Escalation

- **Conveyancing lawyers** (×2): separate firms for decoupling
- **Family lawyer**: for matrimonial / estate implications
- **Tax adviser**: confirm IRAS-defensibility of decoupling structure
- **Bank mortgage specialist**: ensure sole-name refinancing pre-approved
- **Architect / contractor** if planning landed rebuild
- **Independent valuer** for condo decoupling transfer

End: "Illustrative scenario; final ABSD position depends on IRAS assessment of substance and timing. Engage tax counsel for sign-off before executing."
