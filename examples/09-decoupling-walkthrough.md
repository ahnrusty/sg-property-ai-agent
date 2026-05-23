# Example 9: Decoupling Walkthrough (Save $400k+ ABSD)

## Scenario

**Profile**: Married couple, both SC, mid-40s. Joint owners of $1.8M freehold condo in Tiong Bahru (bought 2019, outstanding loan $700k, CPF used + accrued combined $320k). Combined gross income $28,000/month. Want to buy a $2M investment condo in Bishan for rental income.

**Goal**: Buy 2nd property without paying $400k ABSD. Retain Tiong Bahru as own-stay.

## Step 1: Triage

> Agent: This is exactly the scenario decoupling was designed for.
>
> Without decoupling: 20% ABSD on $2M = **$400,000** out of pocket on purchase. Refunded only if you sell Tiong Bahru within 6 months — but you want to keep it.
>
> Decoupling cost: ~$30-35k.
> Net benefit: **~$365k+**.
>
> Let me walk you through.

## Step 2: Feasibility checks

### Loan qualification in sole name

> Agent: Decoupling means Spouse A transfers their 50% share to Spouse B. Spouse B becomes sole owner of Tiong Bahru, with the existing $700k mortgage in their sole name.
>
> Need to verify Spouse B can qualify for the mortgage alone.
>
> What's Spouse B's individual gross monthly income?

User: Spouse B earns $16,000/month. No other debt.

Agent calls `estimate_max_loan(16000, 0, 0.04, 25, 0.55)`:
> Max loan: ~$1,510,000. Far exceeds $700k existing. ✓ Loan qualifies in sole name.

### Spouse A loan qualification for new condo

