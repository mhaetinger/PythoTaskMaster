import tkinter as tk
from tkinter import messagebox, simpledialog, Frame, filedialog
import csv

class TaskMaster:

    def __init__(self):

        self.root = tk.Tk() # iniciar a interface
        self.listaTarefas = []
        self.tarefaSelecionada = None # em qual tarefa esta marcada
        self.rodando = False  # se o programa esta rodando
        self.tela() # executa a tela
        self.root.mainloop() # roda loop principal

    # função telas
    def tela(self):
        self.root.title("Task Master")
        self.root.configure(background='#1e3743')
        self.root.geometry('500x700')
        self.root.resizable(True, True)
        self.root.maxsize(800, 900)
        self.root.minsize(500, 700)
        self.framesTela() # executa os frames

    # função para os frames
    def framesTela(self):

        # frame encarregado pela frame do timer
        self.frameTimer = Frame(self.root, bg='#1e3743')
        self.frameTimer.place(relx=0.5, rely=0.05, anchor='n', relheight=0.25, relwidth=1)
        self.timer()

        # frame para os botões das tarefass
        self.frameButtons = Frame(self.root, bg='#1e3743')
        self.frameButtons.place(relx=0.5, rely=0.35, anchor='n', relheight=0.2, relwidth=1)
        self.botoesTarefa()

        # frame para as tarefass
        self.frameTarefas = Frame(self.root, bg='#1e3743', bd=4, relief='ridge')
        self.frameTarefas.place(relx=0.5, rely=0.5, anchor='n', relheight=0.45, relwidth=0.9)
        self.tarefas()

    #função das tarefas
    def tarefas(self):

        self.labelTarefas = tk.Label(self.frameTarefas, text="Lista de tarefas", font=("Helvetica", 16), bg='#1e3743', fg='white')
        self.labelTarefas.pack(pady=10)

        self.listaTarefasFrame = Frame(self.frameTarefas, bg='#1e3743')
        self.listaTarefasFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # desmarca ao clicar no espaço em branco
        self.listaTarefasFrame.bind("<Button-1>", self.desmarcarTarefa)
        # atualiza a lista de tarefas
        self.atualizarListaTarefas()

    #função dos botoes de tarefas
    def botoesTarefa(self):
        #texto tarefas
        self.labelTarefas = tk.Label(self.frameButtons, text="Tarefas", font=("Helvetica", 24), bg='#1e3743', fg='white')
        self.labelTarefas.place(relx=0.5, rely=0.1, anchor='center', relheight=1, relwidth=1)

        self.botaoAdd = tk.Button(self.frameButtons, text="Add", command=self.addTarefa, font=("Helvetica", 14), bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoAdd.place(relx=0.3, rely=0.6, anchor='center', relheight=0.4, relwidth=0.2)

        self.botaoEdit = tk.Button(self.frameButtons, text="Edit", command=self.editTarefa, font=("Helvetica", 14), bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoEdit.place(relx=0.5, rely=0.6, anchor='center', relheight=0.4, relwidth=0.2)

        self.botaoDel = tk.Button(self.frameButtons, text="Del", command=self.delTarefa, font=("Helvetica", 14), bg='#3b5998', fg='white', padx=10, pady=10)
        self.botaoDel.place(relx=0.7, rely=0.6, anchor='center', relheight=0.4, relwidth=0.2)

    # atualiza lista de tarefa
    def atualizarListaTarefas(self):

        # cria uma lista de Widget filhos
        self.listaInterface = []


        for tarefas in self.listaTarefasFrame.winfo_children():
            tarefas.destroy()

        for i, (tarefa, lista) in enumerate(self.listaTarefas):
            frame = Frame(self.listaTarefasFrame, bg='#1e3743')
            frame.pack(fill=tk.X, padx=10, pady=2)

            chk = tk.Checkbutton(frame, variable=lista, font=("Helvetica", 14), bg='#1e3743', fg='white', selectcolor='#4CAF50', anchor='w')
            chk.pack(side=tk.LEFT)

            tarefas_label = tk.Label(frame, text=tarefa, font=("Helvetica", 14), bg='#1e3743', fg='white', anchor='w')
            tarefas_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tarefas_label.bind("<Button-1>", lambda e, idx=i: self.marcarTarefa(idx))

            self.listaInterface.append((chk, tarefas_label))

        self.atualizarListaTarefasMarcador()

    def addTarefa(self):
        tarefas = simpledialog.askstring("Adicionar Tarefa", "Qual é a tarefa?")
        if tarefas:
            var = tk.IntVar()
            self.listaTarefas.append((tarefas, var))
            self.atualizarListaTarefas()

    def editTarefa(self):
        if self.tarefaSelecionada is not None:
            selected_tarefas_text, var = self.listaTarefas[self.tarefaSelecionada]
            textoNovaTarefa = simpledialog.askstring("Editar Tarefa", "Edite a tarefa:", initialvalue=selected_tarefas_text)
            if textoNovaTarefa:
                self.listaTarefas[self.tarefaSelecionada] = (textoNovaTarefa, var)
                self.atualizarListaTarefas()
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma tarefa para editar.")

    def delTarefa(self):
        if self.tarefaSelecionada is not None:
            del self.listaTarefas[self.tarefaSelecionada]
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

    def finalizarCronometro(self):
        self.rodando = False
        pontos = self.calcularPontos()
        self.gerarRelatorio(pontos)
        messagebox.showinfo("Pontuação Final", f"Sua pontuação final é: {pontos} pontos")
        self.tempoRestante.set(0)
        self.entradaTimer.config(state='normal')
        self.listaTarefas = []
        self.atualizarListaTarefas()

    def limpar(self):
        self.rodando = False
        self.tempoRestante.set(0)
        self.entradaTimer.config(state='normal')
        self.listaTarefas = []
        self.atualizarListaTarefas()
        self.atualizarTimerFormato()

    def calcularPontos(self):
        pontosTarefas = sum(lista.get() for tarefa, lista in self.listaTarefas) * 10
        minutosRestantes = self.tempoRestante.get() // 60
        pontosTempo = minutosRestantes * 2
        return pontosTarefas + pontosTempo

    def gerarRelatorio(self, pontos):
        tarefasRealizadas = [tarefas for tarefas, lista in self.listaTarefas if lista.get() == 1]
        tarefasNaoRealizadas = [tarefas for tarefas, lista in self.listaTarefas if lista.get() == 0]

        caminhoArquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Salvar relatório")
        if not caminhoArquivo:
            return

        with open(caminhoArquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tarefas Realizadas'])
            for tarefa in tarefasRealizadas:
                writer.writerow([tarefa])
            writer.writerow([])
            writer.writerow(['Tarefas Não Realizadas'])
            for tarefa in tarefasNaoRealizadas:
                writer.writerow([tarefa])
            writer.writerow([])
            writer.writerow(['Pontuação Total', pontos])

        messagebox.showinfo("Relatório", f"Relatório gerado: {caminhoArquivo}")


    def timer(self):
        self.tempoRestante = tk.IntVar(value=60) #recebe o valor em segundos para a variavel tempoRestante
        self.rodando = False # timer parado

        self.camadaTitulo = tk.Label(self.frameTimer, text="Task Master", font=("Helvetica", 24, 'bold'), bg='#1e3743', fg='white')
        self.camadaTitulo.place(relx=0.5, rely=0.1, anchor='center')

        self.entradaTimer = tk.Entry(self.frameTimer, font=("Helvetica", 55), justify='center', fg='white', bg='#3b4b59', bd=5, relief='sunken', insertbackground='white')
        self.entradaTimer.insert(0, "01:00")
        self.entradaTimer.place(relx=0.5, rely=0.5, anchor='center')

        self.botaoInicar = tk.Button(self.frameTimer, text="Começar", command=self.comecarTimer, font=("Helvetica", 14), bg='#4CAF50', fg='white', padx=10, pady=10)
        self.botaoInicar.place(relx=0.2, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoPausar = tk.Button(self.frameTimer, text="Pausar", command=self.pausarTimer, font=("Helvetica", 14), bg='#FFC107', fg='white', padx=20, pady=10)
        self.botaoPausar.place(relx=0.4, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoLimpar = tk.Button(self.frameTimer, text="Limpar", command=self.limpar, font=("Helvetica", 14), bg='#F44336', fg='white', padx=20, pady=10)
        self.botaoLimpar.place(relx=0.6, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

        self.botaoFinalizar = tk.Button(self.frameTimer, text="Finalizar", command=self.finalizarCronometro, font=("Helvetica", 14), bg='#3b5998', fg='white', padx=20, pady=10)
        self.botaoFinalizar.place(relx=0.8, rely=0.85, anchor='center', relheight=0.15, relwidth=0.2)

    def comecarTimer(self):
        if not self.rodando:
            try:
                iniciarTimer = self.entradaTimer.get() # se o tempo é maior que zero
                minutos, segundos = map(int, iniciarTimer.split(":")) #separa o time pelos dois pontos
                self.tempoRestante.set(minutos * 60 + segundos) # converte o tempo inserido para segundos
                self.entradaTimer.config(state='disabled', disabledbackground='#3b4b59', disabledforeground='white')
            except ValueError:
                messagebox.showerror("Tempo errado", "Por favor insira no formato Minutos:Segundos.")
                return
        self.rodando = True
        self.atualizarTimer()

    def pausarTimer(self):
        self.rodando = False

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
                self.root.after(1000, self.atualizarTimer)
            else:
                self.finalizarCronometro()

    def atualizarTimerFormato(self):
        minutos, segundos = divmod(self.tempoRestante.get(), 60)
        formatoTimer = f"{minutos:02}:{segundos:02}"
        self.entradaTimer.delete(0, tk.END)
        self.entradaTimer.insert(0, formatoTimer)

TaskMaster()
