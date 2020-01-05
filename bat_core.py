# encoding:gbk
from PIL import Image
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import time
import configparser
import os
# import pytesseract
# import os
# import cv2


# 单击
def single_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0)
    return


# 向下拖拽
def drag_to_bottom(x, y, distance):
    return


# 向上拖拽
def drag_to_top(x, y, distance):
    total = 0
    step = 20
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0)
    while total < distance:
        total = total + step
        win32api.SetCursorPos((x, y - total))
        win32api.Sleep(20)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, x, y - total, 0)
    return


# 脚本退出
def bat_exit(shutdown):
    if shutdown != 0:
        print("脚本执行完毕，5秒后将关机")
        win32api.Sleep(5000)
        os.system("shutdown /s /t 0")
    else:
        input("脚本执行完毕，输入回车以结束\n")
        exit(0)
    return


# 抓取指定位置图像
def grab_pos(left, top, right, bottom):
    size = (left, top, right, bottom)
    img = ImageGrab.grab(size)
    img.save("grab.jpg")
    return


# 图像比较类
class CompareImage:
    @staticmethod
    def calculate(image1, image2):
        g = image1.histogram()
        s = image2.histogram()
        assert len(g) == len(s), "error"

        data = []

        for index in range(0, len(g)):
            if g[index] != s[index]:
                data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
            else:
                data.append(1)

        return sum(data) / len(g)

    @staticmethod
    def split_image(image, part_size):
        pw, ph = part_size
        w, h = image.size

        sub_image_list = []

        assert w % pw == h % ph == 0, "error"

        for i in range(0, w, pw):
            for j in range(0, h, ph):
                sub_image = image.crop((i, j, i + pw, j + ph)).copy()
                sub_image_list.append(sub_image)

        return sub_image_list

    @staticmethod
    def compare_image(file_image1, file_image2, size=(256, 256), part_size=(64, 64)):
        '''
        'file_image1'和'file_image2'是传入的文件路径
         可以通过'Image.open(path)'创建'image1' 和 'image2' Image 对象.
         'size' 重新将 image 对象的尺寸进行重置，默认大小为256 * 256 .
         'part_size' 定义了分割图片的大小.默认大小为64*64 .
         返回值是 'image1' 和 'image2'对比后的相似度，相似度越高，图片越接近，达到1.0说明图片完全相同。
        '''

        image1 = Image.open(file_image1)
        image2 = Image.open(file_image2)

        img1 = image1.resize(size).convert("RGB")
        sub_image1 = CompareImage.split_image(img1, part_size)

        img2 = image2.resize(size).convert("RGB")
        sub_image2 = CompareImage.split_image(img2, part_size)

        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += CompareImage.calculate(im1, im2)

        x = size[0] / part_size[0]
        y = size[1] / part_size[1]

        pre = round((sub_data / (x * y)), 6)
        # print(str(pre * 100) + '%')
        print('图像对比结果: ' + str(pre))
        return pre


# # 提取图像文字
# def get_text_from_img():
#     # 初始化tesseract
#     pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract'
#     img_text = pytesseract.image_to_string(Image.open("grab.png"), lang="chi_sim")
#     img_text = img_text.replace(" ", "")
#     return img_text


# def calculate(image1, image2):
#     # 灰度直方图算法
#     # 计算单通道的直方图的相似值
#     hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
#     hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
#     # 计算直方图的重合度
#     degree = 0
#     for i in range(len(hist1)):
#         if hist1[i] != hist2[i]:
#             degree = degree + \
#                 (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
#     else:
#         degree = degree + 1
#     degree = degree / len(hist1)
#     return degree


# def classify_hist_with_split(image1, image2, size=(256, 256)):
#     # RGB每个通道的直方图相似度
#     # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
#     image1 = cv2.resize(image1, size)
#     image2 = cv2.resize(image2, size)
#     sub_image1 = cv2.split(image1)
#     sub_image2 = cv2.split(image2)
#     sub_data = 0
#     for im1, im2 in zip(sub_image1, sub_image2):
#         sub_data += calculate(im1, im2)
#     sub_data = sub_data / 3
#     return sub_data


