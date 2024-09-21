import os
from enum import Enum
import sys



WINDOW_SIZE = (163,33,1602,946)

RESULTS_FOLDER = "images_res"
CONFIG_FILE = "config.yaml"
IMAGE_FOLDER = "images"
START_FISH_BUTTON_PATH = os.path.join(IMAGE_FOLDER, "start_fish.png")
UP_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "01_up.png")
LEFT_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "02_left.png")
DOWN_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "03_un.png")
RIGHT_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "04_right.png")
WIND_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "05_wind.png")
FIRE_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "06_fire.png")
RAY_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "07_ray.png")
ELE_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "08_electricity.png")
HUANER_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "huaner.png")
USE_BUTTON_PATH = os.path.join(IMAGE_FOLDER, "use_button.png")
TIME_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "time.png")
BUY_BUTTON_PATH = os.path.join(IMAGE_FOLDER, "buy_button.png")
PUSH_GAN_BUTTON_PATH = os.path.join(IMAGE_FOLDER, "push_gan_button.png")
AGAIN_BUTTON_PATH = os.path.join(IMAGE_FOLDER, "again_button.png")
CURRENT_UI_PATH = os.path.join(IMAGE_FOLDER, "current_UI.png")


class fish_state(Enum):
    DEFAULT = 0
    PAO_GAN = 1
    NO_YUER = 2
    BU_YU = 3
    START_FISHING = 4
    END_FISHING = 5
    MIAO_SHA = 6
    EXIT = 7