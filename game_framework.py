import time
import os
frame_time = 0.0

running = None
stack = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def save_record_to_file(record):
    try:
        path = os.path.join(os.getcwd(), 'record.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(record)+'\n')
    except Exception as e:
        print('Failed to save record:', e)

def save_enter_to_file():
    try:
        path = os.path.join(os.getcwd(), 'record.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n')
    except Exception as e:
        print('Failed to save enter:', e)


def quit():
    global running
    running = False
    save_enter_to_file()


def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - current_time
        current_time += frame_time
        frame_rate = 1.0 / frame_time
        # print(f'Frame Time: {frame_time}, Frame Rate: {frame_rate}')

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
