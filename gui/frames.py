import tkinter as tk

def create_frames(parent):
    """
    Cria e retorna os frames principais da interface: frame de máquinas e
    frame de detalhes das máquinas selecionadas.
    """
    # Frame para exibir a lista de máquinas
    frame_maquinas = tk.Frame(parent)  # Usando tk.Frame em vez de BootstrapFrame
    frame_maquinas.pack(fill="both", expand=True)

    # Frame de detalhes das máquinas selecionadas
    frame_detalhes = tk.LabelFrame(parent, text="Máquina Selecionada", padding=10)  # Usando tk.LabelFrame
    frame_detalhes.pack(fill="both", expand=True)

    # Informações de detalhes
    labels = {
        "Nome": tk.Label(frame_detalhes, text="Nome: "),  # Usando tk.Label
        "Descrição": tk.Label(frame_detalhes, text="Descrição: "),  # Usando tk.Label
        "Frequência de Aquisição": tk.Label(frame_detalhes, text="Frequência de Aquisição: "),  # Usando tk.Label
        "Número de Amostras": tk.Label(frame_detalhes, text="Número de Amostras: ")  # Usando tk.Label
    }

    # Posiciona os labels no frame de detalhes
    row = 0
    for key, label in labels.items():
        # Coloca o label na linha e coluna especificados e adiciona um padding
        # em x e y para espaçamento
        label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

    return frame_maquinas, frame_detalhes