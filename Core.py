import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

from JpegCore import JpegCore
from H260Core import H260Core


def watermarking(img_path, wm_path, wm_strength=30.0):
    img = cv2.imread(img_path, 0)  # 直接读为灰度图像
    wm = cv2.imread(wm_path, 0)
    wm_height = wm.shape[0]
    wm_width = wm.shape[1]
    wm = 255 - wm

    # fft
    img_fft = np.fft.fft2(img)
    img_fft_shift = np.fft.fftshift(img_fft)
    img_fft_shift_real = np.log(np.abs(img_fft_shift))

    # watermarking
    img_fft_shift_wm = img_fft_shift.copy()
    img_fft_shift_wm[0:wm_height, 0:wm_width] += wm * wm_strength
    img_fft_shift_wm[-wm_height:, -wm_width:] += cv2.flip(wm, -1) * wm_strength
    img_fft_shift_wm_real = np.log(np.abs(img_fft_shift_wm))

    # ifft
    img_ifft_shift = np.fft.ifftshift(img_fft_shift_wm)
    img_ifft = np.fft.ifft2(img_ifft_shift)
    img_ifft_real = np.abs(img_ifft)

    # process
    img_precessed = img_ifft_real[0:200, 0:200]

    # fft process
    img_processed_fft = np.fft.fft2(img_precessed)
    img_processed_fft_shift = np.fft.fftshift(img_processed_fft)
    img_processed_fft_shift_real = np.log(np.abs(img_processed_fft_shift))

    # plotting
    plt.subplot(231), plt.imshow(img, 'gray'), plt.title('Original Image')
    plt.subplot(232), plt.imshow(img_fft_shift_real, 'gray'), plt.title('Fourier Image')
    plt.subplot(233), plt.imshow(img_fft_shift_wm_real, 'gray'), plt.title('Watermarked Fourier')
    plt.subplot(234), plt.imshow(img_ifft_real, 'gray'), plt.title('Reconstructed Image')
    plt.subplot(235), plt.imshow(img_precessed, 'gray'), plt.title('Processed Image')
    plt.subplot(236), plt.imshow(img_processed_fft_shift_real, 'gray'), plt.title('Processed Fourier')
    plt.show()


def h260(vid_name):
    jpegCore = JpegCore()
    h264Core = H260Core()
    GOBSIZE = 5
    vid = cv2.VideoCapture(vid_name)
    vid_fps = vid.get(cv2.CAP_PROP_FPS)  # 视频的帧率FPS
    vid_total_frame = vid.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频的总帧数
    i = 0
    iFrame = None
    bs = bytearray()
    if vid.isOpened():
        bs.extend(int(vid_total_frame).to_bytes(4, byteorder='big'))
        while True:
            ret, img = vid.read()
            if not ret:
                break
            print("Compressing " + str(i+1) + "-th frame")
            if i % GOBSIZE == 0:
                iFrame = img
                # ba = bytearray('temp', encoding="UTF-8")
                ba = jpegCore.Compress(image=iFrame)
            else:
                vectorList = h264Core.intraCoding(iFrame, img)
                ba = vectorList.tobytes()

            bs.extend((len(ba)).to_bytes(4, byteorder='big'))
            bs.extend(ba)
            i = i + 1
    else:
        print('fail to open')
    if os.path.exists("test.h260"):
        os.remove("test.h260")
    with open("test.h260", 'wb') as o:
        o.write(bs)
        o.flush()


def rh260(h260_name):
    jpegCore = JpegCore()
    h264Core = H260Core()
    GOBSIZE = 5
    frameList = []
    with open(h260_name, 'rb') as o:
        vid_total_frame = int.from_bytes(o.read(4), byteorder='big')
        i = 0
        while i < vid_total_frame:
            print("Decompressing " + str(i+1) + "-th frame")
            size = int.from_bytes(o.read(4), byteorder='big')
            data = o.read(size)
            if i % GOBSIZE == 0:
                iFrame = jpegCore.Decompress(data)
                frameList.append(iFrame)
            else:
                pFrame = h264Core.intraDecoding(iFrame, data)
                frameList.append(pFrame)
            i += 1
        i = 0
        for f in frameList:
            cv2.imshow("test", f)
            cv2.imwrite("output/out-"+str(i)+".bmp", f)
            i += 1
            cv2.waitKey(40)


if __name__ == '__main__':
    # watermarking('Lenna.jpg', 'watermark.png')
    # h260("test.y4m")
    rh260("test.h260")
