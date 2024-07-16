import datetime
import pandas as pd
import matplotlib.pyplot as plt

NOME_DO_ARQUIVO = 'tarefas.csv'

def salvar_input(tasks, tempo, id, timerID):
    data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df_novo = pd.DataFrame({
        'Task': tasks,
        'Tempo': [tempo] * len(tasks),
        'ID': id,
        'timerID': [str(timerID)] * len(tasks),
        'DataHora': [data_hora] * len(tasks),
        'Check': [False] * len(tasks),
        'Pontuacao': [0] * len(tasks)
    })
    
    try:
        df = pd.read_csv(NOME_DO_ARQUIVO)
        df = pd.concat([df, df_novo], ignore_index=True)
    except FileNotFoundError:
        df = df_novo
    
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def concluir_tarefa(id, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    df.loc[(df['ID'] == str(id)) & (df['timerID'] == str(timerID)), 'Check'] = True
    df.to_csv(NOME_DO_ARQUIVO, index=False)
    atualizar_pontuacao(id, timerID)

def remover_tarefa(id, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    df = df[~((df['ID'] == str(id)) & (df['timerID'] == str(timerID)))]
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def desconcluir_tarefa(id, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    df.loc[(df['ID'] == str(id)) & (df['timerID'] == str(timerID)), 'Check'] = False
    df.to_csv(NOME_DO_ARQUIVO, index=False)
    atualizar_pontuacao(id, timerID)

def listar_tarefas():
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    print(df.to_string(index=False))
    
def somar_pontos_por_timerID(timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO)
    df_filtrado = df[df['timerID'] == timerID]
    soma_pontos = df_filtrado['Pontuacao'].sum()
    return soma_pontos

def editar_tarefa(id, timerID, nova_tarefa):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    if str(id) in df['ID'].values and str(timerID) in df['timerID'].values:
        df.loc[(df['ID'] == str(id)) & (df['timerID'] == str(timerID)), 'Task'] = nova_tarefa
        df.to_csv(NOME_DO_ARQUIVO, index=False)

def pausa_timer(timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    data_hora_pausa = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.loc[df['timerID'] == str(timerID), 'DataHoraPausa'] = data_hora_pausa
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def continua_timer(timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    data_hora_continuacao = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.loc[df['timerID'] == str(timerID), 'DataHoraContinuacao'] = data_hora_continuacao
    df.to_csv(NOME_DO_ARQUIVO, index=False)

def concluir_timer(timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    data_hora_conclusao = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.loc[df['timerID'] == str(timerID), 'DataHoraConclusao'] = data_hora_conclusao
    df.to_csv(NOME_DO_ARQUIVO, index=False)
    total_pontos = somar_pontos_por_timerID(timerID)
    #print(f"Total de Pontos: {total_pontos}")
    return total_pontos


def atualizar_pontuacao(id, timerID):
    df = pd.read_csv(NOME_DO_ARQUIVO, dtype={'ID': str, 'timerID': str})
    for index, row in df.iterrows():
        if row['ID'] == str(id) and row['timerID'] == str(timerID):
            if row['Check']:
                df.at[index, 'Pontuacao'] += 1  # Adiciona 1 ponto se a tarefa estiver concluída
            else:
                df.at[index, 'Pontuacao'] = 0
    df.to_csv(NOME_DO_ARQUIVO, index=False)

#tasks = ['Tarefa 1', 'Tarefa 2', 'Tarefa 3']
#tempo = 15
#timerID = '3'
#id = ['4', '5', '6']
#salvar_input(tasks, tempo, id, timerID)
#concluir_tarefa('4', '3')


def carregar_dados_csv(filename='dados_tarefas.csv'):
    df = pd.read_csv(filename)
    df['DataHora'] = pd.to_datetime(df['DataHora'])  
    if 'HorarioModificacao' in df.columns:
        df['HorarioModificacao'] = pd.to_datetime(df['HorarioModificacao'])  
    return df

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
