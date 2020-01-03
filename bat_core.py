# encoding:gbk
from PIL import Image
from PIL import ImageGrab
import win32api
import win32gui
import win32con
import time
# import pytesseract
# import os
# import cv2
# import sys


# ����
def single_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0)
    return


# ������ק
def drag_to_bottom(x, y, distance):
    return


# ������ק
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


# �ű��˳�
def bat_exit():
    input("�ű�ִ����ϣ�����س��Խ���\n")
    exit(0)
    return


# ץȡָ��λ��ͼ��
def grab_pos(left, top, right, bottom):
    size = (left, top, right, bottom)
    img = ImageGrab.grab(size)
    img.save("grab.jpg")
    return


# ͼ��Ƚ���
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
        'file_image1'��'file_image2'�Ǵ�����ļ�·��
         ����ͨ��'Image.open(path)'����'image1' �� 'image2' Image ����.
         'size' ���½� image ����ĳߴ�������ã�Ĭ�ϴ�СΪ256 * 256 .
         'part_size' �����˷ָ�ͼƬ�Ĵ�С.Ĭ�ϴ�СΪ64*64 .
         ����ֵ�� 'image1' �� 'image2'�ԱȺ�����ƶȣ����ƶ�Խ�ߣ�ͼƬԽ�ӽ����ﵽ1.0˵��ͼƬ��ȫ��ͬ��
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
        print('ͼ��ԱȽ��: ' + str(pre))
        return pre


# # ��ȡͼ������
# def get_text_from_img():
#     # ��ʼ��tesseract
#     pytesseract.pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract'
#     img_text = pytesseract.image_to_string(Image.open("grab.png"), lang="chi_sim")
#     img_text = img_text.replace(" ", "")
#     return img_text


# def calculate(image1, image2):
#     # �Ҷ�ֱ��ͼ�㷨
#     # ���㵥ͨ����ֱ��ͼ������ֵ
#     hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
#     hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
#     # ����ֱ��ͼ���غ϶�
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
#     # RGBÿ��ͨ����ֱ��ͼ���ƶ�
#     # ��ͼ��resize�󣬷���ΪRGB����ͨ�����ټ���ÿ��ͨ��������ֵ
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
    # ͼ���ֵ��
    img = Image.open(img_path)
    img = img.convert('L')
    img.save("grey.jpg")

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # ͼƬ��ֵ��
    img = img.point(table, '1')
    img.save("binarization.jpg")


