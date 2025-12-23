# Внешние зависимости
from typing import Tuple, List
import uuid
import asyncio
import requests
from bs4 import BeautifulSoup
# Внутренние модули
from telegram_bot.crud import (sql_add_category_for_map, sql_get_all_maps, sql_add_card,
                               sql_add_card_image)


category_name_with_visual = {
    "smoke": "💨 smoke 💨",
    "flash": "⚡ flash ⚡",
    "molotov": "🔥 molotov 🔥",
    "hegrenade": "💥 he-grenade 💥",
    "oneway": "👀 oneway 👀"
}


class Parser:
    url_base = "https://раскидки-гранат.рф/"

    def __init__(self, dir_files: str):
        self.dir_files = dir_files

    @staticmethod
    def get_response(url_path: str) -> bytes:
        try:
            response = requests.get(url_path)
            response.raise_for_status()

            return response.content

        except requests.exceptions.RequestException as err:
            print(f"Error fetching the URL: {err}")

        except Exception as err:
            print(f"Unexpected error: {err}")


    @classmethod
    def get_name_and_link(cls, content: bytes) -> List[Tuple[str, str]]:
        soup = BeautifulSoup(content, "html.parser")
        blocks = soup.find_all("div", class_="blog-post-content")

        result = []
        for block in blocks:
            block_a = block.find("a")
            block_name = block_a.text.strip()
            block_link = f"{cls.url_base}{block_a.get("href")}"
            result.append((block_name, block_link))

        return result


    @classmethod
    def get_image_and_step(cls, content: bytes) -> Tuple[str, List[str]]:
        soup = BeautifulSoup(content, "html.parser")
        slides = soup.find_all("div", class_="multiphoto-box")
        main_text = soup.find("div", class_="breadcrumb-content text-center")
        description = main_text.find("span").text.strip()

        result = []
        steps = []
        for slide in slides:
            step = slide.find("span").text.strip()
            steps.append(step)

            image_link = f"{cls.url_base}{slide.find("img").get("src")}"
            result.append(image_link)

        description += "\n\n".join(steps)

        return description, result

    def download_image(self, url_path: str, filename: str):
        try:
            response = requests.get(url_path)
            response.raise_for_status()

            with open(f"images/{self.dir_files}/{filename}", 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Изображение сохранено как {filename}")

        except requests.exceptions.RequestException as err:
            print(f"(download) Error fetching the URL: {err}")

        except Exception as err:
            print(f"(download) Unexpected error: {err}")

    async def run(self):
        _, _, maps = await sql_get_all_maps()

        for m in maps:
            await asyncio.sleep(0.5)

            print(f"Карта: https://раскидки-гранат.рф/raskidki-granat-counter-strike-2/{m[1]}/")
            content = self.get_response(
                url_path=f"https://раскидки-гранат.рф/raskidki-granat-counter-strike-2/{m[1]}/"
            )
            categories = self.get_name_and_link(content=content)

            for category_name, category_link in categories[:1]:
                await asyncio.sleep(0.5)

                category_id = await sql_add_category_for_map(
                    name=category_name_with_visual.get(category_name.lower(), "none"),
                    map_id=m[0]
                )

                print(f"Категория: {category_link}")
                content = self.get_response(url_path=category_link)
                cards = self.get_name_and_link(content=content)

                for card_name, card_link in cards:
                    await asyncio.sleep(0.5)

                    print(f"Карточка: {card_link}")
                    content = self.get_response(url_path=card_link)
                    card_description, image_links = self.get_image_and_step(content=content)

                    card_id = await sql_add_card(
                        name=card_name,
                        description=card_description,
                        category_id=category_id,
                        custom=False
                    )

                    card_images = {
                        "file_names": [],
                        "orders": []
                    }
                    for i, image_link in enumerate(image_links, 1):
                        await asyncio.sleep(0.5)

                        image_name = f"{uuid.uuid4()}.jpg"

                        print(f"Изображение: {image_link}")
                        self.download_image(
                            url_path=image_link,
                            filename=image_name
                        )

                        card_images["file_names"].append(image_name)
                        card_images["orders"].append(i)

                    await sql_add_card_image(
                        card_id=card_id,
                        **card_images
                    )


if __name__ == "__main__":
    parser = Parser(dir_files="cards")
    asyncio.run(parser.run())
