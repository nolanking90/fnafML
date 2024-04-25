import mss
from pynput.mouse import Button, Controller
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

main_menu_actions = [(185, 418), (260, 498)]

game_menu_actions = [
    (59, 419),
    (57, 334),
    (59, 100),
    (1217, 439),
    (1219, 364),
    (1217, 100),
]

cam_menu_actions = {
    "1a": (993, 358),
    "1b": (966, 410),
    "1c": (930, 491),
    "2a": (991, 608),
    "2b": (976, 645),
    "3": (901, 592),
    "4a": (1083, 601),
    "4b": (1084, 647),
    "5": (858, 437),
    "6": (1185, 570),
    "7": (1191, 437),
}

def click_pos(x: int, y: int):
    mouse = Controller()
    mouse.position = (x, y)
    mouse.click(Button.left, 1)


def drag_to_screen():
    mouse = Controller()
    mouse.position = (571, 0)
    mouse.position = (571, 570)
    y = 570
    while y < 690:
        mouse.move(0, 1)
        y += 1


# Mouse clicked at (571, 677)Drag to open screen
def toggle_screen():
    drag_to_screen()
    click_pos(571, 677)


# Menu to pick actions
def main_menu():
    print("Main Menu")
    print("1. New Game")
    print("2. Continue Game")

    action = int(input("Select an action: ")) - 1
    if action in [0, 1]:
        click_pos(*main_menu_actions[action])
    else:
        print("Invalid input")


def game_menu():
    while True:
        print("Game Menu")
        print("1. Left Light")
        print("2. Left Door")
        print("3. Look Left")
        print("4. Right Light")
        print("5. Right Door")
        print("6. Look Right")
        print("7. Open Screen")
        print("8. Exit Game Menu")

        action = int(input("Select an action: ")) - 1
        if action in range(6):
            click_pos(*game_menu_actions[action])
        elif action == 6:
            toggle_screen()
        elif action == 7:
            break
        else:
            print("Invalid input")


def cam_menu():
    while True:
        print("Cam Menu")
        print("0. Close Screen")
        print("Enter the number of the camera you want to view")
        print("Cam 1a")
        print("Cam 1b")
        print("Cam 1c")
        print("Cam 2a")
        print("Cam 2b")
        print("Cam 3")
        print("Cam 4a")
        print("Cam 4b")
        print("Cam 5")
        print("Cam 6")
        print("Cam 7")
        print("8. Exit Cam Menu")

        action = input("Select an action: ")
        if action in cam_menu_actions:
            click_pos(*cam_menu_actions[action])
        elif action == "0":
            toggle_screen()
            break
        elif action == "8":
            break
        else:
            print("Invalid input")


def on_main_menu():
    if on_main_menu_helper():
        return True
    else:
        return on_main_menu_helper()


def on_main_menu_helper():
    reference = Image.open("mainmenu.png")
    reference_gray = np.array(reference)

    avg_screen_gray = np.zeros_like(reference_gray).astype(float)

    with mss.mss() as sct:
        for _ in range(10):
            screen = sct.grab(sct.monitors[1])
            screen_raw = Image.frombytes(
                "RGB",
                screen.size,
                screen.bgra,
                "raw",
                "BGRX"
            )

            screen_gray = cv2.cvtColor(np.array(screen_raw), cv2.COLOR_BGR2GRAY)
            screen_gray = screen_gray[
                :screen_gray.shape[0] // 2, 50:screen_gray.shape[1] // 2
            ]
            avg_screen_gray += screen_gray

    avg_screen_gray /= 10
    avg_screen_gray = avg_screen_gray.astype(np.uint8)
    cv2.fastNlMeansDenoising(avg_screen_gray, avg_screen_gray, 50, 7, 21)

    similarity = mse(avg_screen_gray, reference_gray)
    cv2.imwrite("avg_screen_gray_main.png", avg_screen_gray)

    if similarity < 1200:
        return True
    else:
        return False


def on_cam_menu():
    reference = Image.open("screen.png")
    reference_gray = np.array(reference)
    # cv2.fastNlMeansDenoising(reference_gray, reference_gray, 27, 7, 21)

    avg_screen_gray = np.zeros_like(reference_gray).astype(float)

    with mss.mss() as sct:
        for _ in range(10):
            screen = sct.grab(sct.monitors[1])
            screen_raw = Image.frombytes(
                "RGB",
                screen.size,
                screen.bgra,
                "raw",
                "BGRX"
            )

            screen_gray = cv2.cvtColor(np.array(screen_raw), cv2.COLOR_BGR2GRAY)
            screen_gray = screen_gray[330:, 825:]
            avg_screen_gray += screen_gray

    avg_screen_gray /= 10
    avg_screen_gray = avg_screen_gray.astype(np.uint8)
    cv2.fastNlMeansDenoising(avg_screen_gray, avg_screen_gray, 50, 7, 21)
    avg_screen_gray = cv2.bitwise_and(avg_screen_gray, reference_gray)

    cv2.imwrite("avg_screen_gray_cam.png", avg_screen_gray)
    similarity = ssim(avg_screen_gray, reference_gray)

    if similarity > 0.75:
        return True
    else:
        return False


def on_game_menu():
    reference = Image.open("left.png")
    reference_gray = cv2.cvtColor(np.array(reference), cv2.COLOR_BGR2GRAY)

    avg_screen_gray = np.zeros_like(reference_gray).astype(float)

    with mss.mss() as sct:
        for _ in range(10):
            screen = sct.grab(sct.monitors[1])
            screen_raw = Image.frombytes(
                "RGB",
                screen.size,
                screen.bgra,
                "raw",
                "BGRX"
            )

            screen_gray = cv2.cvtColor(np.array(screen_raw), cv2.COLOR_BGR2GRAY)
            avg_screen_gray += screen_gray

    avg_screen_gray /= 10
    avg_screen_gray = avg_screen_gray.astype(np.uint8)

    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(reference_gray, None)
    kp2, des2 = orb.detectAndCompute(avg_screen_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    if des1 is None or des2 is None:
        return False

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    threshold = 200
    is_similar = len(matches) > threshold

    return is_similar



    # leftsimilarity = ssim(screen_gray, reference_gray)
    # cv2.imwrite("avg_screen_gray_game.png", avg_screen_gray)

    # reference = Image.open("right.png")
    # reference_gray = cv2.cvtColor(np.array(reference), cv2.COLOR_BGR2GRAY)
    # rightsimilarity = ssim(screen_gray, reference_gray)
    # cv2.imwrite("avg_screen_gray_game.png", avg_screen_gray)

    # if leftsimilarity > 0.75:
        # return True
    # elif rightsimilarity > 0.75:
        # return True
    # else:
        # return False


# print("Welcome to ProtoObserver")
# while True:
    # if on_main_menu():
        # main_menu()
    # elif on_cam_menu():
        # cam_menu()
    # elif on_game_menu():
        # game_menu()
    # else:
        # print("Unknown screen")
        # print("1. Main Menu")
        # print("2. Game Menu")
        # print("3. Cam Menu")
        # print("4. Exit")

        # action = input("Select an action: ")
        # if action == "1":
            # main_menu()
        # elif action == "2":
            # game_menu()
        # elif action == "3":
            # cam_menu()
        # elif action == "4":
            # break
        # else:
            # print("Invalid input")

# cProfile.run("on_main_menu()")
# cProfile.run("on_cam_menu()")
# cProfile.run("on_game_menu()")
