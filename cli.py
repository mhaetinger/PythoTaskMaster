import curses
import signal
import threading
import time


def timer_print(minutos, segundos):
    x = 0
    y = 0
    for _minutos in reversed(range(0, minutos)):
        global global_minutos
        global_minutos = _minutos + 1
        for _seg in reversed(range(0, segundos)):
            global global_segundos
            global_segundos = _seg + 1
            if should_global_thread_run is False:
                return
            yx = curses.getsyx()
            x = yx[1]
            y = yx[0]
            screen.addstr(0, 0, f"{_minutos}:{_seg}")
            screen.move(y, x)
            screen.refresh()
            time.sleep(1)
    screen.addstr(y, x, "O tempo acabou!")
    screen.refresh()


def print_on_screen(text):
    global last_x
    screen.addstr(last_x, 0, text)
    last_x = last_x + 1


def print_unknown_command(command):
    print_on_screen(f"Comando desconhecido! {command}")


def print_missing_args(command):
    print_on_screen(f"Faltam argumentos para o comando {command}!")


def create_clock_thread(minutos, segundos=60):
    return threading.Thread(target=timer_print, args=[minutos, segundos], daemon=True)


def run_clock_thread(minutos, segundos=60):
    global global_clock_thread
    global_clock_thread = create_clock_thread(minutos, segundos)
    global should_global_thread_run
    should_global_thread_run = True
    global_clock_thread.start()


def split_not_empty(text, splitter=None):
    splitted = []
    for _ in text.split(splitter):
        if _.strip() != "":
            splitted.append(_.strip())
    return splitted


def is_empty(text):
    return text.strip() == ""


def handle_resize():
    counter = 0
    while True:
        time.sleep(1)
        getch_result = screen.getch()
        if getch_result == curses.KEY_RESIZE:
            counter += 1
            print_on_screen(f"resize captured! {counter}")


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
handle_resize()
threading.Thread(handle_resize(), daemon=True).start()
while True:
    screen.refresh()
    screen.addstr(last_x, 0, ">>")
    screen.clrtoeol()
    inputted_value = screen.getstr(last_x, 3).decode("utf-8").strip()
    last_x = last_x + 1
    last_y = 3
    comandos = split_not_empty(inputted_value)
    input_number = len(comandos)
    if input_number == 0:
        continue
    if comandos[0] == "timer":
        if input_number == 1:
            print_missing_args(comandos[0])
            continue
        # testar se não precisa de um try catch aqui
        tempo = int(comandos[1])
        if input_number == 2:
            run_clock_thread(tempo)
            continue
        if comandos[2] != "+":
            print_unknown_command(comandos[2])
            continue
        if input_number == 3:
            print_missing_args(comandos[2])
            continue
        if comandos[3] == "tasks":
            raw_args = inputted_value.split("tasks")[1]
            if is_empty(raw_args):
                print_missing_args(comandos[3])
                continue
            task_args = split_not_empty(raw_args, ",")
            if len(task_args) == 0:
                continue
            # checar se o for em uma lista vazia da exception
            for _ in task_args:
                tasks.append(_.strip())
            run_clock_thread(tempo)
        else:
            print_unknown_command(comandos[3])
            continue
    elif comandos[0] == "tasks":
        for index, _ in enumerate(tasks):
            screen.addstr(last_x, 0, f"Tarefa {index + 1} - {_}")
            last_x = last_x + 1
    elif comandos[0] == "check":
        for _ in comandos[1].split(","):
            if _ in tasks:
                tasks.remove(_)
            screen.addstr(last_x, 0, f"Tarefa {_} concluída!")
            last_x = last_x + 1
    elif comandos[0] == "remove":
        for _ in comandos[1].split(","):
            tasks.remove(_)
            screen.addstr(last_x, 0, f"Tarefa {_} removida!")
            last_x = last_x + 1
    elif comandos[0] == "uncheck":
        for _ in comandos[1].split(","):
            tasks.add(_)
            last_x = last_x + 1
    elif comandos[0] == "edit":
        for _ in comandos[1].split(","):
            indice = tasks.index(_)
            valorAntigo = tasks[indice]
            valorNovo = comandos[3]
            tasks[indice] = valorNovo
            screen.addstr(last_x, 0, f"Tarefa {valorAntigo} agora é {valorNovo}!")
            last_x = last_x + 1
    elif comandos[0] == "stop":
        should_global_thread_run = False
        global_clock_thread = None
    elif comandos[0] == "pause":
        should_global_thread_run = False
    elif comandos[0] == "continue":
        if global_clock_thread is not None:
            should_global_thread_run = True
            global_clock_thread = create_clock_thread(
                global_minutos, global_segundos
            )
            global_clock_thread.start()
    elif comandos[0] == "quit":
        break
    else:
        continue
