import time
import threading
import curses
# def my_start_countdown(tempo):
#     for minutes in reversed(range(0, tempo)):
#         for seg in reversed(range(0, 60)):
#             print(f"\x1b[1;2f{minutes}:{seg} ", end="\r", flush=True)
#             print("\x1b[3;2f")
#             time.sleep(1)
#     print("Time's up!")


# while True:
#     print("\x1b[3;2f")
#     inputted_value = str(input("\x1b[3;2fEsperando input:"))
#     comandos = inputted_value.split()
#     if comandos[0] != "timer":
#         next
#     tempo = int(comandos[1])
#     tasks = comandos[2:]
#     newThread = threading.Thread(target=my_start_countdown, args=[tempo])
#     newThread.start()
#     print("\n")
#     newInput = str(input(""))
#     print(newInput)

#  ideia: usar o getch para pegar os caracteres escritos, e guardar em uma lista que é 
#  printada sempre no mesmo lugar da tela.
#  adicionar e remover de acordo com a ação do usuário
#  toda vez que acontecer uma repetição do loop, jogar o cursor pra linha certa


# while True:
#     inputted_value = str(input("Esperando input:"))
#     comandos = inputted_value.split()
#     if comandos[0] != "timer":
#         next
#     tempo = int(comandos[1])
#     for minutes in reversed(range(0, tempo)):
#         for seg in reversed(range(0, 60)):
#             print(f"{minutes}:{seg} ", end="\r", flush=True)
#             time.sleep(1)
#     print("Time's up!")

def timer_print(tempo):
    timer_rodando = True
    for minutes in reversed(range(0, tempo)):
        for seg in reversed(range(0, 60)):
            yx = curses.getsyx()
            x = yx[1]
            y = yx[0]
            screen.addstr(0,0, f"{minutes}:{seg}")
            screen.move(y,x)
            screen.refresh()
            time.sleep(1)
    print("Acabou o tempo!")

timer_rodando = False
last_y = 0
last_x = 1
screen = curses.initscr()
curses.curs_set(1)
screen.clear()
while True:
    timer_rodando = False
    while True:
        screen.addstr(last_x,0,">>")
        screen.clrtoeol()
        inputted_value = screen.getstr(last_x,3).decode('utf-8').strip()
        last_y = 3
        last_x = last_x+1
        if inputted_value == 'sair':
            break
        else:
            comandos = inputted_value.split()
            if comandos[0] != "timer":
                next
            tempo = int(comandos[1])
            threading.Thread(target = timer_print, args=[tempo], daemon=True).start()
    