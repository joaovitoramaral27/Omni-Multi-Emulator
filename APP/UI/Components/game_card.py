from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle


class GameCard(ButtonBehavior, BoxLayout):

    def __init__(self, game_name, game_path, cover=None, on_select=None, **kwargs):
        super().__init__(**kwargs)

        self.game_name = game_name
        self.game_path = game_path
        self.on_select = on_select

        self.orientation = "horizontal"

        self.size_hint = (None, None)
        self.size = (160, 200)

        self.spacing = 8
        self.padding = 10

        with self.canvas.before:
            Color(0.05, 0.07, 0.15, 1)

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        game_label = Label(
            text=game_name,
            size_hint_x=None,
            width=game_label.texture_size[0]
        )

        self.add_widget(game_label)

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def on_release(self):
        if self.on_select:
            self.on_select(self.game_path)