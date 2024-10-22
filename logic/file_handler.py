
import pandas as pd
from tkinter import filedialog, messagebox, ttk

def carregar_arquivo(content_frame, selecionar_maquina_callback):
    try:
        # Seleciona o arquivo
        caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx")])
        if not caminho_arquivo:
            return

        # Lê o arquivo Excel
        df = pd.read_excel(caminho_arquivo)

        # Verifica se as colunas necessárias existem no arquivo
        colunas_necessarias = ['Name', 'Description', 'Frequencia de aquisição (Amostras/s)', 'Numero de amostras (2^N)']
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(f"A coluna '{coluna}' não foi encontrada no arquivo Excel.")

        # Limpa o content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Cria um frame para a lista de máquinas
        maquinas_frame = ttk.Frame(content_frame)
        maquinas_frame.grid(row=0, column=0, sticky="nsew")

        # Cria um frame para os detalhes
        detalhes_frame = ttk.Frame(content_frame)
        detalhes_frame.grid(row=0, column=1, sticky="nsew")

        # Adiciona os botões das máquinas no frame de máquinas
        for _, row in df.iterrows():
            nome = row['Name']
            descricao = row['Description']
            frequencia = row['Frequencia de aquisição (Amostras/s)']
            amostras = row['Numero de amostras (2^N)']

            btn = ttk.Button(maquinas_frame, text=nome, 
                             command=lambda n=nome, d=descricao, f=frequencia, a=amostras: 
                             selecionar_maquina_callback(n, d, f, a))
            btn.pack(pady=2, fill="x")

        messagebox.showinfo("Sucesso", "Máquinas e informações carregadas com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")