# Flip 7 Game Theory Optimal (GTO) Strategy

## Game Overview

Flip 7 is a press-your-luck card game where players draw cards trying to maximize their score without busting. The key mechanic is:
- **Bust Condition**: Drawing a duplicate number card = 0 points for the round
- **Win Condition**: Collect 7 unique number cards = instant round win + 15 point bonus
- **Goal**: First to 200 points wins

## Deck Composition (94 cards)

### Number Cards (81 total)
The deck has a pyramid distribution where higher numbers are more common:
- 0: 1 card (0 points)
- 1: 1 card
- 2: 2 cards
- 3: 3 cards
- 4: 4 cards
- 5: 5 cards
- 6: 6 cards
- 7: 7 cards
- 8: 8 cards
- 9: 9 cards
- 10: 10 cards
- 11: 11 cards
- 12: 12 cards

**Total number cards by value: 0+1+2+3+4+5+6+7+8+9+10+11+12 = 78**
(Note: The rules state 81 number cards total, implying there may be 13 cards of value 13, or the distribution continues)

### Modifier Cards (13 total estimated)
- +2, +3, +4, +5, +6, +7, +8, +9, +10
- x2 (doubles current score)

### Action Cards
- Freeze! (forces a player to stay)
- Flip Three! (forces 3 draws)
- Second Chance (prevents one bust)

## Core GTO Strategy Principles

### 1. Expected Value (EV) Calculation

The fundamental decision in Flip 7 is: **HIT or STAY?**

**Expected Value of Hitting = Sum of:**
- P(draw safe number) × (current_score + new_card_value + EV_of_continuing)
- P(draw modifier) × (modified_score + EV_of_continuing)
- P(draw action card) × (EV_of_action)
- P(draw duplicate) × (-current_score)

**Expected Value of Staying = current_score**

**Optimal Decision: HIT if EV(Hit) > EV(Stay), otherwise STAY**

### 2. Key Probabilistic Factors

#### Bust Probability
Given you have N unique numbers in your hand:
- Cards remaining in deck: Unknown total - Cards seen
- Duplicate cards of your numbers still in deck: Varies by number (higher numbers have more copies)
- P(bust) = (Sum of remaining duplicates) / (Total cards remaining)

#### Value Gain Probability
- P(draw safe number K) = (remaining cards of K) / (total cards remaining)
- Expected value gain = Sum over all safe numbers K of: P(K) × K

### 3. The "Risk Threshold" Strategy

Based on EV calculations, you should generally:

**STAY when:**
1. Your current score is high relative to risk
2. You have many number cards (bust risk is high)
3. The deck has been depleted of high-value safe cards
4. You're in the lead and securing points is strategic

**HIT when:**
1. Your score is low
2. You have few number cards (1-3 cards)
3. Many high-value safe cards remain in the deck
4. You're behind and need to take risks

### 4. Card Count Considerations

The decision heavily depends on how many unique numbers you have:

**With 1-2 cards:** Almost always HIT
- Low bust probability (~2-5%)
- High upside potential
- Low current score to protect

**With 3-4 cards:** HIT if EV is positive
- Moderate bust probability (~10-20%)
- Still significant upside
- Calculate precise probabilities

**With 5 cards:** Careful calculation needed
- Higher bust probability (~25-35%)
- Only 2 cards away from the 7-card bonus
- Consider going for the bonus if high-value cards remain

**With 6 cards:** High-risk decision
- Very high bust probability (~40-50%+)
- One card away from 7-card bonus (+15 points)
- Usually worth the risk if you have Second Chance
- Without Second Chance, calculate if bonus exceeds current score expectation

### 5. Advanced Tactical Considerations

#### Second Chance Card
- Changes the entire calculation - you can take one extra risk
- With Second Chance: Be more aggressive, especially with 5-6 cards
- Try to push for the 7-card bonus
- The card essentially gives you a "free" draw

