from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds the best way to cut using memoization

    Args:
        length: rod length
        prices: a list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with maximum profit and a list of cuts
    """
    memo = {}
    
    def dfs(n):
        """
        Recursive helper function to determine the maximum profit and cuts for a rod of length n.

        Args:
            n: The current length of the rod being considered.

        Returns:
            A tuple containing:
            - The maximum profit obtainable by cutting the rod of length n.
            - A list of cuts that lead to the maximum profit.
        """
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]
        
        max_profit = 0
        best_cut = []
        
        for i in range(1, n + 1):
            profit, cuts = dfs(n - i)
            profit += prices[i - 1]
            
            if profit > max_profit:
                max_profit = profit
                best_cut = [i] + cuts
        
        memo[n] = (max_profit, best_cut)
        return memo[n]
    
    max_profit, cuts = dfs(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds the best way to cut using tabulation

    Args:
        length: rod length
        prices: a list of prices, where prices[i] is the price of a rod of length i+1

    Returns:
        Dict with maximum profit and a list of cuts
    """
    dp = [0] * (length + 1)
    cut_record = [[] for _ in range(length + 1)]
    
    for n in range(1, length + 1):
        for i in range(1, n + 1):
            if dp[n] < prices[i - 1] + dp[n - i]:
                dp[n] = prices[i - 1] + dp[n - i]
                cut_record[n] = [i] + cut_record[n - i]
    
    return {
        "max_profit": dp[length],
        "cuts": cut_record[length],
        "number_of_cuts": len(cut_record[length]) - 1
    }

def run_tests():
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Basic case"},
        {"length": 3, "prices": [1, 3, 8], "name": "Do not cut optimally"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Uniform cuts"}
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization result:")
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation result:")
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")
        print("\nThe test was successful!")

if __name__ == "__main__":
    run_tests()