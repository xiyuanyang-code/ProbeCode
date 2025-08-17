"""
A sample Python file containing multiple classes and functions to demonstrate
object-oriented and functional programming concepts.
"""

import math
import collections
from typing import List, Optional, Dict, Any, Deque


# --- Original Code ---

class Calculator:
    """
    A simple calculator class that provides basic mathematical operations.

    Attributes:
        precision (int): The number of decimal places to round the results to,
                         defaults to 2.
    """
    
    def __init__(self, precision: int = 2):
        """
        Initializes the Calculator instance.

        Args:
            precision (int): The number of decimal places for the result.
        """
        self.precision = precision
        
    def add(self, a: float, b: float) -> float:
        """
        Performs addition.

        Args:
            a (float): The first operand.
            b (float): The second operand.

        Returns:
            float: The sum of the two operands, rounded to the specified precision.
        """
        return round(a + b, self.precision)
        
    def subtract(self, a: float, b: float) -> float:
        """
        Performs subtraction.

        Args:
            a (float): The first operand.
            b (float): The second operand.

        Returns:
            float: The difference of the two operands, rounded to the specified precision.
        """
        return round(a - b, self.precision)
        
    def multiply(self, a: float, b: float) -> float:
        """
        Performs multiplication.

        Args:
            a (float): The first operand.
            b (float): The second operand.

        Returns:
            float: The product of the two operands, rounded to the specified precision.
        """
        return round(a * b, self.precision)
        
    def divide(self, a: float, b: float) -> Optional[float]:
        """
        Performs division.

        Args:
            a (float): The dividend.
            b (float): The divisor.

        Returns:
            Optional[float]: The quotient of the two operands. Returns None if the
                             divisor is 0.
        """
        if b == 0:
            return None
        return round(a / b, self.precision)


class AdvancedCalculator(Calculator):
    """
    An advanced calculator class that inherits from Calculator and provides
    additional mathematical operations.
    """
    
    def power(self, base: float, exponent: float) -> float:
        """
        Performs exponentiation.

        Args:
            base (float): The base number.
            exponent (float): The exponent.

        Returns:
            float: The result of the power operation, rounded to the specified precision.
        """
        return round(base ** exponent, self.precision)
        
    def sqrt(self, value: float) -> Optional[float]:
        """
        Calculates the square root.

        Args:
            value (float): The number to find the square root of.

        Returns:
            Optional[float]: The square root of the number. Returns None if the
                             input is negative.
        """
        if value < 0:
            return None
        return round(math.sqrt(value), self.precision)


def fibonacci(n: int) -> List[int]:
    """
    Generates the first n numbers of the Fibonacci sequence.

    Args:
        n (int): The number of Fibonacci numbers to generate.

    Returns:
        List[int]: A list containing the first n Fibonacci numbers.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
        
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def is_prime(num: int) -> bool:
    """
    Checks if a number is a prime number.

    Args:
        num (int): The integer to check.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


# --- New Code ---

class DataProcessor:
    """
    A utility class for processing and analyzing data.

    Attributes:
        data (List[Any]): The list of data to be processed.
    """
    
    def __init__(self, data: List[Any]):
        """
        Initializes the DataProcessor instance.

        Args:
            data (List[Any]): A list containing various data types.
        """
        self.data = data
        
    def get_max(self) -> Optional[Any]:
        """
        Returns the maximum value from the data list.

        Returns:
            Optional[Any]: The maximum value in the list. Returns None if the list is empty.
        """
        if not self.data:
            return None
        return max(self.data)
        
    def get_min(self) -> Optional[Any]:
        """
        Returns the minimum value from the data list.

        Returns:
            Optional[Any]: The minimum value in the list. Returns None if the list is empty.
        """
        if not self.data:
            return None
        return min(self.data)
        
    def count_occurrences(self) -> Dict[Any, int]:
        """
        Counts the occurrences of each element in the list.

        Returns:
            Dict[Any, int]: A dictionary where keys are elements and values are their counts.
        """
        return dict(collections.Counter(self.data))


class StringUtils:
    """
    A class with static methods for various string manipulation utilities.
    """
    
    @staticmethod
    def reverse_string(s: str) -> str:
        """
        Reverses a string.

        Args:
            s (str): The string to reverse.

        Returns:
            str: The reversed string.
        """
        return s[::-1]
        
    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        Checks if a string is a palindrome.

        Args:
            s (str): The string to check.

        Returns:
            bool: True if the string is a palindrome, False otherwise.
        """
        s_cleaned = "".join(filter(str.isalnum, s)).lower()
        return s_cleaned == s_cleaned[::-1]

    @staticmethod
    def count_words(s: str) -> int:
        """
        Counts the number of words in a string.

        Args:
            s (str): The string to count words from.

        Returns:
            int: The number of words in the string.
        """
        return len(s.split())


def factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer using recursion.

    Args:
        n (int): The non-negative integer to calculate the factorial of.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is a negative number.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def find_max_in_list(nums: List[float]) -> Optional[float]:
    """
    Finds the maximum value in a list of floating-point numbers.

    Args:
        nums (List[float]): A list of floats.

    Returns:
        Optional[float]: The maximum value in the list. Returns None if the list is empty.
    """
    if not nums:
        return None
    max_val = nums[0]
    for num in nums[1:]:
        if num > max_val:
            max_val = num
    return max_val


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merges two dictionaries. If a key exists in both dictionaries, the value from
    the second dictionary is used.

    Args:
        dict1 (Dict): The first dictionary.
        dict2 (Dict): The second dictionary.

    Returns:
        Dict: A new dictionary containing the merged key-value pairs.
    """
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def main():
    """
    The main function to demonstrate the functionality of all classes and functions.
    """
    print("--- Original Calculator Test ---")
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    
    adv_calc = AdvancedCalculator()
    print(f"2^8 = {adv_calc.power(2, 8)}")
    
    fib_seq = fibonacci(10)
    print(f"First 10 Fibonacci numbers: {fib_seq}")
    
    num = 17
    print(f"Is {num} a prime number? {is_prime(num)}")
    
    print("\n--- New Functionality Test ---")
    
    processor = DataProcessor([1, 2, 3, 4, 3, 2, 1, 5])
    print(f"Maximum value: {processor.get_max()}")
    print(f"Element occurrences: {processor.count_occurrences()}")
    
    reversed_str = StringUtils.reverse_string("hello world")
    print(f"Reversed string: {reversed_str}")
    
    is_pali = StringUtils.is_palindrome("A man, a plan, a canal: Panama")
    print(f"'A man, a plan, a canal: Panama' is a palindrome? {is_pali}")
    
    try:
        fact_5 = factorial(5)
        print(f"Factorial of 5: {fact_5}")
    except ValueError as e:
        print(e)
    
    merged_dict = merge_dicts({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
    print(f"Merged dictionaries: {merged_dict}")


if __name__ == "__main__":
    main()