def bat_main():
    # һЩ����ʱԤ�������ֵ
    target_xg_id = 5
    target_round = 0
    start_pc = 120
    start_hb = 10
    start_time = time.time()
    success_round = 0
    eat_bg = 0

    # ���Դ���
    # grab_pos(652, 359, 755, 389)
    # grab_pos(445, 236, 573, 270)
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
    # bat_exit()

    # �ű���ʼ
    input("�ֹ�һ��ű���v1.0��������ʼ����ȷ����\n\
    1.�ű��Թ���ԱȨ�����������룬�����޷������λ�ģ��ս����\n\
    2.�λ�ģ��ս��������Ҵ��ڿɼ����ڵ�����������С����Ҳ���ܱ��ڵ��ڱ�Ĵ���֮��\n\
    3.�ű�һ����ʼִ�к󣬲�Ҫ���λ�ģ��ս���������ƶ����������Žű�ִ�У������ʲôҲ����\n\
    4.Ҫ��ǰ��Ϸҳ��Ϊ���ͼ��ҳ�棬������߰���Ķ���Ҫ��\n\
    5.Ŀǰ�ű���֧�ֽ����Ժ������Ա�������б�֤�ϳ��������˲��ᷭ��\n\
    ����س���ʾȷ����������")

    inp = input("��������Ҫˢ���ֹ�ID��1-��/2-��/3-ǹ/4-��/5-��/6-ɮ���Իس�ȷ����")
    target_xg_id = int(inp)
    if target_xg_id != 1 and target_xg_id != 2 and target_xg_id != 3 \
            and target_xg_id != 4 and target_xg_id != 5 and target_xg_id != 6:
        print("������ֹ�ID�����ֹ�IDֻ����1-6֮�������")
        bat_exit()

    inp = input("��������Ҫˢ�Ĵ���������0��ʾһֱˢ��û���������Իس�ȷ����")
    target_round = int(inp)
    if target_round < 0:
        print("����Ĵ������󣬴���ֻ����0�����ϵ�����")
        bat_exit()

    inp = input("�����뵱ǰ�������Իس�ȷ����")
    start_pc = int(inp)
    if start_pc < 0:
        print("�����������������ֻ����0�����ϵ�����")
        bat_exit()

    inp = input("�����뵱ǰ�����������Իس�ȷ����")
    start_hb = int(inp)
    if start_hb < 0:
        print("����ĺ����������󣬺�������ֻ����0�����ϵ�����")
        bat_exit()

    print("��Ҫˢ���ֹ��ǣ�" + str(target_xg_id))
    print("��Ҫˢ�Ĵ����ǣ�" + str(target_round))
    print("��ǰ����Ϊ��" + str(start_pc))
    print("��ǰ����Ϊ��" + str(start_hb))
    input("����س���ʾȷ��")

    start_time = time.time()

    print("\n�ű���ʽ��ʼ")
    win32api.Sleep(1000)
    print("\n�����λ�ģ��ս����")
    handle_lan = win32gui.FindWindow("UnityWndClass", "�λ�ģ��ս")
    if handle_lan == 0:
        print("�޷����ҵ��λ�ģ��ս���ڣ��ű������˳�")
        bat_exit()
    else:
        print("���ҵ��λ�ģ��ս����:" + str(handle_lan))
        win32api.Sleep(1000)

    print("�������ƶ���0,0,1024,768")
    win32gui.SetWindowPos(handle_lan, win32con.HWND_TOPMOST, 0, 0, 1024, 768, win32con.SWP_NOZORDER)
    win32api.Sleep(1000)

    print("����ؾ�")
    single_click(977, 303)
    win32api.Sleep(2000)

    print("����ֹ���")
    single_click(530, 160)
    win32api.Sleep(2000)

    while True:
        print("��鵱ǰ�����Ƿ��㹻�������������Щ����")
        time_div = time.time() - start_time
        pc_grow = time_div / 300
        current_pc = int(start_pc + pc_grow + eat_bg * 50 - success_round * 16)
        if current_pc < 16:
            print("��ǰ����Ϊ��" + str(current_pc) + ",��Ҫ�Ժ���")
            win32api.Sleep(1000)
            if eat_bg >= start_hb:
                print("��ǰ��������")
                bat_exit()
            print("�������+��")
            single_click(764, 50)
            win32api.Sleep(1000)
            print("�������")
            single_click(420, 469)
            win32api.Sleep(2000)
            print("����հ����������Ի���")
            single_click(267, 118)
            win32api.Sleep(1000)
        else:
            print("��ǰ����Ϊ��" + str(current_pc) + ",�㹻����")
            win32api.Sleep(1000)

        while True:
            print("�����Ӧ�ֹ�")
            if target_xg_id == 1:
                single_click(219, 228)
            elif target_xg_id == 2:
                single_click(97, 306) # ���λ�������ױ������ڵ���λ�ã��ʶ�λ����һ��
            elif target_xg_id == 3:
                single_click(219, 389)
            elif target_xg_id == 4:
                single_click(219, 465)
            elif target_xg_id == 5:
                single_click(219, 552)
            elif target_xg_id == 6:
                single_click(219, 630)
            win32api.Sleep(1000)

            print("������")
            single_click(958, 700)
            win32api.Sleep(3000)

            print("������ק�б�")
            drag_to_top(375, 500, 250)
            win32api.Sleep(2000)

            print("ѡ��LV.70")
            single_click(371, 638)
            win32api.Sleep(2000)

            print("�����������")
            single_click(870, 700)
            win32api.Sleep(2000)

            print("�������")
            single_click(652, 585)
            win32api.Sleep(2000)

            print("ѭ���������λ�Ƿ����")
            check_pos_3_timeout = False
            check_pso_3_start_time = time.time()
            # index = 0
            while True:
                time_div_check_3 = time.time() - check_pso_3_start_time
                if time_div_check_3 > 120:
                    print("����λ��ⳬʱ���˳����ѭ��")
                    check_pos_3_timeout = True
                    break
                print("�������λλ��")
                single_click(779, 282)
                win32api.Sleep(1500)
                print("������ǰλ��")
                grab_pos(652, 359, 755, 389)
                image_binarization("grab.jpg", 200)
                print("�ȶ�Ԥ��ͼ��")
                com_ret = CompareImage.compare_image("grey.jpg", "grey1.jpg")
                # com_ret = CompareImage.compare_image("grab.jpg", "1.jpg")
                # com_ret = classify_hist_with_split("grab.jpg", "1.jpg")
                # os.rename("grab.jpg", "grab" + str(index) + ".jpg")
                # index = index + 1
                if com_ret > 0.9:
                    print("�ȶԳɹ�������λ����")
                    print("����հ״���������λ���Ͽ�")
                    single_click(787, 171)
                    win32api.Sleep(1000)
                    print("�����ʼս��")
                    single_click(835, 586)
                    win32api.Sleep(5000)
                    break
                else:
                    print("�ȶԲ��ɹ�������λ������")
                    print("1���������Աȶ�")
                    win32api.Sleep(1000)

            if check_pos_3_timeout:
                win32api.Sleep(5000)
                print("�������")
                single_click(83, 59)
                win32api.Sleep(1000)
            else:
                break

        print("ս����ʼ")
        print("�������")
        single_click(957, 700)
        battle_start_time = time.time()
        while True:
            win32api.Sleep(3000)
            battle_last_time = time.time() - battle_start_time
            if success_round == 0 and battle_last_time < 60:
                print("��һ��ˢ����60���ڶ�ʱ����Զ�")
                single_click(977, 232)
                win32api.Sleep(1000)

            if battle_last_time > 240:
                print("ս���ѳ����ķ��ӣ�����ս����������")
                grab_pos(445, 236, 573, 270)
                image_binarization("grab.jpg", 200)
                print("�ȶ�Ԥ��ͼ��")
                # com_ret = CompareImage.compare_image("grab.jpg", "2.jpg")
                com_ret = CompareImage.compare_image("grey.jpg", "grey2.jpg")
                if com_ret > 0.9:
                    print("�ȶԳɹ���ս���ѽ���")
                    win32api.Sleep(5000)
                    print("����հ״�����ս�������")
                    single_click(542, 110)
                    win32api.Sleep(3000)
                    print("����հ״��򿪱���")
                    single_click(542, 110)
                    win32api.Sleep(4000)
                    print("����հ״���ÿ�ս����������У�����û�У���Ӱ�죬���һ�οհ׶��ѣ�")
                    single_click(542, 110)
                    win32api.Sleep(4000)
                    print("����հ״�����")
                    single_click(542, 110)
                    win32api.Sleep(3000)
                    print("���ȡ������")
                    single_click(432, 470)
                    win32api.Sleep(5000)
                    success_round = success_round + 1
                    break

        print("ս����������ս������Ϊ��" + str(success_round))
        if target_round != 0 and success_round >= target_round:
            print("ս�������Ѵ�Ŀ��ֵ���ű������˳�")
            bat_exit()
        else:
            print("��ʼ��һ��ս��")

    bat_exit()
