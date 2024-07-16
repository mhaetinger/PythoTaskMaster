import datetime
import pandas as pd
import matplotlib.pyplot as plt

NOME_DO_ARQUIVO = 'tarefas.csv'

def salvar_input(tasks, tempo, id):
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame({
        'Task': tasks,
        'Tempo': [tempo] * len(tasks),
        'ID': id,
        'DataHora': [data_hora] * len(tasks),
        'Check': [False] * len(tasks)
    })
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def concluir_tarefa(tarefa, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO)
    df.loc[(df['Task'] == tarefa) & (df['ID'] == timerID), 'Check'] = True
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def remover_tarefa(tarefa, id):
    df = pd.read_csv(NOME_DO_ARQUIVO)
    df = df[~((df['Task'] == tarefa) & (df['ID'] == id))]
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def desconcluir_tarefa(tarefa, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO)
    df.loc[(df['Task'] == tarefa) & (df['ID'] == timerID), 'Check'] = False
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def listar_tarefas():
    df = pd.read_csv(NOME_DO_ARQUIVO)
    print(df.to_string(index=False)) 

def editar_tarefa(id_tarefa, nova_tarefa):
    df = pd.read_csv(NOME_DO_ARQUIVO)
    if id_tarefa in df['ID'].values:
        df.loc[df['ID'] == id_tarefa, 'Task'] = nova_tarefa
        df.to_csv(NOME_DO_ARQUIVO, index=False)

#listar_tarefas()
#desconcluir_tarefa('Tarefa 2', 2)
#tasks = ['Tarefa 1', 'Tarefa 2', 'Tarefa 3']
#tempo = 15
#id = [1, 2, 3]
#salvar_input(tasks, tempo, id)
#concluir_tarefa('Tarefa 2', 2)
#remover_tarefa('Tarefa 1', 1)

def salvar_no_csv(dados, filename='dados_tarefas.csv'):
    df = pd.DataFrame(dados, columns=['Tempo', 'Task', 'DataHora'])
    df.to_csv(filename, mode='a', header=False, index=False)

def adiciona_coluna_pausa(filename='dados_tarefas.csv'):
    df = pd.read_csv(filename)
    df['HorarioModificacao'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(filename, index=False)

def carregar_dados_csv(filename='dados_tarefas.csv'):
    df = pd.read_csv(filename)
    df['DataHora'] = pd.to_datetime(df['DataHora'])  
    if 'HorarioModificacao' in df.columns:
        df['HorarioModificacao'] = pd.to_datetime(df['HorarioModificacao'])  
    return df

def adicionar_nova_coluna_tempo(novo_tempo, filename='dados_tarefas.csv'):
    df = carregar_dados_csv(filename)
    if df is not None and not df.empty:
        nova_coluna = f'Tempo_{len(df.columns)}'
        df[nova_coluna] = novo_tempo 
        df.to_csv(filename, index=False)

def plotar_tempo_trabalhado(filename='dados_tarefas.csv'):
    df = carregar_dados_csv(filename)
    if df is not None and not df.empty:
        df['DataHora'] = pd.to_datetime(df['DataHora'])
        df['Dia'] = df['DataHora'].dt.date
        tempo_por_dia = df.groupby('Dia')['Tempo'].sum()

        plt.figure(figsize=(10, 6))
        plt.plot(tempo_por_dia.index, tempo_por_dia.values, marker='o', linestyle='-')
        plt.xlabel('Dia')
        plt.ylabel('Tempo Trabalhado (minutos)')
        plt.title('Tempo Trabalhado ao Longo dos Dias')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Nenhum dado encontrado para plotar.")


#criar_csv()
#entrada = input("Uma tarefa: ")
#tempo, tasks, data_hora = armazenar_input(entrada)
#dados = [[tempo, task, data_hora] for task in tasks]
#salvar_no_csv(dados)
#adiciona_coluna_pausa()
#novo_tempo = 55
#adicionar_nova_coluna_tempo(novo_tempo)
#plotar_tempo_trabalhado()
