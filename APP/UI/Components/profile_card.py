from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle


class ProfileCard(ButtonBehavior, BoxLayout):

    def __init__(self, username, image, on_select=None, **kwargs):
        super().__init__(**kwargs)

        self.username = username
        self.on_select_callback = on_select

        self.orientation = "horizontal"
        self.spacing = 10
        self.padding = 8

        with self.canvas.before:
            Color(0.07, 0.09, 0.18, 1)

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        profile_image = Image(
            source=image,
            size_hint_x=None,
            width=45
        )

        profile_label = Label(
            text=username,
            halign="left",
            valign="middle"
        )

        profile_label.bind(
            size=lambda instance, value: setattr(
                instance,
                "text_size",
                value
            )
        )

        self.add_widget(profile_image)
        self.add_widget(profile_label)

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def on_release(self):
        if self.on_select_callback:
            self.on_select_callback(self.username)