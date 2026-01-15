# Flip 7 GTO Strategy Analyzer

A Python program that provides Game Theory Optimal (GTO) strategy recommendations for the card game **Flip 7**.

## What is Flip 7?

Flip 7 is a press-your-luck card game where players draw cards trying to collect the highest score without busting. Key rules:

- **Objective**: Be the first to reach 200 points across multiple rounds
- **Bust condition**: Drawing a duplicate number card means you score 0 for that round
- **7-card bonus**: Successfully collecting 7 unique number cards = instant round win + 15 point bonus
- **Decision**: On each turn, choose to HIT (draw another card) or STAY (keep your current score)

## Features

This analyzer helps you make optimal decisions by:

✅ **Tracking the deck** - Monitors all cards drawn and calculates remaining probabilities
✅ **Calculating bust risk** - Shows exact probability of busting on the next draw
✅ **Computing expected value** - Determines if hitting has positive EV
✅ **GTO recommendations** - Tells you whether to HIT or STAY based on mathematics
✅ **Real-time analysis** - Updates strategy as the game state changes

## Installation

### Requirements
- Python 3.6 or higher (no external dependencies needed!)

### Setup
```bash
# Clone or download the repository
cd Flip7GTO

# Run the program
python3 flip7_gto.py
```

## Usage

### Starting the Program

```bash
python3 flip7_gto.py
```

### Commands

The program accepts the following inputs:

#### Adding Cards to Your Hand
- `0` through `12` - Add a number card (e.g., type `7` to add a 7 card)
- `+X` - Add a modifier card (e.g., `+5` adds a +5 modifier)
- `x2` - Add a x2 multiplier card
- `sc` or `second chance` - Add a Second Chance card

#### Tracking Opponent Cards (Improves Accuracy!)
- `o NUMBER` - Track opponent's number card (e.g., `o 9` tracks their 9)
- `o +X` - Track opponent's modifier (e.g., `o +5`)
- `o x2` - Track opponent's x2 multiplier
- `o sc` - Track opponent's Second Chance card

**Why track opponent cards?** This removes them from the deck calculations, giving you more accurate bust probabilities without affecting your hand or score!

#### Getting Recommendations
- `recommend` or `r` - Get the GTO recommendation (HIT or STAY)
- `status` or `s` - View current game state and probabilities

#### Managing the Game
- `shuffle` - Shuffle the deck back to full (96 cards) - use when deck runs low
- `new` or `round` - Start a new round (clears hands, keeps deck state)
- `help` or `h` - Show help message
- `quit` or `q` - Exit the program

**Important:**
- Use `shuffle` when the deck runs out of cards (resets deck to 96)
- Use `new` when a round ends (clears your hand and opponent tracking, but deck continues from current state)

### Example Session

```
Enter command or card: 9
✓ Added number card: 9

Enter command or card: o 7
✓ Tracked opponent card: 7

Enter command or card: o 8
✓ Tracked opponent card: 8

Enter command or card: 10
✓ Added number card: 10

Enter command or card: recommend

============================================================
GTO RECOMMENDATION
============================================================
Action: 🎲 HIT (Draw another card)
Reason: HIT - Early game, low bust risk (4.3%)

Current Hand Analysis:
  - Number cards: [9, 10]
  - Cards in hand: 2/7
  - Current score: 19 points
  - Base score: 19
  - Has Second Chance: No
  - Has x2 Multiplier: No

Risk Analysis:
  - Bust probability: 4.3%
  - Safe cards probability: 57.0%

Cards remaining in deck: 92
============================================================

Enter command or card: 11
✓ Added number card: 11

Enter command or card: 12
✓ Added number card: 12

Enter command or card: r

============================================================
GTO RECOMMENDATION
============================================================
Action: ✋ STAY (Keep your current score)
Reason: STAY - Protect your score (EV: 26.0 vs Current: 42)

Current Hand Analysis:
  - Number cards: [9, 10, 11, 12]
  - Cards in hand: 4/7
  - Current score: 42 points
  ...
============================================================
```

