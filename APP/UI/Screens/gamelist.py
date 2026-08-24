from pathlib import Path

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView

from APP.Settings.cover_manager import get_cover
from APP.UI.Components.game_card import GameCard
from APP.Settings.rom_folders import get_folder, save_folder


class GameList(Screen):

    ROM_EXTENSIONS = {
        "GB": [".gb"],
        "GBC": [".gbc"],
        "GBA": [".gba"],
        "DS": [".nds"],
        "NDS": [".nds"],
        "3DS": [".3ds", ".3dsx"],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.system_name = None

        main_layout = BoxLayout(
            orientation="vertical"
        )

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=80
        )

        back_button = Button(
            text="<",
            size_hint_x=None,
            width=50
        )

        back_button.bind(
            on_release=self.go_home
        )

        self.emu_image = Image(
            size_hint=(None, None),
            size=(60, 60)
        )

        self.emu_label = Label()

        header.add_widget(back_button)
        header.add_widget(self.emu_image)
        header.add_widget(self.emu_label)

        main_layout.add_widget(header)

        self.game_grid = GridLayout(
            cols=4,
            spacing=15,
            padding=20,
            size_hint_y=None
        )

        self.game_grid.bind(
            minimum_height=self.game_grid.setter("height")
        )

        scroll = ScrollView()

        scroll.add_widget(self.game_grid)

        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

        add_button = Button(
            text="+",
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={
                "right": 0.98,
                "bottom": 0.03
            }
        )

        add_button.bind(
            on_release=self.open_folder_chooser
        )

        self.add_widget(add_button)

    def set_system(self, system_name):
        print(f"SET SYSTEM: {system_name}")

        self.system_name = system_name

        self.emu_label.text = system_name

        image_path = f"Assets/{system_name}icon.png"

        print(f"IMAGE: {image_path}")

        self.emu_image.source = image_path

        print("ANTES DO LOAD")

        self.load_games()

        print("DEPOIS DO LOAD")

    def load_games(self):
        print(f"CARREGANDO JOGOS: {self.system_name}")

        self.game_grid.clear_widgets()

        folder = get_folder(self.system_name)

        print(f"PASTA ENCONTRADA: {folder}")

        if not folder:
            self.game_grid.add_widget(
                Label(
                    text="Nenhuma pasta de jogos configurada.",
                    size_hint_y=None,
                    height=50
                )
            )

            return

        folder_path = Path(folder)

        print(f"CAMINHO DA PASTA: {folder_path}")

        if not folder_path.exists():
            self.game_grid.add_widget(
                Label(
                    text="A pasta configurada não existe.",
                    size_hint_y=None,
                    height=50
                )
            )

            return

        if not folder_path.is_dir():
            self.game_grid.add_widget(
                Label(
                    text="O caminho configurado não é uma pasta.",
                    size_hint_y=None,
                    height=50
                )
            )

            return

        extensions = self.ROM_EXTENSIONS.get(
            self.system_name,
            []
        )

        print(f"EXTENSÕES ACEITAS: {extensions}")

        try:
            files = list(folder_path.iterdir())

        except Exception as e:
            print(f"ERRO AO LER A PASTA: {e}")

            self.game_grid.add_widget(
                Label(
                    text=f"Erro ao ler a pasta:\n{e}",
                    size_hint_y=None,
                    height=70
                )
            )

            return

        games = []

        for file in files:

            if not file.is_file():
                continue

            if file.suffix.lower() in extensions:
                games.append(file)

        print(f"JOGOS ENCONTRADOS: {len(games)}")

        if not games:
            self.game_grid.add_widget(
                Label(
                    text="Nenhum jogo encontrado.",
                    size_hint_y=None,
                    height=50
                )
            )

            return

        for game in games:

            game_name = game.stem

            try:
                cover = get_cover(
                    game_name,
                    self.system_name
                )

                print(
                    f"COVER PARA {game_name}: {cover}"
                )

                card = GameCard(
                    game_name=game_name,
                    game_path=str(game),
                    cover=cover,
                    on_select=self.select_game
                )

                self.game_grid.add_widget(card)

            except Exception as e:
                print(
                    f"ERRO AO CRIAR CARD PARA {game}: {e}"
                )

    def select_game(self, game_path):
        print(f"Jogo selecionado: {game_path}")

    def open_folder_chooser(self, *args):

        start_path = str(Path.home())

        chooser = FileChooserListView(
            path=start_path,
            dirselect=True
        )

        select_button = Button(
            text="Selecionar pasta",
            size_hint_y=None,
            height=50
        )

        popup_layout = BoxLayout(
            orientation="vertical"
        )

        popup_layout.add_widget(chooser)
        popup_layout.add_widget(select_button)

        popup = Popup(
            title="Selecionar pasta de jogos",
            content=popup_layout,
            size_hint=(0.9, 0.9)
        )

        def select_folder(*args):

            if not chooser.selection:
                return

            folder = chooser.selection[0]

            save_folder(
                self.system_name,
                folder
            )

            popup.dismiss()

            self.load_games()

        select_button.bind(
            on_release=select_folder
        )

        popup.open()

    def go_home(self, *args):
        self.manager.current = "homepage"