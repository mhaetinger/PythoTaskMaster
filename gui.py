import tkinter as tk
import tkinter.font as tkFont
import uuid
from tkinter import ttk, messagebox, simpledialog, Frame, colorchooser
import functions


class TaskMaster:

    def __init__(self):
        self.root = tk.Tk()
        self.listaTarefas = []
        self.tarefaSelecionada = None
        self.pomodoroAtivo = tk.BooleanVar()
        self.intervalos = 0
        self.tempoIntervalo = 0
        self.rodando = False
        self.tela()
        self.root.mainloop()

    def tela(self):
        self.root.title("Task Master")
        self.root.configure(background='#1e3743')
        self.root.geometry('500x700')
        self.root.resizable(True, True)
        self.framesTela()

    def fontes(self):
        self.fonteTitulo = tkFont.Font(family='MS Sans Serif', size=36, weight='bold')
        self.fonteCronometro = tkFont.Font(family='MS Sans Serif', size=55, weight='bold')
        self.fonteTituloPequeno = tkFont.Font(family='MS Sans Serif', size=16, weight='bold')
        self.fonteBotoes = tkFont.Font(family='MS Sans Serif', size=14, weight='bold')

    def framesTela(self):
        self.fontes()
        self.style = ttk.Style()
        self.style.configure("Custom.TCheckbutton", background='#1e3743', foreground='white', font=self.fonteBotoes)
        self.style.map("Custom.TCheckbutton", background=[('active', '#1e3743'), ('selected', '#1e3743')])

        self.frameTimer = Frame(self.root, bg='#1e3743')
        self.frameTimer.place(relx=0.5, rely=0.05, anchor='n', relheight=0.25, relwidth=1)
        self.timer()

        self.frameButtons = Frame(self.root, bg='#1e3743')
        self.frameButtons.place(relx=0.5, rely=0.30, anchor='n', relheight=0.2, relwidth=1)
        self.botoesTarefa()

        self.frameTarefas = Frame(self.root, bg='#1e3743', bd=4, relief='ridge')
        self.frameTarefas.place(relx=0.5, rely=0.5, anchor='n', relheight=0.45, relwidth=0.9)
        self.tarefas()

    def tarefas(self):
        self.camadaTarefas = tk.Label(self.frameTarefas, text="Lista de tarefas", font=self.fonteTituloPequeno, bg='#1e3743', fg='white')
        self.camadaTarefas.pack(pady=10)

        self.listaTarefasFrame = Frame(self.frameTarefas, bg='#1e3743')
        self.listaTarefasFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.listaTarefasFrame.bind("<Button-1>", self.desmarcarTarefa)
        self.atualizarListaTarefas()

    def botoesTarefa(self):
        self.progressoBarra = ttk.Progressbar(self.frameButtons, orient="horizontal", length=300, mode="determinate", maximum=60)
        self.progressoBarra.place(relx=0.2, rely=0.0)

        self.botaoAdd = tk.Button(self.frameButtons, text="Add", command=self.addTarefa, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoAdd.place(relx=0.2, rely=0.85, anchor='center', relheight=0.2, relwidth=0.2)

        self.botaoEdit = tk.Button(self.frameButtons, text="Edit", command=self.editTarefa, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoEdit.place(relx=0.4, rely=0.85, anchor='center', relheight=0.2, relwidth=0.2)

        self.botaoDel = tk.Button(self.frameButtons, text="Del", command=self.delTarefa, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoDel.place(relx=0.6, rely=0.85, anchor='center', relheight=0.2, relwidth=0.2)

        self.botaoCor = tk.Button(self.frameButtons, text="Cor", command=self.definirCor, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoCor.place(relx=0.8, rely=0.85, anchor='center', relheight=0.2, relwidth=0.2)

    def atualizarListaTarefas(self):
        self.listaInterface = []
        for tarefas in self.listaTarefasFrame.winfo_children():
            tarefas.destroy()

        for i, (tarefa, lista, cor, id, timerID) in enumerate(self.listaTarefas):
            frame = Frame(self.listaTarefasFrame, bg='#1e3743')
            frame.pack(fill=tk.X, padx=10, pady=2)

            chk = ttk.Checkbutton(frame, variable=lista, style="Custom.TCheckbutton", command=lambda idx=i: self.alternarTarefa(idx))
            chk.pack(side=tk.LEFT)

            camadaTarefas = tk.Label(frame, text=tarefa, font=self.fonteBotoes, bg='#1e3743', fg=cor, anchor='w')
            camadaTarefas.pack(side=tk.LEFT, fill=tk.X, expand=True)
            camadaTarefas.bind("<Button-1>", lambda e, idx=i: self.marcarTarefa(idx))

            self.listaInterface.append((chk, camadaTarefas))

        self.atualizarListaTarefasMarcador()

    def addTarefa(self):
        tarefa = simpledialog.askstring("Adicionar Tarefa", "Qual é a tarefa?")
        if tarefa:
            var = tk.IntVar()
            cor = 'white'
            id = str(uuid.uuid4())
            timerID = str(uuid.uuid4())
            self.listaTarefas.append((tarefa, var, cor, id, timerID))
            functions.salvar_input([tarefa], 0, [id], timerID)
            self.atualizarListaTarefas()

    def editTarefa(self):
        if self.tarefaSelecionada is not None:
            textoTarefaSelecionada, var, cor, id, timerID = self.listaTarefas[self.tarefaSelecionada]
            textoNovaTarefa = simpledialog.askstring("Editar Tarefa", "Edite a tarefa:", initialvalue=textoTarefaSelecionada)
            if textoNovaTarefa:
                self.listaTarefas[self.tarefaSelecionada] = (textoNovaTarefa, var, cor, id, timerID)
                functions.editar_tarefa(id, timerID, textoNovaTarefa)
                self.atualizarListaTarefas()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma tarefa para editar.")

    def delTarefa(self):
        if self.tarefaSelecionada is not None:
            _, _, _, id, timerID = self.listaTarefas[self.tarefaSelecionada]
            del self.listaTarefas[self.tarefaSelecionada]
            functions.remover_tarefa(id, timerID)
            self.atualizarListaTarefas()
            self.tarefaSelecionada = None
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma tarefa para excluir.")

    def marcarTarefa(self, indiceMarcado):
        self.tarefaSelecionada = indiceMarcado
        self.atualizarListaTarefasMarcador()

    def desmarcarTarefa(self, event):
        self.tarefaSelecionada = None
        self.atualizarListaTarefasMarcador()

    def atualizarListaTarefasMarcador(self):
        for i, (chk, lbl) in enumerate(self.listaInterface):
            if i == self.tarefaSelecionada:
                lbl.config(bg='#3b5998')
            else:
                lbl.config(bg='#1e3743')

    def alternarTarefa(self, indice):
        _, var, _, id, timerID = self.listaTarefas[indice]
        if var.get():
            functions.concluir_tarefa(id, timerID)
        else:
            functions.desconcluir_tarefa(id, timerID)

    def definirCor(self):
        if self.tarefaSelecionada is not None:
            cor = colorchooser.askcolor(title="Escolha uma cor")[1]
            if cor:
                textoTarefaSelecionada, var, _, id, timerID = self.listaTarefas[self.tarefaSelecionada]
                self.listaTarefas[self.tarefaSelecionada] = (textoTarefaSelecionada, var, cor, id, timerID)
                self.atualizarListaTarefas()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma tarefa para definir a cor.")

    def finalizarCronometro(self):
        if self.tempoRestante.get() == 0 and not self.rodando:
            messagebox.showerror("Erro", "Inicie o crônometro novamente.")
            return

        self.rodando = False
        self.tempoRestante.set(0)
        self.entradaTimer.config(state='normal')
        self.listaTarefas = []
        self.atualizarListaTarefas()
        self.limpar()

    def limpar(self):
        self.rodando = False
        self.tempoRestante.set(0)
        self.entradaTimer.config(state='normal')
        self.listaTarefas = []
        self.atualizarListaTarefas()
        self.atualizarTimerFormato()
        self.progressoBarra["value"] = self.progressoBarra["maximum"] - self.tempoRestante.get()

    def timer(self):
        self.tempoRestante = tk.IntVar(value=0)
        self.rodando = False

        self.camadaTitulo = tk.Label(self.frameTimer, text="Task Master", font=self.fonteTitulo, bg='#1e3743', fg='white')
        self.camadaTitulo.place(relx=0.5, rely=0.1, anchor='center')

        self.entradaTimer = tk.Entry(self.frameTimer, font=self.fonteCronometro, justify='center', fg='white', bg='#3b4b59', bd=5, relief='sunken', insertbackground='white')
        self.entradaTimer.insert(0, "00:00")
        self.entradaTimer.place(relx=0.5, rely=0.5, anchor='center')

        self.botaoInicar = tk.Button(self.frameTimer, text="Começar", command=self.comecarTimer, font=self.fonteBotoes, bg='#4CAF50', fg='white', padx=10, pady=10)
        self.botaoInicar.place(relx=0.2, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoPausar = tk.Button(self.frameTimer, text="Pausar", command=self.pausarTimer, font=self.fonteBotoes, bg='#FFC107', fg='white', padx=20, pady=10)
        self.botaoPausar.place(relx=0.4, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoLimpar = tk.Button(self.frameTimer, text="Limpar", command=self.limpar, font=self.fonteBotoes, bg='#F44336', fg='white', padx=20, pady=10)
        self.botaoLimpar.place(relx=0.6, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoFinalizar = tk.Button(self.frameTimer, text="Finalizar", command=self.finalizarCronometro, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=20, pady=10)
        self.botaoFinalizar.place(relx=0.8, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoRelatorio = tk.Button(self.frameTimer, text="Relatório", command=self.gerarRelatorio, font=self.fonteBotoes, bg='#3b5998', fg='white', padx=20, pady=10)
        self.botaoRelatorio.place(relx=0.9, rely=0.08, anchor='center', relheight=0.15, relwidth=0.2)

    def comecarTimer(self):
        if not self.rodando:
            iniciarTimer = self.entradaTimer.get()
            if ":" in iniciarTimer:
                try:
                    minutos, segundos = map(int, iniciarTimer.split(":"))
                    total_segundos = minutos * 60 + segundos
                    if total_segundos > 0:
                        self.tempoRestante.set(total_segundos)
                        self.entradaTimer.config(state='disabled', disabledbackground='#3b4b59', disabledforeground='white')
                        self.progressoBarra["maximum"] = total_segundos
                        self.rodando = True
                        self.atualizarTimer()
                    else:
                        messagebox.showerror("Impossível Começar", "O cronômetro está Zerado")
                except ValueError:
                    messagebox.showerror("Tempo errado", "Por favor insira no formato Minutos:Segundos.")
            else:
                messagebox.showerror("Tempo errado", "Por favor insira no formato Minutos:Segundos.")
        else:
            messagebox.showerror("Cronômetro já em execução", "O cronômetro já está rodando")

    def pausarTimer(self):
        if self.tempoRestante.get() == 0 and not self.rodando:
            messagebox.showerror("Impossivel Pausar", "O cronômetro está finalizado")
            return

        if self.rodando:
            self.rodando = False
            self.botaoPausar.config(text="Continuar")
            functions.pausa_timer(self.listaTarefas[self.tarefaSelecionada][4])
        else:
            self.rodando = True
            self.botaoPausar.config(text="Pausar")
            functions.continua_timer(self.listaTarefas[self.tarefaSelecionada][4])
            self.atualizarTimer()

    def atualizarTimer(self):
        if self.rodando:
            if self.tempoRestante.get() > 0:
                minutos, segundos = divmod(self.tempoRestante.get(), 60)
                formatoTimer = f"{minutos:02}:{segundos:02}"
                self.entradaTimer.config(state='normal')
                self.entradaTimer.delete(0, tk.END)
                self.entradaTimer.insert(0, formatoTimer)
                self.entradaTimer.config(state='disabled', disabledbackground='#3b4b59', disabledforeground='white')
                self.tempoRestante.set(self.tempoRestante.get() - 1)
                self.progressoBarra["value"] = self.progressoBarra["maximum"] - self.tempoRestante.get()
                self.root.after(1000, self.atualizarTimer)
            else:
                self.finalizarCronometro()

    def atualizarTimerFormato(self):
        minutos, segundos = divmod(self.tempoRestante.get(), 60)
        formatoTimer = f"{minutos:02}:{segundos:02}"
        self.entradaTimer.delete(0, tk.END)
        self.entradaTimer.insert(0, formatoTimer)

    def gerarRelatorio(self):
        functions.grafico_pizza_resolvidas()

TaskMaster()
