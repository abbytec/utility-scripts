##### WORTHLESS HELLO WORLD ####
"""
-Que se imprima el print
-Que se sume el numero , este no puede ser entero, pero debe por lo menos tener 4 decimales de precisión.
-Poner un contador del parametro que abuses.
-Que compile
"""

target_string = "hola mundo"
show_text = False

def find_ascii_by_summing(target_ascii):
    global iterations_counter
    current_value = 0.0000
    increment = 0.0001
    
    while True:
        if int(current_value) == target_ascii:
            return current_value
        current_value += increment
        if(show_text):
            print("Buscando caracter ascii a imprimir", current_value)

for char in target_string:
    ascii_value = ord(char)
    found_value = find_ascii_by_summing(ascii_value)
    print(chr(int(found_value)), end="\n")
