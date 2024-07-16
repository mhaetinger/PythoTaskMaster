import curses
import sys
import threading
import time
import functions
import uuid


def get_all_task_names(items):
    return [task.name for task in items if task.enabled == True]


def get_all_task_ids(items):
    return [task.id for task in items if task.enabled == True]


class Task:
    def __init__(self, name):
        self.name = name
        self.id = generate_id()
        self.enabled = True


def timer_print(minutos, segundos):
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
            screen.addstr(1, 0, "                             ")
            screen.addstr(1, 0, f"{_minutos}:{_seg}")
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
    screen.addstr(0, 0, "Digite 'help' para ver comandos")
    screen.addstr(last_x, 0, ">>")
    screen.clrtoeol()
    inputted_value = screen.getstr(last_x, 3).decode("utf-8").strip()
    last_x = last_x + 1
    last_y = 3
    return inputted_value


def generate_id():
    return str(uuid.uuid4())


def verificar_e_remover(list, inputted_value, operacao):
    return list


last_y = 0
last_x = 2
timer_id = None
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
            if should_global_thread_run is True and global_clock_thread is not None:
                print_on_screen("Cancele o timer atual e tente novamente!")
                continue
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
            if len(comandos[3:]) == 1:
                print_missing_args(comandos[3])
                continue
            task_args = splitstrip(raw_args, ",")
            if len(task_args) == 0:
                continue
            if should_global_thread_run is True and global_clock_thread is not None:
                print_on_screen("Cancele o timer atual e tente novamente!")
                continue
            tasks.clear()
            for _ in task_args:
                tasks.append(Task(_.strip()))
            timer_id = generate_id()
            functions.salvar_input(get_all_task_names(tasks), tempo, get_all_task_ids(tasks), timer_id)
            run_clock_thread(tempo)
        else:
            print_unknown_command(comandos[3])
            continue
    elif comandos[0] == "tasks":
        for index, _ in enumerate(tasks):
            if _.enabled:
                print_on_screen(f"Tarefa {index + 1} - {_.name}")
    elif comandos[0] == "check":
        argsString = getlaststr(inputted_value, "check")
        args = splitstrip(argsString, ",")
        reacurring_tasks = [task for task in tasks if task.enabled for _task in args if task.name == _task]
        for _ in reacurring_tasks:
            tasks[tasks.index(_)].enabled = False
            functions.concluir_tarefa(_.id, timer_id)
            print_on_screen(f"{_.name} foi marcada como concluída!")
    elif comandos[0] == "remove":
        argsString = getlaststr(inputted_value, "remove")
        args = splitstrip(argsString, ",")
        reacurring_tasks = [task for task in tasks for _task in args if task.name == _task]
        for _ in reacurring_tasks:
            del tasks[tasks.index(_)]
            functions.remover_tarefa(_.id, timer_id)
            print_on_screen(f"{_.name} foi removido!")
    elif comandos[0] == "uncheck":
        if len(comandos) == 1:
            print_missing_args(comandos[0])
            continue
        argsString = getlaststr(inputted_value, "uncheck")
        args = splitstrip(argsString, ",")
        reacurring_tasks = [task for task in tasks if task.enabled == False for _task in args if task.name == _task]
        for _ in reacurring_tasks:
            functions.desconcluir_tarefa(_.id, timer_id)
            tasks[tasks.index(_)].enabled = True
        print_on_screen(f"Operação em {_.name} concluída!")
    elif comandos[0] == "edit":
        if len(comandos) == 1:
            print_missing_args(comandos[0])
            continue
        argsString = getlaststr(inputted_value, "edit")
        args = splitstrip(argsString, " to ")
        arg1 = args[0]
        arg2 = args[1]
        reacurring_tasks = [task for task in tasks if task.name == arg1 and task.enabled == True]
        if len(reacurring_tasks) == 0:
            print_missing_args("to")
            continue
        for _ in reacurring_tasks:
            indice = tasks.index(_)
            valorAntigo = tasks[indice].name
            valorNovo = arg2
            tasks[indice].name = valorNovo
            functions.editar_tarefa(_.id, timer_id, arg2)
            print_on_screen(f"Tarefa {valorAntigo} agora é {valorNovo}!")
    elif comandos[0] == "stop":
        should_global_thread_run = False
        global_clock_thread = None
        functions.concluir_timer(timer_id)
    elif comandos[0] == "pause":
        should_global_thread_run = False
        functions.pausa_timer(timer_id)
    elif comandos[0] == "continue":
        if global_clock_thread is not None:
            should_global_thread_run = True
            global_clock_thread = create_clock_thread(
                global_minutos, global_segundos
            )
            global_clock_thread.start()
            functions.continua_timer(timer_id)
    elif comandos[0] == "help":
        print_on_screen("timer {minutos} [+ tasks {nome task1}, {nome task 2}, ...]")
        print_on_screen("tasks")
        print_on_screen("check {nome task1}, {nome task2}, ...")
        print_on_screen("remove {nome task1}, {nome task2}, ...")
        print_on_screen("uncheck {nome task1}, {nome task2}, ...")
        print_on_screen("edit {nome task1} to {novo nome task1}")
        print_on_screen("stop")
        print_on_screen("pause")
        print_on_screen("continue")
        print_on_screen("quit")
        print_on_screen("\n")
    elif comandos[0] == "quit":
        break
    else:
        continue
