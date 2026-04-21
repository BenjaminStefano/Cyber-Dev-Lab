# Programa en Consola | Club Nocturno

print("Hola!, Bienvenido a nuestro Club Nocturno...")

edad = input("Dime tu edad porfavor: ")
edad = int(edad)
if(type(edad) == int):
    if(edad >= 120 or edad <= 0):
        print("Esto es imposible")
    elif(edad >= 18 and edad <= 40 ):
        print("Excelente, puedes entrar al Club")
    elif(edad <= 18 and edad >= 5):
        print("Todavia eres un niño, no puedes entrar al Club") 
    else:
        print("No se ha cumplido ninguna de las condiciones")   
