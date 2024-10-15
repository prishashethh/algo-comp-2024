import numpy as np
import random
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    # Total number of users
    n = len(scores)
    half = n//2

    # Assign proposers and receivers
    proposers_indices = random.sample(range(n), half)
    receivers_indices = []
    for i in range(n):
        if i not in proposers_indices:
            receivers_indices.append(i)

    # Create preference lists based on compatibility scores
    def create_preferences(indices, is_proposer):
        preferences = {}
        for i in indices:
            pref_list = []
            for j in receivers_indices if is_proposer else proposers_indices:
                # Check compatibility
                if is_proposer:
                    if (gender_pref[i] == "Men" and gender_id[j] == "Male") or \
                       (gender_pref[i] == "Women" and gender_id[j] == "Female") or \
                       (gender_pref[i] == "Bisexual"):
                        pref_list.append((scores[i][j], j))
                else:
                    if (gender_pref[j] == "Men" and gender_id[i] == "Male") or \
                       (gender_pref[j] == "Women" and gender_id[i] == "Female") or \
                       (gender_pref[j] == "Bisexual"):
                        pref_list.append((scores[j][i], i))  
            # Sort preferences based on compatibility scores in descending order using python sort
            pref_list.sort(reverse=True, key=lambda x: x[0])
            preferences[i] = [x[1] for x in pref_list]  # Store only indices of preferences
        return preferences

    proposer_preferences = create_preferences(proposers_indices, is_proposer=True)
    receiver_preferences = create_preferences(receivers_indices, is_proposer=False)

    free_proposers = list(proposers_indices)  

    # Track a dictionary
    proposals = {proposer: 0 for proposer in proposers_indices}
    receivers = {receiver: None for receiver in receivers_indices}
    
    matches = []

    # Start the Gale-Shapley algorithm loop
    while free_proposers:
        proposer = free_proposers.pop(0)  # Get the first free proposer
        # Get the next receiver from the proposer's preference list
        receiver = proposer_preferences[proposer][proposals[proposer]]

        # Check if the receiver is free
        if receivers[receiver] is None:
            receivers[receiver] = proposer
        else:
            current_match = receivers[receiver]
            if receiver_preferences[receiver].index(proposer) < receiver_preferences[receiver].index(current_match):
                # If the receiver prefers the new proposer, update the match
                receivers[receiver] = proposer
                free_proposers.append(current_match)
            else:
                # The proposer remains free, add back to the free_proposers list
                free_proposers.append(proposer)

        proposals[proposer] += 1

    # Convert the final receiver matches into a list of (proposer, receiver) tuples
    matches = [(receivers[j], j) for j in receivers if receivers[j] is not None]
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)

