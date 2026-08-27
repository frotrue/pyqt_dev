# 스마트 크랙 탐지기 (Smart Crack Detector) — 최종 UI 버전

**한국어** | [English](README.en.md)

이 저장소는 2025년 AI 해커톤 경진대회 **「경기창고」** 프로젝트 **「스마트 크랙 탐지기」**의 **최종 UI/통합 변경본**을 보관하고 있습니다.

PyQt6 기반 데스크톱 인터페이스에서 건축물 이미지를 불러오거나 카메라로 촬영한 뒤, 학습된 YOLOv8 모델로 손상 부위를 탐지하고, 탐지 결과를 기반으로 OpenAI 모델을 이용한 2차 위험도 분석까지 수행하는 프로토타입입니다.

> **수상:** 2025년 AI 해커톤 경진대회 「경기창고」 우수상  
> **프로젝트명:** 스마트 크랙 탐지기 (Smart Crack Detector)  
> **수여기관:** 차세대융합기술연구원

## 프로젝트 범위

이 저장소는 프로젝트의 **최종 데스크톱 UI와 추론 흐름**에 초점을 두고 있습니다.

현재 애플리케이션에서 다루는 손상 클래스는 다음과 같습니다.

- `crack` — 균열
- `corrosion` — 부식
- `ExposedRebars` — 철근 노출
- `spalling` — 박리

전체 동작 흐름은 다음과 같습니다.

1. 로컬 이미지를 업로드하거나 카메라로 이미지를 촬영합니다.
2. 학습된 YOLOv8 모델(`9_21.pt`)로 추론합니다.
3. 탐지된 손상과 confidence 값을 시각화합니다.
4. 탐지 결과 요약을 GPT 분석 모듈에 전달합니다.
5. 분석 이미지와 결과 텍스트를 저장합니다.
6. 결과 탭에서 이전 분석 결과를 다시 확인할 수 있습니다.

## 주요 UI 기능

### 입력 탭

- 카메라 ON/OFF
- 카메라 촬영
- 로컬 이미지 업로드
- YOLO 추론 실행

### 결과 탭

- 탐지 결과 목록
- 결과 이미지 미리보기
- GPT 기반 위험도 및 조치사항 분석
- 이메일 전송 기능

### 설정 탭

- 모델 경로 선택 UI
- 저장 경로 설정 UI

> 이 프로젝트는 해커톤용 프로토타입입니다. 현재 코드에서는 일부 설정 UI가 모든 추론 경로에 완전히 연결되어 있지 않을 수 있습니다.

## AI 처리 흐름

### YOLO 추론

애플리케이션은 Ultralytics YOLO를 통해 `9_21.pt` 모델을 불러오고, confidence threshold `0.5`를 기준으로 추론합니다.

탐지된 클래스와 confidence 값은 결과 이미지와 함께 저장됩니다.

### 2차 위험도 분석

`gpt_ans.py`에서는 YOLO 탐지 결과를 요약해 OpenAI 모델(`gpt-4.1-nano`)에 전달하고, 건축물 위험도와 권장 조치사항을 생성합니다.

이 분석은 프로토타입의 보조 판단 단계이며, 실제 건축물의 구조안전진단이나 전문가 검사를 대체하지 않습니다.

## 모델 학습 코드

대회 당시 YOLOv8 학습 과정에 사용된 코드는 [`training/`](training/) 디렉터리에 아카이브했습니다.

- [`training/train_yolov8.py`](training/train_yolov8.py) — `yolov8s-seg.pt` 기반 학습 스크립트
- [`training/README.md`](training/README.md) — 학습 설정과 원본 코드 출처 설명

아카이브된 코드에는 300 epochs, batch size 16, image size 768, AdamW, learning rate `0.0001` 등의 당시 학습 설정이 남아 있습니다.

이 파일은 2026-08-27에 새로 학습 로직을 작성한 것이 아니라, 2025년 개발 저장소 [`frotrue/smart_crack_detection`](https://github.com/frotrue/smart_crack_detection)에 보존되어 있던 학습 코드를 문서화 목적으로 복사한 것입니다. 과거 커밋 이력은 수정하거나 재작성하지 않았습니다.

또한 현재 보존된 자료만으로는 최종 UI가 사용하는 `9_21.pt`가 이 아카이브 스크립트의 특정 실행에서 직접 생성된 체크포인트라고 단정하지 않습니다. 자세한 내용은 [`training/README.md`](training/README.md)를 참고하세요.

## 기술 스택

- Python 3.11+
- PyQt6
- Ultralytics YOLOv8
- OpenCV
- OpenAI API
- `uv`

## 설치 및 실행

### 요구사항

- Python 3.11 이상
- 유효한 `OPENAI_API_KEY`
- 권장: [`uv`](https://docs.astral.sh/uv/)

### 설치

```bash
git clone https://github.com/frotrue/pyqt_dev.git
cd pyqt_dev
uv sync --frozen
```

애플리케이션 실행 전 OpenAI API 키를 환경변수로 등록해야 합니다.

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="YOUR_API_KEY"

# Linux / macOS
export OPENAI_API_KEY="YOUR_API_KEY"
```

### 실행

```bash
uv run main.py
```

## 저장소 기록

2025년에 작성된 프로젝트 코드와 UI 변경 이력은 Git 히스토리에 그대로 보존되어 있습니다. 이후 문서 정리는 당시 구현과 구분되도록 별도 커밋으로 남기며, 과거 커밋이나 코드 이력을 다시 작성하지 않습니다.

### 문서 정리 기록

- **2026-08-27:** 최종 UI 저장소임을 명확히 하고 포트폴리오/증빙 자료로 활용하기 쉽도록 한국어·영어 README를 재정리했습니다. 이 과정에서 2025년 프로젝트 코드나 과거 커밋 이력은 수정하지 않았습니다.
- **2026-08-27:** 기존 개발 저장소에 남아 있던 YOLOv8 학습 스크립트를 `training/` 디렉터리에 출처를 명시해 아카이브했습니다.
- **2026-08-27:** 실제 프로젝트명인 **「스마트 크랙 탐지기 (Smart Crack Detector)」**에 맞춰 문서의 프로젝트 표기를 정리했습니다.

## 관련 저장소

YOLO 학습 코드와 더 단순한 초기 애플리케이션 흐름의 원본 기록은 아래 저장소에도 보존되어 있습니다.

- [frotrue/smart_crack_detection](https://github.com/frotrue/smart_crack_detection)

## 주의사항

이 저장소는 해커톤을 위해 제작한 실험적 프로토타입입니다. 탐지 결과와 생성된 위험도 분석은 실제 건축물에 대한 전문 구조안전진단, 공학적 판단 또는 공식 검사를 대체하지 않습니다.
