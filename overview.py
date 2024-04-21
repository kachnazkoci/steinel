import tkinter as tk
from tkinter import filedialog
import json

class TargetDisplayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Steinel GridSensor Overview")
        self.root.geometry("1200x675")  # Set window size

        self.canvas = tk.Canvas(self.root, width=1200, height=675, highlightthickness=0)
        self.canvas.pack()

        # Load background image
        self.background_image = tk.PhotoImage(file="img/background.png")
        self.canvas.create_image(600, 337, image=self.background_image)

        # Draw transparent text
        self.canvas.create_text(170, 50, text="OVERVIEW", font=("Comic Sans MS", 39), fill="white")

        browse_button = tk.Button(self.root, text="BROWSE", font=("Comic Sans MS", 15), command=self.browse_file)
        browse_button.place(x=100, y=100)

        self.json_file_label = self.canvas.create_text(150, 200, text="", font=("Comic Sans MS", 11), fill="white")  # Label for JSON file name

        self.targets = []
        self.total_persons = 0
        self.total_certainty = 0

        # Create text labels for Total Persons and Average Certainty
        self.total_persons_label = self.canvas.create_text(100, 630, text="Total Persons:", font=("Comic Sans MS", 13), fill="white")
        self.total_persons_value = self.canvas.create_text(175, 630, text="0", font=("Comic Sans MS", 13), fill="white")
        self.avg_certainty_label = self.canvas.create_text(280, 630, text="Average Certainty:", font=("Comic Sans MS", 13), fill="white")
        self.avg_certainty_value = self.canvas.create_text(370, 630, text="0", font=("Comic Sans MS", 13), fill="white")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_targets(file_path)

    def load_targets(self, file_path):
        self.targets = []
        self.total_persons = 0
        self.total_certainty = 0

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if "data" in data:
                    self.targets = data["data"]
                    self.draw_targets()
                    self.calculate_stats()
                    self.update_info_label()
                    self.update_json_file_label(file_path)  # Update the label with the JSON file name
                else:
                    print("Invalid JSON format.")
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format.")

    def update_json_file_label(self, file_path):
        # Get the file name from the file path and update the label
        file_name = file_path.split("/")[-1]  # Extract the file name from the file path
        self.canvas.itemconfig(self.json_file_label, text="Loaded JSON file: " + file_name)

    def draw_targets(self):
        for target in self.targets:
            x, y = target["x"], target["y"]
            is_person = target["isPerson"]
            certainty = target["certainty"]

            color = "gray"
            if is_person and certainty > 50:
                color = "red"
                self.total_persons += 1
            elif is_person and certainty <= 50:
                color = "orange"
                self.total_persons += 1
            self.total_certainty += certainty

            # Přepočítat souřadnice na základě nové pozice mřížky
            x = x * 20 + 50
            y = y * 20 + 270

            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color)

        # Draw grid
        self.draw_grid()

    def draw_grid(self):
        # Create grid lines
        for i in range(50, 36 * 20 + 50, 20):  # Rozsah od 50 do 710
            self.canvas.create_line(i, 270, i, 15 * 20 + 270, fill='white', dash=(2, 2))
        for i in range(270, 16 * 20 + 270, 20):  # Rozsah od 270 do 590
            self.canvas.create_line(50, i, 35 * 20 + 50, i, fill='white', dash=(2, 2))

        # Create grid labels
        for i in range(35):  # Rozsah od 0 do 34
            self.canvas.create_text(i * 20 + 60, 260, text=str(i), fill='white', font=('Comic Sans MS', 11))
        for i in range(15):  # Rozsah od 0 do 14
            self.canvas.create_text(40, i * 20 + 280, text=str(i), fill='white', font=('Comic Sans MS', 11))

    def calculate_stats(self):
        if self.targets:
            self.avg_certainty = self.total_certainty / len(self.targets)
        else:
            self.avg_certainty = 0

    def update_info_label(self):
        # Update the Total Persons and Average Certainty values
        self.canvas.itemconfig(self.total_persons_value, text=str(round(self.total_persons)))
        self.canvas.itemconfig(self.avg_certainty_value, text=str(round(self.avg_certainty)))

    def run(self):
        self.root.mainloop()

def main():
    app = TargetDisplayApp()
    app.run()

if __name__ == "__main__":
    main()