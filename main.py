# from kivy.uix.screenmanager import Screen
# from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDFloatingActionButton
# from kivymd.uix.label import MDLabel, MDIcon
#
#
# class MainApp(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = "Yellow"
#         self.theme_cls.primary_hue = "A700"
#         self.theme_cls.theme_style = "Dark"
#         screen = Screen()  # Khởi tạo một màn hình mới
#
#         label = MDLabel(
#             text='Hello from KivyMD',
#             halign='center',
#             theme_text_color="Custom",
#             text_color=(0, 0, 1, 1),
#             font_style="Caption"
#         )
#
#         icon_label = MDIcon(
#             icon='access-point',
#             halign='center',
#             pos_hint={"center_x": 0.5, "center_y": 0.2}
#         )
#
#         btn_flat = MDRectangleFlatButton(
#             text='Hello button',
#             pos_hint={"center_x": 0.5, "center_y": 0.4}  # Đặt nút vào giữa màn hình
#         )
#         btn_icon = MDFloatingActionButton(icon='access-point')
#
#         # Thêm các widget vào màn hình
#         screen.add_widget(label)
#         screen.add_widget(icon_label)
#         screen.add_widget(btn_flat)
#         screen.add_widget(btn_icon)
#
#         return screen  # Trả về toàn bộ màn hình chứa các widget
#
#
# if __name__ == '__main__':
#     app = MainApp()
#     app.run()
#
#


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from toolbar import MenuScreen, SecondScreen, screen_helper


# Các lớp màn hình của bạn (MenuScreen, SecondScreen) sẽ giữ nguyên
# Đảm bảo rằng bạn đã import đầy đủ các lớp đã khai báo ở trên

class MyApp(App):
    def build(self):
        # Khởi tạo ScreenManager và load layout
        screen_manager = ScreenManager()

        # Load giao diện màn hình từ string đã khai báo
        Builder.load_string(screen_helper)

        # Thêm các màn hình vào ScreenManager
        screen_manager.add_widget(MenuScreen(name='MenuScreen'))
        screen_manager.add_widget(SecondScreen(name='SecondScreen'))

        return screen_manager


if __name__ == "__main__":
    MyApp().run()

