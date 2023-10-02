"""
    Count win probabilities on given dealing cards for each player .
"""
from collections import Counter
from itertools import combinations


CARDS_VALUE = {"A": "14", "K": "13", "Q": "12", "J": "11"}


def the_most_commons(hand: []):
    """
        Check for pair, 2pairs, full_house, care or set.
    """

    hand_without_suit = []

    for card in hand:
        if card[:-1] in CARDS_VALUE.keys():
            hand_without_suit.append(int(CARDS_VALUE[card[:-1]]))
        else:
            hand_without_suit.append(int(card[:-1]))
    converted_hand = sorted(Counter(hand_without_suit).most_common(),
                            key=lambda item: (-int(item[1]), -int(item[0])))
    if converted_hand[0][1] == 4:
        return [8, converted_hand[0][0], max([i[0] for i in converted_hand[1:]])]

    if converted_hand[0][1] == 3 and converted_hand[1][1] >= 2:
        return [7, converted_hand[0][0], converted_hand[1][0]]

    if converted_hand[0][1] == 3:
        return [4, converted_hand[0][0], converted_hand[1][0], converted_hand[2][0]]

    if converted_hand[0][1] == 2 and converted_hand[1][1] == 2:
        if converted_hand[3][0] > converted_hand[2][0]:
            return [3, converted_hand[0][0], converted_hand[1][0], converted_hand[3][0]]
        return [3, converted_hand[0][0], converted_hand[1][0], converted_hand[2][0]]

    if converted_hand[0][1] == 2:
        return [2, converted_hand[0][0], converted_hand[1][0],
                converted_hand[2][0], converted_hand[3][0]]

    return [1] + [converted_hand[i][0] for i in range(5)]


def is_straight(hand: []):
    """
        Check for straight.
    """

    cards = {"14": 0, "13": 0, "12": 0, "11": 0,
             "10": 0, "9": 0, "8": 0, "7": 0,
             "6": 0, "5": 0, "4": 0, "3": 0, "2": 0, "1": 0}
    counter = 0

    for i in [card[:-1] for card in hand]:
        if i in CARDS_VALUE.keys():
            if i == "A":
                cards["1"] = 1
                cards["14"] = 1
            else:
                cards[CARDS_VALUE[i]] = 1
        else:
            cards[i] = 1

    for quality, _ in cards.items():
        if cards[quality] == 1:
            counter += 1
            if counter == 5:
                return [5, int(quality)+4]
        else:
            counter = 0
    return None


def is_flush(hand: []):
    """
        Check for flush or flush and straight.
    """

    suit = {"S": set(), "H": set(), "D": set(), "C": set()}
    flush = []

    for card in hand:
        suit[card[-1]].add(card[:-1])
    for qualities in suit.values():
        if len(qualities) >= 5:
            for quality in list(qualities):
                if quality in CARDS_VALUE.keys():
                    if quality == "A":
                        flush.append(1)
                        flush.append(14)
                    else:
                        flush.append(int(CARDS_VALUE[quality]))
                else:
                    flush.append(int(quality))
            check_straight = 0
            flush.sort(reverse=True)
            for index in range(len(flush)-1):
                if flush[index] - flush[index+1] == 1:
                    check_straight += 1
                    if check_straight == 4:
                        return [9, flush[index-3]]
                else:
                    check_straight = 0
            return [6] + sorted(flush, reverse=True)[:5]
    return None


def hand_conversion(hand: []):
    """
        Convert the hand into its value.
    """

    hands = []

    if is_flush(hand):
        hands.append(is_flush(hand))

    if is_straight(hand):
        hands.append(is_straight(hand))

    hands.append(the_most_commons(hand))
    hands.sort()
    return hands[-1]


def count_win_probabilities(players_private_cards,
                            known_community_cards,
                            already_dropped_cards=None):
    """
        Count win probabilities for each player.
    """

    all_cards = {'AS', 'AC', 'AD', 'AH', 'KS', 'KC', 'KD', 'KH', 'QS',
                 'QC', 'QD', 'QH', 'JS', 'JC', 'JD', 'JH', '10S', '10C',
                 '10D', '10H', '9S', '9C', '9D', '9H', '8S', '8C', '8D',
                 '8H', '7S', '7C', '7D', '7H', '6S', '6C', '6D', '6H', '5S',
                 '5C', '5D', '5H', '4S', '4C', '4D', '4H', '3S', '3C', '3D',
                 '3H', '2S', '2C', '2D', '2H'}

    for i in players_private_cards:
        all_cards = all_cards.difference(i)

    if already_dropped_cards is not None:
        all_cards = all_cards.difference(set(known_community_cards +
                                             already_dropped_cards))
    else:
        all_cards = all_cards.difference(set(known_community_cards))

    all_variations_of_remaining_cards = sum([list(map(list,
                                                      combinations(all_cards,
                                                                   5-len(known_community_cards))))],
                                            [])
    result_of_each_variation = [0] * len(players_private_cards)

    for i in all_variations_of_remaining_cards:
        all_score_cards = []

        for j in players_private_cards:
            seven_cards = i + known_community_cards + list(j)
            all_score_cards.append(hand_conversion(seven_cards))

        maximum = max(all_score_cards)

        for index, value in enumerate(all_score_cards):
            if value == maximum:
                result_of_each_variation[index] += 1/all_score_cards.count(maximum)

    for index, result in enumerate(result_of_each_variation):
        result_of_each_variation[index] = result/len(all_variations_of_remaining_cards)

    return result_of_each_variation
