# Smart Crack Detection — Final UI Version

[한국어](README.md) | **English**

This repository contains the **final UI/integration revision** of the Smart Crack Detection project developed around the 2025 AI Hackathon competition **"경기창고"**.

The application provides a PyQt6 desktop interface for loading or capturing building images, running a trained YOLOv8 model, reviewing detected defects, and generating a secondary risk assessment with an OpenAI model.

> **Award:** Excellence Award, 2025 AI Hackathon Competition "경기창고"  
> **Awarding organization:** Advanced Institute of Convergence Technology

## Project Scope

This repository focuses on the final desktop UI and inference workflow of the project.

The application currently supports the following defect classes:

- `crack`
- `corrosion`
- `ExposedRebars`
- `spalling`

The main workflow is:

1. Load an image or capture one from a camera.
2. Run inference with the trained YOLOv8 model (`9_21.pt`).
3. Visualize detected defects and confidence scores.
4. Send the summarized detections to the GPT analysis module.
5. Store the annotated image and analysis result.
6. Review previous results from the result tab.

## Main UI Features

### Input tab

- Camera ON/OFF
- Camera capture
- Local image upload
- YOLO inference

### Result tab

- Detection result list
- Annotated image preview
- GPT-based risk assessment
- Optional e-mail sending workflow

### Settings tab

- Model-path selection UI
- Save-path configuration UI

> Note: this repository is a hackathon prototype. Some settings/UI controls may not be fully wired to every inference path in the current code.

## AI Pipeline

### YOLO inference

The UI loads `9_21.pt` with Ultralytics YOLO and runs inference at a confidence threshold of `0.5`.

Detected classes and confidence scores are collected and stored together with the annotated image.

### Secondary risk analysis

`gpt_ans.py` sends the YOLO detection summary to an OpenAI model (`gpt-4.1-nano`) and requests a compact building-risk estimate and recommended action.

This analysis is intended only as a prototype decision-support step and does **not** replace a professional structural safety inspection.

## Tech Stack

- Python 3.11+
- PyQt6
- Ultralytics YOLOv8
- OpenCV
- OpenAI API
- `uv`

## Installation

### Requirements

- Python 3.11 or newer
- A valid `OPENAI_API_KEY`
- Recommended: [`uv`](https://docs.astral.sh/uv/)

### Setup

```bash
git clone https://github.com/frotrue/pyqt_dev.git
cd pyqt_dev
uv sync --frozen
```

Set the OpenAI API key before launching the application.

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="YOUR_API_KEY"

# Linux / macOS
export OPENAI_API_KEY="YOUR_API_KEY"
```

Run:

```bash
uv run main.py
```

## Repository History

The project code and UI changes from 2025 remain preserved in Git history. This README was reorganized later for clearer documentation and portfolio/reference use; historical commits were not rewritten.

### Documentation update

- **2026-08-27:** Reorganized Korean/English documentation for the final UI repository. No historical project code or commit history was rewritten.

## Related Repository

An earlier implementation of the project, including YOLO training code and a simpler application flow, is preserved here:

- [frotrue/smart_crack_detection](https://github.com/frotrue/smart_crack_detection)

## Disclaimer

This repository is an experimental hackathon prototype. Its detections and generated risk assessments are not a substitute for professional inspection, engineering judgment, or an official structural safety diagnosis.
