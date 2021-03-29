import cv2
import numpy as np
import matplotlib.pyplot as plt


def example():
    img = cv2.imread('Lenna.jpg', 0)  # 直接读为灰度图像
    img = cv2.resize(img, (300, 300))

    wm = cv2.imread("watermark.png", 0)
    wm = cv2.resize(wm, (200, 50))
    wm = 255 - wm

    # 快速傅里叶变换算法得到频率分布
    f = np.fft.fft2(img)
    # 默认结果中心点位置在左上角，转移到中间
    fshift = np.fft.fftshift(f)
    # 取绝对值：将复数变化成实数
    # 取对数的目的为了将数据变化到0-255
    # fshift是复数，求绝对值结果才是振幅
    s1 = np.log(np.abs(fshift))

    # 求相位，相位和振幅是频域两个很重要的结果
    # 振幅只是记录图片的明暗，而相位才是记录图像的形状
    s1_angle = np.angle(fshift)

    # 将水印放入频域
    fshift2 = fshift.copy()
    fshift2[0:50, 0:200] += wm * 50.0
    fshift2[-50:, -200:] += cv2.flip(wm, -1) * 50.0

    s2 = np.log(np.abs(fshift2))

    # 逆变换
    f1shift2 = np.fft.ifftshift(fshift2)
    img_back2 = np.fft.ifft2(f1shift2)
    # 出来的复数，无法显示，转成实数
    img_back2 = np.abs(img_back2)

    f1shift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f1shift)
    # 出来的是复数，无法显示
    img_back = np.abs(img_back)


def main():
    img = cv2.imread('Lenna.jpg', 0)  # 直接读为灰度图像
    # img = cv2.resize(img, (300, 300))

    wm = cv2.imread("watermark.png", 0)
    wm = cv2.resize(wm, (200, 50))
    wm = 255 - wm

    # fft
    img_fft = np.fft.fft2(img)
    img_fft_shift = np.fft.fftshift(img_fft)
    img_fft_shift_real = np.log(np.abs(img_fft_shift))

    # ifft
    img_ifft_shift = np.fft.ifftshift(img_fft_shift)
    img_ifft = np.fft.ifft2(img_ifft_shift)
    img_ifft_real = np.abs(img_ifft)


    plt.subplot(231), plt.imshow(img, 'gray'), plt.title('Original Image')
    plt.subplot(232), plt.imshow(img_fft_shift_real, 'gray'), plt.title('Fourier Image')
    plt.subplot(233), plt.imshow(img_ifft_real, 'gray'), plt.title('Reconstructed Image')
    plt.show()


if __name__ == '__main__':
    main()
