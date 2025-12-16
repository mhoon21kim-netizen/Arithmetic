"""
사칙연산 모듈 테스트 케이스
TC-CMM-001 / TC-AO-001
"""
import pytest
from src.arithmetic import Arithmetic


class TestArithmetic:
    """사칙연산 테스트 클래스"""
    
    def test_addition_positive_numbers(self):
        """덧셈 테스트: 양수 (1 + 10 = 11)"""
        assert Arithmetic.add(1, 10) == 11
    
    def test_addition_with_zero(self):
        """덧셈 테스트: 0 포함 (0 + 1 = 1)"""
        assert Arithmetic.add(0, 1) == 1
    
    def test_addition_negative_numbers(self):
        """덧셈 테스트: 음수 (-1 + (-10) = -11)"""
        assert Arithmetic.add(-1, -10) == -11
    
    def test_subtraction(self):
        """뺄셈 테스트 (5 - 2 = 3)"""
        assert Arithmetic.subtract(5, 2) == 3
    
    def test_multiplication_negative_numbers(self):
        """곱셈 테스트: 음수 (-5 * -3 = 15)"""
        assert Arithmetic.multiply(-5, -3) == 15
    
    def test_multiplication_with_zero(self):
        """곱셈 테스트: 0 포함 (0 * 10 = 0)"""
        assert Arithmetic.multiply(0, 10) == 0
    
    def test_division_integer(self):
        """정수 나눗셈 테스트 (5 / 2 = 2)"""
        assert Arithmetic.divide(5, 2) == 2
    
    def test_division_quotient(self):
        """소수점 나눗셈 테스트 (5 ÷ 2 = 2.5)"""
        assert Arithmetic.quotient(5, 2) == 2.5
    
    def test_division_negative(self):
        """나눗셈 테스트: 음수 (-10 / 2 = -5)"""
        assert Arithmetic.divide(-10, 2) == -5
    
    def test_division_by_zero(self):
        """예외 처리 테스트: 0으로 나누기 (0 / 0 = ArithmeticException)"""
        with pytest.raises(ArithmeticError):
            Arithmetic.divide(0, 0)

