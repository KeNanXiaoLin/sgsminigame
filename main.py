import win32gui
import win32con
import pyautogui
import time
import cv2
import numpy as np
import yaml
import keyboard
from threading import Thread
from setting import *
import logging


# 查找窗口句柄
def find_window(title):
    return win32gui.FindWindow(None, title)


# 获取窗口位置和大小
def get_window_rect(hwnd):
    return win32gui.GetWindowRect(hwnd)


def bring_to_front(hwnd):
    # 将窗口置于最前端
    win32gui.SetForegroundWindow(hwnd)
    # 确保窗口激活
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)


def get_screenshot(size, is_save=False, save_path=None):
    img = pyautogui.screenshot(region=size)
    img_np = np.array(img)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    if is_save:
        img.save(save_path)
    return img_np


def write_dict(config_dic, key, value):
    config_dic[key] = value


def write_yaml(data, name):
    with open(name, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)


def read_yaml(name):
    with open(name, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def press_mouse_move(start_x, start_y, x, y, button='left'):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(start_x + x, start_y + y, button=button)


def is_match_template_by_path(img_path, template_path, threshold=0.8):
    template = cv2.imread(template_path)
    img = cv2.imread(img_path)
    # 模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 如果找到匹配项，则返回True
    if len(loc[0]) > 0:
        return True
    else:
        return False


def is_match_template_by_img(img, template, threshold=0.8):
    # 模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 如果找到匹配项，则返回True
    if len(loc[0]) > 0:
        return True
    else:
        return False


def match_template_by_path(img_path, template_path, is_save=False, save_name=None, save_path=None, threshold=0.8):
    template = cv2.imread(template_path)
    img = cv2.imread(img_path)
    # 模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 如果找到匹配项，则返回位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    center = (int(max_loc[0] + template.shape[1] / 2), int(max_loc[1] + template.shape[0] / 2))
    cv2.circle(img, center, 5, (0, 0, 255), -1)
    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 1)
    if is_save:
        cv2.imwrite(os.path.join(save_path, save_name), img)
    return center


def match_template_by_img(img, template, is_save=False, save_name=None, save_path=None, threshold=0.8):
    # 模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # 如果找到匹配项，则返回位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    center = (int(max_loc[0] + template.shape[1] / 2), int(max_loc[1] + template.shape[0] / 2))
    cv2.circle(img, center, 5, (0, 0, 255), -1)
    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 0, 255), 1)
    if is_save:
        cv2.imwrite(os.path.join(save_path, save_name), img)
    return center


