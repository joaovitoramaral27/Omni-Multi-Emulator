from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from APP.UI.Screens.homepage import Homepage
from APP.UI.Screens.gamelist import GameList
from APP.UI.Screens.profile import Profile

from APP.UI.theme import BACKGROUND

Window.clearcolor = BACKGROUND

class OmniApp(App):

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Homepage(name="homepage"))
        screen_manager.add_widget(GameList(name="gamelist"))
        screen_manager.add_widget(Profile(name="profile"))

        return screen_manager


if __name__ == "__main__":
    OmniApp().run()