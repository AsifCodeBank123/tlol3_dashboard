import random
from itertools import combinations

def avoid_same_team_pairing(entities, total_required_pairs=None):
    valid_pairs = [
        (i, j) for i, j in combinations(range(len(entities)), 2)
        if entities[i]['team name'] != entities[j]['team name']
    ]
    random.shuffle(valid_pairs)
    used = set()
    result = []
    for i, j in valid_pairs:
        if i not in used and j not in used:
            result.append((entities[i], entities[j]))
            used.add(i)
            used.add(j)

    if total_required_pairs and len(result) < total_required_pairs:
        remaining = [e for idx, e in enumerate(entities) if idx not in used]
        random.shuffle(remaining)
        while len(result) < total_required_pairs and len(remaining) >= 2:
            result.append((remaining.pop(), remaining.pop()))
    return result

def interleave_seeds(seed1, seed2, group_labels):
    random.shuffle(seed1)
    random.shuffle(seed2)
    interleaved = []
    s1_idx = s2_idx = 0
    while len(interleaved) < len(group_labels) and (s1_idx < len(seed1) or s2_idx < len(seed2)):
        if s1_idx < len(seed1):
            interleaved.append(seed1[s1_idx])
            s1_idx += 1
        if len(interleaved) < len(group_labels) and s2_idx < len(seed2):
            interleaved.append(seed2[s2_idx])
            s2_idx += 1
    qualified = interleaved
    half = len(qualified) // 2
    return qualified[:half], qualified[half:]
