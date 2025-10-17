import sys
import os
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTabWidget, QTextEdit, QListWidget, QListWidgetItem, QLineEdit
)
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt, QTimer
from ultralytics import YOLO
from datetime import datetime
import gpt_ans
from PyQt6.QtWidgets import QMessageBox, QInputDialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# from gpt_ans import get_gpt_response  # 실제 사용 시 주석 해제

# gpt_ans 모듈이 없으므로 임시 함수로 대체
# class MockGptAns:
#     @staticmethod
#     def get_gpt_response(input_str):
#         """GPT 응답을 시뮬레이션합니다."""
#         if "crack" in input_str:
#             return "GPT 응답: 균열이 확인되었습니다. 즉각적인 조사가 필요합니다."
#         elif "corrosion" in input_str:
#             return "GPT 응답: 부식이 확인되었습니다. 보강 작업이 필요할 수 있습니다."
#         else:
#             return "GPT 응답: 심각한 결함은 발견되지 않았습니다."
# gpt_ans = MockGptAns()


# YOLO 클래스 이름
CLASS_NAMES = ["crack", "corrosion", "ExposedRebars","spalling"]


class CameraTab(QWidget):
    """입력 탭: 카메라 ON/OFF, 촬영/업로드, 이미지 전송"""
    def __init__(self, result_tab):
        super().__init__()
        self.setFixedSize(800, 480)  # 🔹 전체 탭 크기 변경
        self.font = QFont("Arial", 10)

        self.result_tab = result_tab
        self.cap = None
        self.camera_on = False
        self.current_image = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # --- UI 구성 ---
        main_layout = QHBoxLayout()

        # 왼쪽 카메라 화면 크기 확대
        self.video_label = QLabel("이미지를 선택하거나 카메라를 켜주세요.")
        self.video_label.setFixedSize(560, 420)  # 🔹 320→560, 320→420
        self.video_label.setStyleSheet("background-color: #222; color: white;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.video_label)

        # 오른쪽 버튼 3개
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)
        self.btn_camera_toggle = QPushButton("카메라 ON")
        self.btn_camera_toggle.setFont(self.font)
        self.btn_camera_toggle.clicked.connect(self.toggle_camera)

        self.btn_capture_upload = QPushButton("사진 촬영 / 업로드")
        self.btn_capture_upload.setFont(self.font)
        self.btn_capture_upload.clicked.connect(self.capture_or_upload)

        self.btn_send = QPushButton("이미지 전송")
        self.btn_send.setFont(self.font)
        self.btn_send.clicked.connect(self.send_image)

        btn_layout.addWidget(self.btn_camera_toggle)
        btn_layout.addWidget(self.btn_capture_upload)
        btn_layout.addWidget(self.btn_send)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def toggle_camera(self):
        if not self.camera_on:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.video_label.setText("카메라를 열 수 없습니다.")
                return
            self.timer.start(30)
            self.camera_on = True
            self.btn_camera_toggle.setText("카메라 OFF")
        else:
            self.timer.stop()
            if self.cap:
                self.cap.release()
                self.cap = None
            self.video_label.setText("카메라가 꺼져 있습니다.")
            self.camera_on = False
            self.btn_camera_toggle.setText("카메라 ON")

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                # 현재 카메라 탭의 크기(320x320)에 맞춰 스케일링
                pixmap = QPixmap.fromImage(qimg).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(pixmap)
                # `self.current_image`에 현재 프레임을 저장하는 코드는 없으므로,
                # 캡처/업로드 시에만 이미지 경로를 설정하도록 유지

    def capture_or_upload(self):
        if self.camera_on:
            ret, frame = self.cap.read()
            if ret:
                save_path = "captured_image.jpg"
                # 프레임 저장 시점에는 현재 화면의 크기 조정 없이 원본 저장
                cv2.imwrite(save_path, frame)
                self.current_image = save_path
                # 미리보기는 탭 크기에 맞게 스케일링
                pixmap = QPixmap(save_path).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(pixmap)
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg)")
            if file_path:
                self.current_image = file_path
                # 미리보기는 탭 크기에 맞게 스케일링
                pixmap = QPixmap(file_path).scaled(
                    self.video_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.video_label.setPixmap(pixmap)

    def send_image(self):
        if not self.current_image:
            self.video_label.setText("⚠️ 이미지를 먼저 선택하거나 촬영하세요!")
            return

    # 폴더 생성
        base_dir = "save_img"
        img_dir = os.path.join(base_dir, "img")
        result_dir = os.path.join(base_dir, "result")
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(result_dir, exist_ok=True)

        # 파일명: 시간 기반
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = os.path.join(img_dir, f"{timestamp}.jpg")
        result_path = os.path.join(result_dir, f"{timestamp}.txt")

        # YOLO 추론 (실제 환경에서는 모델 파일이 존재해야 함)
        try:
            model = YOLO("9_21.pt")
            results = model(self.current_image, save=False, conf=0.7)
        except Exception as e:
            self.video_label.setText(f"YOLO 추론 오류: {e}")
            return # 오류 발생 시 중단

        # 이미지 저장
        annotated_img = None
        if results:
            annotated_img = results[0].plot()
            cv2.imwrite(img_path, annotated_img)

        # 결과 텍스트 생성 및 저장
        result_str = ""
        for r in results:
            if r.boxes is not None and len(r.boxes) > 0:
                for box in r.boxes:
                    cls_idx = int(box.cls[0])
                    conf = float(box.conf[0])
                    cls_name = CLASS_NAMES[cls_idx]
                    result_str += f"{cls_name}: {conf:.2f}\n"

        # GPT 응답 생성
        temp = gpt_ans.get_gpt_response(result_str)

        # 최종 결과 텍스트 (GPT + YOLO)
        final_result_text = f"{temp}\n\n--- YOLOv8 결과 ---\n{result_str}"

        with open(result_path, "w", encoding="utf-8") as f:
            f.write(final_result_text)

        # 결과 탭에 추가 (이미지 + 텍스트)
        self.result_tab.add_result_item(img_path, final_result_text)


class ResultTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 480)
        main_layout = QHBoxLayout()

        # 🔹 오른쪽으로 이동시키기 위해, 오른쪽부터 구성
        right_layout = QVBoxLayout()

        # 상단: 이미지 + 버튼
        top_layout = QHBoxLayout()
        self.detail_label = QLabel("결과를 선택해 주세요.")
        self.detail_label.setFixedSize(480, 240)
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_label.setStyleSheet("background-color: #222; color: white;")

        self.email_button = QPushButton("📧 이메일로 전송")
        self.email_button.setFixedSize(80, 40)
        self.email_button.clicked.connect(self.send_email)

        top_layout.addWidget(self.detail_label)
        top_layout.addWidget(self.email_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        right_layout.addLayout(top_layout)

        # 하단: 텍스트
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        right_layout.addWidget(self.detail_text)

        # 🔹 왼쪽 리스트 → 오른쪽으로 이동
        self.result_list = QListWidget()
        self.result_list.setFixedWidth(200)
        self.result_list.itemClicked.connect(self.show_result_detail)

        # 🔹 기존: main_layout.addWidget(self.result_list) → 위치 변경
        main_layout.addLayout(right_layout)
        main_layout.addWidget(self.result_list)  # 오른쪽으로 이동

        self.setLayout(main_layout)
    def add_result_item(self, img_path, result_str):
        item = QListWidgetItem(os.path.basename(img_path))
        item.setData(Qt.ItemDataRole.UserRole, img_path)
        item.setData(Qt.ItemDataRole.ToolTipRole, result_str)
        self.result_list.addItem(item)

    def show_result_detail(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        text_content = item.data(Qt.ItemDataRole.ToolTipRole)

        pixmap = QPixmap(path).scaled(
            self.detail_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.detail_label.setPixmap(pixmap)
        self.detail_text.setText(text_content)

        self.current_img_path = path
        self.current_text = text_content

    def send_email(self):
        """이메일 전송 기능"""
        if not self.current_img_path or not self.current_text:
            QMessageBox.warning(self, "⚠️ 오류", "전송할 결과를 먼저 선택하세요!")
            return

        recipient, ok = QInputDialog.getText(self, "이메일 전송", "수신자 이메일 주소를 입력하세요:")
        if not ok or not recipient:
            return

        try:
            sender_email = ""
            sender_password = ""
            subject = "건물지키미 분석 결과"

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(self.current_text, "plain"))

            with open(self.current_img_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(self.current_img_path)}")
            msg.attach(part)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            QMessageBox.information(self, "✅ 전송 완료", f"{recipient}에게 결과가 전송되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "❌ 전송 실패", f"이메일 전송 중 오류 발생:\n{e}")


class SettingsTab(QWidget):
    """설정 탭"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ 모델 경로"))
        self.model_path = QLineEdit()
        self.model_path.setText("9_21.pt") # 초기값 설정
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_model_path)
        layout.addWidget(self.model_path)
        layout.addWidget(browse_btn)
        layout.addWidget(QLabel("📁 저장 폴더 설정"))
        self.save_path = QLineEdit()
        self.save_path.setText("save_img") # 초기값 설정
        layout.addWidget(self.save_path)
        layout.addStretch() # 남은 공간 채우기
        self.setLayout(layout)

    def select_model_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "모델 선택", "", "Model Files (*.pt *.onnx)")
        if file_path:
            self.model_path.setText(file_path)


class MainApp(QWidget):
    """메인 GUI"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("라즈베리파이 추론 GUI")
        self.setFixedSize(800, 480)

        self.result_tab = ResultTab()
        self.camera_tab = CameraTab(self.result_tab)
        self.settings_tab = SettingsTab()

        tabs = QTabWidget()
        tabs.addTab(self.camera_tab, "입력")
        tabs.addTab(self.result_tab, "결과")
        tabs.addTab(self.settings_tab, "설정")

        # 🔹 탭 버튼을 오른쪽에 배치
        tabs.setTabPosition(QTabWidget.TabPosition.East)

        # 🔹 가로 배치로 설정 (탭이 오른쪽으로 가게)
        layout = QHBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    # Windows/Linux에서 HiDPI 환경 지원 활성화 (필요 시)
    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())