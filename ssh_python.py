import paramiko
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
import logging
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear

# Configure logging for session activities
logging.basicConfig(filename='session.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class SSHClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NextGen SecureConnect")
        self.session_manager = SessionManager()
        self.ssh_client = None

        self.create_ui()

    def create_ui(self):
        # Session Management UI
        self.session_listbox = tk.Listbox(self.root)
        self.session_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_sessions()

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="New Session", command=self.new_session).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Connect", command=self.connect_session).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Delete Session", command=self.delete_session).pack(side=tk.LEFT)

    def load_sessions(self):
        self.session_listbox.delete(0, tk.END)
        sessions = self.session_manager.load_sessions()
        for session in sessions:
            self.session_listbox.insert(tk.END, f"{session['hostname']} ({session['username']})")

    def new_session(self):
        hostname = simpledialog.askstring("Input", "Hostname:")
        username = simpledialog.askstring("Input", "Username:")
        key_filename = filedialog.askopenfilename(title="Select Private Key File (Optional)")
        password = None
        if not key_filename:
            password = simpledialog.askstring("Input", "Password:", show='*')

        session_data = {
            'hostname': hostname,
            'username': username,
            'key_filename': key_filename if key_filename else None,
            'password': password
        }

        self.session_manager.save_session(session_data)
        self.load_sessions()

    def delete_session(self):
        selected_session = self.session_listbox.curselection()
        if selected_session:
            index = selected_session[0]
            self.session_manager.delete_session(index)
            self.load_sessions()

    def connect_session(self):
        selected_session = self.session_listbox.curselection()
        if selected_session:
            index = selected_session[0]
            session_data = self.session_manager.get_session(index)

            
            self.ssh_client = SSHClient(**session_data)
            x = self.ssh_client.connect()
            if(x==1):
                self.start_terminal()
            else:
                print("did not give proper details")

    def start_terminal(self):
        session = PromptSession()
        while True:
            try:
                command = session.prompt(f"{self.ssh_client.username}@{self.ssh_client.hostname}:~$ ")
                if command.lower() in ['exit', 'quit']:
                    break
                output = self.ssh_client.execute_command(f'cmd.exe /c "{command}"')
                print(output)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

        clear()

class SSHClient:
    def __init__(self, hostname, username, password=None, key_filename=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            if self.key_filename:
                self.client.connect(self.hostname, username=self.username, key_filename=self.key_filename)
            else:
                self.client.connect(self.hostname, username=self.username, password=self.password)
            logging.info(f"Connected to {self.hostname} as {self.username}")
            x = 1
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            x=0
        return x

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        print(error)
        logging.info(f"Executed command: {command}\nOutput: {output}")
        return output

    def close(self):
        self.client.close()
        logging.info(f"Connection to {self.hostname} closed")

class SessionManager:
    def __init__(self, session_file='sessions.json'):
        self.session_file = session_file

    def save_session(self, session_data):
        with open(self.session_file, 'a') as file:
            json.dump(session_data, file)
            file.write('\n')

    def load_sessions(self):
        sessions = []
        try:
            with open(self.session_file, 'r') as file:
                for line in file:
                    sessions.append(json.loads(line))
        except FileNotFoundError:
            pass
        return sessions

    def delete_session(self, index):
        sessions = self.load_sessions()
        if 0 <= index < len(sessions):
            del sessions[index]
            with open(self.session_file, 'w') as file:
                for session in sessions:
                    json.dump(session, file)
                    file.write('\n')

    def get_session(self, index):
        sessions = self.load_sessions()
        if 0 <= index < len(sessions):
            return sessions[index]
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientApp(root)
    root.mainloop()
