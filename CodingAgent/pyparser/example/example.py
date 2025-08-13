#!/usr/bin/env python3
"""
示例Python文件，用于测试解析器
"""

import math
from typing import List, Optional


class Calculator:
    """简单计算器类"""
    
    def __init__(self, precision: int = 2):
        self.precision = precision
        
    def add(self, a: float, b: float) -> float:
        """加法运算"""
        return round(a + b, self.precision)
        
    def subtract(self, a: float, b: float) -> float:
        """减法运算"""
        return round(a - b, self.precision)
        
    def multiply(self, a: float, b: float) -> float:
        """乘法运算"""
        return round(a * b, self.precision)
        
    def divide(self, a: float, b: float) -> Optional[float]:
        """除法运算"""
        if b == 0:
            return None
        return round(a / b, self.precision)


class AdvancedCalculator(Calculator):
    """高级计算器类"""
    
    def power(self, base: float, exponent: float) -> float:
        """幂运算"""
        return round(base ** exponent, self.precision)
        
    def sqrt(self, value: float) -> Optional[float]:
        """平方根运算"""
        if value < 0:
            return None
        return round(math.sqrt(value), self.precision)


def fibonacci(n: int) -> List[int]:
    """生成斐波那契数列"""
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
    """判断一个数是否为质数"""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def main():
    """主函数"""
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    
    adv_calc = AdvancedCalculator()
    print(f"2^8 = {adv_calc.power(2, 8)}")
    
    fib_seq = fibonacci(10)
    print(f"斐波那契数列前10项: {fib_seq}")
    
    num = 17
    print(f"{num} 是质数吗? {is_prime(num)}")


if __name__ == "__main__":
    main()