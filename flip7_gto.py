#!/usr/bin/env python3
"""
Flip 7 GTO Strategy Analyzer

This program tracks the game state of Flip 7 and provides Game Theory Optimal
recommendations for whether to HIT or STAY based on expected value calculations.

Usage:
    python flip7_gto.py

Author: GTO Strategy Analyzer
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
import sys


class Flip7Deck:
    """Represents the Flip 7 deck composition and tracks remaining cards."""

    def __init__(self):
        """Initialize a full Flip 7 deck."""
        # Number cards: pyramid distribution (0-12)
        self.initial_deck = {
            0: 1, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
            7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12
        }

        # Estimate based on 94 total cards - 78 number cards = 16 special cards
        self.initial_modifiers = {
            '+2': 1, '+3': 1, '+4': 1, '+5': 1, '+6': 1,
            '+7': 1, '+8': 1, '+9': 1, '+10': 1, 'x2': 2
        }

        self.initial_actions = {
            'Freeze': 2, 'Flip Three': 2, 'Second Chance': 2
        }

        self.reset()

    def reset(self):
        """Reset the deck to initial state."""
        self.number_cards = self.initial_deck.copy()
        self.modifier_cards = self.initial_modifiers.copy()
        self.action_cards = self.initial_actions.copy()

    def total_remaining_cards(self) -> int:
        """Calculate total cards remaining in deck."""
        return (sum(self.number_cards.values()) +
                sum(self.modifier_cards.values()) +
                sum(self.action_cards.values()))

    def remove_card(self, card_type: str, value):
        """Remove a card from the remaining deck."""
        if card_type == 'number':
            if value in self.number_cards and self.number_cards[value] > 0:
                self.number_cards[value] -= 1
            else:
                print(f"Warning: Number card {value} not available in deck")
        elif card_type == 'modifier':
            if value in self.modifier_cards and self.modifier_cards[value] > 0:
                self.modifier_cards[value] -= 1
            else:
                print(f"Warning: Modifier card {value} not available in deck")
        elif card_type == 'action':
            if value in self.action_cards and self.action_cards[value] > 0:
                self.action_cards[value] -= 1
            else:
                print(f"Warning: Action card {value} not available in deck")


class PlayerHand:
    """Represents a player's current hand state."""

    def __init__(self):
        self.numbers: Set[int] = set()
        self.modifiers: List[str] = []
        self.has_second_chance: bool = False
        self.has_multiplier: bool = False

    def add_number(self, num: int):
        """Add a number card to hand."""
        self.numbers.add(num)

    def add_modifier(self, mod: str):
        """Add a modifier card."""
        if mod == 'x2':
            self.has_multiplier = True
        else:
            self.modifiers.append(mod)

    def add_second_chance(self):
        """Add Second Chance card."""
        self.has_second_chance = True

    def get_base_score(self) -> int:
        """Calculate base score from number cards."""
        return sum(self.numbers)

    def get_total_score(self) -> int:
        """Calculate total score including modifiers."""
        base = self.get_base_score()
        if self.has_multiplier:
            base *= 2

        modifier_sum = 0
        for mod in self.modifiers:
            if mod.startswith('+'):
                modifier_sum += int(mod[1:])

        return base + modifier_sum

    def num_cards(self) -> int:
        """Return number of unique number cards."""
        return len(self.numbers)

    def reset(self):
        """Clear the hand."""
        self.numbers.clear()
        self.modifiers.clear()
        self.has_second_chance = False
        self.has_multiplier = False


