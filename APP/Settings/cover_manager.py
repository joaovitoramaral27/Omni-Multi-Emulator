import json
import re
from pathlib import Path

import requests

from APP.Settings.rawg_config import RAWG_API_KEY


COVERS_FILE = Path(
    "APP/Settings/game_covers.json"
)

COVERS_FOLDER = Path(
    "Assets/Covers"
)

RAWG_URL = "https://api.rawg.io/api/games"


def load_covers():

    if not COVERS_FILE.exists():
        return {}

    try:

        with open(
            COVERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except json.JSONDecodeError:

        return {}


def save_covers(covers):

    COVERS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        COVERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            covers,
            file,
            indent=4,
            ensure_ascii=False
        )


def normalize_name(name):

    name = name.lower()

    name = re.sub(
        r"\.[a-z0-9]+$",
        "",
        name
    )

    name = re.sub(
        r"[\[\(\{].*?[\]\)\}]",
        "",
        name
    )

    name = re.sub(
        r"[^a-z0-9]+",
        " ",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()


def get_cover(game_name, system_name):

    covers = load_covers()

    game_key = (
        f"{system_name}:{game_name}"
    )

    # =================================
    # 1. PROCURAR NO CACHE
    # =================================

    if game_key in covers:

        cover_path = Path(
            covers[game_key]
        )

        if cover_path.exists():

            print(
                f"Capa encontrada no cache: "
                f"{cover_path}"
            )

            return str(cover_path)

    # =================================
    # 2. PROCURAR NA RAWG
    # =================================

    print(
        f"Capa não encontrada localmente: "
        f"{game_name}"
    )

    cover_path = search_rawg_cover(
        game_name,
        system_name
    )

    if not cover_path:

        print(
            f"Nenhuma capa encontrada para: "
            f"{game_name}"
        )

        return None

    # =================================
    # 3. SALVAR NO CACHE
    # =================================

    covers[game_key] = cover_path

    save_covers(covers)

    print(
        f"Capa registrada no JSON: "
        f"{cover_path}"
    )

    return cover_path


def search_rawg_cover(
    game_name,
    system_name
):

    if not RAWG_API_KEY:

        print(
            "ERRO: RAWG_API_KEY não configurada."
        )

        return None

    # =================================
    # PLATAFORMAS
    # =================================

    platform_id = get_rawg_platform_id(
        system_name
    )

    if platform_id is None:

        print(
            f"Plataforma não configurada: "
            f"{system_name}"
        )

        return None

    # =================================
    # BUSCA
    # =================================

    params = {
        "key": RAWG_API_KEY,
        "search": game_name,
        "search_precise": "true",
        "page_size": 10,
        "platforms": platform_id
    }

    print(
        f"Pesquisando na RAWG: "
        f"{game_name}"
    )

    try:

        response = requests.get(
            RAWG_URL,
            params=params,
            timeout=15
        )

        print(
            f"RAWG HTTP: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as e:

        print(
            f"Erro ao acessar RAWG: {e}"
        )

        return None

    except ValueError as e:

        print(
            f"Erro ao interpretar resposta RAWG: "
            f"{e}"
        )

        return None

    results = data.get(
        "results",
        []
    )

    print(
        f"Resultados encontrados: "
        f"{len(results)}"
    )

    if not results:

        return None

    # =================================
    # ENCONTRAR MELHOR RESULTADO
    # =================================

    normalized_game = normalize_name(
        game_name
    )

    selected_game = None

    for result in results:

        result_name = result.get(
            "name",
            ""
        )

        normalized_result = normalize_name(
            result_name
        )

        print(
            f"Resultado RAWG: "
            f"{result_name}"
        )

        if normalized_result == normalized_game:

            selected_game = result

            break

    # Se não encontrou correspondência
    # exata, utiliza o primeiro resultado.
    if selected_game is None:

        selected_game = results[0]

    selected_name = selected_game.get(
        "name",
        ""
    )

    image_url = selected_game.get(
        "background_image"
    )

    print(
        f"Jogo selecionado: "
        f"{selected_name}"
    )

    if not image_url:

        print(
            "O jogo encontrado não possui imagem."
        )

        return None

    print(
        f"Imagem RAWG: "
        f"{image_url}"
    )

    return download_cover(
        image_url,
        game_name,
        system_name
    )


def get_rawg_platform_id(system_name):

    platforms = {

        "GB": 26,

        "GBC": 43,

        "GBA": 27,

        "DS": 10,

        "NDS": 10,

        "3DS": 8
    }

    return platforms.get(
        system_name
    )


def download_cover(
    image_url,
    game_name,
    system_name
):

    folder = (
        COVERS_FOLDER
        / system_name
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    safe_name = re.sub(
        r'[<>:"/\\|?*]',
        "",
        game_name
    )

    file_path = (
        folder
        / f"{safe_name}.jpg"
    )

    print(
        "Baixando capa..."
    )

    try:

        response = requests.get(
            image_url,
            timeout=20
        )

        response.raise_for_status()

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )

    except requests.RequestException as e:

        print(
            f"Erro ao baixar capa: {e}"
        )

        return None

    print(
        f"Capa salva em: "
        f"{file_path}"
    )

    return str(file_path)