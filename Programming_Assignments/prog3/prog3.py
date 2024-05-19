import numpy as np
import random
#random.seed(347829)
def chooseFromDist(p):
    return random.choices(range(1, len(p)+1), weights=p)[0]
    
def rollDice(NDice,NSides):
    return sum(random.randint(1, NSides) for _ in range(NDice))

def chooseDice(Score, LoseCount, WinCount, NDice, M):
    X, Y = Score
    #probability array
    p = np.zeros(NDice)
    total_played = LoseCount[X, Y, 1:].sum() + WinCount[X, Y, 1:].sum()

    # compute win rates for each number of dice, default 0.5
    win_rates = np.zeros(NDice)
    for dice_index in range(1, NDice + 1):
        wins = WinCount[X, Y, dice_index]
        losses = LoseCount[X, Y, dice_index]
        total_outcomes = wins + losses
        win_rates[dice_index - 1] = wins / total_outcomes if total_outcomes > 0 else 0.5


    best_dice = np.argmax(win_rates)
    total_win_rate = win_rates.sum()

    # probability of selecting the best dice option
    p[best_dice] = (total_played * win_rates[best_dice] + M) / (total_played * win_rates[best_dice] + NDice * M)

    # probabilities for the rest of the dice options
    for i in range(NDice):
        if i != best_dice:
            p[i] = ((1 - p[best_dice]) * (total_played * win_rates[i] + M)) / ((total_win_rate - win_rates[best_dice]) * total_played + (NDice - 1) * M)

    return chooseFromDist(p)


def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    scores = [0, 0]
    rolls = [[], []]
    current_player = 0

    while True:
        nDice = chooseDice((scores[current_player], scores[1 - current_player]), LoseCount, WinCount, NDice, M)
        rolls[current_player].append((scores[current_player], scores[1 - current_player], nDice))
        roll_result = rollDice(nDice, NSides)
        scores[current_player] += roll_result

        # wins if exceeded UTarget
        if LTarget <= scores[current_player] <= UTarget:
            # player wins
            break
        elif scores[current_player] > UTarget:
            # player loses, other player wins
            current_player = 1 - current_player
            break

        # switch to the other player
        current_player = 1 - current_player

    for score, opponent_score, dice_count in rolls[current_player]:
        x, y = min(score, UTarget), min(opponent_score, UTarget)  # Ensure indices are within bounds
        WinCount[x, y, dice_count] += 1

    for score, opponent_score, dice_count in rolls[1 - current_player]:
        x, y = min(score, UTarget), min(opponent_score, UTarget)  # Ensure indices are within bounds
        LoseCount[x, y, dice_count] += 1

    return WinCount, LoseCount

def extractAnswer(WinCount, LoseCount):
    # determine  best move using argmax
    best_move_indices = np.argmax(WinCount, axis=2)

    # adjust indices for proper access
    idx = np.arange(WinCount.shape[0])[:, None], np.arange(WinCount.shape[1]), best_move_indices

    win_count = WinCount[idx]
    lose_count = LoseCount[idx]
    total_games = win_count + lose_count

    # calculate win probability
    with np.errstate(divide='ignore', invalid='ignore'):
        win_p = np.where(total_games > 0, win_count / total_games, 0)
    
    win_p = np.round(win_p, 4)

    return best_move_indices, win_p

def prog3(NDice, NSides, LTarget, UTarget, M, NGames):
    # initialize WinCount and LoseCount
    WinCount = np.zeros((LTarget, LTarget, NDice + 1),dtype=int)
    LoseCount = np.zeros((LTarget, LTarget, NDice + 1),dtype=int)

    for _ in range(NGames):
        WinCount, LoseCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

    # extract and return the best moves and win probabilities
    return extractAnswer(WinCount, LoseCount)

def read_input(filename):
    with open(filename, 'r') as file:
        NDice, NSides, LTarget, UTarget, M, NGames = [int(line.strip()) for line in file.readlines()]
    return NDice, NSides, LTarget, UTarget, M, NGames

def main():
    parameters = read_input('input.txt')
    moves, probabilities = prog3(*parameters)
    display_game_info(*parameters)
    display_results(moves, probabilities)

def display_game_info(NDice, NSides, LTarget, UTarget, M, NGames):
    print("Game: NDice=",NDice," NSides=",NSides," LTarget=",LTarget," UTarget=",UTarget)
    print("Reinforcement learning experiment with M =", M, ", NGames =", NGames)

def display_results(best_moves, win_probabilities):
    print("Play =")
    for row in best_moves:
        formatted_row = format_row(row, "{:6d}")
        print(formatted_row)
    
    print("Prob = ")
    for row in win_probabilities:
        formatted_row = format_row(row, "{:10.4f}", zero_format="  0    ")
        print(formatted_row)

def format_row(row, format_spec, zero_format="{:6d}"):
    return " ".join(format_spec.format(item) if item != 0 else zero_format.format(0) for item in row)

if __name__ == "__main__":
    main()
