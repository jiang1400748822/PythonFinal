#判断手指是否弯曲q
def vertify_thumb(finger):
    if 0.0<finger<32.0:
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
    if vertify_thumb(thumb) and vertify_index(index)==False and vertify_middle(middle) and vertify_ring(ring) and vertify_pinky(pinky):
        return "1"
    if vertify_thumb(thumb) and vertify_index(index)==False and vertify_middle(middle)==False and vertify_ring(ring) and vertify_pinky(pinky):
        return "2"
    if vertify_thumb(thumb) and vertify_index(index)==False and vertify_middle(middle)==False and vertify_ring(ring)==False and vertify_pinky(pinky):
        return "3"
    if vertify_thumb(thumb) and vertify_index(index)==False and vertify_middle(middle)==False and vertify_ring(ring)==False and vertify_pinky(pinky)==False:
        return "4"
    if vertify_thumb(thumb)==False and vertify_index(index)==False and vertify_middle(middle)==False and vertify_ring(ring)==False and vertify_pinky(pinky)==False:
        return "5"
    if vertify_thumb(thumb)==False and vertify_index(index) and vertify_middle(middle) and vertify_ring(ring) and vertify_pinky(pinky)==False:
        return "6"
    if vertify_thumb(thumb)==False and vertify_index(index) and vertify_middle(middle) and vertify_ring(ring) and vertify_pinky(pinky):
        if 72.0<index<120.0:
            return "7"
        if index>125.0:
            return "9"

    if vertify_thumb(thumb)==False and vertify_index(index)==False and vertify_middle(middle) and vertify_ring(ring) and vertify_pinky(pinky):
        return "8"
    return ""