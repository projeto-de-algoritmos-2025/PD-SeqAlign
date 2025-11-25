from gui.menu import App
import tkinter as tk

OUTPUT_PATH = 'output.txt'

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, OUTPUT_PATH)
    root.mainloop()