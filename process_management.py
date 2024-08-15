import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import subprocess
import os

class ProcessManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Andromeda Process Manager")
        self.root.geometry("600x400")

        # Treeview to display processes
        self.tree = ttk.Treeview(root, columns=("PID", "Name", "CPU", "Memory"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("CPU", text="CPU %")
        self.tree.heading("Memory", text="Memory %")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Refresh button
        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_processes)
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Kill button
        self.kill_button = tk.Button(root, text="Kill Process", command=self.kill_process)
        self.kill_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Add process button and entry
        self.process_entry = tk.Entry(root)
        self.process_entry.pack(side=tk.LEFT, padx=10, pady=10)
        #self.add_button = tk.Button(root, text="Add Process", command=self.add_process)
        #self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Initial load of processes
        self.refresh_processes()

    def refresh_processes(self):
        # Clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insert process information into the treeview
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            self.tree.insert('', 'end', values=(proc.info['pid'], proc.info['name'], 
                                                proc.info['cpu_percent'], proc.info['memory_percent']))

    def kill_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a process to kill.")
            return
        pid = self.tree.item(selected_item[0])['values'][0]
        try:
            psutil.Process(pid).terminate()
            messagebox.showinfo("Success", f"Process {pid} terminated.")
            self.refresh_processes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate process {pid}: {str(e)}")

    #def add_process(self):
        command = self.process_entry.get()
        if not command:
            messagebox.showwarning("No Command", "Please enter a command to execute.")
            return
        try:
            subprocess.Popen(command.split())
            messagebox.showinfo("Success", f"Process '{command}' started.")
            self.refresh_processes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start process '{command}': {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()
