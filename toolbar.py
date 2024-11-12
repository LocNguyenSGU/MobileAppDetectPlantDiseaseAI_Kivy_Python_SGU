from unittest import result

import tensorflow as tf
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import cv2
import numpy as np

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model("best_model.keras")


# Hàm xử lý ảnh và dự đoán bệnh
def predict_disease(image):
    # Chuyển ảnh sang định dạng phù hợp với mô hình (ví dụ: 224x224 RGB)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (64, 64))
    img = np.expand_dims(img, axis=0)  # Thêm chiều batch
    img = img / 255.0  # Chuẩn hóa ảnh

    # Dự đoán
    prediction = model.predict(img)
    return prediction


class MenuScreen(Screen):
    pass


class SecondScreen(Screen):
    def on_enter(self):
        # Khi màn hình được hiển thị, bật camera
        self.ids.camera.play = True

    def on_leave(self):
        # Khi màn hình bị rời khỏi, dừng camera
        self.ids.camera.play = False

    def capture_image(self):
        # Lấy ảnh từ camera
        camera = self.ids.camera
        texture = camera.texture
        img = np.frombuffer(texture.pixels, dtype=np.uint8).reshape(camera.texture.size[1], camera.texture.size[0], 4)
        img = img[:, :, :3]  # Loại bỏ alpha channel nếu có
        img = cv2.flip(img, 0)
        # Dự đoán bệnh từ ảnh
        prediction = predict_disease(img)

        # Danh sách các tên bệnh (đảm bảo danh sách này có đúng số lượng lớp)
        disease_names = ['Bệnh A', 'Bệnh B', 'Bệnh C']

        # Khởi tạo kết quả dự đoán dưới dạng chuỗi
        result = "Disease Prediction:\n"

        # Duyệt qua tất cả các lớp để hiển thị tên bệnh và xác suất
        for i in range(len(disease_names)):
            predicted_probability = prediction[0][i] * 100  # Tính tỷ lệ phần trăm
            result += f"{disease_names[i]}: {predicted_probability:.2f}%\n"

        # Hiển thị kết quả dự đoán trên UI
        self.ids.result_label.text = result

        # Lưu kết quả vào lịch sử
        with open("history.txt", "a") as f:
            f.write(f"Captured Image - {result}\n")

    def open_filechooser(self):
        # Mở FileChooser để người dùng chọn ảnh
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']  # Chỉ cho phép chọn ảnh
        filechooser.bind(on_selection=lambda instance, value: self.select_image(value))

        # Tạo popup để hiển thị FileChooser
        popup = Popup(title="Select Image", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()


    def select_image(self, selected_files):
        # Kiểm tra nếu có tệp ảnh được chọn
        if selected_files:
            img_path = selected_files[0]
            img = cv2.imread(img_path)

            # Dự đoán bệnh từ ảnh được chọn
            prediction = predict_disease(img)

            # Danh sách các tên bệnh (đảm bảo danh sách này có đúng số lượng lớp)
            disease_names = ['Bệnh A', 'Bệnh B', 'Bệnh C']

            # Xử lý xác suất
            predicted_class = np.argmax(prediction)  # Lấy chỉ số lớp có xác suất cao nhất
            predicted_probability = prediction[0][predicted_class] * 100  # Tính tỷ lệ phần trăm

            # Tạo kết quả dự đoán
            result = f"Disease: {disease_names[predicted_class]} - {predicted_probability:.2f}%"

            # Hiển thị kết quả dự đoán trên UI
            self.ids.result_label.text = result

            # Lưu kết quả vào lịch sử
            with open("history.txt", "a") as f:
                f.write(f"Selected Image: {img_path} - {result}\n")


class DemoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.material_style = "M2"
        screen = Builder.load_string(screen_helper)
        return screen

    def on_menu_press(self):
        print("Menu button pressed")

    def switch_to_second_screen(self):
        # Chuyển sang màn hình thứ hai
        self.root.current = "SecondScreen"

    def switch_to_menu_screen(self):
        # Quay lại màn hình đầu tiên
        self.root.current = "MenuScreen"


screen_helper = """
ScreenManager:
    MenuScreen:
        name: "MenuScreen"
    SecondScreen:
        name: "SecondScreen"

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Demo application'
            left_action_items: [['menu', lambda x: app.on_menu_press()]]
            elevation: 5

        MDLabel:
            text: 'Hello world'
            halign: 'center'

        MDBottomAppBar:
            MDTopAppBar:
                mode: 'end'
                type: 'bottom'
                on_action_button: app.on_menu_press()
                left_action_items: [["coffee", lambda x: app.switch_to_second_screen()]]

<SecondScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'Second Screen'
            left_action_items: [['arrow-left', lambda x: app.switch_to_menu_screen()]]
            elevation: 5

        Camera:
            id: camera
            resolution: (640, 480)
            play: True

        MDLabel:
            id: result_label
            text: 'Disease Prediction will appear here'
            halign: 'center'

        Button:
            text: 'Capture and Predict'
            on_press: root.capture_image()

        Button:
            text: 'Select Image'
            on_press: root.open_filechooser()
"""

DemoApp().run()