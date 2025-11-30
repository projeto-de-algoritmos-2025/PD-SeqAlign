from src.alignment import alignment
from tkinter import messagebox
import tkinter as tk


class App():
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.x, self.y = tk.StringVar(), tk.StringVar()
        self.config = {
            'gap_weight': 1,
            'mism_weight': 1,
            'priority': ['Match', 'Mismatch', 'Gap em X', 'Gap em Y']
        }

        self.root.title("Alinhador de Sequências")
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Alinhador de\nSequências", font=('sylfaen', 16)) \
            .grid(row=0, column=0, pady=(0, 12), sticky='ew')
        
        img = tk.PhotoImage(file="./docs/assets/icons/menu.png")
        menu_bt = tk.Button(frame, image=img, width=12, height=12, command=self.on_config)
        menu_bt.image = img
        menu_bt.grid(row=0, column=0, sticky="se")
        
        tk.Label(frame, text="Sequência X:").grid(row=1, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.x, font=("Consolas", 10)).grid(row=2, column=0, pady=(0, 8), sticky='ew')
        tk.Label(frame, text="Sequência Y:").grid(row=3, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.y, font=("Consolas", 10)).grid(row=4, column=0, pady=(0, 8), sticky='ew')

        tk.Button(frame, text="Alinhar", width=9, command=self.on_align) \
            .grid(row=5, column=0, sticky='sw')
        tk.Button(frame, text="Sair", width=9, command=self.root.destroy) \
            .grid(row=5, column=0, padx=(72, 0), sticky='sw')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)


    def on_align(self):
        if not self.x.get():
            return messagebox.showwarning('String Vazia', f'A string (X) não pode ser vazia!', parent=self.root)
        if not self.y.get():
            return messagebox.showwarning('String Vazia', f'A string (Y) não pode ser vazia!', parent=self.root)
        
        try: 
            a, b, log = alignment(self.config, self.x.get(), self.y.get())
            self.alignment(a, b, log)
        except Exception:
            messagebox.showerror('Erro', f'Ocorreu um erro no alinhamento.', parent=self.root)


    def on_export(self, win, a, b, log):
        try:
            info = f'{'\n'+log['mismatches'] if self.mism_flag else ''}\n\n' \
                   f'matches={log['matches']}, mismatches={log['mismatches'].count('M')}, ' \
                   f'x_gaps={log['x_gaps']}, y_gaps={log['y_gaps']}, ' \
                   f'mism_cost={self.config['mism_weight']}, gap_cost={self.config['gap_weight']}'
            with open(self.path, "w", encoding='utf-8') as f:
                f.write(a + '\n' + b + info)
            messagebox.showinfo('Alinhamento salvo', f'O alinhamento foi salvo em "{self.path}".', parent=win)
        except Exception: 
            messagebox.showerror('Erro', f'Ocorreu um erro ao salvar em "{self.path}".', parent=win)


    def on_config(self):
        win = tk.Toplevel(self.root)
        win.title(f"Configurações")
        win.resizable(False, False), win.grab_set()
        
        gap, mism = tk.IntVar(value=self.config['gap_weight']), tk.IntVar(value=self.config['mism_weight'])

        frame = tk.Frame(win, padx=8, pady=8)
        frame.pack()
        
        tk.Label(frame, text="Configurações", font=('sylfaen', 13)).grid(row=0, column=0, sticky='w')
        img = tk.PhotoImage(file="./docs/assets/icons/help.png")
        help_bt = tk.Button(frame, image=img, width=16, height=16, command=self.on_help)
        help_bt.image = img
        help_bt.grid(row=0, column=1, sticky="e")

        tk.Label(frame, text="Pesos", font=("Arial", 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=(10, 4))
        tk.Label(frame, text="Peso do Gap:").grid(row=2, column=0, sticky='w')
        tk.Label(frame, text="Peso do Mismatch:").grid(row=3, column=0, sticky='w')

        g_spinbox = tk.Spinbox(frame, from_=0, to=float('inf'), textvariable=gap, state="normal", width=4)
        g_spinbox.grid(row=2, column=1, sticky='e')
        g_spinbox = tk.Spinbox(frame, from_=0, to=float('inf'), textvariable=mism, state="normal", width=4)
        g_spinbox.grid(row=3, column=1, sticky='e')

        tk.Label(frame, text="Prioridades", font=("Arial", 10, 'bold')).grid(row=4, column=0, columnspan=2, pady=(10, 4))
        listbox = tk.Listbox(frame, height=3, width=26, justify='center')
        listbox.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky='we')

        def refresh(self):
            if len(listbox.curselection()) and listbox.curselection()[0]:
                p = listbox.curselection()[0]
                top, down = listbox.get(p-1)[3:], listbox.get(p)[3:]
                listbox.insert(p-1, f'{p}. '+down), listbox.insert(p, f'{p+1}. '+top), listbox.delete(p+1, p+2)
            listbox.select_clear(0, tk.END)

        def apply(g, m, p):
            self.config['gap_weight'], self.config['mism_weight'] = g.get(), m.get()
            self.config['priority'] = ['Match'] + [el[3:] for el in p]

        tk.Button(frame, text="Aplicar", width=8, command=lambda: apply(gap, mism, listbox.get(0, tk.END))) \
            .grid(row=6, column=0, columnspan=2, padx=(14, 0), sticky='sw')
        tk.Button(frame, text="Voltar", width=8, command=win.destroy) \
            .grid(row=6, column=0, columnspan=2, padx=(80, 0), sticky='sw')

        listbox.bind("<Button-1>", lambda event: self.root.after(100, refresh, event), add=True)
        for i in range(1, 4): listbox.insert(tk.END, f'{i}. '+self.config['priority'][i])


    def on_help(self):
        help_text = '> Pesos\n' \
                    'O peso é a maneira como\no algoritmo prioriza suas\n' \
                    'ações (gap ou mismatch)\ndurante o alinhamento.\n\n' \
                    '> Prioridades\n' \
                    'A prioridade é o desempate\npara o caso em que custos' \
                    ' de\ngap e mismatch forem iguais.'
        messagebox.showinfo('Ajuda', help_text)


    def highlight(self, text, mism):
        self.mism_flag = not self.mism_flag
        text.config(state='normal')

        if self.mism_flag: text.config(height=3), text.insert('3.0', '\nM: '+mism)
        else: text.delete('3.0', '4.0'), text.config(height=2)

        text.config(state='disabled')


    def alignment(self, a, b, log):
        win = tk.Toplevel(self.root)
        win.title(f"Resultado do Alinhamento")
        win.grab_set()
        
        frame = tk.Frame(win, padx=8, pady=8)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Alinhamento:").grid(row=0, column=0, sticky='w')
        text = tk.Text(frame, height=2, width=32, wrap='none', font=("Consolas", 16))
        text.insert('1.0', 'X: '+a+'\nY: '+b), text.config(state='disabled'), text.grid(row=1, column=0, sticky='we')

        def scroll(event, text_widget):
            if event.delta > 0: text_widget.xview_scroll(-1, "units")
            elif event.delta < 0: text_widget.xview_scroll(1, "units")

        scrollbar = tk.Scrollbar(frame, orient='horizontal', command=text.xview)
        scrollbar.grid(row=2, column=0, sticky='we'), text.config(xscrollcommand=scrollbar.set)
        text.bind("<MouseWheel>", lambda event: scroll(event, text)) # Interação do scroll do mouse (vert.) com a scrollbar (hor.)

        string = f"Custo: {log['cost']} (g: {self.config['gap_weight']}×{log['x_gaps']+log['y_gaps']}, " \
                 f"m: {self.config['mism_weight']}×{log['mismatches'].count('M')})\n" \
                 f"N° de Gaps: {log['x_gaps']+log['y_gaps']} (x: {log['x_gaps']}, y: {log['y_gaps']})\n" \
                 f"N° de Mismatches: {log['mismatches'].count('M')}"
        tk.Label(frame, text=string, justify='left').grid(row=3, column=0, pady=(5, 12), sticky='w')

        self.mism_flag = False
        tk.Checkbutton(frame, text="Destacar Mismatches", command=lambda: self.highlight(text, log['mismatches'])) \
            .grid(row=0, column=0, sticky='e')
        tk.Button(frame, text="Exportar", width=8, command=lambda: self.on_export(win, a, b, log)) \
            .grid(row=4, column=0, sticky='sw')
        tk.Button(frame, text="Voltar", width=8, command=win.destroy) \
            .grid(row=4, column=0, padx=(66, 0), sticky='sw')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(4, weight=1)