def image_binarization(img_path, threshold):
    # 图片灰度化
    img = Image.open(img_path)
    img = img.convert('L')
    img.save("grey.jpg")
    #
    # table = []
    # for i in range(256):
    #     if i < threshold:
    #         table.append(0)
    #     else:
    #         table.append(1)
    #
    # # 图片二值化
    # img = img.point(table, '1')
    # img.save("binarization.jpg")


def translate_xionggui(xionggui_id):
    if xionggui_id == 1:
        return "步"
    elif xionggui_id == 2:
        return "弓"
    elif xionggui_id == 3:
        return "枪"
    elif xionggui_id == 4:
        return "飞"
    elif xionggui_id == 5:
        return "骑"
    elif xionggui_id == 6:
        return "僧"


def translate_yes_or_no(yes_or_no):
    if yes_or_no == 0:
        return "否"
    elif yes_or_no == 1:
        return "是"


def need_eat_bg(start_pc, pc_grow, eat_bg, suc_round):
    current_pc = int(start_pc + pc_grow + eat_bg * 50 - suc_round * 16)
    if current_pc < 16:
        print("当前体力为：" + str(current_pc) + ",需要吃汉堡")
        return True
    else:
        print("当前体力为：" + str(current_pc) + ",不需要吃汉堡")
        return False


