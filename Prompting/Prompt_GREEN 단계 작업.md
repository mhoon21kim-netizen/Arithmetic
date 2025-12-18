# 테스트 케이스 작업 내용 요구사항
_Exported on 12/17/2025 at 15:03:46 GMT+9 from Cursor (2.1.50)_

---

**User**

@Report/테스트_케이스_작업_내용.md 을 분석해서 구현해야 할 기능을 기능/비기능 항목으로 구분해서 목록을 알려줘.

---

**Cursor**

테스트 케이스 보고서를 분석해 기능/비기능 요구사항을 정리 중입니다.


테스트 케이스 보고서를 분석해 기능/비기능 요구사항을 정리했습니다.

## 구현 요구사항 분석 결과

### 기능 요구사항 (Functional Requirements)

#### 1. 덧셈 연산 (`add` 메서드)
- 양수 간 덧셈: `1 + 10 = 11`
- 0 포함 덧셈: `0 + 1 = 1`
- 음수 간 덧셈: `-1 + (-10) = -11`

#### 2. 뺄셈 연산 (`subtract` 메서드)
- 기본 뺄셈: `5 - 2 = 3`

#### 3. 곱셈 연산 (`multiply` 메서드)
- 음수 간 곱셈: `-5 × -3 = 15`
- 0 포함 곱셈: `0 × 10 = 0`

#### 4. 정수 나눗셈 연산 (`divide` 메서드)
- 정수 나눗셈: `5 ÷ 2 = 2` (소수점 버림)
- 음수 포함 나눗셈: `-10 ÷ 2 = -5`
- 0으로 나누기 예외 처리: `0 ÷ 0` → `ArithmeticError` 발생

#### 5. 소수점 나눗셈 연산 (`quotient` 메서드)
- 소수점 포함 나눗셈: `5 ÷ 2 = 2.5` (정확한 소수점 반환)

---

### 비기능 요구사항 (Non-Functional Requirements)

#### 1. 구조적 제약
- 클래스 기반 설계: `Arithmetic` 클래스로 구현
- 정적 메서드 사용: 모든 메서드는 `@staticmethod` 데코레이터 사용
- 파일 위치: `src/arithmetic.py`에 구현
- 모듈 구조: `src` 패키지 내에 위치

#### 2. 예외 처리 규칙
- 예외 타입: 0으로 나누기 시 `ArithmeticError` 예외 발생
- 예외 처리 범위: `divide` 메서드에서 0으로 나누는 경우 처리

#### 3. 반환값 타입 규칙
- 정수 나눗셈: `divide` 메서드는 정수 반환 (소수점 버림)
- 소수점 나눗셈: `quotient` 메서드는 부동소수점 반환

#### 4. 테스트 호환성
- pytest 프레임워크와 호환
- `from src.arithmetic import Arithmetic` 형태로 import 가능해야 함

#### 5. 코드 품질
- 독립적인 메서드: 각 메서드는 독립적으로 동작
- 명확한 메서드명: 기능을 명확히 표현하는 이름 사용

---

### 구현 우선순위

| 우선순위 | 메서드 | 테스트 ID | 중요도 |
|---------|--------|----------|--------|
| 1 | `add()` | TC-001, TC-002, TC-003 | 중요 |
| 2 | `subtract()` | TC-004 | 중요 |
| 3 | `multiply()` | TC-005, TC-006 | 보통/낮음 |
| 4 | `divide()` | TC-007, TC-009, TC-010 | 중요 |
| 5 | `quotient()` | TC-008 | 보통 |

---

### 요약

- 기능 요구사항: 5개 메서드, 10개 테스트 케이스
- 비기능 요구사항: 구조, 예외 처리, 타입 규칙, 호환성

총 10개의 테스트 케이스를 모두 통과하도록 구현해야 합니다.

---

**User**

구현 우선순위를 README.md 파일에 GREEN 단계에서 해야할 목록을 추가해줘.

---

**Cursor**

README.md를 확인하고 GREEN 단계 작업 목록을 추가합니다.


README.md에 GREEN 단계 작업 목록을 추가합니다.


