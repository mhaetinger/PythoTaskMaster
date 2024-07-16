import curses
import sys
import threading
import time
import functions
import uuid


def get_all_task_names(items):
    return [task.name for task in items]


def get_all_task_ids(items):
    return [task.id for task in items]


class Task:
    def __init__(self, name):
        self.name = name
        self.id = generate_id()


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
    print_on_screen("O tempo acabou!")
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


def splitstrip(text, splitter=None):
    splitted = []
    for _ in text.split(splitter):
        if _.strip() != "":
            splitted.append(_.strip())
    return splitted


def getlaststr(text, splitter):
    value = splitstrip(text, splitter)
    if len(value) == 1:
        return value[0]
    else:
        return value[1]


def is_empty(text):
    return text.strip() == ""


def readInput():
    global last_x
    global last_y
    screen.refresh()
    screen.addstr(last_x, 0, ">>")
    screen.clrtoeol()
    inputted_value = screen.getstr(last_x, 3).decode("utf-8").strip()
    last_x = last_x + 1
    last_y = 3
    return inputted_value


# def handle_resize():
#    while True:
#        com = screen.getch()
#        if com == curses.KEY_RESIZE:
#            screen.resize()
def show_exception_and_exit(exc_type, exc_value, tb):
    f = open("cli_logs.txt", "a")
    f.write(f"{exc_type}, {exc_value}, {tb}")


sys.excepthook = show_exception_and_exit
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


def generate_id():
    return str(uuid.uuid4())


def verificar_e_remover(list, inputted_value, operacao):
    argsString = getlaststr(inputted_value, operacao)
    args = splitstrip(argsString, ",")
    reacurring_tasks = [task for task in list for _task in args if task.name == _task]
    for _ in reacurring_tasks:
        del list[list.index(_)]
        print_on_screen(f"Operação em {_.name} concluída!")
    return list

while True:
    inputted_value = readInput()
    comandos = splitstrip(inputted_value)
    input_number = len(comandos)
    if input_number == 0:
        continue
    if comandos[0] == "timer":
        if input_number == 1:
            print_missing_args(comandos[0])
            continue
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
            raw_args = getlaststr(inputted_value, "tasks")
            if is_empty(raw_args):
                print_missing_args(comandos[3])
                continue
            task_args = splitstrip(raw_args, ",")
            if len(task_args) == 0:
                continue
            # checar se o for em uma lista vazia da exception
            for _ in task_args:
                tasks.append(Task(_.strip()))
                functions.salvar_input(get_all_task_names(tasks), tempo, get_all_task_ids(tasks), generate_id())
            run_clock_thread(tempo)
        else:
            print_unknown_command(comandos[3])
            continue
    elif comandos[0] == "tasks":
        for index, _ in enumerate(tasks):
            print_on_screen(f"Tarefa {index + 1} - {_.name}")
    elif comandos[0] == "check":
        tasks = verificar_e_remover(tasks, inputted_value, "check")
    elif comandos[0] == "remove":
        tasks = verificar_e_remover(tasks, inputted_value, "remove")
    elif comandos[0] == "uncheck":
        if len(comandos) == 1:
            print_missing_args(comandos[0])
            continue
        argsString = getlaststr(inputted_value, "uncheck")
        args = splitstrip(argsString, ",")
        for _ in args:
            tasks.append(Task(_))
        print_on_screen(f"Operação em {_} concluída!")
    # edit task1 to task2
    elif comandos[0] == "edit":
        if len(comandos) == 1:
            print_missing_args(comandos[0])
            continue
        argsString = getlaststr(inputted_value, "edit")
        args = splitstrip(argsString, " to ")
        arg1 = args[0]
        arg2 = args[1]
        reacurring_tasks = [task for task in tasks if task.name == arg1]
        if len(reacurring_tasks)==0:
            print_missing_args("to")
            continue
        for _ in reacurring_tasks:
            indice = tasks.index(_)
            valorAntigo = tasks[indice]
            valorNovo = arg2
            tasks[indice].name = valorNovo
            print_on_screen(f"Tarefa {valorAntigo.name} agora é {valorNovo}!")
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
