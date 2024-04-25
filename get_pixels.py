from pynput.mouse import Listener


def on_click(x, y, button, pressed):
    if pressed:
        print("Mouse clicked at ({0}, {1})".format(x, y))


# Listen for mouse clicks
def listen():
    with Listener(on_click=on_click) as listener:
        listener.join()
