from blackjack_art import logo
from os import system, name
import random

deck = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}


def deal_cards(hand):
    """Deal a new card and add to current hand"""
    hand = hand.append(random.choice(list(deck)))


def is_blackjack(user_hand, dealers_hand):
    """Verify if either of the input hands have a Blackjack eligible pair"""
    user_count = 0
    dealer_count = 0
    for hand in user_hand:
        if deck[hand] == 11 or deck[hand] == 10:
            user_count += deck[hand]
    for hand in dealers_hand:
        if deck[hand] == 11 or deck[hand] == 10:
            dealer_count += deck[hand]

    if user_count == 21 and dealer_count == 21:
        print("BLACKJACK: COMPUTER WINS")
        return True
    elif (user_count == 21) and (user_count > dealer_count):
        print("BLACKJACK: USER WINS")
        return True
    elif (dealer_count == 21) and (dealer_count > user_count):
        print("BLACKJACK: COMPUTER WINS")
        return True
    else:
        return False


def calculate_score(user_hand, dealers_hand):
    """Calculate total scores of the input hands and also update the value of 'A' according to the total value of the hand"""
    users_score = 0
    dealers_score = 0

    user_A_count = user_hand.count("A")
    dealers_A_count = dealers_hand.count("A")

    for card in user_hand:
        if card != "A":
            users_score += deck[card]

    if user_A_count > 0:
        users_score += 11 + (user_A_count - 1)

    for card in dealers_hand:
        if card != "A":
            dealers_score += deck[card]

    if dealers_A_count > 0:
        dealers_score += 11 + (dealers_A_count - 1)

    return users_score, dealers_score


def play_again_choice():
    """Choice to play again"""
    play_again = False
    play_again_choice_selection = input("GAME OVER - Do you want to play again (Y / N): ")
    if play_again_choice_selection.upper() == "Y":
        play_again = True
    else:
        play_again = False
    return play_again


def clear():
    """Clear the screen"""
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


def compare(users_score, dealers_score):
    """Verify and compare the user's score and the dealer's score"""
    if users_score > 21 and dealers_score > 21:
        return "Score exceeds 21 for both the user and the computer. Computer wins"

    if users_score == dealers_score:
        return "DRAW"
    elif users_score > 21:
        return "BUST: You loose. User's score exceeded 21"
    elif dealers_score > 21:
        return "WIN: User Wins as Computer's Score exceeds 21"
    elif users_score > dealers_score:
        return f"WIN: User Wins as User's Score {users_score} is greater than Computer's Score {dealers_score}"
    else:
        return f"BUST: You loose as User's Score {users_score} is less than Computer's Score {dealers_score}"


def play_blackjack():
    """Play blackjack"""
    play_again = True
    while play_again:
        user_hand = []
        users_score = 0
        deal_cards(user_hand)
        deal_cards(user_hand)
        dealers_hand = []
        dealers_score = 0
        deal_cards(dealers_hand)
        deal_cards(dealers_hand)
        clear()
        print(logo)
        users_score, dealers_score = calculate_score(user_hand, dealers_hand)
        print(f"USER'S HAND: {user_hand}, CURRENT SCORE: {users_score}")
        print(f"COMPUTER'S HAND: ['{dealers_hand[0]}', 'X'], CURRENT SCORE: {deck[dealers_hand[0]]}")
        if not is_blackjack(user_hand, dealers_hand):
            while not (users_score >= 21):
                choice = input("Do you want another card? (Y / N): ")
                if choice.upper() == "Y":
                    deal_cards(user_hand)
                else:
                    break
                users_score, dealers_score = calculate_score(user_hand, dealers_hand)
                print(f"USER'S HAND: {user_hand}, CURRENT SCORE: {users_score}")
                print(f"COMPUTER'S HAND: ['{dealers_hand[0]}', 'X'], CURRENT SCORE: {deck[dealers_hand[0]]}")
                if users_score > 21:
                    break

            if not (users_score > 21):
                while not (dealers_score > 17):
                    deal_cards(dealers_hand)
                    users_score, dealers_score = calculate_score(user_hand, dealers_hand)
                    if dealers_score > 21:
                        break
                print(f"USER'S HAND: {user_hand}, CURRENT SCORE: {users_score}")
                print(f"COMPUTER'S HAND: {dealers_hand}, CURRENT SCORE: {dealers_score}")

                print(compare(users_score, dealers_score))
            else:
                print("BUST: You loose. User's score exceeded 21")

            if play_again_choice():
                play_again = True
            else:
                break
        else:
            if play_again_choice():
                play_again = True
            else:
                break

    print("THANK YOU FOR PLAYING")


play_blackjack()