class GTOAnalyzer:
    """Analyzes game state and provides optimal decisions."""

    def __init__(self, deck: Flip7Deck, hand: PlayerHand):
        self.deck = deck
        self.hand = hand

    def calculate_bust_probability(self) -> float:
        """Calculate probability of busting on next card draw."""
        if not self.hand.numbers:
            return 0.0

        # Count duplicate cards remaining
        duplicates_remaining = sum(
            self.deck.number_cards.get(num, 0)
            for num in self.hand.numbers
        )

        total_remaining = self.deck.total_remaining_cards()

        if total_remaining == 0:
            return 0.0

        return duplicates_remaining / total_remaining

    def calculate_safe_cards_by_value(self) -> Dict[int, int]:
        """Get remaining count of each safe number card."""
        safe_cards = {}
        for num, count in self.deck.number_cards.items():
            if num not in self.hand.numbers and count > 0:
                safe_cards[num] = count
        return safe_cards

    def calculate_expected_value_simplified(self) -> Tuple[float, Dict]:
        """
        Calculate simplified expected value of hitting.
        Returns (EV, details_dict)
        """
        current_score = self.hand.get_total_score()
        total_remaining = self.deck.total_remaining_cards()

        if total_remaining == 0:
            return current_score, {'reason': 'no_cards_remaining'}

        # Calculate bust probability
        bust_prob = self.calculate_bust_probability()

        # Calculate safe number cards and their expected value
        safe_cards = self.calculate_safe_cards_by_value()
        safe_card_prob = sum(safe_cards.values()) / total_remaining

        # Expected value from safe number cards
        if safe_cards:
            avg_safe_value = sum(k * v for k, v in safe_cards.items()) / sum(safe_cards.values())
        else:
            avg_safe_value = 0

        # Modifier cards probability and value
        total_modifiers = sum(self.deck.modifier_cards.values())
        modifier_prob = total_modifiers / total_remaining

        # Simplified EV calculation
        # EV = P(safe) * (current + avg_safe) + P(modifier) * (current + avg_modifier) - P(bust) * current

        # For simplicity, assume modifiers add ~5 points on average
        avg_modifier_value = 5

        # Base case: immediate reward
        ev_safe = safe_card_prob * (current_score + avg_safe_value)
        ev_modifier = modifier_prob * (current_score + avg_modifier_value)
        ev_bust = bust_prob * 0  # Bust = 0 points
        ev_action = (sum(self.deck.action_cards.values()) / total_remaining) * current_score

        # Simple EV without recursive continuation
        expected_value = ev_safe + ev_modifier + ev_action + ev_bust

        details = {
            'current_score': current_score,
            'bust_probability': bust_prob,
            'safe_card_probability': safe_card_prob,
            'avg_safe_value': avg_safe_value,
            'expected_value': expected_value,
            'cards_in_hand': self.hand.num_cards(),
            'has_second_chance': self.hand.has_second_chance
        }

        return expected_value, details

    def should_hit(self) -> Tuple[bool, str, Dict]:
        """
        Determine if player should HIT or STAY.
        Returns (should_hit, recommendation, details)
        """
        current_score = self.hand.get_total_score()
        num_cards = self.hand.num_cards()

        # Special case: 6 cards (one away from bonus)
        if num_cards == 6:
            bust_prob = self.calculate_bust_probability()
            # Bonus is worth 15 points + whatever the 7th card is (avg ~7)
            # Expected gain ~22 points
            # Risk: lose current_score
            if self.hand.has_second_chance:
                return True, "GO FOR 7-CARD BONUS (you have Second Chance protection)", {}

            expected_bonus = 22 * (1 - bust_prob)
            expected_loss = current_score * bust_prob

            details = {
                'bust_probability': bust_prob,
                'expected_bonus': expected_bonus,
                'expected_loss': expected_loss
            }

            if expected_bonus > expected_loss:
                return True, f"GO FOR 7-CARD BONUS (EV: +{expected_bonus-expected_loss:.1f})", details
            else:
                return False, f"STAY - Bonus risk too high (would risk {current_score} for {expected_bonus:.1f})", details

        # Calculate EV
        ev, details = self.calculate_expected_value_simplified()

        # Adjust for Second Chance (reduces effective bust probability)
        if self.hand.has_second_chance:
            details['second_chance_note'] = "Second Chance active - can survive one bust"
            # More aggressive threshold with Second Chance
            threshold_adjustment = 5
        else:
            threshold_adjustment = 0

        # Decision logic
        bust_prob = details['bust_probability']

        # Very aggressive early game (1-2 cards)
        if num_cards <= 2:
            if bust_prob < 0.15:
                return True, f"HIT - Early game, low bust risk ({bust_prob*100:.1f}%)", details
            elif current_score < 20:
                return True, f"HIT - Score too low to stay ({current_score} points)", details

        # Mid game (3-4 cards)
        if num_cards <= 4:
            if bust_prob < 0.25 and current_score < 35:
                return True, f"HIT - Reasonable risk ({bust_prob*100:.1f}%), score under 35", details
            elif bust_prob < 0.15:
                return True, f"HIT - Low bust risk ({bust_prob*100:.1f}%)", details

        # Late game (5 cards)
        if num_cards == 5:
            if current_score < 40 and bust_prob < 0.35:
                return True, f"HIT - Consider pushing for 7-card bonus (bust risk: {bust_prob*100:.1f}%)", details
            elif bust_prob < 0.20:
                return True, f"HIT - Still reasonable risk ({bust_prob*100:.1f}%)", details

        # Default: compare EV directly (with adjustment)
        if ev > current_score + threshold_adjustment:
            return True, f"HIT - Positive expected value (EV: {ev:.1f} vs Current: {current_score})", details
        else:
            return False, f"STAY - Protect your score (EV: {ev:.1f} vs Current: {current_score})", details

    def get_recommendation(self) -> str:
        """Get a formatted recommendation string."""
        should_hit, reason, details = self.should_hit()

        action = "🎲 HIT (Draw another card)" if should_hit else "✋ STAY (Keep your current score)"

        output = [
            "\n" + "="*60,
            "GTO RECOMMENDATION",
            "="*60,
            f"Action: {action}",
            f"Reason: {reason}",
            "",
            "Current Hand Analysis:",
            f"  - Number cards: {sorted(self.hand.numbers)}",
            f"  - Cards in hand: {self.hand.num_cards()}/7",
            f"  - Current score: {self.hand.get_total_score()} points",
            f"  - Base score: {self.hand.get_base_score()}",
            f"  - Has Second Chance: {'Yes' if self.hand.has_second_chance else 'No'}",
            f"  - Has x2 Multiplier: {'Yes' if self.hand.has_multiplier else 'No'}",
            "",
            "Risk Analysis:",
            f"  - Bust probability: {details.get('bust_probability', 0)*100:.1f}%",
            f"  - Safe cards probability: {details.get('safe_card_probability', 0)*100:.1f}%",
            "",
            f"Cards remaining in deck: {self.deck.total_remaining_cards()}",
            "="*60
        ]

        return "\n".join(output)


