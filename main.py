import tkinter as tk
from tkinter import filedialog
import json
import time

class TargetDisplayApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Target Display App")

        # První prázdný řádek
        tk.Label(master, text="").grid(row=0, column=0, columnspan=2)

        # Tlačítko
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=1, column=0, columnspan=2)

        # 20px mezera
        tk.Label(master, text="").grid(row=2, column=0, columnspan=2)

        # Popisek
        self.info_label = tk.Label(master, text="Choose JSON file to display")
        self.info_label.grid(row=3, column=0, columnspan=2)

        # Mřížka
        self.canvas = tk.Canvas(master, width=700, height=300, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=2)

        # Další prázdný řádek
        tk.Label(master, text="").grid(row=5, column=0, columnspan=2)

        # Text s čísly
        self.info_text = tk.Label(master, text="")
        self.info_text.grid(row=6, column=0, columnspan=2)

        # Poslední prázdný řádek
        tk.Label(master, text="").grid(row=7, column=0, columnspan=2)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_targets(file_path)

    def load_targets(self, file_path):
        self.canvas.delete("all")
        self.info_label.config(text="Loading targets...")

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if "data" in data:
                    self.targets = data["data"]
                    self.draw_targets()
                    self.calculate_stats()
                    self.update_info_label()
                else:
                    self.info_label.config(text="Invalid JSON format.")
        except FileNotFoundError:
            self.info_label.config(text="File not found.")
        except json.JSONDecodeError:
            self.info_label.config(text="Invalid JSON format.")

    def draw_targets(self):
        for target in self.targets:
            x, y = target["x"], target["y"]
            is_person = target["isPerson"]
            certainty = target["certainty"]

            color = "gray"  # default color for non-person targets
            if is_person and certainty > 50:
                color = "red"
            elif is_person and certainty <= 50:
                color = "orange"

            self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill=color)

            # draw grid
            self.draw_grid()
            time.sleep(0.05)  # delay for slower drawing

    def draw_grid(self):
        # draw grid lines
        for i in range(0, 700, 20):
            self.canvas.create_line(0, i, 700, i, fill='gray', dash=(2, 2))
            self.canvas.create_line(i, 0, i, 300, fill='gray', dash=(2, 2))

        # draw grid labels
        for i in range(35):
            self.canvas.create_text(i * 20 + 10, 10, text=str(i), fill='black', font=('Arial', 8))
            self.canvas.create_text(10, i * 20 + 10, text=str(i), fill='black', font=('Arial', 8))

    def calculate_stats(self):
        self.total_persons = sum(1 for target in self.targets if target["isPerson"])
        self.avg_certainty = sum(target["certainty"] for target in self.targets) / len(self.targets) if self.targets else 0

    def update_info_label(self):
        info_text = f"Total Persons: {round(self.total_persons)}\tAverage Certainty: {round(self.avg_certainty)}"
        self.info_text.config(text=info_text)


def main():
    root = tk.Tk()
    app = TargetDisplayApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
