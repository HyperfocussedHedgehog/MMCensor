import math

def intersection_box( xyxy_1, xyxy_2 ):
    xyxy = [
            max( xyxy_1[0], xyxy_2[0] ),
            max( xyxy_1[1], xyxy_2[1] ),
            min( xyxy_1[2], xyxy_2[2] ),
            min( xyxy_1[3], xyxy_2[3] ),
            ]

    if xyxy[0]+10<xyxy[2] and xyxy[1]+10<xyxy[3]:
        return xyxy
    else:
        return None

def union_box( xyxy_1, xyxy_2 ):
    xyxy = [
            min( xyxy_1[0], xyxy_2[0] ),
            min( xyxy_1[1], xyxy_2[1] ),
            max( xyxy_1[2], xyxy_2[2] ),
            max( xyxy_1[3], xyxy_2[3] ),
            ]

    return xyxy

def condense_boxes_single( in_boxes ):
    boxes = in_boxes.copy()
    # takes a numpy of Boxes and unions boxes of the same
    # class that intersect
    # sets t for the unioned boxes to the latest t that
    # contributes to the union
    # does a 'single pass', it doesn't re-check non-intersecting
    # boxes to see if they become intersecting later after one
    # of them grows.  You could do this, I just haven't found it
    # necessary.
    # since we do the intersection by class, we return a 
    # dictionary, indexed by class, where the values are a list
    # of intersected boxes
    by_class = {}
    for box in boxes:
        if box[1] not in by_class:
            by_class[box[1]] = [ box ]
        else:
            intersected = False
            for i in range(len(by_class[box[1]])):
                if intersection_box( by_class[box[1]][i][2:6], box[2:6] ) is not None:
                    by_class[box[1]][i][2:6] = union_box( by_class[box[1]][i][2:6], box[2:6] )
                    by_class[box[1]][i][0] = max( by_class[box[1]][i][0], box[0] )
                    intersected = True
                    break
            if not intersected:
                by_class[box[1]].append( box )

    return( by_class )

def condense_all( in_boxes ):
    boxes = in_boxes.copy()
    bigbox = None
    if len(boxes) != 0:
        bigbox = boxes[0]
        for box in boxes:
            bigbox[2:6] = union_box(bigbox[2:6], box[2:6])
            bigbox[0] = max( bigbox[0], box[0])
    return bigbox

def expand_boxes( in_boxes, percentage):
    for box in in_boxes:
        w = box[4] - box[2]
        h = box[5] - box[3]
        w_diff = math.floor(percentage*w/200)
        h_diff = math.floor(percentage*h/200)
        box[2] = box[2] - w_diff
        box[3] = box[3] - h_diff
        box[4] = box[4] + w_diff
        box[5] = box[5] + h_diff
    return in_boxes

# Bounds the size of the boxes to be within the frame
def expand_boxes_bounded( in_boxes, percentage, frame):
    for box in in_boxes:
        w = box[4] - box[2]
        h = box[5] - box[3]
        w_diff = math.floor(percentage*w/200)
        h_diff = math.floor(percentage*h/200)
        frame_h, frame_w, _ = frame.shape
        box[2] = max(0, box[2] - w_diff)
        box[3] = max(0, box[3] - h_diff)
        box[4] = min(frame_w, box[4] + w_diff)
        box[5] = min(frame_h, box[5] + h_diff)
    return in_boxes