class GameSession:
    """Manages a game session with user interaction."""

    def __init__(self):
        self.deck = Flip7Deck()
        self.hand = PlayerHand()
        self.analyzer = GTOAnalyzer(self.deck, self.hand)

    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*60)
        print("FLIP 7 - GAME THEORY OPTIMAL STRATEGY ANALYZER")
        print("="*60)
        print("\nThis program helps you make optimal decisions in Flip 7.")
        print("Track your cards and the analyzer will tell you whether to HIT or STAY.")
        print("\nCommands:")
        print("  - Enter a number (0-12) to add a number card to your hand")
        print("  - Enter '+X' (e.g., +5) to add a modifier card")
        print("  - Enter 'x2' to add a x2 multiplier")
        print("  - Enter 'sc' or 'second chance' to add Second Chance card")
        print("  - Enter 'recommend' or 'r' to get the optimal play recommendation")
        print("  - Enter 'status' or 's' to see current game state")
        print("  - Enter 'shuffle' or 'reset' to reset for a new round")
        print("  - Enter 'quit' or 'q' to exit")
        print("="*60 + "\n")

    def print_status(self):
        """Print current game status."""
        print("\n" + "-"*60)
        print("CURRENT GAME STATE")
        print("-"*60)
        print(f"Your hand: {sorted(self.hand.numbers)}")
        print(f"Number of cards: {self.hand.num_cards()}/7")
        print(f"Current score: {self.hand.get_total_score()} points")
        print(f"  - Base (numbers): {self.hand.get_base_score()}")
        print(f"  - Modifiers: {self.hand.modifiers}")
        print(f"  - Has x2: {self.hand.has_multiplier}")
        print(f"Second Chance: {'Yes' if self.hand.has_second_chance else 'No'}")
        print(f"\nCards remaining in deck: {self.deck.total_remaining_cards()}")

        # Show safe cards
        safe_cards = self.analyzer.calculate_safe_cards_by_value()
        if safe_cards:
            print("\nSafe number cards remaining:")
            for num in sorted(safe_cards.keys()):
                count = safe_cards[num]
                print(f"  {num}: {count} card(s)")

        bust_prob = self.analyzer.calculate_bust_probability()
        print(f"\nBust probability if you draw: {bust_prob*100:.1f}%")
        print("-"*60 + "\n")

    def handle_input(self, user_input: str) -> bool:
        """
        Handle user input. Returns False if should exit.
        """
        user_input = user_input.strip().lower()

        if user_input in ['quit', 'q', 'exit']:
            print("\nThanks for using Flip 7 GTO Analyzer!")
            return False

        elif user_input in ['shuffle', 'reset', 'new', 'restart']:
            self.deck.reset()
            self.hand.reset()
            print("\n✓ Deck shuffled! Starting new round.")
            return True

        elif user_input in ['status', 's', 'state']:
            self.print_status()
            return True

        elif user_input in ['recommend', 'r', 'rec', 'advice']:
            if self.hand.num_cards() == 0:
                print("\n⚠ No cards in hand yet. Draw some cards first!")
            else:
                print(self.analyzer.get_recommendation())
            return True

        elif user_input in ['help', 'h', '?']:
            self.print_welcome()
            return True

        # Parse card input
        elif user_input.startswith('+'):
            # Modifier card
            try:
                value = int(user_input[1:])
                if 2 <= value <= 10:
                    self.hand.add_modifier(f'+{value}')
                    self.deck.remove_card('modifier', f'+{value}')
                    print(f"✓ Added modifier: +{value}")
                else:
                    print("⚠ Invalid modifier. Use +2 through +10")
            except ValueError:
                print("⚠ Invalid modifier format. Example: +5")
            return True

        elif user_input == 'x2':
            self.hand.add_modifier('x2')
            self.deck.remove_card('modifier', 'x2')
            print("✓ Added x2 multiplier")
            return True

        elif user_input in ['sc', 'secondchance', 'second chance', 'second_chance']:
            self.hand.add_second_chance()
            self.deck.remove_card('action', 'Second Chance')
            print("✓ Added Second Chance card")
            return True

        else:
            # Try to parse as number card
            try:
                num = int(user_input)
                if 0 <= num <= 12:
                    if num in self.hand.numbers:
                        print(f"\n⚠ WARNING: You already have {num}! This would be a BUST!")
                        confirm = input("Are you sure you want to add this (bust)? (yes/no): ").strip().lower()
                        if confirm in ['yes', 'y']:
                            print("\n💥 BUST! You scored 0 points this round.")
                            print("Type 'shuffle' to start a new round.")
                    else:
                        self.hand.add_number(num)
                        self.deck.remove_card('number', num)
                        print(f"✓ Added number card: {num}")

                        # Check for 7-card bonus
                        if self.hand.num_cards() == 7:
                            bonus_score = self.hand.get_total_score() + 15
                            print("\n" + "🎉"*20)
                            print("SEVEN UNIQUE CARDS - INSTANT ROUND WIN!")
                            print(f"Final score: {bonus_score} points (+15 bonus)")
                            print("🎉"*20)
                            print("\nType 'shuffle' to start a new round.")
                else:
                    print("⚠ Invalid number. Use 0-12")
            except ValueError:
                print(f"⚠ Unknown command: '{user_input}'. Type 'help' for commands.")
            return True

    def run(self):
        """Run the interactive session."""
        self.print_welcome()

        while True:
            try:
                user_input = input("Enter command or card: ").strip()
                if not user_input:
                    continue

                should_continue = self.handle_input(user_input)
                if not should_continue:
                    break

            except KeyboardInterrupt:
                print("\n\nInterrupted. Exiting...")
                break
            except EOFError:
                print("\n\nExiting...")
                break


def main():
    """Main entry point."""
    session = GameSession()
    session.run()


if __name__ == "__main__":
    main()
