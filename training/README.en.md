# YOLOv8 Training Archive

[한국어](README.md) | **English**

This directory preserves the YOLOv8 training code used during the 2025 AI Hackathon competition **"경기창고"** for documentation and portfolio/reference purposes.

`train_yolov8.py` was copied on 2026-08-27 from `main.py` in the earlier development repository [`frotrue/smart_crack_detection`](https://github.com/frotrue/smart_crack_detection) and organized here alongside the final UI repository.

> The current Git commit for this copy is from 2026, but the training logic is based on code preserved in the 2025 development repository. Historical commits were not rewritten or backdated.

## Training configuration

The archived script contains the following configuration:

- base model: `yolov8s-seg.pt`
- epochs: `300`
- batch size: `16`
- image size: `768`
- workers: `4`
- device: `0`
- patience: `300`
- optimizer: `AdamW`
- initial learning rate: `0.0001`
- weight decay: `0.0005`
- augmentation: enabled

## Dataset path

The following path in the script is the local development path used at the time of the project:

```text
/home/user/ai_hackathon/dataset/data.yaml
```

To run the script in another environment, update the `data=` value to the actual dataset YAML path.

The dataset itself has not been newly copied into this archive.

## Relationship to the final UI model

The final UI in this repository loads `9_21.pt`. This archived script demonstrates that a concrete YOLO training workflow was part of the project, but the material currently preserved in the repositories is not sufficient to state that `9_21.pt` was produced by a specific execution of this exact script.

## Original record

- Original repository: [`frotrue/smart_crack_detection`](https://github.com/frotrue/smart_crack_detection)
- Original file: [`main.py`](https://github.com/frotrue/smart_crack_detection/blob/main/main.py)
- Final UI in this repository: [`../main.py`](../main.py)

## Documentation principle

This directory is an archive of historical project material, not a post-competition rewrite of the training implementation. No training metrics or settings that are not supported by the preserved source have been added.
