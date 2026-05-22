from ctypes import *
import cv2
import numpy as np
import numpy.ctypeslib as npct

class Detector():
    def __init__(self,model_path,dll_path):
        self.yolov5 = CDLL(dll_path)
        self.yolov5.Detect.argtypes = [c_void_p,c_int,c_int,POINTER(c_ubyte),npct.ndpointer(dtype = np.float32, ndim = 2, shape = (50, 6), flags="C_CONTIGUOUS")]
        self.yolov5.Init.restype = c_void_p
        self.yolov5.Init.argtypes = [c_void_p]
        self.yolov5.cuda_free.argtypes = [c_void_p]
        self.c_point = self.yolov5.Init(model_path)

    def predict(self,img):
        rows, cols = img.shape[0], img.shape[1]
        res_arr = np.zeros((50,6),dtype=np.float32)
        self.yolov5.Detect(self.c_point,c_int(rows), c_int(cols), img.ctypes.data_as(POINTER(c_ubyte)),res_arr)
        self.bbox_array = res_arr[~(res_arr==0).all(1)]
        return self.bbox_array

    def free(self):
        self.yolov5.cuda_free(self.c_point)

def visualize(img,bbox_array):
    for temp in bbox_array:
        bbox = [temp[0],temp[1],temp[2],temp[3]]  #xywh
        clas = int(temp[4])
        score = temp[5]
        if clas == 0:
            cv2.rectangle(img, (int(temp[0]), int(temp[1])), (int(temp[0] + temp[2]), int(temp[1] + temp[3])),
                          (0, 0, 249), 2)
            img = cv2.putText(img, str(clas) + " " + str(round(score, 2)), (int(temp[0]), int(temp[1]) - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 249), 1)
        elif clas ==1:
            cv2.rectangle(img, (int(temp[0]), int(temp[1])), (int(temp[0] + temp[2]), int(temp[1] + temp[3])),
                          (105, 0, 0), 2)
            img = cv2.putText(img, str(clas) + " " + str(round(score, 2)), (int(temp[0]), int(temp[1]) - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (105, 0, 0), 1)

        elif clas ==2:
            cv2.rectangle(img, (int(temp[0]), int(temp[1])), (int(temp[0] + temp[2]), int(temp[1] + temp[3])),
                          (0, 255, 0), 2)
            img = cv2.putText(img, str(clas) + " " + str(round(score, 2)), (int(temp[0]), int(temp[1]) - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return img


if __name__ == '__main__':
    det = Detector(model_path=b"./best160-1.engine",dll_path="./best160-1.dll")  # b'' is needed
    img = cv2.imread("148.jpg")
    detcted = det.predict(img)
    print(detcted)
    img = visualize(img,detcted)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    det.free()
    cv2.destroyAllWindows()