def check_current_UI():
    """
    检查当前状态,一共有5种UI：
    1.抛竿界面,对应:huaner.png,fish_state.PAO_GAN,抛竿界面有两种状态转换：
    一种是鱼饵不足，切换到鱼饵不足界面fish_state.NO_YUER，一种是鱼饵充足，正确进入钓鱼界面
    2.鱼饵不足界面,对应:use_button.png
    3.开始钓鱼界面,对应:time.png
    4.结束钓鱼界面,对应:again_button.png
    5.如果是史诗以上的鱼，还有秒杀界面,对应:01_up.png
    :return:
    """
    global current_state, size,current_img
    start_button = cv2.imread(START_FISH_BUTTON_PATH)
    huaner = cv2.imread(HUANER_IMAGE_PATH)
    use_button = cv2.imread(USE_BUTTON_PATH)
    time_icon = cv2.imread(TIME_IMAGE_PATH)
    buy_button = cv2.imread(BUY_BUTTON_PATH)
    push_gan_button = cv2.imread(PUSH_GAN_BUTTON_PATH)
    again_button = cv2.imread(AGAIN_BUTTON_PATH)
    up_button = cv2.imread(UP_IMAGE_PATH)
    current_UI_path = os.path.join(IMAGE_FOLDER, "current_UI.png")

    while True:
        current_img = get_screenshot(size, is_save=False, save_path=current_UI_path)
        if current_state == fish_state.DEFAULT:
            if is_match_template_by_img(current_img, start_button, threshold=0.8):
                logging.info("开始钓鱼界面，状态不变")
                continue
            elif is_match_template_by_img(current_img, huaner, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到抛竿状态")
                current_state = fish_state.PAO_GAN
            elif is_match_template_by_img(current_img, use_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到鱼饵不足状态")
                current_state = fish_state.NO_YUER
            elif is_match_template_by_img(current_img, again_button, threshold=0.7):
                logging.info(f"当前状态: {current_state} 转换到结束钓鱼状态")
                current_state = fish_state.END_FISHING
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.PAO_GAN:
            if is_match_template_by_img(current_img, use_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到鱼饵不足状态")
                current_state = fish_state.NO_YUER
            elif is_match_template_by_img(current_img, time_icon, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到开始钓鱼状态")
                current_state = fish_state.BU_YU
            elif is_match_template_by_img(current_img, buy_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 鱼饵不足")
                current_state = fish_state.EXIT
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.NO_YUER:
            if not is_match_template_by_img(current_img, use_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到抛竿状态")
                current_state = fish_state.PAO_GAN
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.BU_YU:
            if is_match_template_by_img(current_img, push_gan_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到开始钓鱼状态")
                current_state = fish_state.START_FISHING
            elif is_match_template_by_img(current_img, again_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到结束钓鱼状态")
                current_state = fish_state.END_FISHING
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.START_FISHING:
            if is_match_template_by_img(current_img, again_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到结束钓鱼状态")
                current_state = fish_state.END_FISHING
            elif is_match_template_by_img(current_img, up_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到秒杀状态")
                current_state = fish_state.MIAO_SHA
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.END_FISHING:
            if is_match_template_by_img(current_img, huaner, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到抛竿状态")
                current_state = fish_state.PAO_GAN
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.MIAO_SHA:
            if is_match_template_by_img(current_img, again_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到结束钓鱼状态")
                current_state = fish_state.END_FISHING
            elif is_match_template_by_img(current_img, push_gan_button, threshold=0.8):
                logging.info(f"当前状态: {current_state} 转换到继续钓鱼状态")
                current_state = fish_state.START_FISHING
            if keyboard.is_pressed('esc'):
                logging.info(f"当前状态: {current_state} 转换到退出状态, 退出原因: 按下esc")
                current_state = fish_state.EXIT
            continue
        elif current_state == fish_state.EXIT:
            logging.info("钓鱼结束")
            break


def fenlei_all_pos(point_list):
    """
    对识别出来的所有位置进行分类，得到图像的位置
    :return: 返回分类好的一堆点的平均值
    """
    res_points = []
    for i in range(len(point_list)):
        m_set = set()
        if point_list[i] is None:
            continue
        m_set.add(point_list[i])
        for j in range(i + 1, len(point_list)):
            if point_list[j] is None:
                continue
            if abs(point_list[i][0] - point_list[j][0]) < 10 and abs(point_list[i][1] - point_list[j][1]) < 10:
                m_set.add(point_list[j])
                point_list[j] = None
        if len(m_set) > 1:
            average_x = int(sum([x[0] for x in m_set]) / len(m_set))
            average_y = int(sum([x[1] for x in m_set]) / len(m_set))
            res_points.append((average_x, average_y))
    return res_points


def handle_window(config_dic):
    """
    处理窗口,包括查找窗口、调整窗口大小、置顶窗口等
    :return:
    """
    window_title = config_dic.get('window_title', None)
    if window_title is None:
        window_title = "MuMu模拟器12"
        write_dict(config_dic, 'window_title', window_title)
        write_yaml(config_dic, CONFIG_FILE)
        exit("请设置窗口标题")
    # 示例：查找记事本窗口
    hWnd = find_window(window_title)
    if hWnd:
        bring_to_front(hWnd)
        win32gui.SetWindowPos(hWnd, None, size[0], size[1], size[2], size[3], 0)
        time.sleep(0.5)


def main():
    global current_state, size,current_img

    # 都是配置文件里面读取出来的变量
    size = WINDOW_SIZE
    if not os.path.exists(CONFIG_FILE):
        config_dic = {}
    else:
        config_dic = read_yaml(CONFIG_FILE)
    write_dict(config_dic, 'window_size', size)
    current_state = fish_state.DEFAULT
    handle_window(config_dic)

    start_fishing_pos = config_dic.get('start_fishing_pos', None)
    lagan_pos = config_dic.get('lagan_pos', None)
    guogao_pos = config_dic.get('guogao_pos', None)
    guogao_color = config_dic.get('guogao_color', None)
    orgin_lagan_color = config_dic.get('orgin_lagan_color', None)
    dir_icon_pos_list = config_dic.get('dir_icon_pos_list', None)
    again_icon_center = config_dic.get('again_icon_center', None)
    shougan_time = 0
    shougan_interval = config_dic.get('shougan_interval', 15)
    write_dict(config_dic, 'shougan_interval', shougan_interval)
    wait_time = config_dic.get('wait_time', 0.065)
    write_dict(config_dic, 'wait_time', wait_time)
    dir_icon_path_list = [UP_IMAGE_PATH, DOWN_IMAGE_PATH, LEFT_IMAGE_PATH,
                          RIGHT_IMAGE_PATH, WIND_IMAGE_PATH, FIRE_IMAGE_PATH,
                          RAY_IMAGE_PATH, ELE_IMAGE_PATH]
    # 用于控制某些状态的点击次数
    start_fishing_first_click = True
    first_paogan = True
    first_huner = True
    first_buyu = True
    first_diaoyu = True
    first_again = True
    first_miao_sha = True
    # 开启一个线程，检查当前状态
    t1 = Thread(target=check_current_UI)
    t1.start()
    while True:
        if current_state == fish_state.DEFAULT and start_fishing_first_click:
            logging.info("进入默认状态")
            if start_fishing_pos is None:
                start_fishing_UI_path = os.path.join(IMAGE_FOLDER, "start_fishing_UI.png")
                start_fishing_UI_img = get_screenshot(size, is_save=False, save_path=start_fishing_UI_path)
                start_fishing_button_img = cv2.imread(START_FISH_BUTTON_PATH)
                start_fishing_pos = match_template_by_img(start_fishing_UI_img, start_fishing_button_img, is_save=False,
                                                          save_name="start_fishing_pos.png", save_path=RESULTS_FOLDER)
                start_fishing_pos = (start_fishing_pos[0] + size[0], start_fishing_pos[1] + size[1])
                write_dict(config_dic, 'start_fishing_pos', start_fishing_pos)
                write_yaml(config_dic, CONFIG_FILE)
                logging.info(f"""开始钓鱼按钮位置: {start_fishing_pos}""")
            pyautogui.click(start_fishing_pos)
            start_fishing_first_click = False
            continue
        elif current_state == fish_state.PAO_GAN and first_paogan:
            logging.info("进入抛竿状态")
            # 模拟点击拉杆
            press_mouse_move(start_x=start_fishing_pos[0], start_y=start_fishing_pos[1], x=0, y=-100, button='left')
            first_paogan = False
            first_again = True
            continue
        elif current_state == fish_state.NO_YUER and first_huner:
            logging.info("进入鱼饵不足状态")
            use_button_path = os.path.join(IMAGE_FOLDER, "use_button.png")
            huaner_UI_path = os.path.join(IMAGE_FOLDER, "huaner_UI.png")
            huaner_UI_img = get_screenshot(size, is_save=False, save_path=huaner_UI_path)
            use_button_img = cv2.imread(use_button_path)
            use_button_pos = match_template_by_img(huaner_UI_img, use_button_img, is_save=False,
                                                   save_name="use_button_pos.png", save_path=RESULTS_FOLDER)
            use_button_pos = (use_button_pos[0] + size[0], use_button_pos[1] + size[1])
            pyautogui.click(use_button_pos)
            first_huner = False
            first_paogan = True
            continue
        elif current_state == fish_state.BU_YU and first_buyu:
            logging.info("进入叉鱼状态")
            pyautogui.click(start_fishing_pos)
            first_buyu = False
            continue
        elif current_state == fish_state.START_FISHING:
            logging.info("进入开始钓鱼状态")
            if lagan_pos is None:
                shotscreen_path = os.path.join(IMAGE_FOLDER, "fishing_shotscreen.png")
                fishing_shotscreen_img = get_screenshot(size, is_save=False, save_path=shotscreen_path)
                push_gan_icon_img = cv2.imread(PUSH_GAN_BUTTON_PATH)
                guogao_img = cv2.imread(GUOGAO_IMAGE_PATH)
                lagan_pos = match_template_by_img(fishing_shotscreen_img, push_gan_icon_img, is_save=False,
                                                  save_name="push_gan_icon.png", save_path=RESULTS_FOLDER)
                guogao_pos = match_template_by_img(fishing_shotscreen_img, guogao_img, is_save=False,
                                                   save_name="guogao_icon.png", save_path=RESULTS_FOLDER)
                lagan_pos = (lagan_pos[0] + size[0], lagan_pos[1] + size[1])
                guogao_pos = (guogao_pos[0] + size[0], guogao_pos[1] + size[1])
                guogao_color = pyautogui.pixel(guogao_pos[0], guogao_pos[1])
                write_dict(config_dic, 'lagan_pos', lagan_pos)
                write_dict(config_dic, 'guogao_pos', guogao_pos)
                write_dict(config_dic, 'guogao_color', guogao_color)
                logging.info(f"拉杆位置: {lagan_pos},过高位置: {guogao_pos}, 过高颜色: {guogao_color}")
                orgin_lagan_color = pyautogui.pixel(lagan_pos[0], lagan_pos[1])
                write_dict(config_dic, 'orgin_lagan_color', orgin_lagan_color)
                logging.info(f"拉杆颜色: {orgin_lagan_color}""")
                write_yaml(config_dic, CONFIG_FILE)

            # 第一次进入钓鱼界面，模拟一段时间长按
            if first_diaoyu:
                logging.info("第一次进入钓鱼界面，模拟长按")
                shougan_time = time.time()
                # 模拟长按一段时间
                pyautogui.mouseDown(start_fishing_pos, button='left')
                time.sleep(2)
                pyautogui.mouseUp(button='left')
                first_diaoyu = False
            else:
                now_lagan_color = pyautogui.pixel(lagan_pos[0], lagan_pos[1])
                now_guogao_color = pyautogui.pixel(guogao_pos[0], guogao_pos[1])
                if now_lagan_color != config_dic['orgin_lagan_color']:
                    logging.info("拉杆颜色改变，尝试左右移动拉杆")
                    press_mouse_move(start_x=lagan_pos[0], start_y=lagan_pos[1], x=100, y=0, button='left')
                    press_mouse_move(start_x=lagan_pos[0], start_y=lagan_pos[1], x=-100, y=0, button='left')
                if now_guogao_color != config_dic['guogao_color']:
                    wait_time = 0.2
                    config_dic['wait_time'] = wait_time
                else:
                    wait_time = 0.01
                    config_dic['wait_time'] = wait_time
                if time.time() - shougan_time > shougan_interval:
                    logging.info("可以收杆了")
                    press_mouse_move(start_x=start_fishing_pos[0], start_y=start_fishing_pos[1], x=0, y=-75,
                                     button='left')
                    shougan_time = time.time()
                pyautogui.click(start_fishing_pos, button='left')
                logging.info(f"当前等待时间: {wait_time}")
                time.sleep(wait_time)
            # 开始钓鱼
            continue
        elif current_state == fish_state.END_FISHING and first_again:
            logging.info("进入结束钓鱼状态")
            # 结束钓鱼
            if again_icon_center is None:
                agian_icon_path = os.path.join(IMAGE_FOLDER, "again_button.png")
                again_icon = cv2.imread(agian_icon_path)
                next_screenshot_path = os.path.join(IMAGE_FOLDER, "game_over_screenshot.png")
                game_over_screenshot_img = get_screenshot(size, is_save=False, save_path=next_screenshot_path)
                again_icon_center = match_template_by_img(game_over_screenshot_img, again_icon, is_save=False,
                                                          save_name="again_icon.png", save_path=RESULTS_FOLDER)
                again_icon_center = (again_icon_center[0] + size[0], again_icon_center[1] + size[1])
                write_dict(config_dic, 'again_icon_center', again_icon_center)
                write_yaml(config_dic, CONFIG_FILE)
                logging.info(f"点击再次钓鱼按钮位置: {again_icon_center}")

            pyautogui.click(again_icon_center)
            first_again = False
            start_fishing_first_click = True
            first_paogan = True
            first_huner = True
            first_buyu = True
            first_diaoyu = True
            first_miao_sha = True
            continue
        elif current_state == fish_state.MIAO_SHA and first_miao_sha:
            # 秒杀界面
            if dir_icon_pos_list is None:
                half_buttom_screenshot_path = os.path.join(IMAGE_FOLDER, "half_buttom_screenshot.png")
                half_buttom_size = (size[0], (size[1] + size[3]) // 2, size[2], (size[1] + size[3]) // 2)
                half_buttom_img = get_screenshot(half_buttom_size, is_save=False,
                                                 save_path=half_buttom_screenshot_path)

                dir_icon_pos_list = {}

                for dir_icon_path in dir_icon_path_list:
                    logging.info(f"当前方向图标路径: {dir_icon_path}")
                    dir_icon = cv2.imread(dir_icon_path)
                    dir_icon_pos = match_template_by_img(half_buttom_img, dir_icon, is_save=False,
                                                         save_name=os.path.basename(dir_icon_path),
                                                         save_path=RESULTS_FOLDER)
                    dir_icon_pos = (dir_icon_pos[0] + half_buttom_size[0], dir_icon_pos[1] + half_buttom_size[1])
                    name = os.path.basename(dir_icon_path).split('.')[0]
                    dir_icon_pos_list[name] = dir_icon_pos
                    logging.info(f"{name} 方向图标位置: {dir_icon_pos}""")
                write_dict(config_dic, 'dir_icon_pos_list', dir_icon_pos_list)
                write_yaml(config_dic, CONFIG_FILE)
            all_icon_dic = {}
            half_top_icon_path = os.path.join(IMAGE_FOLDER, "half_top_icon.png")
            half_top_size = (size[0], size[1], size[2], (size[3] + size[1]) // 2)
            half_top_img = get_screenshot(half_top_size, is_save=False,
                                          save_path=half_top_icon_path)
            for dir_icon_path in dir_icon_path_list:
                dir_icon = cv2.imread(dir_icon_path)
                res = cv2.matchTemplate(half_top_img, dir_icon, cv2.TM_CCOEFF_NORMED)
                res_loc = np.where(res >= 0.8)
                if len(res_loc[0]) > 0:
                    points = list(zip(*res_loc[::-1]))
                    res_points = fenlei_all_pos(points)
                    for point in res_points:
                        all_icon_dic[point] = os.path.basename(dir_icon_path).split('.')[0]
            # 排序，从左到右
            all_icon_list = sorted(all_icon_dic.items(), key=lambda x: x[0][0])
            for pos, name in all_icon_list:
                logging.info(f"{name}, 位置: {pos}")
                print(f"{name}, 位置: {pos}")
                click_pos = dir_icon_pos_list[name]
                pyautogui.click(click_pos)
            continue
        elif current_state == fish_state.EXIT:
            write_yaml(config_dic, CONFIG_FILE)
            logging.info("退出程序")
            break
        else:
            continue


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
