import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv
from datetime import datetime

# Função para criar a tabela de vendas no banco de dados
def criar_tabela_vendas():
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT,
                        hora TEXT,
                        valor REAL,
                        produtos TEXT
                    )''')
    conexao.commit()
    conexao.close()

# Função para inserir uma venda no banco de dados
def inserir_venda(data, hora, valor, produtos):
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO vendas (data, hora, valor, produtos) VALUES (?, ?, ?, ?)", (data, hora, valor, produtos))
    conexao.commit()
    conexao.close()

# Função para calcular o total das vendas em um determinado período
def calcular_total_vendas(data_inicio, data_fim):
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM(valor) FROM vendas WHERE data BETWEEN ? AND ?", (data_inicio, data_fim))
    total_vendas = cursor.fetchone()[0]
    conexao.close()
    return total_vendas if total_vendas else 0

# Função para exportar os dados para um arquivo CSV
def exportar_dados_para_arquivo(nome_arquivo):
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT data, hora, valor, produtos FROM vendas")
    dados = cursor.fetchall()
    conexao.close()

    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        cabecalho = ['Data', 'Hora', 'Valor', 'Produtos']
        writer = csv.writer(arquivo_csv)
        writer.writerow(cabecalho)
        for venda in dados:
            writer.writerow(venda)

# Função para exibir relatórios de vendas
def exibir_relatorio_vendas():
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT data, hora, valor, produtos FROM vendas")
    dados = cursor.fetchall()
    conexao.close()

    relatorio = "Relatório de Vendas:\n" + "-" * 30 + "\n"
    for venda in dados:
        relatorio += f"Data: {venda[0]}, Hora: {venda[1]}, Valor: R${venda[2]:.2f}, Produtos: {venda[3]}\n"
    return relatorio

# Função para obter as vendas do dia atual
def obter_vendas_do_dia():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    conexao = sqlite3.connect("padex.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT data, hora, valor, produtos FROM vendas WHERE data = ?", (data_atual,))
    dados = cursor.fetchall()
    conexao.close()
    return dados

# Função para atualizar a lista de vendas do dia atual
def atualizar_lista_vendas_do_dia():
    lista_vendas.delete(0, tk.END)
    vendas_do_dia = obter_vendas_do_dia()
    for venda in vendas_do_dia:
        lista_vendas.insert(tk.END, f"{venda[0]} {venda[1]} | Valor: R${venda[2]:.2f} | Produtos: {venda[3]}")


# Função para lidar com o botão "Registrar Venda"
def registrar_venda():
    data = entry_data.get()
    hora = entry_hora.get()
    valor = entry_valor.get()
    produtos = entry_produtos.get()

    if not data or not hora or not valor or not produtos:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Certifique-se de digitar um número válido.")
        return

    inserir_venda(data, hora, valor, produtos)
    messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
    atualizar_lista_vendas_do_dia()

# Função para lidar com o botão "Calcular Total de Vendas"
def calcular_total():
    data_inicio = entry_data_inicio.get()
    data_fim = entry_data_fim.get()

    if not data_inicio or not data_fim:
        messagebox.showerror("Erro", "Por favor, preencha as datas de início e fim.")
        return

    try:
        datetime.strptime(data_inicio, "%d/%m/%Y")
        datetime.strptime(data_fim, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use o formato dd/mm/aaaa.")
        return

    total_vendas = calcular_total_vendas(data_inicio, data_fim)
    messagebox.showinfo("Total de Vendas", f"Total de vendas no período: R${total_vendas:.2f}")

# Função para lidar com o botão "Exibir Relatório de Vendas"
def exibir_relatorio():
    relatorio = exibir_relatorio_vendas()
    messagebox.showinfo("Relatório de Vendas", relatorio)

# Função para lidar com o botão "Exportar Dados para Arquivo CSV"
def exportar_dados():
    nome_arquivo = entry_nome_arquivo.get()
    if not nome_arquivo:
        messagebox.showerror("Erro", "Por favor, digite o nome do arquivo CSV.")
        return
    exportar_dados_para_arquivo(nome_arquivo)
    messagebox.showinfo("Sucesso", f"Dados exportados para o arquivo {nome_arquivo}.")

# Função para lidar com o botão "Sair"
def sair():
    root.destroy()

### REORGANIZAR E TESTAR NOVOS LOCAIS
### ADICIONAR UMA IMAGEM NO FUNDO PODE SER UMA BOA IDEIA
### PEDIR A SUGESTÃO DO ADEMIR E DO FERNANDO SOBRE A INTERFACE

# Criar a tabela de vendas no banco de dados
criar_tabela_vendas()

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Padex - Controle de Vendas da Panificadora")

# Frame geral
frame_principal = tk.Frame(root)
frame_principal.pack(padx=10, pady=5)

# Frame para listar as vendas do dia
frame_lista_vendas = tk.Frame(frame_principal)
frame_lista_vendas.pack(pady=5)
label_lista_vendas = tk.Label(frame_lista_vendas, text="Vendas do Dia Atual")
label_lista_vendas.pack(side=tk.LEFT)

# Listbox para exibir as vendas do dia atual
lista_vendas = tk.Listbox(frame_lista_vendas, width=50)
lista_vendas.pack()

# Botão "Atualizar"
btn_atualizar = tk.Button(frame_lista_vendas, text="Atualizar", command=atualizar_lista_vendas_do_dia)
btn_atualizar.pack(side=tk.LEFT)

# Botão para registrar Venda
frame_registrar_venda = tk.Frame(frame_principal)
frame_registrar_venda.pack(pady=5)
label_registrar_venda = tk.Label(frame_registrar_venda, text="Registrar Venda")
label_registrar_venda.pack(side=tk.LEFT)
label_data = tk.Label(frame_registrar_venda, text="Data:")
label_data.pack(side=tk.LEFT)
entry_data = tk.Entry(frame_registrar_venda, width=12)
entry_data.pack(side=tk.LEFT)
entry_data.insert(tk.END, datetime.now().strftime("%d/%m/%Y"))
label_hora = tk.Label(frame_registrar_venda, text="Hora:")
label_hora.pack(side=tk.LEFT)
entry_hora = tk.Entry(frame_registrar_venda, width=10)
entry_hora.pack(side=tk.LEFT)
entry_hora.insert(tk.END, datetime.now().strftime("%H:%M"))
label_valor = tk.Label(frame_registrar_venda, text="Valor:")
label_valor.pack(side=tk.LEFT)
entry_valor = tk.Entry(frame_registrar_venda, width=10)
entry_valor.pack(side=tk.LEFT)
label_produtos = tk.Label(frame_registrar_venda, text="Produtos:")
label_produtos.pack(side=tk.LEFT)
entry_produtos = tk.Entry(frame_registrar_venda, width=30)
entry_produtos.pack(side=tk.LEFT)
btn_registrar_venda = tk.Button(frame_registrar_venda, text="Registrar", command=registrar_venda)
btn_registrar_venda.pack(side=tk.LEFT)

# botão para Calcular Total de Vendas
frame_total_vendas = tk.Frame(frame_principal)
frame_total_vendas.pack(pady=5)
label_total_vendas = tk.Label(frame_total_vendas, text="Calcular Total de Vendas")
label_total_vendas.pack(side=tk.LEFT)
label_data_inicio = tk.Label(frame_total_vendas, text="Data Início:")
label_data_inicio.pack(side=tk.LEFT)
entry_data_inicio = tk.Entry(frame_total_vendas, width=12)
entry_data_inicio.pack(side=tk.LEFT)
entry_data_inicio.insert(tk.END, datetime.now().strftime("%d/%m/%Y"))
label_data_fim = tk.Label(frame_total_vendas, text="Data Fim:")
label_data_fim.pack(side=tk.LEFT)
entry_data_fim = tk.Entry(frame_total_vendas, width=12)
entry_data_fim.pack(side=tk.LEFT)
entry_data_fim.insert(tk.END, datetime.now().strftime("%d/%m/%Y"))
btn_calcular_total = tk.Button(frame_total_vendas, text="Calcular", command=calcular_total)
btn_calcular_total.pack(side=tk.LEFT)

# botão para Exibir Relatório de Vendas
frame_relatorio_vendas = tk.Frame(frame_principal)
frame_relatorio_vendas.pack(pady=5)
label_relatorio_vendas = tk.Label(frame_relatorio_vendas, text="Exibir Relatório de Vendas")
label_relatorio_vendas.pack(side=tk.LEFT)
btn_exibir_relatorio = tk.Button(frame_relatorio_vendas, text="Exibir", command=exibir_relatorio)
btn_exibir_relatorio.pack(side=tk.LEFT)

# botão para Exportar Dados para Arquivo CSV
frame_exportar_dados = tk.Frame(frame_principal)
frame_exportar_dados.pack(pady=5)
label_exportar_dados = tk.Label(frame_exportar_dados, text="Exportar Dados para Arquivo CSV")
label_exportar_dados.pack(side=tk.LEFT)
label_nome_arquivo = tk.Label(frame_exportar_dados, text="Nome do Arquivo:")
label_nome_arquivo.pack(side=tk.LEFT)
entry_nome_arquivo = tk.Entry(frame_exportar_dados, width=30)
entry_nome_arquivo.pack(side=tk.LEFT)
btn_exportar_dados = tk.Button(frame_exportar_dados, text="Exportar", command=exportar_dados)
btn_exportar_dados.pack(side=tk.LEFT)

# Botão "Sair"
btn_sair = tk.Button(root, text="Sair", command=sair)
btn_sair.pack()

# Função principal que interage com o usuário
def main():

    # Função para atualizar a lista de vendas do dia atual
    def atualizar_lista_vendas_do_dia():
        lista_vendas.delete(0, tk.END)
        vendas_do_dia = obter_vendas_do_dia()
        for venda in vendas_do_dia:
            lista_vendas.insert(tk.END, f"{venda[0]} {venda[1]} | Valor: R${venda[2]:.2f} | Produtos: {venda[3]}")


# Iniciar a interface
root.mainloop()
