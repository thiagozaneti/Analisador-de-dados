import tkinter as tk
from tkinter import ttk
from ttkbootstrap import BootstrapFrame  # Importando o frame do Bootstrap

def create_frames(parent):
    """
    Cria e retorna os frames principais da interface: frame de máquinas e
    frame de detalhes das máquinas selecionadas.
    """
    # Frame para exibir a lista de máquinas
    frame_maquinas = BootstrapFrame(parent)  # Usando BootstrapFrame
    frame_maquinas.pack(fill="both", expand=True)

    # Frame de detalhes das máquinas selecionadas
    frame_detalhes = ttk.LabelFrame(parent, text="Máquina Selecionada", padding=10)
    frame_detalhes.pack(fill="both", expand=True)

    # Informações de detalhes
    labels = {
        "Nome": ttk.Label(frame_detalhes, text="Nome: "),
        "Descrição": ttk.Label(frame_detalhes, text="Descrição: "),
        "Frequência de Aquisição": ttk.Label(frame_detalhes, text="Frequência de Aquisição: "),
        "Número de Amostras": ttk.Label(frame_detalhes, text="Número de Amostras: ")
    }

    # Posiciona os labels no frame de detalhes
    row = 0
    for key, label in labels.items():
        # Coloca o label na linha e coluna especificados e adiciona um padding
        # em x e y para espaçamento
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

    return frame_maquinas, frame_detalhes
