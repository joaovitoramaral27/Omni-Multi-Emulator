from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

from APP.UI.Components.emulator_card import EmulatorCard

class Homepage(Screen):

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

        profile_area = BoxLayout(
        orientation="horizontal",
        size_hint_x=None,
        width=180
    )

        profile_image = Image(
        source="Assets/LowProfile.png",
        size_hint_x=None,
        width=80
        )

        profile_label = Button(
        text="Profile",
        background_color=(103/255, 103/255, 197/255, 1),
        on_release=self.open_profile
        )
        
        title_label = Label(
            text="Omni"
        )

        profile_area.add_widget(profile_image)
        profile_area.add_widget(profile_label)
        header.add_widget(profile_area)
        header.add_widget(title_label)

        main_layout.add_widget(header)

        content = BoxLayout(
            orientation="vertical"
        )

        console_area = AnchorLayout(
            anchor_x="center",
            anchor_y="center"
        )

        console_grid = GridLayout(
            cols=3,
            spacing=20,
            padding=20,
            size_hint=(None, None),
            width=620,
            height=500
        )

        console_grid.add_widget(
            EmulatorCard(image="Assets/GBicon.png", system_name="GB", on_select=self.select_system)
        )

        console_grid.add_widget(
            EmulatorCard(image="Assets/GBCicon.png", system_name="GBC", on_select=self.select_system)
        )

        console_grid.add_widget(
            EmulatorCard(image="Assets/GBAicon.png", system_name="GBA", on_select=self.select_system)
        )

        console_grid.add_widget(
            EmulatorCard(image="Assets/DSicon.png", system_name="DS", on_select=self.select_system)
        )

        console_grid.add_widget(
            EmulatorCard(image="Assets/3DSicon.png", system_name="3DS", on_select=self.select_system)
        )

        console_area.add_widget(console_grid)
        content.add_widget(console_area)

        main_layout.add_widget(content)

        self.add_widget(main_layout)

    def select_system(self, system_name):
        game_list = self.manager.get_screen("gamelist")

        game_list.set_system(system_name)

        self.manager.current = "gamelist"

    def open_profile(self, instance):
        self.manager.current = "profile"