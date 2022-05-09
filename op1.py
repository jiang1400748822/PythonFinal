# 导入OpenCV
from pickle import TRUE
import cv2
# 导入mediapipe
import mediapipe as mp
# 导入电脑音量控制模块
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# 导入其他依赖包
import time
import math
import numpy as np

class HandControlVolume:
    def __init__(self):
        # 初始化medialpipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        # 获取电脑音量范围
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume_range = self.volume.GetVolumeRange()

        #初始化手势
        self.hand_result = ''
        
        #手势测试值
        self.sum_thumb=[]
        self.sum_index=[]
        self.sum_middle=[]
        self.sum_ring=[]
        self.sum_pinky=[]

        #手势模式
        self.model = 0

    #角度计算函数
    def angle_calc(a1,a2):
        a1_x=a1[0]
        a1_y=a1[1]

        a2_x=a2[0]
        a2_y=a2[1]

        try:
            angle= math.degrees(math.acos((a1_x*a2_x+a1_y*a2_y)/(((a1_x**2+a1_y**2)**0.5)*((a2_x**2+a2_y**2)**0.5))))
        except:
            angle =500.
        if angle > 180.:
            angle = 500.
        return angle

    #各个手指角度计算函数
    def hand_angle(hands):
        angle_list = {}
        #------ thumb 大拇指角度
        angle_thumb = HandControlVolume.angle_calc(
                                ( (int(hands[1][1])- int(hands[2][1]))  ,  (int(hands[1][2])- int(hands[2][2]))  ),
                                ( (int(hands[3][1])- int(hands[4][1]))  ,  (int(hands[3][2])- int(hands[4][2]))  )
                            )
        angle_list['thumb'] = angle_thumb

        #------ index  食指角度
        angle_index = HandControlVolume.angle_calc(
            ( (int(hands[5][1])- int(hands[6][1]))  ,  (int(hands[5][2])- int(hands[6][2]))  ),
            ( (int(hands[7][1])- int(hands[8][1]))  ,  (int(hands[7][2])- int(hands[8][2]))  )
        )
        angle_list['index'] = angle_index

        #------ middle  中指角度
        angle_middle = HandControlVolume.angle_calc(
            ( (int(hands[9][1])- int(hands[10][1]))  ,  (int(hands[9][2])- int(hands[10][2]))  ),
            ( (int(hands[11][1])- int(hands[12][1]))  ,  (int(hands[11][2])- int(hands[12][2]))  )
        )
        angle_list['middle'] = angle_middle

        #------ ring  无名指角度
        angle_ring = HandControlVolume.angle_calc(
            ( (int(hands[13][1])- int(hands[14][1]))  ,  (int(hands[13][2])- int(hands[14][2]))  ),
            ( (int(hands[15][1])- int(hands[16][1]))  ,  (int(hands[15][2])- int(hands[16][2]))  )
        )
        angle_list['ring'] = angle_ring

        #------ pinky  无名指角度
        angle_pinky = HandControlVolume.angle_calc(
            ( (int(hands[17][1])- int(hands[18][1]))  ,  (int(hands[17][2])- int(hands[18][2]))  ),
            ( (int(hands[19][1])- int(hands[20][1]))  ,  (int(hands[19][2])- int(hands[20][2]))  )
        )
        angle_list['pinky'] = angle_pinky

        return angle_list

    #判断手指是否弯曲q
    def vertify_thumb(finger):
        # if mi<finger<ma:
        #     return True
        # else:
        #     return False
        if 0.0<finger<28.0:
            return False
        else:
            return True
    def vertify_index(finger):
        if 0.0<finger<10.0:
            return False
        else:
            return True
    
    def vertify_middle(finger):
        if 0.0<finger<10.0:
            return False
        else:
            return True
    
    def vertify_ring(finger):
        if 0.0<finger<10.0:
            return False
        else:
            return True

    def vertify_pinky(finger):
        if 0.2<finger<10.1:
            return False
        else:
            return True
            
    def hand_vertify(thumb,index,middle,ring,pinky):
        if HandControlVolume.vertify_thumb(thumb) and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle) and HandControlVolume.vertify_ring(ring) and HandControlVolume.vertify_pinky(pinky):
            return "1"
        if HandControlVolume.vertify_thumb(thumb) and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle)==False and HandControlVolume.vertify_ring(ring) and HandControlVolume.vertify_pinky(pinky):
            return "2"
        if HandControlVolume.vertify_thumb(thumb) and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle)==False and HandControlVolume.vertify_ring(ring)==False and HandControlVolume.vertify_pinky(pinky):
            return "3"
        if HandControlVolume.vertify_thumb(thumb) and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle)==False and HandControlVolume.vertify_ring(ring)==False and HandControlVolume.vertify_pinky(pinky)==False:
            return "4"
        if HandControlVolume.vertify_thumb(thumb)==False and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle)==False and HandControlVolume.vertify_ring(ring)==False and HandControlVolume.vertify_pinky(pinky)==False:
            return "5"
        if HandControlVolume.vertify_thumb(thumb)==False and HandControlVolume.vertify_index(index) and HandControlVolume.vertify_middle(middle) and HandControlVolume.vertify_ring(ring) and HandControlVolume.vertify_pinky(pinky)==False:
            return "6"
        if HandControlVolume.vertify_thumb(thumb)==False and HandControlVolume.vertify_index(index) and HandControlVolume.vertify_middle(middle) and HandControlVolume.vertify_ring(ring) and HandControlVolume.vertify_pinky(pinky):
            if 72.0<index<120.0:
                return "7"
            if index>125.0:
                return "9"

        if HandControlVolume.vertify_thumb(thumb)==False and HandControlVolume.vertify_index(index)==False and HandControlVolume.vertify_middle(middle) and HandControlVolume.vertify_ring(ring) and HandControlVolume.vertify_pinky(pinky):
            return "8"
        return ""

    # 主函数
    def recognize(self):
        # OpenCV读取视频流
        cap = cv2.VideoCapture(0)
        # 视频分辨率
        resize_w = 640
        resize_h = 480

        # 画面显示初始化参数
        rect_height = 0
        rect_percent_text = 0

        with self.mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.5,max_num_hands=1) as hands:
            while cap.isOpened():
                success, image = cap.read()
                image = cv2.resize(image, (resize_w, resize_h))

                if not success:
                    print("空帧.")
                    continue
                #print(image)
                #手势识别模式切换
                if cv2.waitKey(2) & 0xFF == 109:
                    if self.model == 1:
                        self.model = 0
                    else:
                        self.model = 1
                # 令数组只读
                image.flags.writeable = False
                # 转为RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # 镜像
                image = cv2.flip(image, 1)#1水平翻转  0垂直翻转  -1水平垂直翻转
                # mediapipe模型处理
                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # 判断是否有手掌
                if results.multi_hand_landmarks:
                    # 遍历每个手掌
                    for hand_landmarks in results.multi_hand_landmarks:
                        # 在画面标注手指
                        self.mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())

                        # 解析手指，存入各个手指坐标
                        landmark_list = []
                        landmark_list_pm=[]
                        for landmark_id, finger_axis in enumerate(hand_landmarks.landmark):
                            landmark_list.append(
                                [landmark_id, finger_axis.x, finger_axis.y,finger_axis.z]
                                )

                            landmark_list_pm.append(
                                [landmark_id, math.ceil(finger_axis.x* resize_w), math.ceil(finger_axis.y* resize_h)]
                                )
                        
                        #手指角度
                        self.hand_result = ''
                        hand_angle_dict = HandControlVolume.hand_angle(landmark_list_pm)
 
                        #手势值分析 
                        self.sum_thumb.append(hand_angle_dict['thumb'])
                        self.sum_index.append(hand_angle_dict['index'])
                        self.sum_middle.append(hand_angle_dict['middle'])
                        self.sum_ring.append(hand_angle_dict['ring'])
                        self.sum_pinky.append(hand_angle_dict['pinky'])


                        if self.model==1:
                            self.hand_result=HandControlVolume.hand_vertify(hand_angle_dict['thumb'],hand_angle_dict['index'],hand_angle_dict['middle'],hand_angle_dict['ring'],hand_angle_dict['pinky'])
                            if self.hand_result=="1":
                                self.volume.SetMasterVolumeLevel(-58.725, None)
                                rect_percent_text = 10

                            if self.hand_result=="2":
                                self.volume.SetMasterVolumeLevel(-52.2, None)
                                rect_percent_text = 20

                            if self.hand_result=="3":
                                self.volume.SetMasterVolumeLevel(-45.675, None)
                                rect_percent_text = 30

                            if self.hand_result=="4":
                                self.volume.SetMasterVolumeLevel(-39.15, None)
                                rect_percent_text = 40

                            if self.hand_result=="5":
                                self.volume.SetMasterVolumeLevel(-32.625, None)
                                rect_percent_text = 50

                            if self.hand_result=="6":
                                self.volume.SetMasterVolumeLevel(-26.1, None)
                                rect_percent_text = 60
                                
                            if self.hand_result=="7":
                                self.volume.SetMasterVolumeLevel(-19.575, None)
                                rect_percent_text = 70

                            if self.hand_result=="8":
                                self.volume.SetMasterVolumeLevel(-13.05, None)
                                rect_percent_text = 80

                            if self.hand_result=="9":
                                self.volume.SetMasterVolumeLevel(-6.525, None)
                                rect_percent_text = 90
                            rect_height = 2*rect_percent_text

                        print(hand_angle_dict)

                        if landmark_list:
                            # 获取大拇指指尖坐标
                            thumb_finger_tip = landmark_list[4]
                            thumb_finger_tip_x = math.ceil(thumb_finger_tip[1] * resize_w)
                            thumb_finger_tip_y = math.ceil(thumb_finger_tip[2] * resize_h)
                            # 获取食指指尖坐标
                            index_finger_tip = landmark_list[8]
                            index_finger_tip_x = math.ceil(index_finger_tip[1] * resize_w)
                            index_finger_tip_y = math.ceil(index_finger_tip[2] * resize_h)
                            # 中间点
                            finger_middle_point = (thumb_finger_tip_x+index_finger_tip_x)//2, (thumb_finger_tip_y+index_finger_tip_y)//2
                            # print(thumb_finger_tip_x)
                            thumb_finger_point = (thumb_finger_tip_x,thumb_finger_tip_y)
                            index_finger_point = (index_finger_tip_x,index_finger_tip_y) 
                            if self.model==0:
                            # 画指尖2点
                                image = cv2.circle(image,thumb_finger_point,10,(255,0,255),-1)
                                image = cv2.circle(image,index_finger_point,10,(255,0,255),-1)
                                image = cv2.circle(image,finger_middle_point,10,(255,0,255),-1)
                                # 画2点连线
                                image = cv2.line(image,thumb_finger_point,index_finger_point,(255,0,255),5)
                                #勾股定理计算长度
                                line_len = math.hypot((index_finger_tip_x-thumb_finger_tip_x),(index_finger_tip_y-thumb_finger_tip_y))
                                # 获取电脑最大最小音量
                                min_volume = self.volume_range[0]
                                max_volume = self.volume_range[1]
                                #print(f"最小音量：{self.volume_range[0]}  最大音量：{self.volume_range[1]}")
                                # 将指尖长度映射到音量上
                                vol = np.interp(line_len,[50,300],[min_volume,max_volume])
                                # 将指尖长度映射到矩形显示上
                                rect_height = np.interp(line_len,[50,300],[0,200])
                                rect_percent_text = np.interp(line_len,[50,300],[0,100])

                                # 设置电脑音量
                                self.volume.SetMasterVolumeLevel(vol, None)

                # 显示矩形
                cv2.putText(image, str(math.ceil(rect_percent_text))+"%", (20, 350),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                image = cv2.rectangle(image,(30,100),(60,300),(255, 0, 0),3)
                image = cv2.rectangle(image,(30,math.ceil(300-rect_height)),(60,300),(255, 0, 0),-1)

                cv2.putText(image, "hand_result:  "+self.hand_result, (10, 70),cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255),3)
                # 显示画面
                cv2.imshow('volume controll', image)
                if cv2.waitKey(3) & 0xFF == 113:
                    print(f'大拇指平均值：{np.average(self.sum_thumb)}  最小值：{min(self.sum_thumb)}  最大值：{max(self.sum_thumb)}')  
                    print(f'食指平均值：{np.average(self.sum_index)}最小值：{min(self.sum_index)}  最大值：{max(self.sum_index)}  ')  
                    print(f'中指平均值：{np.average(self.sum_middle)}最小值：{min(self.sum_middle)}  最大值：{max(self.sum_middle)}  ')  
                    print(f'无名指平均值：{np.average(self.sum_ring)}最小值：{min(self.sum_ring)}  最大值：{max(self.sum_ring)}  ')
                    print(f'小拇指平均值：{np.average(self.sum_pinky)}最小值：{min(self.sum_pinky)}  最大值：{max(self.sum_pinky)}  ')
                    break
            cap.release()

# 开始程序
control = HandControlVolume()
control.recognize()
