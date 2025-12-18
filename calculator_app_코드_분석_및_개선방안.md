# calculator_app.py 코드 분석 및 개선 방안

## 1단계: 코드 스멜 분석

### 1.1 발견된 코드 스멜

#### 1. Long Method (긴 메서드)
- **위치**: `setup_ui()` 메서드 (44-158줄, 약 115줄)
- **문제점**: 
  - 단일 메서드가 너무 많은 책임을 가짐
  - 윈도우 생성, 디스플레이 설정, 버튼 생성, 레이아웃 배치를 모두 처리
  - 가독성 저하 및 유지보수 어려움
- **영향**: SRP 위반

#### 2. Duplicate Code (중복 코드)
- **위치**: 
  - 이벤트 핸들러 메서드들 (`on_number_clicked`, `on_operator_clicked`, `on_equals_clicked` 등)
  - 스타일시트 정의 (각 버튼 타입별로 유사한 스타일 반복)
- **문제점**:
  - 이벤트 핸들러들이 동일한 패턴 반복 (try-except, display 업데이트)
  - 스타일시트가 거의 동일한 구조 반복
- **영향**: DRY 원칙 위반, 유지보수 비용 증가

#### 3. Magic Strings (매직 문자열)
- **위치**: 
  - 버튼 타입: `"number"`, `"operator"`, `"equals"`, `"special"`
  - 버튼 텍스트: `"C"`, `"+/-"`, `"="`
  - 스타일시트 색상 코드: `"#ffffff"`, `"#f5f5f5"` 등
- **문제점**:
  - 하드코딩된 문자열로 인한 오타 위험
  - 타입 안정성 부족
  - 변경 시 여러 곳 수정 필요
- **영향**: 유지보수성 저하

#### 4. Feature Envy (기능 질투)
- **위치**: `create_button()` 메서드
- **문제점**:
  - 스타일시트가 메서드 내부에 하드코딩
  - 스타일 관련 로직이 UI 클래스에 혼재
- **영향**: 응집도 저하

#### 5. Primitive Obsession (원시 타입 집착)
- **위치**: 버튼 타입을 문자열로 처리
- **문제점**:
  - 버튼 타입을 문자열로 표현하여 타입 안정성 부족
  - Enum이나 상수 클래스 사용 권장
- **영향**: 타입 안정성 부족

#### 6. Dead Code (사용하지 않는 코드)
- **위치**: `import os` (7줄)
- **문제점**: 사용하지 않는 import
- **영향**: 코드 품질 저하

#### 7. Long Parameter List (긴 매개변수 리스트)
- **위치**: 버튼 정의 튜플 `(row, col, rowspan, colspan, text, button_type)`
- **문제점**: 6개의 매개변수로 가독성 저하
- **영향**: 가독성 저하

---

## 2단계: 정적 분석

### 2.1 순환 복잡도 (Cyclomatic Complexity)

#### 높은 복잡도 메서드
1. **`setup_ui()`**: 복잡도 약 8-10
   - 여러 if-elif 분기 (버튼 타입별 처리)
   - 중첩된 로직

2. **`create_button()`**: 복잡도 4
   - 4개의 if-elif 분기 (버튼 타입별 스타일)

3. **`connect_button()`**: 복잡도 5
   - 4개의 if-elif 분기 + 중첩된 if

### 2.2 결합도 (Coupling)

#### 높은 결합도
- **PyQt6 위젯에 강하게 결합**: `QPushButton`, `QLineEdit`, `QGridLayout` 등
- **CalculatorEngine에 의존**: 하지만 인터페이스가 아닌 구체 클래스에 의존
- **스타일시트 하드코딩**: 스타일 변경 시 코드 수정 필요

### 2.3 응집도 (Cohesion)

#### 낮은 응집도
- **UI 구성과 스타일이 혼재**: `setup_ui()`에서 레이아웃과 스타일을 모두 처리
- **이벤트 핸들링 로직 분산**: 각 핸들러가 독립적으로 존재하지만 공통 패턴 반복

### 2.4 코드 메트릭

| 메트릭 | 값 | 평가 |
|--------|-----|------|
| 파일 크기 | 393줄 | 보통 |
| 클래스 수 | 1 | 단일 클래스 |
| 메서드 수 | 9 | 적절 |
| 평균 메서드 길이 | ~40줄 | 다소 김 |
| 최대 메서드 길이 | 115줄 | 너무 김 |
| 순환 복잡도 | 8-10 | 높음 |

