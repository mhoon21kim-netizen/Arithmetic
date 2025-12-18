#!/usr/bin/env python
"""
계산기 애플리케이션 실행 스크립트

프로젝트 루트에서 실행 가능하도록 만든 진입점
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# calculator_app 모듈의 main 함수 실행
from src.calculator_app import main

if __name__ == "__main__":
    main()

