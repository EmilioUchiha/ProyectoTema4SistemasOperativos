import tkinter as tk
from vista import Vista
from CambioContexto import CambioContexto


root = tk.Tk()

vista = Vista(root)
controlador = CambioContexto(vista, root)

root.mainloop()