---

## 3단계: SOLID 원칙 분석

### 3.1 SRP (Single Responsibility Principle) - 단일 책임 원칙

#### 위반 사항
1. **`CalculatorApp` 클래스가 너무 많은 책임**
   - UI 렌더링
   - 이벤트 핸들링
   - 스타일 관리
   - 레이아웃 구성
   - 에러 처리

2. **`setup_ui()` 메서드가 너무 많은 일을 수행**
   - 윈도우 설정
   - 디스플레이 생성
   - 버튼 생성 및 배치
   - 이벤트 연결

#### 개선 방안
- UI 구성, 스타일 관리, 이벤트 핸들링을 별도 클래스로 분리
- Factory 패턴으로 버튼 생성 분리
- Strategy 패턴으로 스타일 관리 분리

### 3.2 OCP (Open/Closed Principle) - 개방/폐쇄 원칙

#### 위반 사항
1. **새로운 버튼 타입 추가 시 `create_button()` 수정 필요**
   - if-elif 체인으로 버튼 타입 처리
   - 새로운 타입 추가 시 코드 수정 필요

2. **스타일 변경 시 코드 수정 필요**
   - 스타일시트가 메서드 내부에 하드코딩

#### 개선 방안
- Strategy 패턴으로 버튼 스타일 관리
- Factory 패턴으로 버튼 생성
- 설정 파일로 스타일 분리

### 3.3 LSP (Liskov Substitution Principle) - 리스코프 치환 원칙

#### 준수 상태
- ✅ 현재 상속 관계가 없어 해당 없음

### 3.4 ISP (Interface Segregation Principle) - 인터페이스 분리 원칙

#### 준수 상태
- ✅ 현재 인터페이스가 없어 해당 없음

### 3.5 DIP (Dependency Inversion Principle) - 의존성 역전 원칙

#### 위반 사항
1. **구체 클래스에 직접 의존**
   - `CalculatorEngine` 구체 클래스에 직접 의존
   - 인터페이스나 추상 클래스 부재

2. **PyQt6 위젯에 직접 의존**
   - `QPushButton`, `QLineEdit` 등 구체 위젯에 직접 의존

#### 개선 방안
- `CalculatorEngine`에 대한 인터페이스 정의
- 위젯 팩토리 패턴 적용

---

## 4단계: 개선 방안 (단계별)

### 4.1 단계 1: 상수 및 Enum 정의

**목표**: Magic String 제거, 타입 안정성 향상

**구현 내용**:
```python
from enum import Enum

class ButtonType(Enum):
    NUMBER = "number"
    OPERATOR = "operator"
    EQUALS = "equals"
    SPECIAL = "special"

class ButtonConfig:
    """버튼 설정 상수"""
    FONT_FAMILY = "Arial"
    FONT_SIZE_DISPLAY = 20
    FONT_SIZE_BUTTON = 16
    BUTTON_HEIGHT = 60
    LAYOUT_SPACING = 5
    
    # 색상 상수
    COLOR_NUMBER_BG = "#ffffff"
    COLOR_OPERATOR_BG = "#f5f5f5"
    COLOR_EQUALS_BG = "#4A90E2"
    COLOR_SPECIAL_BG = "#f9f9f9"
```

**효과**:
- Magic String 제거
- 타입 안정성 향상
- 중앙 집중식 상수 관리

### 4.2 단계 2: 스타일 관리 분리

**목표**: 스타일시트 로직을 별도 클래스로 분리

**구현 내용**:
```python
class ButtonStyleManager:
    """버튼 스타일 관리 클래스"""
    
    @staticmethod
    def get_style(button_type: ButtonType) -> str:
        """버튼 타입에 따른 스타일 반환"""
        styles = {
            ButtonType.NUMBER: ButtonStyleManager._number_style(),
            ButtonType.OPERATOR: ButtonStyleManager._operator_style(),
            ButtonType.EQUALS: ButtonStyleManager._equals_style(),
            ButtonType.SPECIAL: ButtonStyleManager._special_style(),
        }
        return styles.get(button_type, "")
    
    @staticmethod
    def _number_style() -> str:
        return f"""
            QPushButton {{
                background-color: {ButtonConfig.COLOR_NUMBER_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}
        """
    # ... 기타 스타일 메서드
```

