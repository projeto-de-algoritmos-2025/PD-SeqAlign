from tkinter import messagebox, simpledialog
import tkinter as tk


class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Alinhador de Sequências")

        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill='both', expand=True)

        self.a, self.b = tk.StringVar(), tk.StringVar()

        def validate_str(char, string):
            return len(string) <= 20 or char == ''
        val_str = self.root.register(validate_str)

        tk.Label(frame, text="Alinhador de\nSequências", font='sylfaen') \
            .grid(row=0, column=0, pady=(0, 12), sticky='ew')
        
        img = tk.PhotoImage(file="./docs/assets/menu.png")
        menu_bt = tk.Button(frame, image=img, width=12, height=12, command=self.root.destroy)
        menu_bt.image = img
        menu_bt.grid(row=0, column=0, sticky="se")
        
        tk.Label(frame, text="Sequência A:").grid(row=1, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.a).grid(row=2, column=0, pady=(0, 8), sticky='ew')
        tk.Label(frame, text="Sequência B:").grid(row=3, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.b).grid(row=4, column=0, pady=(0, 8), sticky='ew')

        tk.Button(frame, text="Alinhar", width=8, command=self.root.destroy) \
            .grid(row=5, column=0, sticky='sw')
        tk.Button(frame, text="Sair", width=8, command=self.root.destroy) \
            .grid(row=5, column=0, padx=(66, 0), sticky='sw')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)