"""Archived YOLOv8 training script from the 2025 경기창고 project.

This file was copied on 2026-08-27 from the original development repository
for documentation and portfolio/reference purposes. The training logic below
is preserved from the historical source rather than rewritten as current code.

Original source:
https://github.com/frotrue/smart_crack_detection/blob/main/main.py
"""

from ultralytics import YOLO


def main():
    model = YOLO("yolov8s-seg.pt")

    model.train(
        data="/home/user/ai_hackathon/dataset/data.yaml",
        epochs=300,
        batch=16,
        imgsz=768,
        workers=4,
        device=0,
        patience=300,
        optimizer="AdamW",
        lr0=0.0001,
        weight_decay=0.0005,
        augment=True,
    )

    # results = model.val()
    # print(results)


if __name__ == "__main__":
    main()
