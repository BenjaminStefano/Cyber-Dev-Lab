import tkinter as tk
from tkinter import messagebox

def verificar_login():
    usuario = input_usuario.get()
    contraseña = input_contraseña.get()

    if usuario == "admin123" and contraseña == "1234":
        messagebox.showinfo("Login", "Acceso permitido, bienvenido!!")
    else:
        messagebox.showerror("Login", "Usuario o contraseña incorrectos")

ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x250")

tk.Label(ventana, text="Usuario").pack()
input_usuario = tk.Entry(ventana)
input_usuario.pack()

tk.Label(ventana, text="Contraseña").pack()
input_contraseña = tk.Entry(ventana, show="*")
input_contraseña.pack()

tk.Button(ventana, text="Login", command=verificar_login).pack(pady=10)

ventana.mainloop()