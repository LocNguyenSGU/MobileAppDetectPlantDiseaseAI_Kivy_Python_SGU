from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
import cv2


class CameraApp(MDApp):
    def build(self):
        # Giao diện chính
        self.layout = MDBoxLayout(orientation='vertical')

        # Thanh tiêu đề
        self.toolbar = MDLabel(
            text="Plant Disease Detector",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )
        self.layout.add_widget(self.toolbar)

        # Nút mở camera
        self.camera_button = MDFloatingActionButton(
            icon="camera",
            pos_hint={"center_x": 0.5},
            on_release=self.start_camera
        )
        self.layout.add_widget(self.camera_button)

        # Khu vực hiển thị camera
        self.image_widget = Image()  # Dùng Image để hiển thị luồng camera
        self.layout.add_widget(self.image_widget)

        return self.layout

    def start_camera(self, *args):
        self.capture = cv2.VideoCapture(0)  # Mở camera
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Cập nhật khung hình

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Chuyển đổi hình ảnh OpenCV thành Kivy texture
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image_widget.texture = texture  # Gán texture cho Image widget

    def on_stop(self):
        # Giải phóng camera khi thoát ứng dụng
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()


if __name__ == '__main__':
    CameraApp().run()