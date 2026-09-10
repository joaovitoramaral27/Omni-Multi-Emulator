from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

from APP.UI.Components.emulator_card import EmulatorCard

class Profile(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(
            orientation="vertical"
        )

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=60
        )

        back_button = Button(
            text="<",
            size_hint_x=None,
            width=50
        )

        back_button.bind(
            on_release=self.go_home
        )

        header.add_widget(back_button)

        main_layout.add_widget(header)

        self.add_widget(main_layout)

    def go_home(self, *args):
        self.manager.current = "homepage"   