#### Information from Other Players
- Track what numbers other players have shown
- Reduces uncertainty about deck composition
- Adjusts probabilities in your favor or against you

#### Position in Round
- Early in round: Play slightly more conservatively (others may bust)
- Late in round: If you're behind the current leader, take more risks
- If you're leading: Consider staying to lock in a good score

#### Score Differential
- Far behind in overall game: Take more risks to catch up
- Leading by a lot: Play more conservatively
- Close game: Optimize EV strictly

### 6. Specific Threshold Guidelines

These are approximate thresholds (vary based on deck state):

| Cards in Hand | Minimum Score to Consider Staying | Aggressive Stay | Conservative Stay |
|--------------|-----------------------------------|-----------------|-------------------|
| 1 | Never | Never | 12+ |
| 2 | 15+ | 20+ | 25+ |
| 3 | 25+ | 30+ | 35+ |
| 4 | 35+ | 40+ | 45+ |
| 5 | 40+ | 45+ | 50+ |
| 6 | 45+ (or go for 7) | 50+ (or go for 7) | Consider the 7 |

**Note:** These are rough guidelines. The optimal threshold varies significantly based on:
- Which specific numbers you have (high vs low)
- How many duplicates remain in the deck
- Modifier cards you've collected

## Simplified Decision Tree

```
START OF TURN
│
├─ Have 6 cards?
│  ├─ Yes: Have Second Chance?
│  │  ├─ Yes: GO FOR 7 (almost always worth it)
│  │  └─ No: Calculate P(bust) vs bonus value
│  └─ No: Continue...
│
├─ Have 5 cards?
│  ├─ Score < 40: Calculate EV (often HIT if many safe cards remain)
│  └─ Score >= 40: Consider staying unless going for 7-card bonus
│
├─ Have 3-4 cards?
│  ├─ Score < 30: HIT (unless bust probability > 30%)
│  └─ Score >= 30: Calculate precise EV
│
└─ Have 1-2 cards?
   └─ Almost always HIT (unless extreme bust risk or score > 25)
```

## Mathematical Framework

### Complete EV Formula

Let:
- `S` = current score (sum of number cards)
- `M` = modifier bonus (from +X cards)
- `D` = multiplier (2 if you have x2, else 1)
- `N` = set of numbers in your hand
- `R` = remaining cards in deck
- `C_k` = count of card value k remaining in deck

Current Total = (S × D) + M

For each possible next card k:
1. If k is a duplicate (k ∈ N): Result = 0
2. If k is a number (k ∉ N): Result = (S+k) × D + M + EV_continue
3. If k is a modifier +X: Result = (S × D) + M + X + EV_continue
4. If k is a x2: Result = (S × 2D) + M + EV_continue
5. If k is an action: Handle separately

```
EV(Hit) = Σ [P(k) × Value(k)] for all k in remaining deck

where:
P(k) = C_k / |R|
Value(k) = outcome value as defined above
```

**HIT if EV(Hit) > Current Total, otherwise STAY**

## Practical Implementation

The Python program provided implements this strategy by:
1. Tracking all cards seen (your hand + discards + other players' visible cards)
2. Calculating exact remaining card counts
3. Computing bust probability for each specific number
4. Calculating expected value of hitting
5. Recommending HIT or STAY based on EV comparison

## Summary: The Core Insight

**Flip 7 GTO strategy is fundamentally about risk-adjusted expected value.**

The optimal player:
1. Tracks the deck composition precisely
2. Calculates bust probability given current hand
3. Estimates value gain from safe cards
4. Compares EV(Hit) vs EV(Stay)
5. Makes the mathematically optimal decision

The key skill is balancing the **upside of gaining points** against the **downside of busting** based on:
- How many cards you have (more cards = higher bust risk)
- Which specific numbers you have (higher numbers = more duplicates exist)
- What cards remain in the deck
- Your position in the game

This creates a dynamic risk-reward calculation that changes every turn and every card drawn.
