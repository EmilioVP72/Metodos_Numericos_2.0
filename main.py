import tkinter as tk
from Gauss_Jordan import GaussJordanApp
from Newton_Raphson import NewtonRaphsonApp  

def open_gauss_jordan():
    gauss_root = tk.Toplevel()
    gauss_app = GaussJordanApp(gauss_root)
    gauss_root.mainloop()

def open_newton_raphson():
    newton_root = tk.Toplevel()
    newton_app = NewtonRaphsonApp(newton_root)
    newton_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Métodos Numéricos")
    root.geometry("300x200")
    
    tk.Label(root, text="Seleccione un método:").pack(pady=10)
    
    btn_gauss = tk.Button(root, text="Gauss-Jordan", command=open_gauss_jordan)
    btn_gauss.pack(pady=5)
    
    btn_newton = tk.Button(root, text="Newton-Raphson", command=open_newton_raphson)
    btn_newton.pack(pady=5)
    
    root.mainloop()
