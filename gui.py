import tkinter as tk
from tkinter import messagebox
from tkinter import Frame

class TaskMaster:

    #PRIN
    def __init__(self):
        self.root = root = tk.Tk()
        self.tela() # chama a função tela
        self.framesTela()
        root.mainloop()

    def tela(self):
        self.root.title("Task Master")
        self.root.configure(background='#1e3743') # cor de fundo #1e3743
        self.root.geometry('500x700') # tamanho inicial padrao
        self.root.resizable(True, True) # se ajusta
        self.root.maxsize(800, 900)  # tamanho maximo
        self.root.minsize(500,700) # tamanho minimo

    def framesTela(self):
        # Frame do timer (parte superior)
        self.frameTimer = Frame(self.root, bg='#1e3743')
        self.frameTimer.place(relx=0.5, rely=0.10, anchor='center', relheight=0.2, relwidth=1)
        self.timer() # chama a função time

        # Frame das tarefas (parte inferior interna)
        self.frameTasks = Frame(self.root, bg='#182c35', bd=4, relief='ridge')
        self.frameTasks.place(relx=0.5, rely=0.75, anchor='center', relheight=0.7, relwidth=0.9)


    def timer(self):
        self.tempoRestante = tk.IntVar(value=3600)  # Valor inicial de uma hora
        self.running = False

        self.entradaTimer = tk.Entry(self.frameTimer, font=("Helvetica", 55), justify='center', fg='white', bg='#1e3743', bd=2, insertbackground='white')
        self.entradaTimer.insert(0, "60:00")
        self.entradaTimer.place(relx=0.4, rely=0.5, anchor='center', relheight=0.5, relwidth=0.5)

        #botão de começar
        self.botaoInicar = tk.Button(self.frameTimer, text="Começar", command=self.comecarTimer, font=("Helvetica", 14), bg='#4CAF50', fg='white', padx=10, pady=10)
        self.botaoInicar.place(relx=0.8, rely=0.2, anchor='center', relheight=0.2, relwidth=0.2)

        #botão de pausar
        self.botaoPausar = tk.Button(self.frameTimer, text="Pausar", command=self.pausarTimer, font=("Helvetica", 14), bg='#FFC107', fg='white', padx=20, pady=10)
        self.botaoPausar.place(relx=0.8, rely=0.45, anchor='center', relheight=0.2, relwidth=0.2)

        #botão de parar
        self.botaoParar = tk.Button(self.frameTimer, text="Parar", command=self.pararTimer, font=("Helvetica", 14), bg='#F44336', fg='white', padx=20, pady=10)
        self.botaoParar.place(relx=0.8, rely=0.7, anchor='center', relheight=0.2, relwidth=0.2)



    def comecarTimer(self):
        if not self.running:
            try:
                iniciarTimer = self.entradaTimer.get() #pega valor colocado pelo usuario
                minutos, segundos = map(int, iniciarTimer.split(":"))
                self.tempoRestante.set(minutos * 60 + segundos)
                self.entradaTimer.config(state='disabled', disabledbackground='#1e3743', disabledforeground='white')
            except ValueError:
                messagebox.showerror("Tempo errado", "Por favor insira no formato Minutos:Segundos.")
                return
        self.running = True
        self.atualizarTimer()

    def pausarTimer(self):
        self.running = False

    def pararTimer(self):
        self.running = False
        self.tempoRestante.set(0) # volta pra zero
        self.entradaTimer.config(state='normal')
        self.atualizarTimerFormato()

    def atualizarTimer(self):
        if self.running:
            if self.tempoRestante.get() > 0:
                minutos, segundos = divmod(self.tempoRestante.get(), 60)
                formatoTimer = f"{minutos:02}:{segundos:02}"
                self.entradaTimer.config(state='normal')
                self.entradaTimer.delete(0, tk.END)
                self.entradaTimer.insert(0, formatoTimer)
                self.entradaTimer.config(state='disabled', disabledbackground='#1e3743', disabledforeground='white')
                self.tempoRestante.set(self.tempoRestante.get() - 1)
                self.root.after(1000, self.atualizarTimer)
            else:
                self.running = False
                messagebox.showinfo("Acabou o tempo!", "Tarefas fechadas.")
                self.entradaTimer.config(state='normal')

    def atualizarTimerFormato(self):
        minutos, segundos = divmod(self.tempoRestante.get(), 60)
        formatoTimer = f"{minutos:02}:{segundos:02}"
        self.entradaTimer.delete(0, tk.END)
        self.entradaTimer.insert(0, formatoTimer)



TaskMaster()
