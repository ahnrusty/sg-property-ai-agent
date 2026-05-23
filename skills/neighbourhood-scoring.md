# Neighbourhood Scoring

A structured way to compare locations without relying on vibes.

## Scoring dimensions (1 to 10 each)

| Dimension | What to measure |
|-----------|------------------|
| Commute | Door-to-door time to your primary workplace by your usual mode |
| MRT access | Walking distance, number of lines, future line additions |
| Schools | Distance to your priority schools, school tier, balloting risk |
| Amenities | Supermarket, hawker centre, clinics, parks, gym within 5 to 10 min walk |
| Healthcare | Distance to GP, polyclinic, hospital |
| Lifestyle | F&B variety, malls, libraries, cultural venues |
| Greenery | Parks, park connectors, beaches |
| Future plans | URA Master Plan upside (good) or disruption (bad) |
| Noise | Expressway, airport flight path, MRT line, construction, schools, places of worship |
| Safety | Crime stats by neighbourhood (low overall in SG; relative) |
| Community fit | Demographics, languages, vibe (subjective but worth thinking about) |
| Resale liquidity | How frequently do nearby comparable units sell |

## Where to find data

| Question | Source |
|----------|--------|
| Commute time | Google Maps in your usual departure hour |
| MRT walking distance | OneMap measured route, not as-the-crow-flies |
| Schools and balloting | MOE School Finder, past 5 years balloting data |
| Amenities | Google Maps, foursquare, walk it personally |
| URA Master Plan | URA Space (https://www.ura.gov.sg/maps) |
| Noise / flight path | Google Maps Street View at different times, ICA flight path maps |
| Crime | SPF annual report; SPC report at the planning area level |
| Demographics | Singstat |
| Transacted prices | URA Realis (private), HDB Resale Statistics (HDB) |
| Listings activity | PropertyGuru / 99.co listing counts, days on market |

## OCR / RCR / CCR designations

URA divides the island into three regions for tracking:

- **CCR (Core Central Region)**: Districts 9, 10, 11, downtown (D1-D4 partly), Sentosa
- **RCR (Rest of Central Region)**: outside CCR but within central area (parts of D3, D5, D7-D8, D12-D15)
- **OCR (Outside Central Region)**: everywhere else

Generally: CCR is premium (and most foreign-investor-sensitive), RCR is balanced (good owner-occupier rental and resale), OCR is suburban (largest market, primary HDB upgrader destination).

## Walking distance reality check

Property listings love "5-minute walk to MRT". Verify:

- Use OneMap walking route, not aerial distance
- Walk it yourself at 80m/min (slow ~6.4 km/h)
- 5 mins = ~400 m; 10 mins = ~800 m
- Account for: stairs, lift waiting, road crossings, weather (covered or not)

## School balloting (Phase 2C is the public one)

For Primary 1 (P1) registration:

- **Phase 1**: Older siblings already in the school
- **Phase 2A**: Children of alumni or staff
- **Phase 2B**: Active parents in school or community
- **Phase 2C**: General public, **distance-based**

For Phase 2C, "1 km" and "1 to 2 km" categories matter for popular schools. Confirm:

- Address falls within 1 km of school
- School has not changed its catchment in past 2 years
- Historical balloting demand for that school
- You will stay at the address for the period MOE requires (typically until child completes P1)

## Future plans matrix

URA Master Plan affects every area. Walk through the relevant items:

| Item | Good for value | Bad for value |
|------|----------------|----------------|
| New MRT station | Yes (post-construction) | During construction (noise, traffic) |
| Mixed-use development nearby | Yes (amenities) | Maybe (density, traffic) |
| New school | Yes (catchment expansion) | Maybe (traffic at school hours) |
| Industrial / utility nearby | Usually negative | Rarely positive |
| Park development | Yes | Rarely negative |
| Expressway widening | Mixed (better access) | Negative (noise) |
| New private launches (supply) | Negative short-term (price pressure) | Maybe long-term (area gentrification) |
| HDB BTO supply increase | Negative short-term for resale | Maybe long-term (population growth) |

Always pull the most recent URA Master Plan (refreshed every 5 years; interim amendments published).

## Output template

```
### Area: <name>

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Commute to <workplace> | | |
| MRT access | | |
| Schools | | |
| Amenities | | |
| Healthcare | | |
| Lifestyle | | |
| Greenery | | |
| Future plans | | |
| Noise | | |
| Resale liquidity | | |
| **Overall fit** | / 100 | |

Top 3 reasons to choose:
1. 
2. 
3. 

Top 3 cautions:
1. 
2. 
3. 
```