```markdown
# Arithmetic Operations Test Project

## 프로젝트 개요

사칙연산(덧셈, 뺄셈, 곱셈, 나눗셈)의 정확도를 검증하는 테스트 프로젝트입니다.
TDD(Test-Driven Development)의 RED-GREEN-REFACTOR 사이클을 따라 개발합니다.

## 프로젝트 정보

- **프로젝트명**: 인사관리 앱 시스템 구축 (사칙연산 모듈)
- **테스트 ID**: TC-CMM-001 (Common Module) / TC-AO-001 (Arithmetic Operations)
- **작성자**: 홍길동
- **승인자**: 박문수
- **작성일**: 2020-09-01
- **버전**: v1.0
- **테스트 범위**: 공통 모듈

## 테스트 환경

- **언어**: Python
- **IDE**: PyCharm
- **운영 체제**: Windows 10
- **테스트 프레임워크**: pytest (권장)

## 테스트 목적

사칙연산 기능의 정확도와 예외 처리를 검증하여 안정적인 수학 연산 모듈을 구축합니다.

## 테스트 케이스

### 기본 연산 테스트

| 테스트 케이스 | 입력값 | 예상값 | 중요도 | 상태 |
|------------|--------|--------|--------|------|
| 덧셈 (양수) | 1 + 10 | 11 | 중요 | 성공 |
| 덧셈 (0 포함) | 0 + 1 | 1 | 중요 | 성공 |
| 덧셈 (음수) | -1 + (-10) | -11 | 보통 | 성공 |
| 뺄셈 | 5 - 2 | 3 | 중요 | 성공 |
| 곱셈 (음수) | -5 * -3 | 15 | 보통 | 성공 |
| 곱셈 (0 포함) | 0 * 10 | 0 | 낮음 | 성공 |
| 정수 나눗셈 | 5 / 2 | 2 | 중요 | 성공 |
| 소수점 나눗셈 | 5 ÷ 2 (quotient) | 2.5 | 보통 | 성공 |
| 나눗셈 (음수) | -10 / 2 | -5 | 중요 | 성공 |

### 예외 처리 테스트

| 테스트 케이스 | 입력값 | 예상값 | 중요도 | 상태 |
|------------|--------|--------|--------|------|
| 0으로 나누기 | 0 / 0 | ArithmeticException | 중요 | 성공 |

## 전제 조건

1. 프로그램은 오류 없이 성공적으로 컴파일되어야 합니다.
2. 모든 종속성을 올바르게 설치하고 구성해야 합니다.
3. Python 3.7 이상이 설치되어 있어야 합니다.

## 설치 방법

```bash
# 프로젝트 디렉토리로 이동
cd Arithmetic

# 가상 환경 생성 (선택사항)
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 의존성 설치
pip install pytest
```

## 프로젝트 구조

```
Arithmetic/
├── README.md
├── requirements.txt
├── src/
│   └── arithmetic.py      # 사칙연산 모듈
└── tests/
    └── test_arithmetic.py # 테스트 케이스
```

## TDD 개발 방식

이 프로젝트는 **RED-GREEN-REFACTOR** 사이클을 따릅니다:

1. **RED**: 실패하는 테스트를 먼저 작성 ✅ (완료)
2. **GREEN**: 테스트를 통과하는 최소한의 코드 작성 ⏳ (진행 중)
3. **REFACTOR**: 코드를 개선하고 최적화 ⏳ (예정)

## GREEN 단계 작업 목록

### 구현 파일 생성
- [ ] `src/arithmetic.py` 파일 생성
- [ ] `Arithmetic` 클래스 구현

### 메서드 구현 (우선순위 순)

#### 우선순위 1: `add()` 메서드 구현
- [ ] 양수 간 덧셈: `1 + 10 = 11` (TC-001)
- [ ] 0 포함 덧셈: `0 + 1 = 1` (TC-002)
- [ ] 음수 간 덧셈: `-1 + (-10) = -11` (TC-003)
- [ ] 테스트 실행 및 통과 확인

#### 우선순위 2: `subtract()` 메서드 구현
- [ ] 기본 뺄셈: `5 - 2 = 3` (TC-004)
- [ ] 테스트 실행 및 통과 확인

#### 우선순위 3: `multiply()` 메서드 구현
- [ ] 음수 간 곱셈: `-5 × -3 = 15` (TC-005)
- [ ] 0 포함 곱셈: `0 × 10 = 0` (TC-006)
- [ ] 테스트 실행 및 통과 확인

#### 우선순위 4: `divide()` 메서드 구현
- [ ] 정수 나눗셈: `5 ÷ 2 = 2` (소수점 버림) (TC-007)
- [ ] 음수 포함 나눗셈: `-10 ÷ 2 = -5` (TC-009)
- [ ] 0으로 나누기 예외 처리: `0 ÷ 0` → `ArithmeticError` 발생 (TC-010)
- [ ] 테스트 실행 및 통과 확인

#### 우선순위 5: `quotient()` 메서드 구현
- [ ] 소수점 나눗셈: `5 ÷ 2 = 2.5` (TC-008)
- [ ] 테스트 실행 및 통과 확인

### 최종 확인
- [ ] 모든 테스트 케이스 통과 확인 (10개)
- [ ] 테스트 커버리지 100% 확인

## 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 상세 출력과 함께 실행
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_arithmetic.py
```

