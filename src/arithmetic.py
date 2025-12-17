class Arithmetic:
    """사칙연산 클래스"""
    
    @staticmethod
    def add(a, b):
        """덧셈 연산"""
        return a + b
    
    @staticmethod
    def subtract(a, b):
        """뺄셈 연산"""
        return a - b
    
    @staticmethod
    def multiply(a, b):
        """곱셈 연산"""
        return a * b
    
    @staticmethod
    def divide(a, b):
        """정수 나눗셈 연산"""
        if b == 0:
            raise ArithmeticError("Division by zero")
        return a // b
    
    @staticmethod
    def quotient(a, b):
        """소수점 나눗셈 연산"""
        return a / b


if __name__ == "__main__":
    """직접 실행 시 테스트 케이스 실행 및 예제 출력"""
    import sys
    import os
    
    # 프로젝트 루트를 경로에 추가
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    print("=" * 60)
    print("Arithmetic 클래스 테스트 실행")
    print("=" * 60)
    print()
    
    # 테스트 케이스 실행
    try:
        import pytest
        print("pytest를 사용하여 테스트 실행 중...")
        print()
        exit_code = pytest.main(["-v", "tests/test_arithmetic.py"])
        print()
        if exit_code == 0:
            print("=" * 60)
            print("✅ 모든 테스트 통과!")
            print("=" * 60)
        else:
            print("=" * 60)
            print("❌ 일부 테스트 실패")
            print("=" * 60)
    except ImportError:
        print("⚠️  pytest가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install pytest")
        print()
        print("대신 간단한 예제를 실행합니다:")
        print("-" * 60)
        
        # pytest가 없을 경우 간단한 예제 실행
        print("\n[덧셈 테스트]")
        print(f"  Arithmetic.add(1, 10) = {Arithmetic.add(1, 10)}")
        print(f"  Arithmetic.add(0, 1) = {Arithmetic.add(0, 1)}")
        print(f"  Arithmetic.add(-1, -10) = {Arithmetic.add(-1, -10)}")
        
        print("\n[뺄셈 테스트]")
        print(f"  Arithmetic.subtract(5, 2) = {Arithmetic.subtract(5, 2)}")
        
        print("\n[곱셈 테스트]")
        print(f"  Arithmetic.multiply(-5, -3) = {Arithmetic.multiply(-5, -3)}")
        print(f"  Arithmetic.multiply(0, 10) = {Arithmetic.multiply(0, 10)}")
        
        print("\n[나눗셈 테스트]")
        print(f"  Arithmetic.divide(5, 2) = {Arithmetic.divide(5, 2)}")
        print(f"  Arithmetic.divide(-10, 2) = {Arithmetic.divide(-10, 2)}")
        print(f"  Arithmetic.quotient(5, 2) = {Arithmetic.quotient(5, 2)}")
        
        print("\n[예외 처리 테스트]")
        try:
            Arithmetic.divide(0, 0)
            print("  ❌ 예외가 발생하지 않았습니다!")
        except ArithmeticError as e:
            print(f"  ✅ ArithmeticError 발생: {e}")
        
        print()
        print("=" * 60)
        print("예제 실행 완료")
        print("=" * 60)

