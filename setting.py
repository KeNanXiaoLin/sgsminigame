import os
from enum import Enum
import sys
import logging


# 日志配置
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'
LOG_FILE_NAME = 'log.txt'
LOG_FILE_ENCODING = 'utf-8'
LOG_FILE_MODE = 'a'
with open(LOG_FILE_NAME, "w", encoding=LOG_FILE_ENCODING) as f:
    f.write("开始记录日志：\n")

logging.basicConfig(level=LOG_LEVEL,
                    format=LOG_FORMAT,
                    datefmt=LOG_DATE_FORMAT,
                    filename=LOG_FILE_NAME,
                    encoding=LOG_FILE_ENCODING,
                    filemode=LOG_FILE_MODE)

WINDOW_SIZE = (163, 33, 1602, 946)

RESULTS_FOLDER = "images_res"
CONFIG_FILE = "config.yaml"

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # 获取exe文件所在的目录路径
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    IMAGE_FOLDER = os.path.join(base_path, "data")
    # logging.info(f"打包成exe文件,文件路径为{base_path}")
else:
    IMAGE_FOLDER = "images"
    # logging.info(f"未打包成exe文件,文件路径为{os.path.abspath(__file__)}")

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
GUOGAO_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "guogao.png")
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
