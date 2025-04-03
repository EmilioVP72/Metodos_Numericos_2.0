import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import re

class GaussJordanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Gauss-Jordan")
        self.create_main_ui()
    
    def create_main_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Ingrese el número de ecuaciones:").pack(pady=5)
        self.num_eq_entry = tk.Entry(self.root)
        self.num_eq_entry.pack(pady=5)
        tk.Button(self.root, text="Ingresar ecuaciones", command=self.get_equations).pack(pady=5)
    
    def get_equations(self):
        try:
            self.num_eq = int(self.num_eq_entry.get())
            if self.num_eq <= 0:
                raise ValueError("El número de ecuaciones debe ser mayor que 0.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Ingrese las ecuaciones (Ej: 2x1 + 3x2 - x3 = 5)").pack(pady=5)
        self.eq_entries = []
        for i in range(self.num_eq):
            entry = tk.Entry(self.root, width=50)
            entry.pack(pady=2)
            self.eq_entries.append(entry)
        
        tk.Button(self.root, text="Resolver", command=self.solve).pack(pady=5)
    
    def parse_equation(self, equation):
        coef_pattern = re.compile(r'([-+]?\d*\.?\d*)x(\d+)')
        const_pattern = re.compile(r'([-+]?\d+)$')
        
        coefs = [0] * (self.num_eq + 1)
        equation = equation.replace(" ", "")
        
        for match in coef_pattern.finditer(equation):
            coef = match.group(1)
            idx = int(match.group(2)) - 1
            coefs[idx] = float(coef) if coef not in ["", "+", "-"] else (1 if coef in ["", "+"] else -1)
        
        match = const_pattern.search(equation)
        if match:
            coefs[-1] = float(match.group(1))
        
        return coefs
    
    def solve(self):
        try:
            matrix = np.array([self.parse_equation(entry.get()) for entry in self.eq_entries], dtype=float)
        except Exception:
            messagebox.showerror("Error", "Formato incorrecto de ecuación.")
            return
        
        self.show_solution(matrix)
    
    def show_solution(self, matrix):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        text_area = scrolledtext.ScrolledText(self.root, width=60, height=20)
        text_area.pack(pady=5)
        
        def log_step(step):
            text_area.insert(tk.END, step + "\n")
            text_area.insert(tk.END, np.array2string(matrix, precision=2, suppress_small=True) + "\n\n")
        
        for i in range(self.num_eq):
            pivot = matrix[i, i]
            matrix[i] /= pivot
            log_step(f"Dividiendo fila {i+1} entre {pivot}")
            
            for k in range(self.num_eq):
                if k != i:
                    factor = matrix[k, i]
                    matrix[k] -= factor * matrix[i]
                    log_step(f"Restando {factor} veces fila {i+1} de fila {k+1}")
        
        tk.Label(self.root, text="Resultados:").pack(pady=5)
        for i in range(self.num_eq):
            tk.Label(self.root, text=f"X{i+1} = {matrix[i, -1]:.6f}").pack()
        
        tk.Button(self.root, text="Regresar", command=self.create_main_ui).pack(pady=10)
