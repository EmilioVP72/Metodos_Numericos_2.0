import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

class ReglaFalsaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Regla Falsa")
        
        # Variables de entrada
        self.funcion_var = tk.StringVar()
        self.a_var = tk.StringVar()
        self.b_var = tk.StringVar()
        self.error_var = tk.StringVar()
        
        # Interfaz
        self.create_widgets()
    
    def create_widgets(self):
        frame_input = ttk.Frame(self.root, padding="10")
        frame_input.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(frame_input, text="Función f(x):").grid(row=0, column=0)
        ttk.Entry(frame_input, textvariable=self.funcion_var, width=30).grid(row=0, column=1)
        
        ttk.Label(frame_input, text="Valor de A:").grid(row=1, column=0)
        ttk.Entry(frame_input, textvariable=self.a_var, width=10).grid(row=1, column=1)
        
        ttk.Label(frame_input, text="Valor de B:").grid(row=2, column=0)
        ttk.Entry(frame_input, textvariable=self.b_var, width=10).grid(row=2, column=1)
        
        ttk.Label(frame_input, text="Error permitido:").grid(row=3, column=0)
        ttk.Entry(frame_input, textvariable=self.error_var, width=10).grid(row=3, column=1)
        
        ttk.Button(frame_input, text="Resolver", command=self.resolver).grid(row=4, columnspan=2)
        
        # Tabla de iteraciones
        self.tree = ttk.Treeview(self.root, columns=("Iter", "A", "B", "Xr", "f(Xr)", "Error"), show="headings")
        for col in ("Iter", "A", "B", "Xr", "f(Xr)", "Error"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=1, column=0)
    
    def evaluar(self, expr, x_val):
        x = sp.symbols('x')
        return float(expr.subs(x, x_val))
    
    def resolver(self):
        try:
            funcion = self.funcion_var.get()
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            error_permitido = float(self.error_var.get())
            
            x = sp.symbols('x')
            expr = sp.sympify(funcion)
            
            if self.evaluar(expr, a) * self.evaluar(expr, b) >= 0:
                messagebox.showerror("Error", "f(a) y f(b) deben tener signos opuestos")
                return
            
            self.tree.delete(*self.tree.get_children())
            iteracion = 0
            xr = a
            error = float('inf')
            
            while error > error_permitido:
                fa = self.evaluar(expr, a)
                fb = self.evaluar(expr, b)
                xr_nuevo = b - (fb * (a - b)) / (fa - fb)
                fxr = self.evaluar(expr, xr_nuevo)
                
                if iteracion > 0:
                    error = abs((xr_nuevo - xr) / xr_nuevo) * 100
                
                self.tree.insert("", "end", values=(iteracion, round(a, 6), round(b, 6), round(xr_nuevo, 6), round(fxr, 6), round(error, 6)))
                
                if fa * fxr < 0:
                    b = xr_nuevo
                else:
                    a = xr_nuevo
                
                xr = xr_nuevo
                iteracion += 1
            
            messagebox.showinfo("Resultado", f"Raíz aproximada: {xr:.6f}\nIteraciones: {iteracion}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ReglaFalsaApp(root)
    root.mainloop()