**효과**:
- Feature Envy 해결
- 스타일 관리 중앙화
- OCP 준수 (새 스타일 추가 용이)

### 4.3 단계 3: 버튼 팩토리 패턴 적용

**목표**: 버튼 생성 로직 분리, OCP 준수

**구현 내용**:
```python
class ButtonFactory:
    """버튼 생성 팩토리"""
    
    @staticmethod
    def create_button(text: str, button_type: ButtonType) -> QPushButton:
        """버튼 생성 및 스타일 적용"""
        button = QPushButton(text)
        button.setFont(QFont(ButtonConfig.FONT_FAMILY, ButtonConfig.FONT_SIZE_BUTTON))
        button.setMinimumHeight(ButtonConfig.BUTTON_HEIGHT)
        button.setStyleSheet(ButtonStyleManager.get_style(button_type))
        return button
```

**효과**:
- 버튼 생성 로직 분리
- SRP 준수
- 재사용성 향상

### 4.4 단계 4: 레이아웃 구성 분리

**목표**: `setup_ui()` 메서드 분해

**구현 내용**:
```python
class CalculatorApp(QMainWindow):
    def setup_ui(self):
        """UI 구성 요소 설정"""
        self._setup_window()
        self._setup_display()
        self._setup_button_grid()
    
    def _setup_window(self):
        """윈도우 기본 설정"""
        self.setWindowTitle("계산기")
        self.setFixedSize(300, 400)
        # ...
    
    def _setup_display(self):
        """디스플레이 영역 설정"""
        # ...
    
    def _setup_button_grid(self):
        """버튼 그리드 설정"""
        # ...
```

**효과**:
- Long Method 해결
- 메서드 책임 명확화
- 가독성 향상

### 4.5 단계 5: 이벤트 핸들러 통합

**목표**: 중복 코드 제거, 공통 패턴 추출

**구현 내용**:
```python
class CalculatorApp(QMainWindow):
    def _handle_button_click(self, action: Callable[[], str]):
        """공통 버튼 클릭 핸들러"""
        try:
            display = action()
            self.display.setText(display)
        except ArithmeticError as e:
            self.display.setText("Error: 0으로 나눌 수 없습니다")
            print(f"오류 발생: {e}")
        except Exception as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_number_clicked(self, number: str):
        """숫자 버튼 클릭 핸들러"""
        self._handle_button_click(lambda: self.engine.input_number(number))
    
    def on_operator_clicked(self, operator: str):
        """연산자 버튼 클릭 핸들러"""
        self._handle_button_click(lambda: self.engine.input_operator(operator))
```

**효과**:
- Duplicate Code 제거
- 에러 처리 중앙화
- 유지보수성 향상

### 4.6 단계 6: 버튼 설정 데이터 구조화

**목표**: 버튼 정의를 데이터 구조로 분리

**구현 내용**:
```python
from dataclasses import dataclass

@dataclass
class ButtonDefinition:
    """버튼 정의 데이터 클래스"""
    row: int
    col: int
    rowspan: int
    colspan: int
    text: str
    button_type: ButtonType

class ButtonLayoutConfig:
    """버튼 레이아웃 설정"""
    
    @staticmethod
    def get_button_definitions() -> list[ButtonDefinition]:
        """버튼 정의 리스트 반환"""
        return [
            ButtonDefinition(0, 0, 1, 1, "7", ButtonType.NUMBER),
            ButtonDefinition(0, 1, 1, 1, "8", ButtonType.NUMBER),
            # ...
        ]
```

**효과**:
- Long Parameter List 해결
- 데이터와 로직 분리
- 가독성 향상

### 4.7 단계 7: 인터페이스 정의 (DIP 준수)

**목표**: 의존성 역전 원칙 준수

**구현 내용**:
```python
from abc import ABC, abstractmethod

class ICalculatorEngine(ABC):
    """계산기 엔진 인터페이스"""
    
    @abstractmethod
    def input_number(self, number: str) -> str:
        pass
    
    @abstractmethod
    def input_operator(self, operator: str) -> str:
        pass
    
    @abstractmethod
    def calculate(self) -> str:
        pass
    
    @abstractmethod
    def clear(self) -> str:
        pass
    
    @abstractmethod
    def toggle_sign(self) -> str:
        pass

class CalculatorApp(QMainWindow):
    def __init__(self, engine: ICalculatorEngine = None):
        super().__init__()
        self.engine = engine or CalculatorEngine()  # 의존성 주입
        self.setup_ui()
```

