import tkinter as tk
from tkinter import messagebox
import numpy as np

class JacobiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Jacobi")
        
        # Configuración inicial
        tk.Label(root, text="Número de variables:").grid(row=0, column=0)
        self.txtNumVariables = tk.Entry(root, width=5)
        self.txtNumVariables.grid(row=0, column=1)
        
        tk.Label(root, text="Error permitido:").grid(row=0, column=2)
        self.txtErrorPermitido = tk.Entry(root, width=10)
        self.txtErrorPermitido.grid(row=0, column=3)
        
        self.btnGenerar = tk.Button(root, text="Generar matriz", command=self.generar_matriz)
        self.btnGenerar.grid(row=0, column=4)
        
        self.frame_matriz = tk.Frame(root)
        self.frame_matriz.grid(row=1, column=0, columnspan=5)
        
        self.btnResolver = tk.Button(root, text="Resolver", command=self.resolver_sistema, state=tk.DISABLED)
        self.btnResolver.grid(row=2, column=0, columnspan=5)
        
        self.resultados_label = tk.Label(root, text="")
        self.resultados_label.grid(row=3, column=0, columnspan=5)
        
    def generar_matriz(self):
        try:
            self.n = int(self.txtNumVariables.get())
            if self.n <= 0:
                raise ValueError
            
            for widget in self.frame_matriz.winfo_children():
                widget.destroy()
            
            self.camposMatriz = []
            self.camposB = []
            
            for i in range(self.n):
                fila = []
                for j in range(self.n):
                    txt = tk.Entry(self.frame_matriz, width=5)
                    txt.grid(row=i, column=j)
                    fila.append(txt)
                self.camposMatriz.append(fila)
                
                txtB = tk.Entry(self.frame_matriz, width=5)
                txtB.grid(row=i, column=self.n)
                self.camposB.append(txtB)
            
            self.btnResolver.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Error", "Número de variables inválido.")
    
    def resolver_sistema(self):
        try:
            errorPermitido = float(self.txtErrorPermitido.get())
            matriz = np.zeros((self.n, self.n))
            b = np.zeros(self.n)
            
            for i in range(self.n):
                for j in range(self.n):
                    matriz[i][j] = float(self.camposMatriz[i][j].get())
                b[i] = float(self.camposB[i].get())
            
            x = np.zeros(self.n)
            iteraciones = 0
            max_iter = 1000
            convergencia = False
            
            while iteraciones < max_iter:
                x_nuevo = np.copy(x)
                for i in range(self.n):
                    suma = sum(matriz[i][j] * x[j] for j in range(self.n) if j != i)
                    x_nuevo[i] = (b[i] - suma) / matriz[i][i]
                
                if np.linalg.norm(x_nuevo - x, np.inf) < errorPermitido:
                    convergencia = True
                    break
                x = x_nuevo
                iteraciones += 1
            
            if not convergencia:
                messagebox.showwarning("Advertencia", "El método no convergió en 1000 iteraciones.")
            
            self.resultados_label.config(text=f"Iteraciones: {iteraciones}\nSolución: {x}")
        except ValueError:
            messagebox.showerror("Error", "Verifica los valores ingresados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JacobiApp(root)
    root.mainloop()
