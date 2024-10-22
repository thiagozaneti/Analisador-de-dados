import tkinter as tk
from tkinter import tk, messagebox 
import tkinter.font as tkfont
from logic.file_handler import carregar_arquivo
from logic.csv_save import salvar_dados_csv
from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag,
                   AiInputMode, create_float_buffer, ScanOption, 
                   ScanStatus, InterfaceType, Range)
import threading
import time
from datetime import datetime

# Variáveis globais
selected_machine = None
is_acquiring = False
daq_device = None
ai_device = None

def main():
    root = tk.Tk()  # Usando Bootstrap em vez de tk.Tk()
    root.title("Analisador de Dados de Vibração")
    root.geometry("800x600")
    style = tk.Style()
    style.theme_use("flatly")  # Alterando o tema para um tema do Bootstrap

    # Configurar o grid
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Frame para botões de controle
    control_frame = tk.Frame(root)
    control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # Botão para carregar arquivo de configuração
    btn_carregar = tk.Button(control_frame, text="Carregar Configurações", 
                              command=lambda: carregar_arquivo(content_frame, selecionar_maquina))
    btn_carregar.pack(side="left", padx=5)

    # Botão para iniciar/parar a aquisição de dados
    btn_aquisicao = tk.Button(control_frame, text="Iniciar Aquisição", 
                               command=lambda: toggle_aquisicao(btn_aquisicao))
    btn_aquisicao.pack(side="left", padx=5)

    # Frame para conteúdo (lista de máquinas e detalhes)
    content_frame = tk.Frame(root)
    content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Criar duas colunas no content_frame
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()

def toggle_aquisicao(btn):
    global is_acquiring, selected_machine
    if not is_acquiring:
        if selected_machine:
            is_acquiring = True
            btn.config(text="Parar Aquisição")
            threading.Thread(target=iniciar_aquisicao, args=(btn,), daemon=True).start()
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma máquina antes de iniciar a aquisição.")
    else:
        is_acquiring = False
        btn.config(text="Iniciar Aquisição")

def iniciar_aquisicao(btn):
    global is_acquiring, daq_device, ai_device, selected_machine
    try:
        # Configuração do dispositivo DAQ
        devices = get_daq_device_inventory(InterfaceType.ANY)
        if not devices:
            raise RuntimeError('Nenhum dispositivo DAQ encontrado')

        daq_device = DaqDevice(devices[0])
        ai_device = daq_device.get_ai_device()

        if ai_device is None:
            raise RuntimeError('O dispositivo não suporta entrada analógica')

        daq_device.connect()

        # Configuração dos parâmetros de aquisição
        low_channel = 0
        high_channel = 3  # Ajuste conforme necessário
        input_mode = AiInputMode.SINGLE_ENDED
        range_index = 0
        samples_per_channel = selected_machine["amostras"]
        rate = selected_machine["frequencia"]
        scan_options = ScanOption.DEFAULTIO | ScanOption.CONTINUOUS
        flags = AInScanFlag.DEFAULT

        ranges = ai_device.get_info().get_ranges(input_mode)
        channel_count = high_channel - low_channel + 1
        data = create_float_buffer(channel_count, samples_per_channel)

        # Iniciar a aquisição
        actual_rate = ai_device.a_in_scan(low_channel, high_channel, input_mode,
                                          ranges[range_index], samples_per_channel,
                                          rate, scan_options, flags, data)

        # Gera um timestamp único para este conjunto de dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        print(f"Aquisição iniciada. Taxa real: {actual_rate} Hz")

        while is_acquiring:
            # Obter o status da operação de fundo
            status, transfer_status = ai_device.get_scan_status()

            if status == ScanStatus.RUNNING:
                index = transfer_status.current_index
                # Processar e salvar os dados
                dados_atuais = [data[index + i] for i in range(channel_count)]
                nome_arquivo = salvar_dados_csv(selected_machine["nome"], dados_atuais, timestamp)
                print(f"Dados adquiridos e salvos em {nome_arquivo}: {dados_atuais}")

            time.sleep(0.1)

    except Exception as e:
        print(f"Erro durante a aquisição: {e}")
        messagebox.showerror("Erro", f"Erro durante a aquisição: {e}")
    finally:
        if ai_device:
            ai_device.scan_stop()
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()
        
        is_acquiring = False
        btn.config(text="Iniciar Aquisição")
        messagebox.showinfo("Aquisição Concluída", "A aquisição de dados foi concluída.")

def selecionar_maquina(nome, descricao, frequencia, amostras):
    global selected_machine
    selected_machine = {
        "nome": nome,
        "descricao": descricao,
        "frequencia": float(frequencia),
        "amostras": int(amostras)
    }
    print(f"Máquina selecionada: {nome}")
    print(f"Frequência de aquisição: {frequencia} Hz")
    print(f"Número de amostras: {amostras}")

if __name__ == "__main__":
    main()
