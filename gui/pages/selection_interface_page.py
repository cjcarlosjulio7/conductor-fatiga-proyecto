from flet import *
from gui.resources.resources_path import (ImagePaths, FontsPath)


class SelectionInterface:
    def __init__(self, page):
        super().__init__()
        self.images = ImagePaths()
        self.fonts = FontsPath()

        self.page = page

        self.page.fonts = {
            "Brittany": self.fonts.brittany_font,
            "Cardo": self.fonts.cardo_font
        }

    def main(self):
        drowsiness_image = Image(src=self.images.image_2, fit=ImageFit.COVER, height=400)
        
        drowsiness_button = ElevatedButton(
            text="Somnolencia",
            on_click=self.drowsiness,
            bgcolor='#944adc',
            color='#FFFFFF',
            width=180,
            height=40,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            )
        )

        

        center_column = Column(
            controls=[
                Container(height=30),
                drowsiness_image,
                drowsiness_button,
            ],
            alignment='center',
            horizontal_alignment='center',
            spacing=20,
            expand=True
        )


        elements = Container(
            content=Row(
                controls=[  
                    center_column
                ],
                alignment='spaceEvenly',
                vertical_alignment='center',
            ),
            bgcolor="#fffffe",
            padding=0,
            expand=True
        )
        return elements

    def drowsiness(self, e):
        self.page.go("/drowsiness_page")

    