## 성공/실패 기준

- **성공**: 모든 테스트 사례가 예상한 결과를 생성합니다.
- **실패**: 테스트 케이스가 예상한 결과를 생성하지 않습니다.

## 특별 절차

1. 테스트 결과를 기록하고 이에 따라 테스트 사례 문서를 업데이트합니다.
2. 즉각적인 해결을 위해 모든 실패를 개발팀에 전달하세요.

## 라이선스

이 프로젝트는 내부 테스트 목적으로 사용됩니다.

## RED 브랜치 추가
RED 브랜치 추가하고 PR 요청함니다.



```

README.md에 GREEN 단계 작업 목록을 추가했습니다.

추가된 내용:
1. **TDD 개발 방식 섹션 업데이트**: 각 단계의 현재 상태 표시 (RED 완료, GREEN 진행 중, REFACTOR 예정)
2. **GREEN 단계 작업 목록 섹션 추가**:
   - 구현 파일 생성 체크리스트
   - 우선순위별 메서드 구현 체크리스트 (1~5)
   - 각 메서드별 테스트 케이스와 예상 결과 포함
   - 최종 확인 항목

각 작업 항목은 체크박스로 표시되어 진행 상황을 추적할 수 있습니다. 테스트 케이스 보고서의 구현 우선순위를 반영했습니다.

---

**User**

@README.md 내용 중  @README.md (104-131) 를 최소단위로 구현할려고 하는데 먼저 시나리오를 작성해서 보여주고 승인 받은 후 구현해줘.

---

**Cursor**

GREEN 단계 최소 단위 구현 시나리오 작성 중. 승인 후 구현 진행.


최소 단위 구현 시나리오 작성 중.


```markdown
# GREEN 단계 최소 단위 구현 시나리오

## 목표
TDD의 GREEN 단계 원칙에 따라 최소한의 코드로 모든 테스트를 통과시키기

## 현재 상태
- ✅ RED 단계 완료: 테스트 케이스 10개 작성 완료
- ❌ 구현 코드 없음: `src/arithmetic.py` 파일 미존재
- ❌ 모든 테스트 실패: `ModuleNotFoundError: No module named 'src.arithmetic'`

## 구현 전략
**최소 단위 구현 원칙**: 각 단계마다 최소한의 코드만 작성하여 해당 테스트만 통과시키기

---

## 단계별 구현 시나리오

### Phase 1: 기본 구조 생성 (1단계)

**목표**: 모듈을 찾을 수 있도록 기본 구조만 생성

1. **파일 생성**
   - `src/arithmetic.py` 파일 생성
   - `Arithmetic` 클래스 선언만 추가 (메서드 없음)

2. **예상 결과**
   - `ModuleNotFoundError` 해결
   - 모든 테스트에서 `AttributeError: type object 'Arithmetic' has no attribute 'add'` 발생

3. **검증**
   ```bash
   pytest tests/test_arithmetic.py -v
   ```

---

### Phase 2: 우선순위 1 - `add()` 메서드 구현 (2단계)

**목표**: 덧셈 관련 테스트 3개 통과

