from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

from filesharer import FileSharer
import time
import webbrowser
import os

Builder.load_file("frontend.kv")


class CameraScreen(Screen):

    def start(self):
        """Starts camera and changes Button text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera_button.text = "Stop Camera"

    def stop(self):
        """Stops camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera.texture = None
        self.ids.camera_button.text = "Start Camera"

    def capture(self):
        """Creates a filename with the current time, then captures
        and saves a photo image under the filename. If the 'files'
        directory doesn't exist, one will be created"""
        if os.path.exists("files"):
            pass
        else:
            os.mkdir("files")
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.file_path = f"files/{current_time}.png"
        self.ids.camera.export_to_png(self.file_path)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.file_path


class ImageScreen(Screen):
    # Link exception message variable
    exception_message = "Create a Link First"

    def create_link(self):
        """Accesses the photo file_path, uploads it to the web,
        and inserts the link in the Label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.file_path
        fileshare = FileSharer(file_path)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard available for pasting"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.exception_message

    def open_link(self):
        """Open link with default web browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.exception_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
