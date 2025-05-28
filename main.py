# Programa para interface gráfica com ESP32
# Criado por Professor Cristiano Teixeira
# Data: 2023-10-01
# Licença: Apache-2.0
# Este programa é um exemplo de interface gráfica para comunicação com um ESP32.
# Ele utiliza a biblioteca Tkinter para criar a interface e a biblioteca pyserial para comunicação serial.


import tkinter as tk
from tkinter import scrolledtext
import serial
import time

# Função para se conectar ao ESP32 via comunicação serial
def conectar_esp32(porta, baudrate=9600):
    try:
        ser = serial.Serial(porta, baudrate)
        print(f"Conectado ao ESP32 na porta {porta} com baudrate {baudrate}")
        return ser
    except serial.SerialException as e:
        print(f"Erro ao conectar ao ESP32: {e}")
        return None

# Função para monitorar e receber informações de distância, temperatura e umidade
def monitorar_sensores(ser):
    if ser and ser.is_open:
        ser.write(b'GET_SENSORS\n')  # Envia comando para obter dados dos sensores
        time.sleep(1)
        if ser.in_waiting > 0:
            dados = ser.readline().decode('utf-8').strip()
            print(f"Dados dos sensores: {dados}")
            return dados
    else:
        print("Conexão serial não está aberta.")
        return None

# Função para receber dados em forma de texto
def receber_dados_texto(ser):
    if ser and ser.is_open:
        ser.write(b'GET_TEXT\n')  # Envia comando para obter dados em texto
        time.sleep(1)
        if ser.in_waiting > 0:
            texto = ser.readline().decode('utf-8').strip()
            print(f"Dados recebidos: {texto}")
            return texto
    else:
        print("Conexão serial não está aberta.")
        return None

# Função para enviar uma sequência de caracteres até ser dado ENTER
def enviar_sequencia(ser, sequencia):
    if ser and ser.is_open:
        ser.write(sequencia.encode('utf-8') + b'\n')  # Envia a sequência de caracteres seguida de ENTER
        print(f"Sequência enviada: {sequencia}")
    else:
        print("Conexão serial não está aberta.")









