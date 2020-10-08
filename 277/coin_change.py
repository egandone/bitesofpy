from typing import List


# Got this algorithm from https://www.youtube.com/watch?v=8VSZvHySVF0
def solve(n, coins, coin_index, cache):
    # If we have hit 0 then we have a solution
    if n == 0:
        return 1
        # If we have gone too far then this branch is not a solution
    if n < 0:
        return 0
        # If we have run out of coind then there is also no solution for this branch
    if coin_index >= len(coins):
        return 0

        # If already computed use it.
    key = (n, coin_index)
    if key in cache:
        return cache[key]

        # Count if we use the coin at the index - so we solve
        # for n - the coin value at the index
    num_with_coin_picked = solve(
        n - coins[coin_index], coins, coin_index, cache)
    # Count if we move to the next coin
    num_without_coin_picked = solve(n, coins, coin_index + 1, cache)

    # Total is the sum down each branch
    result = num_with_coin_picked + num_without_coin_picked
    # Save the result in the cache
    cache[key] = result
    return result


def make_changes(n: int, coins: List[int]) -> int:
    """
    Input: n - the changes amount
          coins - the coin denominations
    Output: how many ways to make this changes
    """
    return solve(n, coins, 0, dict())
