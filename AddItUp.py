import numpy as np

def simulate_game(policy):
    """ Returns a tuple of (winning choices, losing choices """
    player_1_choices = {1:0, 2:0, 3:0, 4:0, 5:0}
    player_1_total = 0
    player_2_choices = {1:0, 2:0, 3:0, 4:0, 5:0}
    player_2_total = 0
    for i in range(100):
        player_1_choice = np.random.choice([1,2,3,4,5], p=policy)
        player_1_choices[player_1_choice] += 1
        player_2_choice = np.random.choice([1,2,3,4,5], p=policy)
        player_2_choices[player_2_choice] += 1
        player_1_total += player_1_choice
        player_2_total += player_2_choice

    if player_1_total>player_2_total:
        winning_choices = player_1_choices
        losing_choices = player_2_choices
    else:
        winning_choices = player_2_choices
        losing_choices = player_1_choices
    return winning_choices, losing_choices

def normalize(policy):
    policy = np.clip(policy,0,1)
    return policy / np.sum(policy)

if __name__ == '__main__':
    number_games = 2000
    choices = [1,2,3,4,5]
    policy = np.array([0.2,0.2,0.2,0.2,0.2])
    learning_rate = 0.0001
    for i in range(number_games):
        win_counter, lose_counters = simulate_game(policy)
        for j, choice in enumerate(choices):
            net_wins = win_counter[choice] - lose_counters[choice]
            policy[j] += learning_rate*net_wins
        policy = normalize(policy)
        print('%d %s' %(i,policy))
