import tkinter as tk
from tkinter import messagebox
import math

modo_grados = True

def alternar_modo():
    global modo_grados
    modo_grados = not modo_grados
    btn_modo.config(text="DEG" if modo_grados else "RAD", fg="#00E5FF" if not modo_grados else "#FFD700")

def click(v):
    entrada.config(state='normal')
    entrada.insert(tk.END, str(v))
    entrada.config(state='readonly')

def borrar():
    entrada.config(state='normal')
    entrada.delete(0, tk.END)
    entrada.config(state='readonly')

def retroceso():
    entrada.config(state='normal')
    entrada.delete(len(entrada.get())-1, tk.END)
    entrada.config(state='readonly')

def calcular():
    try:
        expr = entrada.get().replace('^', '**').replace('mod', '%')
        def to_rad(x): return math.radians(x) if modo_grados else x
        safe_dict = {
            "math": math, "sin": lambda x: math.sin(to_rad(x)),
            "cos": lambda x: math.cos(to_rad(x)), "tan": lambda x: math.tan(to_rad(x)),
            "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
            "ecuacion": lambda a,b,c: f"x1:{round((-b+math.sqrt(b**2-4*a*c))/(2*a),2)} x2:{round((-b-math.sqrt(b**2-4*a*c))/(2*a),2)}"
        }
        res = eval(expr, {"__builtins__": None}, safe_dict)
        historial.insert(0, f"{entrada.get()} = {res}")
        entrada.config(state='normal')
        entrada.delete(0, tk.END)
        entrada.insert(0, str(res))
        entrada.config(state='readonly')
    except: messagebox.showerror("Error", "Operacion Invalida")

def on_key(event):
    if event.char in "0123456789.+-*/()": click(event.char)
    elif event.keysym == "Return": calcular()
    elif event.keysym == "BackSpace": retroceso()
    elif event.keysym == "Escape": borrar()
    return "break"

root = tk.Tk()
root.title("Calculadora UI")
root.geometry("380x620")
root.configure(bg="#0F172A") # Azul muy oscuro (Slate 900)

# Pantalla de visualización
pantalla_frame = tk.Frame(root, bg="#1E293B", bd=0)
pantalla_frame.pack(pady=20, padx=20, fill="x")

entrada = tk.Entry(pantalla_frame, font=("Consolas", 32), bg="#1E293B", fg="#F8FAFC", borderwidth=0, justify="right", state='readonly', readonlybackground="#1E293B")
entrada.pack(padx=10, pady=(10,0), fill="x")

historial = tk.Listbox(pantalla_frame, height=2, font=("Consolas", 10), bg="#1E293B", fg="#94A3B8", borderwidth=0, highlightthickness=0)
historial.pack(padx=10, pady=(0,10), fill="x")

# Grid de botones
btn_frame = tk.Frame(root, bg="#0F172A")
btn_frame.pack(expand=True, fill="both", padx=15, pady=10)

def btn_ui(t, r, c, cmd, bg="#334155", fg="#F8FAFC", s=1):
    btn = tk.Button(btn_frame, text=t, font=("Arial", 12, "bold"), bg=bg, fg=fg, borderwidth=0, 
                   activebackground="#475569", activeforeground="white", relief="flat", command=cmd)
    btn.grid(row=r, column=c, columnspan=s, sticky="nsew", padx=4, pady=4)
    return btn

# Fila 0: Controles
btn_modo = btn_ui("DEG", 0, 0, alternar_modo, "#1E293B", "#FFD700")
btn_ui("AC", 0, 1, borrar, "#EF4444", "white")
btn_ui("⌫", 0, 2, retroceso, "#334155")
btn_ui("(", 0, 3, lambda: click("("), "#334155")
btn_ui(")", 0, 4, lambda: click(")"), "#334155")

# Fila 1: Cientifico
btn_ui("sin", 1, 0, lambda: click("sin("))
btn_ui("cos", 1, 1, lambda: click("cos("))
btn_ui("tan", 1, 2, lambda: click("tan("))
btn_ui("sqrt", 1, 3, lambda: click("sqrt("))
btn_ui("/", 1, 4, lambda: click("/"), "#6366F1")

# Fila 2, 3, 4: Numeros
nums = [('7','8','9','*'), ('4','5','6','-'), ('1','2','3','+')]
for i, row in enumerate(nums):
    for j, val in enumerate(row):
        color = "#6366F1" if not val.isdigit() else "#334155"
        btn_ui(val, i+2, j, lambda v=val: click(v), color)

# Botones laterales y extra
btn_ui("^", 2, 4, lambda: click("^"), "#6366F1")
btn_ui("mod", 3, 4, lambda: click(" mod "), "#6366F1")
btn_ui("pi", 4, 4, lambda: click("pi"), "#334155")

# Fila 5: Base
btn_ui("0", 5, 0, lambda: click("0"), "#334155", s=2)
btn_ui(".", 5, 2, lambda: click("."), "#334155")
btn_ui("=", 5, 3, calcular, "#10B981", "white", s=2)

for i in range(5): btn_frame.grid_columnconfigure(i, weight=1)
for i in range(6): btn_frame.grid_rowconfigure(i, weight=1)

root.bind("<Key>", on_key)
root.mainloop()
