# Hedge Counterexample

[Français](README.md) · [Español](README.es.md)

**Find the exact scenario where an apparently complementary hedge stops covering.**

Similar titles establish neither identical settlement rules nor execution of both legs. This laboratory checks declared time predicates and explicit fill quantities, then exports a replayable witness using integer-cent arithmetic.

## Try it

Python 3.11+; standard library, no key or platform connection.

```sh
git clone https://github.com/gbesse/hedge-counterexample
cd hedge-counterexample
python3 -m hedge_counterexample serve --lang en
```

Open `http://127.0.0.1:8773/?lang=en`. Two entirely **fictional** exercises:

- **Timezone gap**: buying yes before 22:00 UTC and no before 22:00 New York does not cover an event between those deadlines. With ten units per leg and declared costs/fees, worst settled net is **−924 fictional cents**.
- **Partial fills**: with identical rules, fully filling both legs yields a minimum of **+76**. Independent quantities of 0, 5 or 10 produce a worst case of **−462**, when only one leg fills.

Enable pending settlement to retain a **net interval**, not a realized loss: ten units on each leg give `[−924, 1076]`, unresolved committed cost 924. `settled_net_cents` stays `null`. No probability or recommendation follows from this.

![Witness](docs/preview-fr.png)

```sh
python3 -m hedge_counterexample demo > analysis.json
python3 -m hedge_counterexample analyze hedge_counterexample/examples/partial-fill-gap.json
python3 -m hedge_counterexample verify case.json witness.json
```

Browser export contains `source_case` and `worst`; save these objects separately for `verify`. `pip install .` also provides `hedge-counterexample`. FR/EN/ES UI and errors; user data stays unchanged.

## Exact computation scope

Contracts pay 100 cents per winning unit, with yes/no side, integer price, per-unit fee and a fixed fee when at least one unit fills. Example fees are **invented**: 1 cent per unit + 2 per filled leg; no fixed fee at zero fill. No platform fee formula is implemented.

The rule language supports `before`, `at_or_before`, `not`, `and`, `or` over timestamped, optionally absent events. Each event has an explicit integer UTC-second domain. Deadlines use explicit UTC/offset or local time + IANA timezone. Nonexistent local times fail; ambiguous autumn times require `fold: 0` or `fold: 1`.

For each event, search examines domain endpoints and seconds around each deadline, then groups identical atomic truth vectors. These cells suffice **for this restricted language**. Crossing cells with all declared fill quantities finds the worst net or lower bound. Exhaustiveness excludes omitted rules or quantities. Limits: three events, six contracts, twenty atomic predicates, five quantities per contract, 100,000 trials. Witness verification replays the same rule and arithmetic engine; it is not an independent exhaustiveness proof.

## Existing work and limits

[Polymarket documents full and partial execution](https://docs.polymarket.com/trading/place-orders) and [settlement under predefined rules](https://help.polymarket.com/en/articles/13364518-how-are-prediction-markets-resolved). They motivate the problem; no market contract text is redistributed. Our [jev-contract-graph](https://github.com/gbesse/jev-contract-graph) already explores contract relations. This project focuses on **normalized temporal witnesses + filled quantity + fees + unknown settlement**, without market collection.

Data consists of invented contracts, not real arbitrage. No automatic legal-contract interpretation, trading API, live orderbook, currency risk, latency, capital requirement, liquidity, market impact or investment recommendation. Values are not forecasts. No SOTA superiority, real profitability or human adoption claimed.

## Verify

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Thirteen tests cover inclusive boundaries, DST, ambiguous/nonexistent times, fees, zero fills, unresolved intervals and forged witnesses. Critical cells are checked against second-by-second enumeration on twenty small random cases. FR/EN/ES browser, both exercises, full/partial fills, pending settlement, export and mobile. Python 3.11/3.12 CI and installed wheel outside source. MIT; public alpha.
