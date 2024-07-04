import time
import threading
import curses

def log(txt):
    logs.write(txt)
    logs.flush()

def timer_print(tempo):
    timer_rodando = True
    x = 0
    y = 0
    for minutes in reversed(range(0, tempo)):
        for seg in reversed(range(0, 60)):
            yx = curses.getsyx()
            x = yx[1]
            y = yx[0]
            screen.addstr(0,0, f"{minutes}:{seg}")
            screen.move(y,x)
            screen.refresh()
            time.sleep(1)
    screen.addstr(y,x, "O tempo acabou!")
    screen.refresh()

def handle_resize():
    while(True):
        key = screen.getch()
        log(key)
        if(key=="KEY_RESIZE"):
            h,w = screen.getmaxyx()
            screen.resize(h,w)
            log(f"resize detected! {h},{w}")    
                
logs = open("cli_logs.txt", "w")
timer_rodando = False
last_y = 0
last_x = 1
screen = curses.initscr()
curses.curs_set(1)
screen.clear()
threading.Thread(target=handle_resize, daemon=True).start()
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
    