import tkinter as tk
from customtkinter import CTkLabel, CTkButton

class Interfaz:
    def __init__(self, results):
        self.window = tk.Tk()
        self.results = results

    def setup_ui(self):
        self.window.title("Resultados del Test de Gestos")
        self.window.geometry("400x300")

        label = CTkLabel(self.window, text="Resultados del Test", font=("Arial", 16))
        label.pack(pady=10)

        for letra, precision in self.results.items():
            result_label = CTkLabel(self.window, text=f"Letra {letra}: {precision}%")
            result_label.pack()

        close_button = CTkButton(self.window, text="Cerrar", command=self.window.quit)
        close_button.pack(pady=10)

    def main(self):
        self.setup_ui()
        self.window.mainloop()

if __name__ == "__main__":
    # Supongamos que los resultados son un diccionario con letras como claves y precisiones como valores
    resultados = {'A': 85, 'B': 90, 'C': 75, 'D': 80}

    interfaz = Interfaz(resultados)
    interfaz.main()
