import tkinter as tk
from tkinter import filedialog
import json
import time

class TargetDisplayApp:
    def __init__(self):
        # Create Tkinter window for displaying points
        self.root = tk.Tk()
        self.root.title("Target Display App")
        self.root.geometry("800x500")  # Set initial window size

        # First row: empty
        print("\n")
        print("\n")
        print("\n")

        # Second row: BROWSE Button and text "Choose JSON file to display"
        self.browse_button = tk.Button(self.root, text="BROWSE", command=self.browse_file)
        self.browse_button.place(x=20, y=5)  # Button is 5px from the edge of the window
        self.choose_json_label = tk.Label(self.root, text="Choose JSON file to display")
        self.choose_json_label.place(x=100, y=10)  # Text is 10px from the button

        # Third row: empty
        print()

        # Fourth row: Canvas with drawn targets...canvas, a button and the texts are moved the way I like it better
        self.canvas = tk.Canvas(self.root, width=700, height=300, bg="white")
        self.canvas.place(x=30, y=40)  # Canvas starts 20px from the edge of he window

        # Fifth row: empty
        print()

        # Sixth row: Total Persons and Average certainty
        self.total_persons_label = tk.Label(self.root, text="Total Persons:")
        self.total_persons_label.place(x=20, y=360)  # Text is 20px from the edge of the window
        self.total_persons_value = tk.Label(self.root, text="0")
        self.total_persons_value.place(x=100, y=360)  # Value is farther from the text
        self.avg_certainty_label = tk.Label(self.root, text="Average Certainty:")
        self.avg_certainty_label.place(x=125, y=360)  # Text is farther from the previous label
        self.avg_certainty_value = tk.Label(self.root, text="0")
        self.avg_certainty_value.place(x=230, y=360)  # Value is farther from the text
        self.total_persons_label.place_forget()
        self.total_persons_value.place_forget()
        self.avg_certainty_label.place_forget()
        self.avg_certainty_value.place_forget()

        # Seventh row: empty
        print()

        self.targets = []
        self.total_persons = 0
        self.total_certainty = 0

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_targets(file_path)
            # Show Total Persons and Average Certainty labels after loading targets
            self.total_persons_label.place(x=20, y=360)
            self.total_persons_value.place(x=100, y=360)
            self.avg_certainty_label.place(x=125, y=360)
            self.avg_certainty_value.place(x=230, y=360)

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
                else:
                    print("Invalid JSON format.")
        except FileNotFoundError:
            print("File not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format.")

    def draw_targets(self):
        self.canvas.delete("all")
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

            self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill=color)

            # draw grid
            self.draw_grid()
            time.sleep(0.05)

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
        if self.targets:
            self.avg_certainty = self.total_certainty / len(self.targets)
        else:
            self.avg_certainty = 0

    def update_info_label(self):
        self.total_persons_value.config(text=str(round(self.total_persons)))
        self.avg_certainty_value.config(text=str(round(self.avg_certainty)))

    def run(self):
        self.root.mainloop()


def main():
    app = TargetDisplayApp()
    app.run()


if __name__ == "__main__":
    main()
