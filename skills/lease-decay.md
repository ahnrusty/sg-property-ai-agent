# Lease Decay

Singapore leasehold property (99-year, and HDB which is 99-year) loses value over time as the lease runs down. Most private leasehold and all HDB are subject to this.

## Bala's Curve

Bala's Table (used by SLA for premium computation when extending leases) is the de facto reference. It maps remaining lease to a residual land value as a percentage of freehold.

| Remaining lease (years) | Approx. % of freehold value |
|-------------------------|-----------------------------|
| 99 | 96 |
| 90 | 94 |
| 80 | 92 |
| 70 | 90 |
| 60 | 86 |
| 50 | 81 |
| 40 | 73 |
| 30 | 60 |
| 20 | 41 |
| 10 | 18 |

The curve is convex: value drops slowly in the first 30 to 40 years, then accelerates downward.

## Practical implications

### Bank loan tenure

Bank loan tenure is constrained by remaining lease minus a buffer. Typical formula:

> Max bank loan tenure = min(30 years, remaining lease − 20, 75 − borrower age)

For a 50-year remaining lease, max tenure ≈ 30 years (if borrower age allows).
For a 35-year remaining lease, max tenure ≈ 15 years. Monthly repayment shoots up.

### CPF OA usage

CPF OA usage is pro-rated when remaining lease does not cover the youngest buyer to age 95.

- If remaining lease covers youngest to < age 65, **no CPF** can be used.
- If between 65 and 95: pro-rated.

For an older buyer of an older flat, this can mean the entire down payment must be in cash.

### Resale buyer pool

As lease shortens, the pool of buyers who can afford and finance the unit shrinks:

- < 60 years: many CPF and loan constraints
- < 40 years: predominantly cash buyers, en-bloc plays, or rental investors
- < 30 years: niche; often HDB resale flats facing SERS / VERS uncertainty

This compresses prices faster than the raw curve suggests.

### Rental yield illusion

Older leasehold can show higher rental yields because price has dropped faster than rent. Calculate **after-CPF, after-tax IRR over your intended hold period**, not just current yield. Lease decay is a constant negative drag.

## When older leasehold makes sense

- You are paying mostly cash, have no CPF dependency, and intend to live there or hold for ≤ 10 years
- You expect en-bloc within the hold period (high uncertainty; do not pay for the en-bloc premium upfront)
- You are buying for the location or specific unit that is unavailable elsewhere
- You have no children to whom you intend to bequeath the property
- The price clearly reflects the lease (compare $/psf to comparable freehold and 99-year newer projects)

## When older leasehold does NOT make sense

- You plan to use significant CPF
- You plan to hold 20+ years and pass to heirs
- You are buying purely for capital appreciation
- The market is paying a premium for hoped-for en-bloc
- Bank loan tenure forces uncomfortable monthly payments

## HDB lease decay

HDB flats are 99-year leasehold. Unique considerations:

- SERS (Selective En-bloc Redevelopment Scheme): government can compulsorily acquire and offer replacement; only a small percentage of flats are ever selected
- VERS (Voluntary Early Redevelopment Scheme): announced policy for flats aged 70+; details still evolving; do not assume your flat will be selected
- At lease end (year 99), flat reverts to HDB and tenant must vacate without compensation. Plan for sale or replacement well before this point.

For HDB resale, broadly avoid flats with < 60 years remaining unless your specific situation (older buyer, cash-rich, downsize) makes the maths work.

## Lease extension

For private 99-year leasehold land, extension is possible but discretionary by SLA and at a premium (typically computed using Bala's Curve). Not all sites are eligible; many are not.

For HDB, lease extension is generally not available; SERS / VERS are the mechanisms.

## How to discuss with seller / agent

- "What is the remaining lease at expected completion date?"
- "How does your asking price compare to recent transacted $/psf in this project for similar remaining-lease units?"
- "Has the MCST or any owner started discussions on en-bloc or lease top-up?"
- "What CPF usage cap applies for a buyer aged X with this remaining lease?"

If the agent does not know, get a second opinion before paying option fee.
