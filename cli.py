import time
import threading
import curses

def timer_print(minutos, segundos):
    x = 0
    y = 0
    for _minutos in reversed(range(0, minutos)):
        global global_minutos
        global_minutos = _minutos+1 
        for _seg in reversed(range(0, segundos)):
            global global_segundos
            global_segundos = _seg+1
            if should_global_thread_run is False:
                return
            yx = curses.getsyx()
            x = yx[1]
            y = yx[0]
            screen.addstr(0,0, f"{_minutos}:{_seg}")
            screen.move(y,x)
            screen.refresh()
            time.sleep(1)
    screen.addstr(y,x, "O tempo acabou!")
    screen.refresh()
    
def createClockThread(minutos, segundos = 60):
    return threading.Thread(target = timer_print, args=[minutos, segundos], daemon=True)

# def handle_resize():
#    while True:
#        com = screen.getch()
#        if com == curses.KEY_RESIZE:
#            screen.resize() 
      
last_y = 0
last_x = 1
tasks = []
should_global_thread_run = False
global_clock_thread = None
global_minutos = 0
global_segundos = 0
screen = curses.initscr()
curses.curs_set(1)
screen.keypad(True)
screen.clear()
while True:
    while True:
        screen.refresh()
        screen.addstr(last_x,0,">>")
        screen.clrtoeol()
        inputted_value = screen.getstr(last_x,3).decode('utf-8').strip()
        last_y = 3
        last_x = last_x+1
        comandos = inputted_value.split()
        if comandos[0]=="timer":
            tempo = int(comandos[1])
            if comandos[2]=="tasks":
                for _ in comandos[3].split(","):
                    tasks.append(_)
            global_clock_thread = createClockThread(tempo)
            should_global_thread_run = True
            global_clock_thread.start()
        elif comandos[0]=="tasks":
            for index, _ in enumerate(tasks):
                screen.addstr(last_x, 0, f"Tarefa {index+1} - {_}")
                last_x = last_x+1
        elif comandos[0]=="check":
            for _ in comandos[1].split(","):
                if _ in tasks:
                    tasks.remove(_)
                screen.addstr(last_x, 0, f"Tarefa {_} concluída!")
                last_x = last_x+1
        elif comandos[0]=="remove":
            for _ in comandos[1].split(","):
                tasks.remove(_)
                screen.addstr(last_x, 0, f"Tarefa {_} removida!")
                last_x = last_x+1
        elif comandos[0]=="uncheck":
            for _ in comandos[1].split(","):
                tasks.add(_)
                last_x = last_x+1
        elif comandos[0]=="edit":
            for _ in comandos[1].split(","):
                indice = tasks.index(_)
                valorAntigo = tasks[indice]
                valorNovo = comandos[3]
                tasks[indice] = valorNovo
                screen.addstr(last_x, 0, f"Tarefa {valorAntigo} agora é {valorNovo}!")
                last_x = last_x+1
        elif comandos[0]=="stop":
            should_global_thread_run = False
            global_clock_thread = None
        elif(comandos[0] == "pause"):
            should_global_thread_run = False
        elif(comandos[0]=="continue"):
            if(global_clock_thread is not None):
                should_global_thread_run = True
                global_clock_thread = createClockThread(global_minutos, global_segundos)
                global_clock_thread.start()
        else:
            next
    