#### 2-1. 최소 구현: 첫 번째 테스트 통과
1. **구현**
   - `add()` 정적 메서드 추가
   - 최소 구현: `return a + b` (양수 테스트 통과)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_positive_numbers -v
   ```

3. **예상 결과**
   - ✅ TC-001 통과
   - ❌ TC-002, TC-003도 통과 (덧셈은 기본 연산이므로)

#### 2-2. 검증: 모든 덧셈 테스트 통과 확인
1. **전체 덧셈 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_positive_numbers -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_with_zero -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_negative_numbers -v
   ```

2. **예상 결과**
   - ✅ TC-001, TC-002, TC-003 모두 통과
   - 덧셈은 기본 연산이므로 추가 로직 불필요

---

### Phase 3: 우선순위 2 - `subtract()` 메서드 구현 (3단계)

**목표**: 뺄셈 테스트 1개 통과

1. **구현**
   - `subtract()` 정적 메서드 추가
   - 최소 구현: `return a - b`

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_subtraction -v
   ```

3. **예상 결과**
   - ✅ TC-004 통과

---

### Phase 4: 우선순위 3 - `multiply()` 메서드 구현 (4단계)

**목표**: 곱셈 테스트 2개 통과

1. **구현**
   - `multiply()` 정적 메서드 추가
   - 최소 구현: `return a * b`

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_multiplication_negative_numbers -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_multiplication_with_zero -v
   ```

3. **예상 결과**
   - ✅ TC-005, TC-006 모두 통과
   - 곱셈은 기본 연산이므로 추가 로직 불필요

---

### Phase 5: 우선순위 4 - `divide()` 메서드 구현 (5단계)

**목표**: 정수 나눗셈 테스트 3개 통과 (TC-007, TC-009, TC-010)

#### 5-1. 최소 구현: 정수 나눗셈 기본 로직
1. **구현**
   - `divide()` 정적 메서드 추가
   - 최소 구현: `return a // b` (정수 나눗셈 연산자 사용)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_integer -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_negative -v
   ```

3. **예상 결과**
   - ✅ TC-007 통과 (5 // 2 = 2)
   - ✅ TC-009 통과 (-10 // 2 = -5)
   - ❌ TC-010 실패 (0 // 0는 ZeroDivisionError 발생, ArithmeticError 필요)

#### 5-2. 예외 처리 추가: 0으로 나누기
1. **구현 수정**
   - `divide()` 메서드에 예외 처리 추가
   - `if b == 0: raise ArithmeticError()` 추가

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_by_zero -v
   ```

3. **예상 결과**
   - ✅ TC-010 통과 (ArithmeticError 발생)

#### 5-3. 전체 divide 테스트 확인
1. **전체 divide 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_integer -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_negative -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_by_zero -v
   ```

2. **예상 결과**
   - ✅ TC-007, TC-009, TC-010 모두 통과

---

### Phase 6: 우선순위 5 - `quotient()` 메서드 구현 (6단계)

**목표**: 소수점 나눗셈 테스트 1개 통과

1. **구현**
   - `quotient()` 정적 메서드 추가
   - 최소 구현: `return a / b` (일반 나눗셈 연산자 사용)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_quotient -v
   ```

3. **예상 결과**
   - ✅ TC-008 통과 (5 / 2 = 2.5)

---

### Phase 7: 최종 검증 (7단계)

**목표**: 모든 테스트 통과 확인

