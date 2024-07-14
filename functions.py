import datetime
import pandas as pd
import matplotlib.pyplot as plt

def armazenar_input(entrada):
    tempo_str, tasks_str = entrada.split(", ")
    tempo = int(tempo_str.strip())
    tasks = [task.strip() for task in tasks_str.split(";")]
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return tempo, tasks, data_hora

def criar_csv(filename='dados_tarefas.csv'):
    df = pd.DataFrame(columns=['Tempo', 'Task', 'DataHora'])
    df.to_csv(filename, index=False)

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
#entrada = "30, olhar filme; pipoca"
#tempo, tasks, data_hora = armazenar_input(entrada)
#dados = [[tempo, task, data_hora] for task in tasks]
#salvar_no_csv(dados)
#adiciona_coluna_pausa()
#novo_tempo = 55
#adicionar_nova_coluna_tempo(novo_tempo)
#plotar_tempo_trabalhado()
