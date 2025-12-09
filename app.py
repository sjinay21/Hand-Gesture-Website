# Main file
# import flet as ft
# import os
# import time
# import ctypes

# class GestureApp:
#     def __init__(self):
#         self.current_process = None

#     def kill_current_process(self):
#         if self.current_process:
#             try:
#                 import psutil
#                 parent = psutil.Process(self.current_process.pid)
#                 for child in parent.children(recursive=True):
#                     child.kill()
#                 parent.kill()
#                 self.current_process = None
#             except psutil.NoSuchProcess:
#                 pass

#     def run_script(self, script_name):
#         self.kill_current_process()
#         try:
#             import subprocess, sys
#             self.current_process = subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#         except Exception as e:
#             print(f"Error running {script_name}: {str(e)}")

# def main(page: ft.Page):
#     page.title = "Gesture Control Software"
#     page.window_width = 900
#     page.window_height = 650
#     page.theme_mode = ft.ThemeMode.DARK
#     page.bgcolor = "black"

#     app = GestureApp()

#     # 🔹 Show a Windows popup notification on startup
#     ctypes.windll.user32.MessageBoxW(0, "Gesture Control App is starting...", "Startup Notification", 1)

#     # 🔹 Delay execution for 3 seconds (optional, for smoother startup)
#     time.sleep(3)

#     def handle_window_close(e):
#         app.kill_current_process()
#         page.window_destroy()

#     page.window_prevent_close = True
#     page.on_window_close = handle_window_close

#     # 🔹 Background Image
#     background = ft.Image(src="./assets/639904.jpg", fit=ft.ImageFit.COVER)

#     # 🔹 Create feature buttons
#     def create_feature_button(text, script_name, icon):
#         return ft.FilledButton(
#             content=ft.Row([
#                 ft.Icon(icon, color=ft.Colors.WHITE, size=24),
#                 ft.Text(text, size=18, weight=ft.FontWeight.BOLD)
#             ], alignment=ft.MainAxisAlignment.CENTER),
#             width=400,
#             height=50,
#             bgcolor=ft.Colors.BLUE_ACCENT,
#             on_click=lambda _: app.run_script(script_name)
#         )

#     title = ft.Text("🚀 Gesture Control Software", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT)
#     subtitle = ft.Text("🌟 Select a feature to launch:", size=20, color=ft.Colors.GREY_300)

#     features = ft.Column([
#         create_feature_button("🎨 Air Canvas ML", "air_canvas_ml.py", ft.Icons.BRUSH_ROUNDED),
#         create_feature_button("👀 Eye Control", "eye_control.py", ft.Icons.REMOVE_RED_EYE_ROUNDED),
#         create_feature_button("🔊 Volume & Brightness Control", "vb_control.py", ft.Icons.VOLUME_UP_ROUNDED),
#         create_feature_button("⌨️ Hand Gesture Keyboard", "main.py", ft.Icons.KEYBOARD_ALT_ROUNDED),
#         create_feature_button("🚀 App Launcher", "launcher.py", ft.Icons.LAUNCH_ROUNDED),
#     ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)

#     stop_button = ft.FilledButton(
#         "⏹ Stop Current Feature",
#         icon=ft.Icons.STOP_CIRCLE_ROUNDED,
#         color=ft.Colors.WHITE,
#         on_click=lambda _: app.kill_current_process(),
#         width=400,
#         height=50,
#         bgcolor=ft.Colors.RED_ACCENT
#     )

#     page.add(ft.Stack([
#         background,
#         ft.Column([
#             title,
#             subtitle,
#             ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
#             features,
#             ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
#             stop_button
#         ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, opacity=1.0)
#     ]))

# if __name__ == "__main__":
#     ft.app(target=main)










# Updated file
import flet as ft
import os
import time
import ctypes

class GestureApp:
    def __init__(self):
        self.current_process = None

    def kill_current_process(self):
        if self.current_process:
            try:
                import psutil
                parent = psutil.Process(self.current_process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                self.current_process = None
            except psutil.NoSuchProcess:
                pass

    def run_script(self, script_name):
        self.kill_current_process()
        try:
            import subprocess, sys
            self.current_process = subprocess.Popen([sys.executable, script_name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        except Exception as e:
            print(f"Error running {script_name}: {str(e)}")

def main(page: ft.Page):
    page.title = "Gesture Control Software"
    page.window_width = 900
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "black"

    app = GestureApp()

    ctypes.windll.user32.MessageBoxW(0, "Gesture Control App is starting...", "Startup Notification", 1)
    time.sleep(3)

    def handle_window_close(e):
        app.kill_current_process()
        page.window_destroy()

    page.window_prevent_close = True
    page.on_window_close = handle_window_close

    background = ft.Image(src="./assets/639904.jpg", fit=ft.ImageFit.COVER)

    def create_feature_button(text, script_name, icon):
        return ft.FilledButton(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.WHITE, size=24),
                ft.Text(text, size=18, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=400,
            height=50,
            bgcolor=ft.Colors.BLUE_ACCENT,
            on_click=lambda _: app.run_script(script_name)
        )

    title = ft.Text("🚀 Gesture Control Software", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT)
    subtitle = ft.Text("🌟 Select a feature to launch:", size=20, color=ft.Colors.GREY_300)

    features = ft.Column([
        create_feature_button("🎨 Air Canvas ML", "./air_canvas_ml.py", ft.Icons.BRUSH_ROUNDED),
        create_feature_button("👀 Eye Control", "./eye_control.py", ft.Icons.REMOVE_RED_EYE_ROUNDED),
        create_feature_button("🔊 Volume & Brightness Control", "./vb_control.py", ft.Icons.VOLUME_UP_ROUNDED),
        create_feature_button("⌨️ Hand Gesture Keyboard", "./keyboard.py", ft.Icons.KEYBOARD_ALT_ROUNDED),
        create_feature_button("🚀 App Launcher", "./windows.py", ft.Icons.LAUNCH_ROUNDED),
        create_feature_button("🎹 Air Piano", "./air_piano.py", ft.Icons.MUSIC_NOTE_ROUNDED),
    ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    stop_button = ft.FilledButton(
        "⏹ Stop Current Feature",
        icon=ft.Icons.STOP_CIRCLE_ROUNDED,
        color=ft.Colors.WHITE,
        on_click=lambda _: app.kill_current_process(),
        width=400,
        height=50,
        bgcolor=ft.Colors.RED_ACCENT
    )

    page.add(ft.Stack([
        background,
        ft.Column([
            title,
            subtitle,
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            features,
            ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
            stop_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, opacity=1.0)
    ]))

if __name__ == "__main__":
    ft.app(target=main)
