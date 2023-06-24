

def is_bbox_contained(bbox1, bbox2):
    x1, y1, x2, y2 = bbox1
    x3, y3, x4, y4 = bbox2

    if x3 <= x1 <= x2 <= x4 and y3 <= y1 <= y2 <= y4:
        return True
    else:
        return False
