from poker.constants import Rank

DESCRIPTIONS = {
    Rank.ROYAL_FLUSH: "royal flush: {suit}",
    Rank.STRAIGHT_FLUSH: "straight flush: {high}-high {suit}",
    Rank.FOUR_OF_A_KIND: "four of a kind: {value}",
    Rank.FULL_HOUSE: "full house: {trips} over {pair}",
    Rank.FLUSH: "flush: {suit}",
    Rank.STRAIGHT: "straight: {high}-high",
    Rank.THREE_OF_A_KIND: "three of a kind: {value}",
    Rank.TWO_PAIR: "two pair: {high} and {low}",
    Rank.PAIR: "pair: {value}",
    Rank.HIGH_CARD: "high card: {value}",
}
