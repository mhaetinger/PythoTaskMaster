import pandas as pd
import matplotlib.pyplot as plt


def criar_arquivo_csv(nome_arquivo, tarefas, tempos):
    # Cria um DataFrame
    df = pd.DataFrame({'Tarefa': tarefas, 'Tempo': tempos})

    # Salva o DataFrame em um arquivo CSV
    df.to_csv(nome_arquivo, index=False)
    print(f"Arquivo {nome_arquivo} criado com sucesso.")


def ler_arquivo_csv(nome_arquivo):
    try:
        df = pd.read_csv(nome_arquivo)

        print(df)
        return df
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return None


def criar_grafico(df):
    # convertendo a coluna 'Tempo' para valores numéricos
    df['Tempo'] = pd.to_numeric(df['Tempo'])

    plt.figure(figsize=(10, 6))
    plt.bar(df['Tarefa'], df['Tempo'], color='blue')

    plt.title('Tempo por Tarefa')
    plt.xlabel('Tarefa')
    plt.ylabel('Tempo (minutos)')

    plt.show()


def main():
    # Solicita os dados do usuário
    tarefas = []
    tempos = []

    for i in range(2):
        tarefa = input(f"Digite a tarefa {i + 1}: ")
        tempo = input(f"Digite o tempo para a tarefa {i + 1} (em minutos): ")

        tarefas.append(tarefa)
        tempos.append(tempo)

    # nome do arquivo CSV
    nome_arquivo = "tarefas.csv"

    # cria o arquivo CSV
    criar_arquivo_csv(nome_arquivo, tarefas, tempos)

    # le o arquivo CSV
    df = ler_arquivo_csv(nome_arquivo)

    # cria o gráfico
    if df is not None:
        criar_grafico(df)


# Executa a função main
main()
