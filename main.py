from flet import *
from gui.pages.start_page import Start
from gui.pages.selection_interface_page import SelectionInterface
from gui.pages.drowsiness_page import Drowsiness
import tkinter as tk


class MainApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "Proyecto Construcción de Software"
        self.page.bgcolor = "#fffffe"
        self.page.window.resizable = False
        self.page.padding = 0
        self.page.window.width = 1000
        self.page.window.height = 680

        # Obtener tamaño de la pantalla
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        pos_x = (screen_width // 2) - (self.page.window.width // 2)
        pos_y = (screen_height // 2) - (self.page.window.height // 2)
        root.destroy()

        # Establecer posición centrada de la ventana
        self.page.window.left = pos_x
        self.page.window.top = pos_y
        

        self.page.theme = Theme(
            page_transitions=PageTransitionsTheme(
                android=PageTransitionTheme.FADE_UPWARDS,
                ios=PageTransitionTheme.CUPERTINO,
                macos=PageTransitionTheme.ZOOM,
                linux=PageTransitionTheme.ZOOM,
                windows=PageTransitionTheme.FADE_UPWARDS,
            ),
        )

        self.selection_interface_page = SelectionInterface(page)
        self.drowsiness_page = Drowsiness(page)

        self.page.on_route_change = self.route_change
        self.page.go("/")

    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/":
            self.page.views.append(
                View(
                    route="/",
                    controls=[self.selection_interface_page.main()],
                )
            )

        elif self.page.route == "/selection_interface_page":
            self.selection_interface_page.main() #se cambio la página de inicio 
            self.page.views.append(
                View(
                    route="/selection_interface_page",
                    controls=[self.selection_interface_page.main()],
                )
            )

        elif self.page.route == "/drowsiness_page":
            self.page.views.append(
                View(route="/drowsiness_page", controls=[self.drowsiness_page.main()])
            )

        self.page.update()


def main(page: Page):
    MainApp(page)


if __name__ == "__main__":
    app(target=main)
