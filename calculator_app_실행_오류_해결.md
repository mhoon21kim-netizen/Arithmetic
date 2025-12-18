# calculator_app.py 실행 오류 해결 가이드

## 문제 상황

```
python calculator_app.py
# 오류: can't open file 'calculator_app.py': [Errno 2] No such file or directory
```

## 문제 원인

1. **파일 위치 불일치**
   - 실제 파일 위치: `src/calculator_app.py`
   - 실행 시도 위치: 프로젝트 루트 (`Arithmetic/`)
   - Python은 현재 디렉토리에서 파일을 찾으므로 파일을 찾을 수 없음

2. **프로젝트 구조**
   ```
   Arithmetic/
   ├── calculator_app.py  ❌ (존재하지 않음)
   └── src/
       └── calculator_app.py  ✅ (실제 위치)
   ```

## 해결 방법

### 방법 1: 올바른 경로로 실행 (즉시 해결)

```powershell
# 프로젝트 루트에서
python src/calculator_app.py
```

또는

```powershell
# 모듈로 실행
python -m src.calculator_app
```

### 방법 2: 실행 스크립트 생성 (권장)

프로젝트 루트에 실행 스크립트를 생성하여 편리하게 실행할 수 있도록 합니다.

**장점**:
- 사용자가 쉽게 실행 가능
- 프로젝트 구조 변경 시에도 유연함
- 표준적인 Python 프로젝트 구조

### 방법 3: PATH 설정 (선택사항)

환경 변수나 스크립트를 통해 경로를 자동으로 설정할 수 있습니다.

---

## 권장 해결 방법: 실행 스크립트 생성

프로젝트 루트에 `run_calculator.py` 또는 `calculator.py` 파일을 생성하여 
사용자가 쉽게 실행할 수 있도록 하는 것이 가장 좋은 방법입니다.

