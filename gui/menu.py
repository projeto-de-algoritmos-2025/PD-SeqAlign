from src.alignment import alignment
from tkinter import messagebox, simpledialog
import tkinter as tk


class App():
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.a, self.b = tk.StringVar(), tk.StringVar()

        self.root.title("Alinhador de Sequências")
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Alinhador de\nSequências", font='sylfaen') \
            .grid(row=0, column=0, pady=(0, 12), sticky='ew')
        
        img = tk.PhotoImage(file="./docs/assets/menu.png")
        menu_bt = tk.Button(frame, image=img, width=12, height=12, command=self.set_order)
        menu_bt.image = img
        menu_bt.grid(row=0, column=0, sticky="se")
        
        tk.Label(frame, text="Sequência A:").grid(row=1, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.a).grid(row=2, column=0, pady=(0, 8), sticky='ew')
        tk.Label(frame, text="Sequência B:").grid(row=3, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.b).grid(row=4, column=0, pady=(0, 8), sticky='ew')

        tk.Button(frame, text="Alinhar", width=8, command=self.on_align) \
            .grid(row=5, column=0, sticky='sw')
        tk.Button(frame, text="Sair", width=8, command=self.root.destroy) \
            .grid(row=5, column=0, padx=(66, 0), sticky='sw')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)


    def on_align(self):
        if not self.a.get():
            return messagebox.showwarning('String Vazia', f'A string (a) não pode ser vazia!', parent=self.root)
        if not self.b.get():
            return messagebox.showwarning('String Vazia', f'A string (b) não pode ser vazia!', parent=self.root)
        
        try: 
            a, b, log = alignment(self.a.get(), self.b.get())
            self.alignment(a, b, log)
        except Exception:
            messagebox.showerror('Erro', f'Ocorreu um erro no alinhamento.', parent=self.root)


    def alignment(self, a, b, log):
        win = tk.Toplevel(self.root)
        win.title(f"Resultado do Alinhamento")
        win.grab_set()
        
        frame = tk.Frame(win, padx=8, pady=8)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Alinhamento:").grid(row=0, column=0, sticky='w')
        text = tk.Text(frame, height=2, width=32, wrap='word', font=("Arial", 16))
        text.insert('1.0', a+'\n'+b), text.config(state='disabled')
        text.grid(row=1, column=0, pady=(0, 8), sticky='ew')

        string = f"N° de Gaps: {log['gaps']}\nN° de Mismatches: {log['mism']}"
        tk.Label(frame, text=string, justify='left').grid(row=2, column=0, pady=(0, 12), sticky='w')

        tk.Button(frame, text="Exportar", width=8, command=lambda: self.on_export(win, a, b, log)).grid(row=5, column=0, sticky='sw')
        tk.Button(frame, text="Voltar", width=8, command=win.destroy).grid(row=5, column=0, padx=(66, 0), sticky='sw')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(3, weight=1)


    def on_export(self, win, a, b, log):
        try:
            with open(self.path, "w") as f:
                f.write(a + '\n' + b + f'\n\ng={log['gaps']}, m={log['mism']}')
            messagebox.showinfo('Alinhamento salvo', f'O alinhamento foi salvo em "{self.path}".', parent=win)
        except Exception: 
            messagebox.showerror('Erro', f'Ocorreu um erro ao salvar em "{self.path}".', parent=win)


    def set_order(self):
        messagebox.showinfo('Ordem de alinhamento', f'WIP', parent=self.root)