Agent calls `estimate_max_loan(12000, 0, 0.04, 30, 0.55)`:
> Max loan: ~$1,420,000.
>
> For $2M new condo at 75% LTV (Spouse A's first property): loan = $1.5M. **Tight**.
>
> Options:
> 1. Increase down payment (use more CPF + cash), reduce loan to $1.4M
> 2. Spouse B co-signs as guarantor (but doesn't go on title) — verify with bank if this affects ABSD profile
> 3. Reduce target price to $1.85M to lower loan requirement
>
> Pre-confirm with bank before proceeding.

## Step 3: Decoupling cost calculation

Transferring 50% of $1.8M condo = $900k consideration.

Agent calls `calculate_bsd(900_000)`:
> BSD = 1%×180 + 2%×180 + 3%×540 = 1,800 + 3,600 + 16,200 = **$21,600**

| Cost component | Amount |
|----------------|--------|
| BSD on $900k transfer | $21,600 |
| Lawyer A (transferring spouse) | $2,500 |
| Lawyer B (remaining spouse) | $2,500 |
| Mortgage refinancing in sole name | $1,500 |
| Professional valuation | $700 |
| **Total decoupling cash cost** | **~$28,800** |

CPF refund to Spouse A:
> Assume Spouse A's CPF share = half of $320k = $160k. Returns to Spouse A's OA. Useful for new condo down payment.

## Step 4: New condo math (Spouse A as first-time buyer)

Agent calls:
- `calculate_bsd(2_000_000)`: 1%×180 + 2%×180 + 3%×640 + 4%×500 + 5%×500 = 1,800 + 3,600 + 19,200 + 20,000 + 25,000 = **$69,600**
- `calculate_absd(2_000_000, "SC", 1)`: **$0** (Spouse A first property)

Cash + CPF at $2M, 75% LTV:
| Item | Amount |
|------|--------|
| Loan: 75% LTV | $1,500,000 |
| Down payment | $500,000 |
| 5% cash component (min) | $100,000 |
| Balance down payment (CPF + cash) | $400,000 |
| BSD | $69,600 |
| Legal | $3,500 |
| Stamp duty admin + valuation | $1,000 |

Total cash needed for new condo: $100,000 + balance cash if CPF insufficient + $3,500 + $1,000 + BSD if not from CPF.

With Spouse A's CPF $160k available post-decoupling: covers chunk of down payment. Plus pre-existing CPF balance.

## Step 5: Combined cash + CPF plan

Decoupling phase:
- BSD on transfer: $21,600 (cash)
- Legal + admin: $7,200
- **Subtotal**: $28,800

New condo phase (assuming $50k Spouse A CPF available beyond decoupling refund):
- Cash component (5% min): $100,000
- Down payment top-up (cash): ~$190,000 (if CPF total $160k from refund + $50k other = $210k toward $500k down)
- BSD: $69,600 (CPF or cash)
- Legal: $3,500
- Admin: $1,000

**Total cash outlay (decoupling + condo)**: ~$28,800 + $100k + ~$190k + $5k = **~$324,000**

**ABSD avoided**: $400,000.
**Net benefit**: ~**$76,000** (after accounting for $324k vs $400k+ ABSD alternative).

Wait — that doesn't capture everything. Let me redo the comparison.

### Apples-to-apples comparison

**Path 1: Pay ABSD, no decoupling** ($2M new condo as second property):
- Pay 20% ABSD: $400,000 (cash, refundable only if sell Tiong Bahru — but we want to keep it)
- LTV drops to 45% on new condo: down payment = $1,100,000
- 5% min cash: $100,000
- Balance down payment: $1,000,000 (CPF + cash)
- BSD: $69,600
- Legal: $3,500
- **Cash needed**: $400,000 ABSD + $100k cash + cash for top-up beyond CPF + $3,500 legal
- Plus: lose option to rent Tiong Bahru flexibly (joint ownership friction for rental decisions)

**Path 2: Decouple, then buy as first property**:
- Decoupling: $28,800
- New condo at 75% LTV: down payment $500,000
- 5% min cash: $100,000
- Balance: $400,000 (CPF + cash)
- BSD: $69,600
- Legal: $3,500
- **Cash needed**: $28,800 + $100k + cash top-up + $5k legal/admin

The Path 2 saving: avoid $400k ABSD AND get 75% LTV (vs 45%) on the new condo, which means **~$600k less needed in down payment** for the new condo too.

**Cleaner net benefit**: $400k ABSD saved + $600k freed from down payment for productive uses + decoupling cost $28.8k = **~$971k in capital efficiency**.

## Step 6: Risk and timing

| Risk | Mitigation |
|------|------------|
| Loan rejection in sole name | Pre-qualify with bank before decoupling |
| IRAS challenge | Separate lawyers, time gap, market-value transfer, professional valuation |
| CPF refund delay | Buffer cash for 4-6 week processing |
| Insurance restructure | Spouse B obtains new HPS/MRTA in sole name |
| Will / nomination updates | Engage estate planner |
| Tiong Bahru AGM changes | Notify MCST of new sole owner |
| Property tax change | Re-declare AV / owner status |
| Rental income going forward | Sole name on tenancy agreements |

## Step 7: Execution timeline

| Week | Action |
|------|--------|
| W1 | Engage 2 lawyers, brief decoupling structure |
| W1-W2 | Bank pre-qualification: refinancing in Spouse B sole name |
| W1-W2 | Bank pre-qualification: Spouse A new loan for $1.5M |
| W2 | Independent valuation of Tiong Bahru |
| W3 | OTP signed for decoupling transfer at market value |
| W3 | Exercise OTP; both lawyers process |
| W4 | BSD on transfer paid ($21,600) within 14 days |
| W5-W7 | Refinancing in Spouse B sole name |
| W7-W8 | CPF refund to Spouse A processed; lands in OA |
| W8 | Decoupling complete. Tiong Bahru solely owned by Spouse B. Spouse A property-free for ABSD. |
| W9-W12 | Search and viewings for Bishan condo |
| W12 | OTP signed by Spouse A on $2M condo |
| W14 | BSD paid ($69,600); ABSD $0 |
| W14-W22 | Condo completion (8-12 weeks for resale) |
| W22 | Move-in to new condo (or rent it out from Day 1 if pure investment) |

Total: ~5-6 months end-to-end.

## Step 8: Post-decoupling lifestyle

- **Tiong Bahru**: Spouse B sole owner. If you continue to live there together, that's fine; ownership is legal, occupancy is practical.
- **Bishan condo**: Spouse A sole owner. If rented out, rental income to Spouse A's name; tax filed accordingly.
- **Joint family finances**: continue as before via joint accounts; the legal ownership change doesn't affect daily life.
- **Resale of either property later**: each is independently saleable by its sole owner.

## Step 9: When decoupling can backfire

- **Divorce**: decoupled property is sole-owned. Matrimonial division becomes more complex. Discuss with family lawyer before decoupling.
- **One spouse passes away**: sole-owned property follows the will. Update wills to reflect.
- **Future second purchase**: each spouse has used their "first-property" status. Next second property by either spouse triggers ABSD again.

## Step 10: Escalation

- **Conveyancing lawyers** ×2 (separate firms strongly recommended)
- **Family lawyer**: matrimonial implications
- **Estate planning lawyer**: wills, CPF nominations
- **Tax adviser**: IRAS-defensibility, especially if multiple properties or trust structures
- **Bank mortgage specialist**: pre-qualify both refinancing and new loan
- **Insurance broker**: restructure HPS/MRTA

End: "Decoupling is a powerful but structural change. Done right, it saves $400k+ and unlocks portfolio flexibility. Done wrong, it triggers IRAS scrutiny or loan failure. Plan with all the right professionals before executing."