1. **전체 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py -v
   ```

2. **예상 결과**
   - ✅ 모든 테스트 통과 (10개)
   - ✅ 테스트 커버리지 100%

3. **README.md 체크리스트 업데이트**
   - 각 단계 완료 시 체크박스 체크

---

## 구현 코드 예상 구조

```python
# src/arithmetic.py

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
```

---

## 구현 순서 요약

| 단계 | 작업 | 테스트 ID | 예상 시간 |
|------|------|----------|----------|
| 1 | 기본 구조 생성 | - | 1분 |
| 2 | `add()` 메서드 | TC-001, TC-002, TC-003 | 2분 |
| 3 | `subtract()` 메서드 | TC-004 | 1분 |
| 4 | `multiply()` 메서드 | TC-005, TC-006 | 1분 |
| 5 | `divide()` 메서드 | TC-007, TC-009, TC-010 | 3분 |
| 6 | `quotient()` 메서드 | TC-008 | 1분 |
| 7 | 최종 검증 | 전체 (10개) | 1분 |

**총 예상 시간**: 약 10분

---

## 검증 기준

### 각 단계별 검증
- ✅ 해당 단계의 테스트가 통과하는가?
- ✅ 이전 단계의 테스트가 여전히 통과하는가? (회귀 테스트)
- ✅ 코드가 최소한으로 구현되었는가?

### 최종 검증
- ✅ 모든 테스트 케이스 통과 (10개)
- ✅ 테스트 커버리지 100%
- ✅ README.md 체크리스트 완료

---

## 주의사항

1. **최소 단위 원칙**: 각 단계에서 최소한의 코드만 작성
2. **점진적 구현**: 한 번에 하나의 기능만 구현
3. **테스트 우선**: 각 구현 후 즉시 테스트 실행
4. **회귀 방지**: 새 기능 추가 시 기존 테스트도 함께 실행

---

**시나리오 작성일**: 2025-12-16  
**승인 대기 중**: 사용자 승인 후 구현 진행

```

GREEN 단계 최소 단위 구현 시나리오를 작성했습니다.

## 시나리오 요약

**7단계 점진적 구현 계획:**

1. **Phase 1**: 기본 구조 생성 (모듈/클래스 선언)
2. **Phase 2**: `add()` 메서드 구현 (TC-001, TC-002, TC-003)
3. **Phase 3**: `subtract()` 메서드 구현 (TC-004)
4. **Phase 4**: `multiply()` 메서드 구현 (TC-005, TC-006)
5. **Phase 5**: `divide()` 메서드 구현 (TC-007, TC-009, TC-010) - 예외 처리 포함
6. **Phase 6**: `quotient()` 메서드 구현 (TC-008)
7. **Phase 7**: 최종 검증 (전체 10개 테스트 통과 확인)

**핵심 원칙:**
- 최소 단위 구현: 각 단계에서 최소한의 코드만 작성
- 점진적 진행: 한 번에 하나의 기능만 구현
- 테스트 우선: 각 구현 후 즉시 테스트 실행
- 예상 소요 시간: 약 10분

시나리오 파일은 `GREEN_단계_구현_시나리오.md`에 저장했습니다.

이 시나리오로 진행할까요? 승인해 주시면 단계별로 구현하겠습니다.

---

**User**

네

---

**Cursor**

시나리오에 따라 단계별로 구현을 진행합니다.


```python
class Arithmetic:
    """사칙연산 클래스"""
    pass

```

Phase 1 완료. Phase 2 진행: `add()` 메서드 구현.


```python
class Arithmetic:
    """사칙연산 클래스"""
    
    @staticmethod
    def add(a, b):
        """덧셈 연산"""
        return a + b


```

TC-001 통과. 나머지 덧셈 테스트 확인 중.


Phase 2 완료: 모든 덧셈 테스트 통과. Phase 3 진행: `subtract()` 메서드 구현.


```python
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


```

Phase 3 완료: TC-004 통과. Phase 4 진행: `multiply()` 메서드 구현.


```python
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


```

Phase 4 완료: TC-005, TC-006 통과. Phase 5 진행: `divide()` 메서드 구현 (예외 처리 포함).


```python
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


```

Phase 5 완료: TC-007, TC-009, TC-010 통과. Phase 6 진행: `quotient()` 메서드 구현.


```python
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


```

Phase 6 완료: TC-008 통과. Phase 7 진행: 최종 검증 (전체 테스트 통과 확인).


모든 테스트 통과. README.md 체크리스트 업데이트 및 최종 코드 확인 중.


README.md 체크리스트 업데이트 중.


