# YOLOv8 학습 코드 아카이브

**한국어** | [English](README.en.md)

이 디렉터리는 2025년 AI 해커톤 경진대회 **「경기창고」** 프로젝트 당시 사용한 YOLOv8 학습 코드를 증빙·문서화 목적으로 보관합니다.

`train_yolov8.py`는 기존 개발 저장소 [`frotrue/smart_crack_detection`](https://github.com/frotrue/smart_crack_detection)의 `main.py`에 남아 있던 학습 코드를 2026-08-27에 이 최종 UI 저장소로 복사해 정리한 것입니다.

> 이 파일의 현재 Git 커밋 날짜는 2026년이지만, 학습 로직 자체는 2025년 개발 저장소에 남아 있던 코드를 기반으로 합니다. 과거 커밋 이력은 수정하거나 재작성하지 않았습니다.

## 학습 설정

아카이브된 스크립트에는 다음 설정이 남아 있습니다.

- 기반 모델: `yolov8s-seg.pt`
- epochs: `300`
- batch size: `16`
- image size: `768`
- workers: `4`
- device: `0`
- patience: `300`
- optimizer: `AdamW`
- initial learning rate: `0.0001`
- weight decay: `0.0005`
- augmentation: 활성화

## 데이터셋 경로

스크립트의 다음 경로는 대회 당시 로컬 개발환경 경로입니다.

```text
/home/user/ai_hackathon/dataset/data.yaml
```

따라서 현재 다른 환경에서 그대로 실행하려면 `data=` 값을 실제 데이터셋 YAML 경로로 수정해야 합니다.

데이터셋 자체는 이 아카이브에 새로 포함하지 않았습니다.

## 현재 UI 모델과의 관계

최종 UI 저장소의 `main.py`는 `9_21.pt` 모델을 사용합니다. 이 학습 스크립트는 프로젝트의 실제 YOLO 학습 과정이 존재했음을 보여주는 과거 코드 아카이브이지만, 현재 저장소에 남아 있는 자료만으로는 `9_21.pt`가 이 스크립트의 특정 실행에서 직접 생성된 체크포인트라고 단정하지 않습니다.

## 원본 기록

- 원본 저장소: [`frotrue/smart_crack_detection`](https://github.com/frotrue/smart_crack_detection)
- 원본 파일: [`main.py`](https://github.com/frotrue/smart_crack_detection/blob/main/main.py)
- 이 저장소의 최종 UI: [`../main.py`](../main.py)

## 문서화 원칙

이 디렉터리는 대회 이후 새 기능을 추가하기 위한 학습 코드가 아니라, 당시 개발 내용을 한 저장소에서 확인하기 쉽도록 정리한 아카이브입니다. 학습 결과 수치나 당시 존재하지 않았던 설정은 새로 만들어 기재하지 않습니다.
