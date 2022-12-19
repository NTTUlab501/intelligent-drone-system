import numpy as np
import cv2
class BoundBox:
    def __init__(self, xmin, ymin, xmax, ymax, objness = None, classes = None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
        self.objness = objness
        self.classes = classes

        self.label = -1
        self.score = -1

    def get_label(self):
        if self.label == -1:
            self.label = np.argmax(self.classes)
        
        return self.label
    
    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.get_label()]
            
        return self.score



class drawYolo:
    def __init__(self,image_h,image_w):
        self.__image_h = image_h
        self.__image_w = image_w
        self.__input_h = 416
        self.__input_w = 416
        self.__obj_thresh = 0.5
        self.__nms_thresh = 0.45
        self.__anchors = [ [12, 16, 19, 36, 40, 28],[36, 75, 76, 55, 72, 146],[142, 110, 192, 243, 459, 401]]
        self.__labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", \
                      "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", \
                      "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", \
                      "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", \
                      "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", \
                      "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", \
                      "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", \
                      "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", \
                      "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", \
                      "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        
    
    def computeYoloNetWork(self,netout):
        boxes = list()
        for i in range(len(netout)):
            # decode the output of the network
            boxes += self.__decode_netout(netout[i][0], self.__anchors[i])
        boxes = self.__correct_yolo_boxes(boxes)
        boxes = self.__do_nms(boxes)
        v_boxes, v_labels, v_scores = self.__get_boxes(boxes)
        
        return  v_boxes, v_labels, v_scores

    def draw_boxes_opencv(self,image, v_boxes, v_labels, v_scores):
        # plot each box
        for i in range(len(v_boxes)):
            box = v_boxes[i]
            # get coordinates
            y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
            #print("({},{}),({},{})".format(x1,y1,x2,y2))
            if x1 < 0:
                x1 = 1
            if y1 < 0:
                y1 = 1
            if x2 > image.shape[1]:
                x2 = image.shape[1] -10
            if y2 > image.shape[0]:
                y2 = image.shape[0] -10
            try:
                if v_labels[i] == "person" or v_labels[i] == "car" :
                    cw = x2-x1
                    ch = y2-y1
                    #print(x1,y1, x2,y2)
                    ROI = image[y1:y2,x1:x2]
                    level = 30
                    #ROI = cv2.blur(ROI, (20, 20))
                    h = int(ch/level) 
                    w = int(cw/level) 
                    ROI = cv2.resize(ROI, (w,h), interpolation=cv2.INTER_LINEAR)
                    ROI = cv2.resize(ROI, (cw,ch), interpolation=cv2.INTER_NEAREST)
                    image[y1:y2,x1:x2] = ROI
                    #image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    #label = "%s (%.3f)" % (v_labels[i], v_scores[i])
                    #image = cv2.putText(image, label, (x1, y2), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)
                    
                    ##DEBUG
                    #print(x1,y1,x2,y2,label)
            except:
                pass
        return image
    
    def __sigmoid(self,x):
        return 1. / (1. + np.exp(-x))
    
    def __decode_netout(self,netout,anchors):
        grid_h, grid_w = netout.shape[:2]
        nb_box = 3
        netout = netout.reshape((grid_h, grid_w, nb_box, -1))
        nb_class = netout.shape[-1] - 5

        boxes = []

        netout[..., :2]  = self.__sigmoid(netout[..., :2])
        netout[..., 4:]  = self.__sigmoid(netout[..., 4:])
        netout[..., 5:]  = netout[..., 4][..., np.newaxis] * netout[..., 5:]
        netout[..., 5:] *= netout[..., 5:] > self.__obj_thresh

        for i in range(grid_h*grid_w):
            row = i / grid_w
            col = i % grid_w

            for b in range(nb_box):
                # 4th element is objectness score
                objectness = netout[int(row)][int(col)][b][4]
                #objectness = netout[..., :4]

                #if(objectness.all() <= self.__obj_thresh): continue
                if (objectness <= self.__obj_thresh).all(): continue
                # first 4 elements are x, y, w, and h
                x, y, w, h = netout[int(row)][int(col)][b][:4]

                x = (col + x) / grid_w # center position, unit: image width
                y = (row + y) / grid_h # center position, unit: image height
                w = anchors[2 * b + 0] * np.exp(w) / self.__input_w # unit: image width
                h = anchors[2 * b + 1] * np.exp(h) / self.__input_h # unit: image height  

                # last elements are class probabilities
                classes = netout[int(row)][col][b][5:]

                box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, objectness, classes)
                #box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, None, classes)

                boxes.append(box)

        return boxes

    def __correct_yolo_boxes(self,yolo_boxes):
        boxes = yolo_boxes
        image_h, image_w, net_h, net_w = self.__image_h,self.__image_w,self.__input_h,self.__input_w
        
        if (float(net_w)/image_w) < (float(net_h)/image_h):
            new_w = net_w
            new_h = (image_h*net_w)/image_w
        else:
            new_h = net_w
            new_w = (image_w*net_h)/image_h

        for i in range(len(boxes)):
            x_offset, x_scale = (net_w - new_w)/2./net_w, float(new_w)/net_w
            y_offset, y_scale = (net_h - new_h)/2./net_h, float(new_h)/net_h

            boxes[i].xmin = int((boxes[i].xmin - x_offset) / x_scale * image_w)
            boxes[i].xmax = int((boxes[i].xmax - x_offset) / x_scale * image_w)
            boxes[i].ymin = int((boxes[i].ymin - y_offset) / y_scale * image_h)
            boxes[i].ymax = int((boxes[i].ymax - y_offset) / y_scale * image_h)
        return boxes

    def __bbox_iou(self,box1, box2):
        def _interval_overlap(interval_a, interval_b):
            x1, x2 = interval_a
            x3, x4 = interval_b

            if x3 < x1:
                if x4 < x1:
                    return 0
                else:
                    return min(x2,x4) - x1
            else:
                if x2 < x3:
                     return 0
                else:
                    return min(x2,x4) - x3     

        intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
        intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])

        intersect = intersect_w * intersect_h

        w1, h1 = box1.xmax-box1.xmin, box1.ymax-box1.ymin
        w2, h2 = box2.xmax-box2.xmin, box2.ymax-box2.ymin

        union = w1*h1 + w2*h2 - intersect

        return float(intersect) / union


    def __do_nms(self,yolo_boxes):
        boxes = yolo_boxes
        if len(boxes) > 0:
            nb_class = len(boxes[0].classes)
        else:
            return
        for c in range(nb_class):
            sorted_indices = np.argsort([-box.classes[c] for box in boxes])

            for i in range(len(sorted_indices)):
                index_i = sorted_indices[i]

                if boxes[index_i].classes[c] == 0: continue

                for j in range(i+1, len(sorted_indices)):
                    index_j = sorted_indices[j]

                    if self.__bbox_iou(boxes[index_i], boxes[index_j]) >= self.__nms_thresh:
                        boxes[index_j].classes[c] = 0
        return boxes
    
    def __get_boxes(self,yolo_boxes):
        boxes = yolo_boxes
        labels = self.__labels
        thresh = self.__obj_thresh
        v_boxes, v_labels, v_scores = list(), list(), list()
        # enumerate all boxes
        for box in boxes:
            # enumerate all possible labels
            for i in range(len(labels)):
                # check if the threshold for this label is high enough
                if box.classes[i] > thresh:
                    v_boxes.append(box)
                    v_labels.append(labels[i])
                    v_scores.append(box.classes[i]*100)
                    # don't break, many labels may trigger for one box
        return v_boxes, v_labels, v_scores