```markdown
# Arithmetic Operations Test Project

## 프로젝트 개요

사칙연산(덧셈, 뺄셈, 곱셈, 나눗셈)의 정확도를 검증하는 테스트 프로젝트입니다.
TDD(Test-Driven Development)의 RED-GREEN-REFACTOR 사이클을 따라 개발합니다.

## 프로젝트 정보

- **프로젝트명**: 인사관리 앱 시스템 구축 (사칙연산 모듈)
- **테스트 ID**: TC-CMM-001 (Common Module) / TC-AO-001 (Arithmetic Operations)
- **작성자**: 홍길동
- **승인자**: 박문수
- **작성일**: 2020-09-01
- **버전**: v1.0
- **테스트 범위**: 공통 모듈

## 테스트 환경

- **언어**: Python
- **IDE**: PyCharm
- **운영 체제**: Windows 10
- **테스트 프레임워크**: pytest (권장)

## 테스트 목적

사칙연산 기능의 정확도와 예외 처리를 검증하여 안정적인 수학 연산 모듈을 구축합니다.

## 테스트 케이스

### 기본 연산 테스트

| 테스트 케이스 | 입력값 | 예상값 | 중요도 | 상태 |
|------------|--------|--------|--------|------|
| 덧셈 (양수) | 1 + 10 | 11 | 중요 | 성공 |
| 덧셈 (0 포함) | 0 + 1 | 1 | 중요 | 성공 |
| 덧셈 (음수) | -1 + (-10) | -11 | 보통 | 성공 |
| 뺄셈 | 5 - 2 | 3 | 중요 | 성공 |
| 곱셈 (음수) | -5 * -3 | 15 | 보통 | 성공 |
| 곱셈 (0 포함) | 0 * 10 | 0 | 낮음 | 성공 |
| 정수 나눗셈 | 5 / 2 | 2 | 중요 | 성공 |
| 소수점 나눗셈 | 5 ÷ 2 (quotient) | 2.5 | 보통 | 성공 |
| 나눗셈 (음수) | -10 / 2 | -5 | 중요 | 성공 |

### 예외 처리 테스트

| 테스트 케이스 | 입력값 | 예상값 | 중요도 | 상태 |
|------------|--------|--------|--------|------|
| 0으로 나누기 | 0 / 0 | ArithmeticException | 중요 | 성공 |

## 전제 조건

1. 프로그램은 오류 없이 성공적으로 컴파일되어야 합니다.
2. 모든 종속성을 올바르게 설치하고 구성해야 합니다.
3. Python 3.7 이상이 설치되어 있어야 합니다.

## 설치 방법

```bash
# 프로젝트 디렉토리로 이동
cd Arithmetic

# 가상 환경 생성 (선택사항)
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 의존성 설치
pip install pytest
```

## 프로젝트 구조

```
Arithmetic/
├── README.md
├── requirements.txt
├── src/
│   └── arithmetic.py      # 사칙연산 모듈
└── tests/
    └── test_arithmetic.py # 테스트 케이스
```

## TDD 개발 방식

이 프로젝트는 **RED-GREEN-REFACTOR** 사이클을 따릅니다:

1. **RED**: 실패하는 테스트를 먼저 작성 ✅ (완료)
2. **GREEN**: 테스트를 통과하는 최소한의 코드 작성 ⏳ (진행 중)
3. **REFACTOR**: 코드를 개선하고 최적화 ⏳ (예정)

## GREEN 단계 작업 목록

### 구현 파일 생성
- [x] `src/arithmetic.py` 파일 생성
- [x] `Arithmetic` 클래스 구현

### 메서드 구현 (우선순위 순)

#### 우선순위 1: `add()` 메서드 구현
- [x] 양수 간 덧셈: `1 + 10 = 11` (TC-001)
- [x] 0 포함 덧셈: `0 + 1 = 1` (TC-002)
- [x] 음수 간 덧셈: `-1 + (-10) = -11` (TC-003)
- [x] 테스트 실행 및 통과 확인

#### 우선순위 2: `subtract()` 메서드 구현
- [x] 기본 뺄셈: `5 - 2 = 3` (TC-004)
- [x] 테스트 실행 및 통과 확인

#### 우선순위 3: `multiply()` 메서드 구현
- [x] 음수 간 곱셈: `-5 × -3 = 15` (TC-005)
- [x] 0 포함 곱셈: `0 × 10 = 0` (TC-006)
- [x] 테스트 실행 및 통과 확인

#### 우선순위 4: `divide()` 메서드 구현
- [x] 정수 나눗셈: `5 ÷ 2 = 2` (소수점 버림) (TC-007)
- [x] 음수 포함 나눗셈: `-10 ÷ 2 = -5` (TC-009)
- [x] 0으로 나누기 예외 처리: `0 ÷ 0` → `ArithmeticError` 발생 (TC-010)
- [x] 테스트 실행 및 통과 확인

#### 우선순위 5: `quotient()` 메서드 구현
- [x] 소수점 나눗셈: `5 ÷ 2 = 2.5` (TC-008)
- [x] 테스트 실행 및 통과 확인

### 최종 확인
- [x] 모든 테스트 케이스 통과 확인 (10개)
- [x] 테스트 커버리지 100% 확인

## 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 상세 출력과 함께 실행
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_arithmetic.py
```

