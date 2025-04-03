import sympy as sp
import tkinter as tk
from tkinter import messagebox, ttk

class NewtonRaphsonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Newton-Raphson")
        
        # Variables de entrada
        self.funcion = tk.StringVar()
        self.x_inicial = tk.StringVar()
        self.error_permitido = tk.StringVar()
        
        # Creación de widgets
        tk.Label(root, text="Ingrese su función:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.funcion).grid(row=0, column=1)
        
        tk.Label(root, text="Valor de X inicial:").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.x_inicial).grid(row=1, column=1)
        
        tk.Label(root, text="Error permitido:").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.error_permitido).grid(row=2, column=1)
        
        self.btn_validar = tk.Button(root, text="Validar", command=self.validar)
        self.btn_validar.grid(row=3, column=0)
        
        self.btn_resolver = tk.Button(root, text="Resolver", command=self.resolver, state=tk.DISABLED)
        self.btn_resolver.grid(row=3, column=1)
        
        # Tabla de resultados
        self.tree = ttk.Treeview(root, columns=("Iteración", "x_i", "f(x_i)", "f'(x_i)", "x_i+1", "Error"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        self.tree.grid(row=4, column=0, columnspan=2)

        # Resultados finales
        self.lbl_resultado = tk.Label(root, text="Raíz encontrada: -")
        self.lbl_resultado.grid(row=5, column=0, columnspan=2)

        self.lbl_iteraciones = tk.Label(root, text="Iteraciones: -")
        self.lbl_iteraciones.grid(row=6, column=0, columnspan=2)
    
    def validar(self):
        try:
            self.funcion_expr = sp.sympify(self.funcion.get())
            self.x0 = float(self.x_inicial.get())
            self.error_max = float(self.error_permitido.get())
            if self.error_max <= 0:
                raise ValueError("El error debe ser positivo")
            self.btn_resolver.config(state=tk.NORMAL)
            messagebox.showinfo("Validación exitosa", "Los datos son válidos. Puedes resolver.")
        except Exception as e:
            messagebox.showerror("Error de validación", str(e))
            self.btn_resolver.config(state=tk.DISABLED)
    
    def resolver(self):
        self.tree.delete(*self.tree.get_children())
        x = sp.Symbol('x')
        df = sp.diff(self.funcion_expr, x)
        xi = self.x0
        error = float('inf')
        iteracion = 1

        while error > self.error_max:
            fx = self.funcion_expr.subs(x, xi).evalf()
            dfx = df.subs(x, xi).evalf()
            
            if dfx == 0:
                messagebox.showerror("Error", f"Derivada cero en x = {xi}. El método falla.")
                return
            
            xi1 = xi - (fx / dfx)
            error = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')
            
            self.tree.insert("", "end", values=(iteracion, round(xi, 6), round(fx, 6), round(dfx, 6), round(xi1, 6), round(error, 6)))
            
            xi = xi1
            iteracion += 1
        
        self.lbl_resultado.config(text=f"Raíz encontrada: {xi:.6f}")
        self.lbl_iteraciones.config(text=f"Iteraciones: {iteracion - 1}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()