## How It Works

### The GTO Strategy

The analyzer uses expected value (EV) calculations to determine optimal play:

```
EV(Hit) = Σ [P(card) × Value(outcome)]

Where:
- P(card) = Probability of drawing each specific card
- Value(outcome) = Expected points if that card is drawn

Optimal Decision: HIT if EV(Hit) > Current Score, otherwise STAY
```

### Key Factors

The recommendation considers:

1. **Bust Probability** - Likelihood of drawing a duplicate number
2. **Safe Card Distribution** - Which safe cards remain and their values
3. **Cards in Hand** - More cards = higher bust risk
4. **Current Score** - Higher scores are more valuable to protect
5. **Second Chance** - Allows one free bust (changes strategy dramatically)
6. **7-Card Bonus** - Special consideration when close to 7 cards

### Strategy Guidelines

The analyzer follows these principles:

**With 1-2 cards:** Almost always HIT
- Very low bust probability (~2-5%)
- Low score to protect
- High upside potential

**With 3-4 cards:** HIT if EV is positive
- Moderate bust risk (~10-25%)
- Calculate precise probabilities
- Consider score threshold (~35 points)

**With 5 cards:** Careful calculation
- Higher bust risk (~25-40%)
- Consider pushing for 7-card bonus
- Typically stay above 40-45 points

**With 6 cards:** Critical decision
- Very high bust risk (~40-50%+)
- One card from 7-card bonus (+15 points)
- Usually worth the risk WITH Second Chance
- Calculate bonus EV vs bust risk

## File Structure

```
Flip7GTO/
├── flip7_gto.py          # Main Python program (interactive analyzer)
├── gto_strategy.md       # Detailed GTO strategy guide
├── README.md             # This file
└── index.html            # Game rules reference
```

## Understanding the Output

### Recommendation Format

```
Action: 🎲 HIT or ✋ STAY
Reason: [Explanation of why this is optimal]

Current Hand Analysis:
  - Shows your cards and score

Risk Analysis:
  - Bust probability: % chance you bust on next card
  - Safe cards probability: % chance you draw a safe card
```

### Bust Probability

This is the most important metric:
- **< 10%**: Very safe to hit
- **10-20%**: Generally safe, consider score
- **20-30%**: Moderate risk, need good reason to hit
- **30-40%**: High risk, usually only hit if score is low
- **> 40%**: Very high risk, typically stay (unless going for 7-card bonus)

## Strategy Tips

1. **Track opponent cards** - Use `o NUMBER` to track visible opponent cards for better accuracy
2. **Track cards carefully** - The analyzer is only as good as your input
3. **Trust the math** - GTO strategy may feel counterintuitive but it's optimal
4. **Second Chance changes everything** - Be much more aggressive with it
5. **6-card decision** - The 7-card bonus is usually worth pursuing with Second Chance
6. **Low scores** - Don't stay on scores below 25-30 unless bust risk is extreme
7. **Position matters** - If others have busted, you can be more conservative

## Advanced Usage

### Understanding Shuffle vs New Round

The program distinguishes between two different game events:

**Shuffle (`shuffle` command):**
- Resets the deck to full 96 cards
- Keeps your current hand
- Keeps opponent card tracking
- Use this when: The deck runs out of cards and needs reshuffling

