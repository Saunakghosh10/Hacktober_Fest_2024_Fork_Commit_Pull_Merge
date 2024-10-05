from typing import List, Tuple

def weighted_subset_sum(n: int, w: List[int], v: List[int], W: int, K: int, 
                        must_pair: List[Tuple[int, int]], cannot_pair: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    # Initialize memoization table
    dp = [[[-1 for _ in range(K + 1)] for _ in range(W + 1)] for _ in range(n)]
    selected = [False] * n

    def solve(idx: int, weight: int, count: int) -> int:
        if idx == n or weight == W or count == K:
            return 0
        
        if dp[idx][weight][count] != -1:
            return dp[idx][weight][count]
        
        not_take = solve(idx + 1, weight, count)
        take = 0
        
        # Check if we can take this item
        can_take = all(not (pair[0] == idx and selected[pair[1]]) and 
                       not (pair[1] == idx and selected[pair[0]]) 
                       for pair in cannot_pair)
        
        if can_take and weight + w[idx] <= W and count + 1 <= K:
            # Check if we need to take the paired item
            extra_weight, extra_value = 0, 0
            for pair in must_pair:
                if pair[0] == idx and not selected[pair[1]]:
                    extra_weight, extra_value = w[pair[1]], v[pair[1]]
                    break
                elif pair[1] == idx and not selected[pair[0]]:
                    extra_weight, extra_value = w[pair[0]], v[pair[0]]
                    break
            
            if weight + w[idx] + extra_weight <= W and count + 1 + (extra_weight > 0) <= K:
                selected[idx] = True
                take = v[idx] + extra_value + solve(idx + 1, weight + w[idx] + extra_weight, count + 1 + (extra_weight > 0))
                selected[idx] = False
        
        dp[idx][weight][count] = max(take, not_take)
        return dp[idx][weight][count]

    max_value = solve(0, 0, 0)

    # Backtrack to find the selected items
    selected_items = []
    idx, weight, count = 0, 0, 0
    while idx < n and weight < W and count < K:
        not_take = dp[idx + 1][weight][count] if idx + 1 < n else 0
        take = 0
        
        can_take = all(not (pair[0] == idx and selected[pair[1]]) and 
                       not (pair[1] == idx and selected[pair[0]]) 
                       for pair in cannot_pair)
        
        if can_take and weight + w[idx] <= W and count + 1 <= K:
            extra_weight, extra_value = 0, 0
            for pair in must_pair:
                if pair[0] == idx and not selected[pair[1]]:
                    extra_weight, extra_value = w[pair[1]], v[pair[1]]
                    break
                elif pair[1] == idx and not selected[pair[0]]:
                    extra_weight, extra_value = w[pair[0]], v[pair[0]]
                    break
            
            if weight + w[idx] + extra_weight <= W and count + 1 + (extra_weight > 0) <= K:
                take = v[idx] + extra_value + dp[idx + 1][weight + w[idx] + extra_weight][count + 1 + (extra_weight > 0)]
        
        if take > not_take:
            selected_items.append(idx)
            selected[idx] = True
            weight += w[idx]
            count += 1
            
            # Add the paired item if necessary
            for pair in must_pair:
                if pair[0] == idx and not selected[pair[1]]:
                    selected_items.append(pair[1])
                    selected[pair[1]] = True
                    weight += w[pair[1]]
                    count += 1
                    break
                elif pair[1] == idx and not selected[pair[0]]:
                    selected_items.append(pair[0])
                    selected[pair[0]] = True
                    weight += w[pair[0]]
                    count += 1
                    break
        idx += 1

    return max_value, selected_items

# Example usage
if __name__ == "__main__":
    n = 5
    w = [2, 3, 4, 5, 1]
    v = [3, 4, 5, 8, 1]
    W = 10
    K = 3
    must_pair = [(0, 1)]
    cannot_pair = [(2, 3)]

    max_value, selected_items = weighted_subset_sum(n, w, v, W, K, must_pair, cannot_pair)
    print(f"Maximum value: {max_value}")
    print(f"Selected items: {selected_items}")