class ESP32InterfaceApp:
    def __init__(self, root):
        corprincipal= "#1a1a1a"  # Cor principal (preto)
        cordecontraste= "#ffa500"  # Cor de contraste (dourado)
        cordesabilitado= "#808080"  # Cor desabilitada (cinza)
        self.root = root
        self.root.title("ESP32 Interface")
        self.root.geometry("900x460")
        self.root.configure(bg=corprincipal)  # Fundo preto
        linha=0
        # Label de título
        self.title_label = tk.Label(root, text="Interface com ESP32", bg=corprincipal, fg=cordecontraste, font=("Consolas", 16))
        self.title_label.grid(row=linha, column=0, columnspan=2, pady=10)
        linha+=1

        # Configuração da área de texto para exibir mensagens recebidas
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, bg=corprincipal, fg=cordecontraste, insertbackground=cordecontraste, font=("Consolas", 10))
        self.text_area.grid(row=linha, column=0, columnspan=2, padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)
        linha+=1

        # Botão para apagar mensagens
        self.clear_button = tk.Button(root, text="Apagar Mensagens", command=self.clear_messages, bg=cordecontraste, fg=corprincipal, font=("Consolas", 10), relief=tk.FLAT)
        self.clear_button.grid(row=linha, column=0, padx=10, pady=5, sticky="w")
        linha+=1

        # Botões personalizados
        self.buttons_frame = tk.Frame(root, bg=corprincipal)
        self.buttons_frame.grid(row=linha, column=0, columnspan=2, pady=10)

        self.custom_buttons = []
        for i in range(6):
            button = tk.Button(self.buttons_frame, text=f"Botão {i+1}", command=lambda i=i: self.custom_button_action(i), bg=cordecontraste, fg=corprincipal, font=("Consolas", 10), relief=tk.FLAT)
            button.grid(row=0, column=i, padx=5)
            self.custom_buttons.append(button)
        linha+=1

        # Entrada de texto para enviar comandos
        self.command_entry = tk.Entry(root, bg=corprincipal, fg=cordecontraste, insertbackground=cordecontraste, font=("Consolas", 10), width=50)
        self.command_entry.grid(row=linha, column=0, padx=10, pady=10, sticky="w")

        # Botão para enviar comandos
        self.send_button = tk.Button(root, text="Enviar", command=self.send_command, bg=cordecontraste, fg=corprincipal, font=("Consolas", 10), relief=tk.FLAT)
        self.send_button.grid(row=linha, column=1, padx=10, pady=10, sticky="e")

        # Novo frame a direita para informações personalizadas
        self.info_frame = tk.Frame(root, bg=corprincipal)
        self.info_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10)
        self.info_label = tk.Label(self.info_frame, text="Informações Personalizadas", bg=corprincipal, fg=cordecontraste, font=("Consolas", 12))
        self.info_label.grid(row=0, column=0, pady=10)
        
        # Adcionar um botão switch para conexão
        self.serial_label = tk.Label(self.info_frame, text="Serial:", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.serial_label.grid(row=1, column=0, pady=5)
        
        
        #self.switch_button = tk.Button(self.infoframe, text='OFF', command=self.toggle_switch, bg='red', fg='white', font=("Consolas", 10), relief=tk.FLAT)
        #self.switch_button.grid(row=1, column=1, pady=5)


        self.switch_button = tk.Button(self.info_frame, text='OFF', command=self.toggle_switch, bg='red', fg='white', font=("Consolas", 10), relief=tk.FLAT)
        self.switch_button.grid(row=1, column=1, pady=5)
        
        # Adicionar uma label para distância e uma caixa de texto para exibir a distância
        self.distance_label = tk.Label(self.info_frame, text="Distância:", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.distance_label.grid(row=2, column=0, pady=5)
        self.distance_value = tk.Label(self.info_frame, text="0 cm", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.distance_value.grid(row=2, column=1, pady=5)
        # Adicionar uma label para temperatura e uma caixa de texto para exibir a temperatura
        self.temperature_label = tk.Label(self.info_frame, text="Temperatura:", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.temperature_label.grid(row=3, column=0, pady=5)
        self.temperature_value = tk.Label(self.info_frame, text="0 °C", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.temperature_value.grid(row=3, column=1, pady=5)
        # Adicionar uma label para umidade e uma caixa de texto para exibir a umidade
        self.humidity_label = tk.Label(self.info_frame, text="Umidade:", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.humidity_label.grid(row=4, column=0, pady=5)
        self.humidity_value = tk.Label(self.info_frame, text="0 %", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.humidity_value.grid(row=4, column=1, pady=5)
        # Adicionar uma label para LEDs e três labels para os LEDs
        self.humidity_label = tk.Label(self.info_frame, text="Leds indicativos:", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.humidity_label.grid(row=5, column=0, rowspan=3, pady=5)
        # Adiciona três Labels uma do lado da outra, bem próximas, ainda dentro do frame de informações com nomes LED1 LED2 LED3
        # E abaixo dessas labels um botão sem nada escrito para simular o botão de ligar e desligar, um Azul, Um Amarelo e um Vermelho, 
        # Quando Desabilitados ficarão todos cinzas
        self.led1_label = tk.Label(self.info_frame, text="LED1", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.led1_label.grid(row=5, column=1, pady=5)
        self.led2_label = tk.Label(self.info_frame, text="LED2", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.led2_label.grid(row=5, column=2, pady=5)
        self.led3_label = tk.Label(self.info_frame, text="LED3", bg=corprincipal, fg=cordecontraste, font=("Consolas", 10))
        self.led3_label.grid(row=5, column=3, pady=5)
        # Adiciona três botões para ligar e desligar os LEDs
        self.led1_button = tk.Button(self.info_frame, text="", command=lambda: self.toggle_led(1), bg=cordesabilitado, fg=cordesabilitado, font=("Consolas", 10), relief=tk.FLAT)
        self.led1_button.grid(row=6, column=1, padx=5, pady=5)
        self.led2_button = tk.Button(self.info_frame, text="", command=lambda: self.toggle_led(2), bg=cordesabilitado, fg=cordesabilitado, font=("Consolas", 10), relief=tk.FLAT)
        self.led2_button.grid(row=6, column=2, padx=5, pady=5)
        self.led3_button = tk.Button(self.info_frame, text="", command=lambda: self.toggle_led(3), bg=cordesabilitado, fg=cordesabilitado, font=("Consolas", 10), relief=tk.FLAT)
        self.led3_button.grid(row=6, column=3, padx=5, pady=5)
        

        # Configuração da comunicação serial (ajuste conforme necessário)
        self.serial_port = None
        try:
            self.serial_port = serial.Serial('COM3', 115200, timeout=1)  # Ajuste a porta e baudrate
        except serial.SerialException:
            self.log_message("Erro: Não foi possível conectar ao ESP32.")

    def log_message(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def clear_messages(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

    def custom_button_action(self, button_index):
        self.log_message(f"Botão {button_index + 1} pressionado. (Ação personalizada aqui)")
    
    def toggle_led(self, led_number):
        #lembrar de descomentar a parte de baixo para enviar o comando para o ESP32
        #if self.serial_port and self.serial_port.is_open:
        if True:
            #command = f"LED{led_number}"
            #self.serial_port.write((command + "\n").encode())
            #self.log_message(f"Comando enviado: {command}")
            # Atualiza a cor do botão correspondente quando lcicar no LED1 muda a cor do botão para azul, LE+D2 Amarelo e LED3 Vermelho
            # Quando Clicar uma segunda vez muda a cor do botão para cinza
            if led_number == 1:
                if self.led1_button['bg'] == "#808080":
                    self.led1_button['bg'] = "#0000ff"  
                elif self.led1_button['bg'] == "#0000ff":
                    self.led1_button['bg'] = "#808080"
            elif led_number == 2:
                if self.led2_button['bg'] == "#808080":
                    self.led2_button['bg'] = "#ffff00"  
                elif self.led2_button['bg'] == "#ffff00":
                    self.led2_button['bg'] = "#808080"
            elif led_number == 3:
                if self.led3_button['bg'] == "#808080":
                    self.led3_button['bg'] = "#ff0000"  
                elif self.led3_button['bg'] == "#ff0000":
                    self.led3_button['bg'] = "#808080"        
        else:
            self.log_message("Erro: Porta serial não está conectada.")   

    
    
    def toggle_switch(self):
        if self.switch_button.config('text')[-1] == 'OFF':
            self.switch_button.config(text='ON', bg='green')
            # Substitua pela porta correta
            #porta = 'COM3' 
            #self.ser = conectar_esp32(porta) # Conecta no ESP32
        else:
            self.switch_button.config(text='OFF', bg='red')
            #self.ser.close() # Fecha a conexão



    def send_command(self):
        command = self.command_entry.get()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((command + "\n").encode())
            self.log_message(f"Comando enviado: {command}")
        else:
            self.log_message("Erro: Porta serial não está conectada.")
        self.command_entry.delete(0, tk.END)

    def receive_data(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.readline().decode().strip()
                if data:
                    self.log_message(f"Recebido: {data}")
            except serial.SerialException:
                self.log_message("Erro ao ler dados do ESP32.")
        self.root.after(100, self.receive_data)

    def run(self):
        self.receive_data()
        self.root.mainloop()


#CARREGA A FUNÇÃO PRINCIPAL
if __name__ == "__main__":
    
    # abre a Interface
    root = tk.Tk()
    app = ESP32InterfaceApp(root)
    app.run()