**New Round (`new` or `round` command):**
- Clears your hand
- Clears opponent card tracking
- **Keeps the deck state** (doesn't reshuffle)
- Use this when: The round ends and players start new hands

**Example scenario:**
```
# You're playing your turn
Enter command or card: 10
Enter command or card: 11
Enter command or card: 12

# Deck runs out, dealer shuffles
Enter command or card: shuffle
✓ Deck shuffled! (Your hand and opponent cards remain)

# You continue playing
Enter command or card: 9

# Round ends, you choose to stay with 4 cards
# Everyone starts new hands for the next round
Enter command or card: new
✓ New round started! (Hand and opponent tracking reset, deck continues)

# Deck still has same cards remaining from before
# Only your hand is cleared
```

### Tracking Other Players' Cards

The program now has **built-in opponent card tracking** that significantly improves accuracy in multi-player games:

**How it works:**
```
# Track opponent's visible cards
Enter command or card: o 7    # Opponent has a 7
✓ Tracked opponent card: 7

Enter command or card: o 12   # Opponent has a 12
✓ Tracked opponent card: 12

Enter command or card: o +5   # Opponent has a +5 modifier
✓ Tracked opponent card: +5
```

**Benefits:**
1. Removes opponent cards from deck calculations (more accurate probabilities)
2. Does NOT affect your hand or score (only tracks what's visible)
3. Shown in status display for reference
4. Significantly improves bust probability accuracy

**Best practices:**
- Track all visible number cards from active opponents
- Don't worry about tracking every modifier/action card (less impact)
- Use `new` when starting a new round (clears tracking)
- Use `shuffle` only when the deck actually gets reshuffled
- Focus on cards from players still in the round

### Optimal Thresholds by Card Count

| Cards | Conservative Stay | Aggressive Stay | Notes |
|-------|------------------|-----------------|-------|
| 1 | Never | 12+ | Almost always hit |
| 2 | 20+ | 15+ | Very low bust risk |
| 3 | 35+ | 25+ | Still favorable to hit |
| 4 | 45+ | 35+ | Moderate risk zone |
| 5 | 50+ | 40+ | High risk, consider 7-card push |
| 6 | Consider 7 | Consider 7 | Go for bonus with Second Chance |

*These are approximate guidelines - actual recommendations vary based on specific cards and deck state*

## Technical Details

### Deck Composition

The Flip 7 deck contains 94 cards:

**Number Cards (81 total):**
- Pyramid distribution: 1 card of 0, 1 of 1, 2 of 2, 3 of 3... up to 12 of 12
- Higher numbers are more common (more duplicates exist)

**Modifier Cards:**
- +2, +3, +4, +5, +6, +7, +8, +9, +10 (1 of each estimated)
- x2 multiplier (2 cards estimated)

**Action Cards:**
- Freeze! (2 cards)
- Flip Three! (2 cards)
- Second Chance (2 cards)

### Probability Calculations

The program tracks:
- Exact count of each card type remaining
- Total cards remaining in deck
- For each number in your hand, how many duplicates remain
- Bust probability = (sum of duplicates) / (total remaining)

### Expected Value Formula

Simplified EV calculation:
```
EV(Hit) = P(safe) × (score + avg_safe_value)
        + P(modifier) × (score + modifier_value)
        + P(action) × (score)
        - P(bust) × (score)
```

Where:
- P(safe) = probability of drawing a safe number card
- P(modifier) = probability of drawing a modifier
- P(action) = probability of drawing an action card
- P(bust) = probability of drawing a duplicate

## Limitations

1. **Action cards are simplified** - The program doesn't fully model Freeze! and Flip Three! effects on EV
2. **No multi-step lookahead** - Calculates immediate EV, not future turn potential
3. **Single player focus** - Doesn't consider game theory of competing players
4. **Modifier estimation** - Exact modifier card distribution is estimated
5. **Manual input required** - You must enter all cards (can't read from camera/game)

## Contributing

Feel free to enhance this analyzer! Possible improvements:
- Multi-turn lookahead with dynamic programming
- Multiplayer game theory considerations
- GUI interface
- Card recognition via camera
- Tournament mode with multiple rounds
- Statistical tracking of outcomes

## License

This is an educational tool for analyzing Flip 7 strategy. The game Flip 7 is designed by Eric Olsen and published by OP Games.

## Support

For issues, questions, or suggestions, please refer to the `gto_strategy.md` file for detailed strategy explanations.

---

**Good luck, and may your expected values always be positive!** 🎲