**효과**:
- DIP 준수
- 테스트 용이성 향상
- 결합도 감소

---

## 5단계: 개선 우선순위

### 우선순위 1 (즉시 개선)
1. ✅ **Dead Code 제거**: `import os` 제거
2. ✅ **상수 정의**: Magic String을 상수로 변환
3. ✅ **메서드 분해**: `setup_ui()` 메서드 분리

### 우선순위 2 (단기 개선)
4. ✅ **스타일 관리 분리**: `ButtonStyleManager` 클래스 생성
5. ✅ **버튼 팩토리**: `ButtonFactory` 클래스 생성
6. ✅ **이벤트 핸들러 통합**: 공통 핸들러 메서드 생성

### 우선순위 3 (중기 개선)
7. ✅ **데이터 구조화**: `ButtonDefinition` 데이터 클래스
8. ✅ **인터페이스 정의**: `ICalculatorEngine` 인터페이스
9. ✅ **설정 파일 분리**: 스타일을 외부 파일로 분리

---

## 6단계: 개선 효과 예상

### 코드 품질 지표 개선

| 지표 | 개선 전 | 개선 후 | 개선율 |
|------|---------|---------|--------|
| 최대 메서드 길이 | 115줄 | ~30줄 | 74% 감소 |
| 순환 복잡도 | 8-10 | 3-4 | 60% 감소 |
| 중복 코드 | 높음 | 낮음 | 80% 감소 |
| Magic String | 15+ | 0 | 100% 제거 |
| 결합도 | 높음 | 낮음 | 50% 감소 |

### SOLID 원칙 준수도

| 원칙 | 개선 전 | 개선 후 |
|------|---------|---------|
| SRP | ⚠️ 부분 위반 | ✅ 준수 |
| OCP | ⚠️ 위반 | ✅ 준수 |
| LSP | ✅ 해당 없음 | ✅ 해당 없음 |
| ISP | ✅ 해당 없음 | ✅ 해당 없음 |
| DIP | ⚠️ 위반 | ✅ 준수 |

---

## 7단계: 구현 체크리스트

### 단계별 구현 체크리스트

- [ ] **1단계**: 상수 및 Enum 정의
  - [ ] `ButtonType` Enum 생성
  - [ ] `ButtonConfig` 클래스 생성
  - [ ] Magic String 제거

- [ ] **2단계**: 스타일 관리 분리
  - [ ] `ButtonStyleManager` 클래스 생성
  - [ ] 스타일시트 메서드 분리
  - [ ] `create_button()` 메서드 리팩토링

- [ ] **3단계**: 버튼 팩토리 패턴
  - [ ] `ButtonFactory` 클래스 생성
  - [ ] 버튼 생성 로직 이동

- [ ] **4단계**: 레이아웃 구성 분리
  - [ ] `_setup_window()` 메서드 생성
  - [ ] `_setup_display()` 메서드 생성
  - [ ] `_setup_button_grid()` 메서드 생성

- [ ] **5단계**: 이벤트 핸들러 통합
  - [ ] `_handle_button_click()` 메서드 생성
  - [ ] 이벤트 핸들러 리팩토링

- [ ] **6단계**: 데이터 구조화
  - [ ] `ButtonDefinition` 데이터 클래스 생성
  - [ ] `ButtonLayoutConfig` 클래스 생성

- [ ] **7단계**: 인터페이스 정의
  - [ ] `ICalculatorEngine` 인터페이스 생성
  - [ ] 의존성 주입 개선

---

## 결론

현재 `calculator_app.py`는 기능적으로는 잘 작동하지만, 여러 코드 스멜과 SOLID 원칙 위반 사항이 있습니다. 
단계적으로 개선하면 코드 품질, 유지보수성, 확장성을 크게 향상시킬 수 있습니다.

**주요 개선 포인트**:
1. Long Method 분해
2. Duplicate Code 제거
3. Magic String 제거
4. 스타일 관리 분리
5. 인터페이스 정의로 DIP 준수

이러한 개선을 통해 더 깔끔하고 유지보수하기 쉬운 코드가 됩니다.

