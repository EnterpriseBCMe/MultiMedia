import cv2
import numpy as np
import matplotlib.pyplot as plt


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
    vid = cv2.VideoCapture(vid_name)
    vid_fps = vid.get(cv2.CAP_PROP_FPS)  # 视频的帧率FPS
    vid_total_frame = vid.get(cv2.CAP_PROP_FRAME_COUNT)  # 视频的总帧数
    if vid.isOpened():
        while True:
            ret, img = vid.read()
            if not ret:
                break
            cv2.imshow("test", img)
            cv2.waitKey(int((1000/vid_fps)))
    else:
        print('视频打开失败！')


if __name__ == '__main__':
    # watermarking('Lenna.jpg', 'watermark.png')
    h260("test.y4m")