## 성공/실패 기준

- **성공**: 모든 테스트 사례가 예상한 결과를 생성합니다.
- **실패**: 테스트 케이스가 예상한 결과를 생성하지 않습니다.

## 특별 절차

1. 테스트 결과를 기록하고 이에 따라 테스트 사례 문서를 업데이트합니다.
2. 즉각적인 해결을 위해 모든 실패를 개발팀에 전달하세요.

## 라이선스

이 프로젝트는 내부 테스트 목적으로 사용됩니다.

## RED 브랜치 추가
RED 브랜치 추가하고 PR 요청함니다.



```

## GREEN 단계 구현 완료

### 구현 결과 요약

**모든 단계 완료:**
- Phase 1: 기본 구조 생성
- Phase 2: `add()` 메서드 구현 (TC-001, TC-002, TC-003)
- Phase 3: `subtract()` 메서드 구현 (TC-004)
- Phase 4: `multiply()` 메서드 구현 (TC-005, TC-006)
- Phase 5: `divide()` 메서드 구현 (TC-007, TC-009, TC-010)
- Phase 6: `quotient()` 메서드 구현 (TC-008)
- Phase 7: 최종 검증

### 최종 테스트 결과

```
============================= 10 passed in 0.02s ==============================
```

- 모든 테스트 케이스 통과: 10/10
- 테스트 커버리지: 100%
- 린터 오류: 없음

### 구현된 코드

`src/arithmetic.py` 파일에 다음 메서드가 구현되었습니다:
- `add()`: 덧셈 연산
- `subtract()`: 뺄셈 연산
- `multiply()`: 곱셈 연산
- `divide()`: 정수 나눗셈 연산 (0으로 나누기 예외 처리 포함)
- `quotient()`: 소수점 나눗셈 연산

### 업데이트된 파일

1. `src/arithmetic.py`: 구현 코드 작성 완료
2. `README.md`: GREEN 단계 체크리스트 모두 완료 표시

**TDD GREEN 단계 완료.** 다음 단계는 REFACTOR입니다.

```plaintext
============================= 10 passed in 0.02s ==============================
```

---

**User**

첨부 파일과 같이 Arithmetic.py 실행했을때 아무것도 안나오는데 실행결과 만들수 있을까?

---

**Cursor**

`arithmetic.py`를 직접 실행해도 출력이 없습니다. `if __name__ == "__main__":` 블록을 추가해 실행 시 결과가 보이도록 수정 중입니다.


실행 시 결과가 보이도록 `if __name__ == "__main__":` 블록을 추가 중입니다. 테스트 케이스를 실행해 결과를 출력합니다.


```python
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


```

실행해 동작 확인 중입니다.


이제 `arithmetic.py`를 직접 실행하면 테스트 결과가 출력됩니다.

## 추가된 기능

1. **pytest가 설치된 경우**: 모든 테스트 케이스를 자동 실행하고 결과를 출력합니다.
2. **pytest가 없는 경우**: 간단한 예제를 실행해 각 메서드의 동작을 보여줍니다.

## 실행 결과

```
============================================================
Arithmetic 클래스 테스트 실행
============================================================

pytest를 사용하여 테스트 실행 중...

... (10개 테스트 모두 통과) ...

============================================================
✅ 모든 테스트 통과!
============================================================
```

이제 `python src/arithmetic.py`를 실행하면 테스트 결과를 확인할 수 있습니다. IDE에서 직접 실행해도 동일한 결과가 표시됩니다.

```plaintext
============================================================
Arithmetic 클래스 테스트 실행
============================================================

pytest를 사용하여 테스트 실행 중...

... (10개 테스트 모두 통과) ...

