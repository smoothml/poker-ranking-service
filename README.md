# Single Poker Hand Ranking Service
## Project Scope
This service comprises an API to compute the rank of an individual poker hand. The scope of this project is to:

- Write an algorithm that takes a hand of cards and identifies the ranking of the given hand.
- Expose an API to serve this algorithm via an endpoint `/rank`, that accepts a valid poker hand and returns its ranking.
- Rank information should be formatted as `<rank_name>: <description>`, see description format for each different rank below.

## Poker Rules

A poker hand consists of 5 cards dealt from a deck. A deck is composed of 52 cards ordered as `2 through 10`, `J` (*Jack*), `Q` (*Queen*), `K` (*King*), and `A` (*Ace*); and split across 4 suits: *♠ Spades* (black), *♦ Diamonds* (red), *♣ Clubs* (black), and *♥ Hearts* (red).

Poker hands are ranked by the following partial order from highest to lowest:

**1. Royal Flush**  ~ `[ A♥ K♥ Q♥ J♥ 10♥ ]`

The best hand possible, a royal flush consists of A, K, Q, J and 10, all of the same suit.

Description format: `<suit>`

**2. Straight Flush** ~ `[ 6♥ 7♥ 8♥ 9♥ 10♥ ]`

Also very rare, a straight flush consists of any straight that is all the same suit. Note Ace can act as value `1` to form a straight with values `2 3 4 5`.

Description format: `<highest_value>-high <suit>`

**3. Four of a Kind** ~ `[ A♥ A♣ A♦ A♠ K♥ ]`

Four of a kind, or 'quads', consists of four cards of equal value along with another card known as a side card.

Description format: `<quads value>`

**4. Full House** ~ `[ A♥ A♣ A♦ K♠ K♥ ]`

A full house consists of three cards of one value and two cards of another.

Description format: `<trips_value> over <pair_value>`

**5. FLush** ~ `[ K♣ 10♣ 8♣ 7♣ 5♣ ]`

A flush is a hand which has all cards of the same suit.

Description format: `<suit>`

**6. Straight** ~ `[ 10♥ 9♣ 8♦ 7♠ 6♥ ]`

A straight has five cards of consecutive value that are not all the same suit. Note Ace can act as value `1` to form a straight with values `2 3 4 5`.

Description format: `<highest_value>-high`

**7. Three of a Kind** ~ `[ A♥ A♣ A♦ K♠ Q♥ ]`

Also known as 'trips', three of a kind is 3 cards of the same value and 2 side cards of different values.

Description format: `<trips value>`

**8. Two Pair** ~ `[ A♥ A♣ K♦ K♠ 7♥ ]`

Two pair cosists of two cards of the same value, and three extra cards.

Description format: `<high_pair_value> and <low_pair_value>`

**9. Pair** ~ `[ A♥ A♣ K♦ J♠ 7♥ ]`

One pair consists of two cards of the same value, and three extra cards.

Description format: `<pair_value>`

**10. High Card** ~ `[ A♥ K♣ Q♦ 9♠ 7♥ ]`

Five cards that do not interact with each other to make any of the above hands.

Description format: `<value>`

## Examples

```
Query: "2H 3D 5S 9C KD"
Result: "high card: King"

~

Query: "2H 4D 4S 2C 4H"
Result: "full house: 4 over 2"

~

Query: "6H 7H 8H 9H 10H"
Result: "straight flush: 10-high diamonds"
```

## Requirements
- Python 3.11
- [Poetry](https://python-poetry.org/)
- [GNU Make](https://www.gnu.org/software/make/)

## Usage
- Install with `make install`.
- Run linting and tests with `make quality test coverage clean`.
- Build the API container with `make build`, then run API with `docker compose up -d`.
- Check API health with `curl localhost:8000`
- Query API for rank with e.g.
  ```shell
  curl -X POST -d '2H 3D 5S 10C KD' localhost:8000/rank
  ```