def bat_main():
    # 一些测试时预定义的数值
    target_xg_id = 5
    target_round = 0
    start_pc = 120
    start_hb = 10
    start_time = time.time()
    shutdown = 0
    exit_pos_2_no_ball = 1
    exit_pos_3_no_ball = 0
    success_round = 0
    eat_bg = 0

    config = configparser.ConfigParser()
    config.read("config.ini")
    threshold1 = float(config.get("threshold", "threshold1"))
    threshold2 = float(config.get("threshold", "threshold2"))
    threshold3 = float(config.get("threshold", "threshold3"))
    threshold4 = float(config.get("threshold", "threshold4"))

    # 测试代码
    # grab_pos(652, 359, 755, 389)
    # grab_pos(445, 236, 573, 270)
    # image_binarization("grab.jpg", 200)
    # grab_pos(408, 356, 427, 375)
    # grab_pos(673, 356, 692, 375)
    # image_binarization("grab.jpg", 200)
    # img1 = cv2.imread("grey.jpg")
    # img2 = cv2.imread("grey1.jpg")
    # print(classify_hist_with_split(img1, img2))
    # CompareImage.compare_image("grey.jpg", "grey1.jpg")
    # CompareImage.compare_image("grey.jpg", "grey2.jpg")
    # img1 = cv2.imread("binarization.jpg")
    # img2 = cv2.imread("binarization1.jpg")
    # print(classify_hist_with_split(img1, img2))
    # CompareImage.compare_image("binarization.jpg", "binarization1.jpg")

    # handle_lan = win32gui.FindWindow("UnityWndClass", "梦幻模拟战")
    # if handle_lan == 0:
    #     print("无法查找到梦幻模拟战窗口，脚本即将退出")
    #     bat_exit(0)
    # else:
    #     print("查找到梦幻模拟战窗口:" + str(handle_lan))
    #     win32api.Sleep(1000)
    #
    # print("将窗口移动到0,0,1024,768")
    # win32gui.PostMessage(handle_lan, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # win32api.Sleep(1000)
    # win32gui.SetWindowPos(handle_lan, win32con.HWND_TOPMOST, 0, 0, 1024, 768, win32con.SWP_SHOWWINDOW)
    # win32gui.SetWindowPos(handle_lan, win32con.HWND_NOTOPMOST, 0, 0, 1024, 768, win32con.SWP_SHOWWINDOW)
    # win32api.Sleep(1000)

    # bat_exit(0)

    # 移动脚本窗口
    handle_bat = win32gui.FindWindow("ConsoleWindowClass", None)
    if handle_bat != 0:
        # print("移动脚本窗口")
        win32gui.SetWindowPos(handle_bat, win32con.HWND_TOPMOST, 1024, 0, 600, 768, win32con.SWP_NOZORDER)

    # 脚本开始
    print("简单兄贵挂机脚本（v1.2）即将开始，请确保：\n\
    1.梦幻模拟战程序存在，目前只支持官网的pc端\n\
    2.当前游戏页面为大地图主页面，别的乱七八糟的都不要有\n\
    3.脚本开始运行后梦战模拟战窗口不要被遮挡，也不要在梦幻模拟战窗口区域移动或点击鼠标干扰脚本执行\n\
    4.唯一需要人工干预的地方是第一次刷的时候进入战斗地图时的准备画面，给了10秒时间调换人物，\
10秒并不算长，所以要上场的人物的技能和兵种最好是在外面就调好\n\
    5.脚本源码在脚本目录的bat_core.py中，可以自行修改\n\
    6.脚本的主要流程是在模拟鼠标点击，有几个关键的点是如何判断三号位存在、战斗结束以及二三号位是否有球，目前采用的方法是比对关键区域的图像，\
图像模板在脚本目录下的grey1.jpg、grey2.jpg、grey3.jpg、grey4.jpg中，判断比对结果的阈值在脚本目录的config.ini中，分别对应了三号位比对、战斗结束比对、二号位有球比对、三号位有球比对。\
脚本启动后，留意脚本输出的结果，如果发现三号位存在但图像对比结果仍然不通过的话，可以调低config.ini中的阈值使其略低于图像比对结果即可，\
同理其他图像比对也是如此。注意不要调的太低，否则容易被干扰\n\
    7.上面一条看不明白的话可以先不管，脚本跑起来以后注意下脚本输出信息就知道是什么意思了\n\
    8.脚本随时可以关闭，感觉不对劲了关闭脚本即可")
    input("输入回车表示确认以上事项")

    inp = input("请输入想要刷的兄贵ID，1-步/2-弓/3-枪/4-飞/5-骑/6-僧，以回车确定：")
    target_xg_id = int(inp)
    if target_xg_id != 1 and target_xg_id != 2 and target_xg_id != 3 \
            and target_xg_id != 4 and target_xg_id != 5 and target_xg_id != 6:
        print("输入错误，只能是1-6之间的数字")
        bat_exit(0)

    inp = input("请输入想要刷的次数，输入0表示一直刷到没有体力，以回车确定：")
    target_round = int(inp)
    if target_round < 0:
        print("输入错误，只能是0及以上的数字")
        bat_exit(0)

    inp = input("请输入当前体力，以回车确定：")
    start_pc = int(inp)
    if start_pc < 0:
        print("输入错误，只能是0及以上的数字")
        bat_exit(0)

    inp = input("请输入当前汉堡数量，以回车确定：")
    start_hb = int(inp)
    if start_hb < 0:
        print("输入错误，只能是0及以上的数字")
        bat_exit(0)

    inp = input("3号位无球时重新组队，0-否/1-是，以回车确定：")
    exit_pos_3_no_ball = int(inp)
    if exit_pos_3_no_ball != 0 and exit_pos_3_no_ball != 1:
        print("输入错误，只能是0或1")
        bat_exit(0)

    inp = input("脚本执行完后是否关机，0-否/1-是，以回车确定：")
    shutdown = int(inp)
    if shutdown != 0 and shutdown != 1:
        print("关机控制输入错误，只能是0或1")
        bat_exit(0)

    print("\n想要刷的兄贵是：" + translate_xionggui(target_xg_id))
    print("想要刷的次数是：" + str(target_round))
    print("当前体力为：" + str(start_pc))
    print("当前汉堡为：" + str(start_hb))
    print("三号位无球时是否重新组队：" + translate_yes_or_no(exit_pos_3_no_ball))
    print("脚本结束后是否关机：" + translate_yes_or_no(shutdown))
    print("config.ini中配置的三号位存在的比较阈值为：" + str(threshold1))
    print("config.ini中配置的战斗结束的比较阈值为：" + str(threshold2))
    print("config.ini中配置的二号位有球的比较阈值为：" + str(threshold3))
    print("config.ini中配置的三号位有球的比较阈值为：" + str(threshold4))
    input("输入回车表示确认")

    start_time = time.time()

    print("\n脚本正式开始")
    win32api.Sleep(1000)
    print("\n查找梦幻模拟战窗口")
    handle_lan = win32gui.FindWindow("UnityWndClass", "梦幻模拟战")
    if handle_lan == 0:
        print("无法查找到梦幻模拟战窗口，脚本即将退出")
        bat_exit(0)
    else:
        print("查找到梦幻模拟战窗口:" + str(handle_lan))
        win32api.Sleep(1000)

    print("将窗口移动到0,0,1024,768")
    win32gui.PostMessage(handle_lan, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetWindowPos(handle_lan, win32con.HWND_TOPMOST, 0, 0, 1024, 768, win32con.SWP_SHOWWINDOW)
    win32gui.SetWindowPos(handle_lan, win32con.HWND_NOTOPMOST, 0, 0, 1024, 768, win32con.SWP_SHOWWINDOW)
    win32api.Sleep(2000)

    print("点击秘境")
    single_click(977, 303)
    win32api.Sleep(2000)

    print("点击日常活动")
    single_click(973, 290)
    win32api.Sleep(1000)

    print("点击兄贵健身房")
    single_click(530, 160)
    win32api.Sleep(2000)

    last_round_ret = 0
    while True:
        if last_round_ret != 1:
            print("检查当前体力是否足够（检查体力会有些许误差）")
            time_div = time.time() - start_time
            pc_grow = time_div / 300
            current_pc = int(start_pc + pc_grow + eat_bg * 50 - success_round * 16)
            if current_pc < 16:
                print("当前体力为：" + str(current_pc) + ",需要吃汉堡")
                win32api.Sleep(1000)
                if eat_bg >= start_hb:
                    print("当前汉堡不足")
                    bat_exit(shutdown)
                print("点击体力+号")
                single_click(764, 50)
                win32api.Sleep(1000)
                print("点击汉堡")
                single_click(420, 469)
                win32api.Sleep(2000)
                print("点击空白消除汉堡对话框")
                single_click(267, 118)
                win32api.Sleep(1000)
                eat_bg = eat_bg + 1
            else:
                print("当前体力为：" + str(current_pc) + ",足够继续")
                win32api.Sleep(1000)

        # 取消邀请会在健身房页面
        # 继续邀请会在组队页面，但是继续邀请页面返回的话直接返回到大地图
        need_exit_room = False
        while True:
            if last_round_ret != 1 and not need_exit_room:
                print("点击对应兄贵")
                if target_xg_id == 1:
                    single_click(219, 228)
                elif target_xg_id == 2:
                    single_click(97, 306)  # 这个位置是容易被邀请遮挡的位置，故定位靠左一点
                elif target_xg_id == 3:
                    single_click(219, 389)
                elif target_xg_id == 4:
                    single_click(219, 465)
                elif target_xg_id == 5:
                    single_click(219, 552)
                elif target_xg_id == 6:
                    single_click(219, 630)
                win32api.Sleep(1000)

                print("点击组队")
                single_click(958, 700)
                win32api.Sleep(3000)

                print("向上拖拽列表")
                drag_to_top(375, 500, 250)
                win32api.Sleep(1000)

                print("选中LV.70")
                single_click(371, 638)
                win32api.Sleep(2000)

            if last_round_ret != 1 or need_exit_room:
                print("点击创建队伍")
                single_click(870, 700)
                win32api.Sleep(2000)

                print("点击创建")
                single_click(652, 585)
                win32api.Sleep(2000)

            print("循环检测三号位是否存在")
            check_pso_3_start_time = time.time()
            # index = 0
            while True:
                time_div_check_3 = time.time() - check_pso_3_start_time
                if time_div_check_3 > 40:
                    print("三号位检测超过40秒，这个房间已经没什么吸引力了，退出检测循环")
                    need_exit_room = True
                    break
                print("点击三号位位置")
                single_click(779, 282)
                win32api.Sleep(1500)
                print("截屏当前位置")
                grab_pos(652, 359, 755, 389)
                image_binarization("grab.jpg", 200)
                print("比对预留图像")
                com_ret = CompareImage.compare_image("grey.jpg", "grey1.jpg")
                # com_ret = CompareImage.compare_image("grab.jpg", "1.jpg")
                # com_ret = classify_hist_with_split("grab.jpg", "1.jpg")
                # os.rename("grab.jpg", "grab" + str(index) + ".jpg")
                # index = index + 1
                if com_ret > threshold1:
                    print("比对成功，三号位存在")
                    print("点击空白处消除三号位资料框")
                    single_click(787, 171)
                    win32api.Sleep(1000)

                    if exit_pos_2_no_ball != 0:
                        print("判断二号位是否有球")
                        grab_pos(408, 356, 427, 375)
                        image_binarization("grab.jpg", 200)
                        print("比对预留图像")
                        com_ret = CompareImage.compare_image("grey.jpg", "grey3.jpg")
                        if com_ret > threshold3:
                            print("比对成功，二号位有球")
                        else:
                            print("比对不成功，二号位无球，需要重新组队")
                            need_exit_room = True
                            break

                    if exit_pos_3_no_ball != 0:
                        print("判断三号位是否有球")
                        grab_pos(673, 356, 692, 375)
                        image_binarization("grab.jpg", 200)
                        print("比对预留图像")
                        com_ret = CompareImage.compare_image("grey.jpg", "grey3.jpg")
                        if com_ret > threshold4:
                            print("比对成功，三号位有球")
                        else:
                            print("比对不成功，三号位无球，需要重新组队")
                            need_exit_room = True
                            break

                    need_exit_room = False
                    print("点击开始战斗")
                    single_click(835, 586)
                    win32api.Sleep(5000)
                    break
                else:
                    print("比对不成功，三号位不存在")
                    print("点击空白处消除一下干扰")
                    single_click(787, 171)
                    print("1秒后继续尝试比对")
                    win32api.Sleep(1000)

            if need_exit_room:
                win32api.Sleep(2000)
                print("点击空白")
                single_click(60, 415)
                win32api.Sleep(1000)
                print("点击离开队伍")
                single_click(173, 582)
                win32api.Sleep(2000)
                # if last_round_ret == 0:
                #     print("点击返回")
                #     single_click(86, 60)
                #     win32api.Sleep(2000)
                # else:
                #     last_round_ret = 0
            else:
                break

        print("战斗开始")
        if success_round == 0:
            print("第一次刷，给10秒时间调换人物，不需要调换或者已经调换好了可以手动点击“出击”早点开始")
            win32api.Sleep(10000)

        print("点击出击")
        single_click(957, 700)
        battle_start_time = time.time()
        while True:
            win32api.Sleep(3000)
            battle_last_time = time.time() - battle_start_time
            if success_round == 0:
                if battle_last_time < 60:
                    print("第一次刷，在60秒内循环点击自动")
                    single_click(977, 232)

            if battle_last_time > 180:
                print("战斗已超过三分钟，截屏战斗结算区域")
                grab_pos(445, 236, 573, 270)
                image_binarization("grab.jpg", 200)
                print("比对预留图像")
                # com_ret = CompareImage.compare_image("grab.jpg", "2.jpg")
                com_ret = CompareImage.compare_image("grey.jpg", "grey2.jpg")
                if com_ret > threshold2:
                    print("比对成功，战斗已结束")
                    win32api.Sleep(5000)
                    print("点击空白处消除战斗结算框")
                    single_click(542, 110)
                    win32api.Sleep(3000)
                    print("点击空白处打开宝箱")
                    single_click(542, 110)
                    win32api.Sleep(6000)
                    print("点击空白处继续")
                    single_click(542, 110)
                    win32api.Sleep(3000)
                    success_round = success_round + 1

                    print("检查体力是否能继续")
                    if need_eat_bg(start_pc, (time.time() - start_time) / 300, eat_bg, success_round):
                        last_round_ret = -1
                        print("点击取消邀请")
                        single_click(432, 470)
                        win32api.Sleep(5000)
                    else:
                        last_round_ret = 1
                        print("点击继续邀请")
                        single_click(595, 470)
                        win32api.Sleep(5000)
                    break

            if battle_last_time > 1200:
                print("战斗已超过20分钟还没检测到结束，应该是输了")
                print("点击空白")
                single_click(542, 110)
                win32api.Sleep(3000)
                success_round = success_round + 1
                last_round_ret = -1
                print("点击取消邀请")
                single_click(432, 470)
                win32api.Sleep(5000)
                break

        print("战斗结束，总战斗次数为：" + str(success_round))
        if target_round != 0 and success_round >= target_round:
            print("战斗次数已达目标值，脚本即将退出")
            bat_exit(shutdown)
        else:
            print("开始下一轮战斗")