============================================================
✅ 모든 테스트 통과!
============================================================
```

---

**User**

테스트 결과가 아니라 실행 결과과 나오도록 수정해줘

---

**Cursor**

테스트 실행 대신 예제 실행 결과가 출력되도록 수정 중입니다.


테스트 실행 대신 예제 실행 결과가 출력되도록 수정 중입니다.


```python
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
    """직접 실행 시 예제 실행 결과 출력"""
    print("=" * 60)
    print("Arithmetic 클래스 실행 결과")
    print("=" * 60)
    print()
    
    # 덧셈 예제
    print("[덧셈 연산]")
    print(f"  Arithmetic.add(1, 10) = {Arithmetic.add(1, 10)}")
    print(f"  Arithmetic.add(0, 1) = {Arithmetic.add(0, 1)}")
    print(f"  Arithmetic.add(-1, -10) = {Arithmetic.add(-1, -10)}")
    print()
    
    # 뺄셈 예제
    print("[뺄셈 연산]")
    print(f"  Arithmetic.subtract(5, 2) = {Arithmetic.subtract(5, 2)}")
    print()
    
    # 곱셈 예제
    print("[곱셈 연산]")
    print(f"  Arithmetic.multiply(-5, -3) = {Arithmetic.multiply(-5, -3)}")
    print(f"  Arithmetic.multiply(0, 10) = {Arithmetic.multiply(0, 10)}")
    print()
    
    # 나눗셈 예제
    print("[나눗셈 연산]")
    print(f"  Arithmetic.divide(5, 2) = {Arithmetic.divide(5, 2)}")
    print(f"  Arithmetic.divide(-10, 2) = {Arithmetic.divide(-10, 2)}")
    print(f"  Arithmetic.quotient(5, 2) = {Arithmetic.quotient(5, 2)}")
    print()
    
    # 예외 처리 예제
    print("[예외 처리]")
    try:
        Arithmetic.divide(0, 0)
        print("  ❌ 예외가 발생하지 않았습니다!")
    except ArithmeticError as e:
        print(f"  ✅ ArithmeticError 발생: {e}")
    print()
    
    print("=" * 60)
    print("실행 완료")
    print("=" * 60)


```

실행 결과 확인 중입니다.


---

**User**

첨부한 이미지처럼 입력을 받아 처리하는 콘솔 프로그램으로 만들어줘.

---

**Cursor**

이미지에 맞춰 입력을 받아 처리하는 콘솔 프로그램으로 변경 중입니다.


이미지에 맞춰 사용자 입력을 받아 처리하는 콘솔 프로그램으로 변경 중입니다.


```python
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
    """간단한 사칙연산 콘솔 프로그램"""
    
    # 입력 화면
    print("입력화면")
    try:
        num1 = int(input("첫번째 정수값 >>"))
        operator = input("연산자>>")
        num2 = int(input("두번째 정수값>>"))
    except ValueError:
        print("올바른 정수를 입력해주세요.")
        exit(1)
    
    # 결과 뷰 화면
    print()
    print("결과 뷰 화면")
    print("=" * 30)
    
    # 연산자에 따른 계산 수행
    try:
        if operator == "+":
            result = Arithmetic.add(num1, num2)
            print(f"{num1} + {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}+{num2}={result}입니다.")
        elif operator == "-":
            result = Arithmetic.subtract(num1, num2)
            print(f"{num1} - {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}-{num2}={result}입니다.")
        elif operator == "*":
            result = Arithmetic.multiply(num1, num2)
            print(f"{num1} * {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}*{num2}={result}입니다.")
        elif operator == "/":
            result = Arithmetic.divide(num1, num2)
            print(f"{num1} / {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}/{num2}={result}입니다.")
        elif operator == "//":
            result = Arithmetic.divide(num1, num2)
            print(f"{num1} // {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}//{num2}={result}입니다.")
        elif operator == "÷" or operator == "÷":
            result = Arithmetic.quotient(num1, num2)
            print(f"{num1} ÷ {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}÷{num2}={result}입니다.")
        else:
            print(f"지원하지 않는 연산자입니다: {operator}")
            print("지원하는 연산자: +, -, *, /, //, ÷")
            exit(1)
    except ArithmeticError as e:
        print(f"오류가 발생했습니다: {e}")
        exit(1)


```

