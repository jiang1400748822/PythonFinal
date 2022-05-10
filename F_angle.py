import math
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
    angle_thumb = angle_calc(
                                ( (int(hands[1][1])- int(hands[2][1]))  ,  (int(hands[1][2])- int(hands[2][2]))  ),
                                ( (int(hands[3][1])- int(hands[4][1]))  ,  (int(hands[3][2])- int(hands[4][2]))  )
                            )
    angle_list['thumb'] = angle_thumb

        #------ index  食指角度
    angle_index = angle_calc(
            ( (int(hands[5][1])- int(hands[6][1]))  ,  (int(hands[5][2])- int(hands[6][2]))  ),
            ( (int(hands[7][1])- int(hands[8][1]))  ,  (int(hands[7][2])- int(hands[8][2]))  )
        )
    angle_list['index'] = angle_index

        #------ middle  中指角度
    angle_middle = angle_calc(
            ( (int(hands[9][1])- int(hands[10][1]))  ,  (int(hands[9][2])- int(hands[10][2]))  ),
            ( (int(hands[11][1])- int(hands[12][1]))  ,  (int(hands[11][2])- int(hands[12][2]))  )
        )
    angle_list['middle'] = angle_middle

        #------ ring  无名指角度
    angle_ring = angle_calc(
            ( (int(hands[13][1])- int(hands[14][1]))  ,  (int(hands[13][2])- int(hands[14][2]))  ),
            ( (int(hands[15][1])- int(hands[16][1]))  ,  (int(hands[15][2])- int(hands[16][2]))  )
        )
    angle_list['ring'] = angle_ring

        #------ pinky  无名指角度
    angle_pinky = angle_calc(
            ( (int(hands[17][1])- int(hands[18][1]))  ,  (int(hands[17][2])- int(hands[18][2]))  ),
            ( (int(hands[19][1])- int(hands[20][1]))  ,  (int(hands[19][2])- int(hands[20][2]))  )
        )
    angle_list['pinky'] = angle_pinky

    return angle_list