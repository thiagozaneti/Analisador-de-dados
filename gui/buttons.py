from ttkbootstrap import BootstrapButton  # Importando o botão do Bootstrap

def create_select_button(parent, nome, descricao, frequencia, amostras, atualizar_detalhes):
    """
    Cria um botão de seleção e retorna.
    
    :param parent: O pai do widget
    :param nome: O nome da máquina
    :param descricao: A descri o da máquina
    :param frequencia: A frequ ncia de aquisi o da máquina
    :param amostras: O n mero de amostras da máquina
    :param atualizar_detalhes: A fun o para atualizar as informa es de detalhes
    """
    return BootstrapButton(parent, text="Selecionar", command=lambda: atualizar_detalhes(nome, descricao, frequencia, amostras))  # Usando BootstrapButton
