import numpy as np
import cv2
from PIL import Image


class H260Core:
    def __init__(self):
        self.p = 0

    def __Rgb2Yuv(self, r, g, b):
        # 从图像获取YUV矩阵
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
        v = 0.5 * r - 0.419 * g - 0.081 * b + 128
        return y, u, v

    def __Fill(self, matrix):
        # 图片的长宽都需要满足是16的倍数（采样长宽会缩小1/2和取块长宽会缩小1/8）
        # 图像压缩三种取样方式4:4:4、4:2:2、4:2:0
        fh, fw = 0, 0
        if self.height % 16 != 0:
            fh = 16 - self.height % 16
        if self.width % 16 != 0:
            fw = 16 - self.width % 16
        res = np.pad(matrix, ((0, fh), (0, fw)), 'constant',
                     constant_values=(0, 0))
        return res

    def __SearchForSimilarBlock(self, iy, pBlock, center):
        offset = self.p // 2
        last = False
        currentCenter = center
        bestCenter = center
        bestDiff = np.inf
        while not last:
            if offset == 1:
                last = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    nx, ny = int(currentCenter[0] + offset * i), int(currentCenter[1] + offset * j)
                    if nx < 0 or nx + 8 > iy.shape[0] or ny < 0 or ny + 8 > iy.shape[1]:
                        continue
                    diff = np.sum(np.abs(iy[nx:nx + 8, ny:ny + 8] - pBlock)) / 64
                    if diff < bestDiff:
                        bestCenter = (nx, ny)
                        bestDiff = diff
            offset //= 2
        return bestCenter

    def intraCoding(self, iFrame, pFrame):
        self.height = iFrame.shape[0]
        self.width = iFrame.shape[1]
        self.p = 50
        ir = iFrame[:, :, 0]
        ig = iFrame[:, :, 1]
        ib = iFrame[:, :, 2]
        pr = pFrame[:, :, 0]
        pg = pFrame[:, :, 1]
        pb = pFrame[:, :, 2]
        iy, iu, iv = self.__Rgb2Yuv(ir, ig, ib)
        py, _, _ = self.__Rgb2Yuv(pr, pg, pb)
        # 先对图像进行填充
        iy = self.__Fill(iy)
        iu = self.__Fill(iu)
        iv = self.__Fill(iv)
        py = self.__Fill(py)
        shape = (self.height // 8, self.width // 8, 8, 8)
        strides = iy.itemsize * np.array([self.width * 8, 8, self.width, 1])
        pBlocks = np.lib.stride_tricks.as_strided(py, shape=shape, strides=strides)
        vectorList = np.zeros((self.height // 8, self.width // 8, 2), dtype=np.int8)
        for i in range(pBlocks.shape[0]):
            for j in range(pBlocks.shape[1]):
                sx, sy = self.__SearchForSimilarBlock(iy, pBlocks[i][j], (i * 8, j * 8))
                vectorList[i, j, 0], vectorList[i, j, 1] = sx - (i * 8), sy - (j * 8)
        return vectorList

    def intraDecoding(self, iFrame, vListData):
        self.height = iFrame.shape[0]
        self.width = iFrame.shape[1]
        vectorList = np.frombuffer(vListData, dtype=np.int8).reshape((self.height//8, self.width//8, 2))
        ir = iFrame[:, :, 0]
        ig = iFrame[:, :, 1]
        ib = iFrame[:, :, 2]
        iy, iu, iv = self.__Rgb2Yuv(ir, ig, ib)
        iy = self.__Fill(iy)
        iu = self.__Fill(iu)
        iv = self.__Fill(iv)
        newPy = np.zeros(iy.shape)
        newPu = np.zeros(iy.shape)
        newPv = np.zeros(iy.shape)
        for i in range(vectorList.shape[0]):
            for j in range(vectorList.shape[1]):
                sx, sy = vectorList[i, j, 0] + i * 8, vectorList[i, j, 1] + j * 8
                newPy[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = iy[sx:sx + 8, sy:sy + 8]
                newPu[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = iu[sx:sx + 8, sy:sy + 8]
                newPv[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = iv[sx:sx + 8, sy:sy + 8]
        newPy = newPy[0:self.height, 0:self.width]
        newPu = newPu[0:self.height, 0:self.width]
        newPv = newPv[0:self.height, 0:self.width]
        r = (newPy + 1.402 * (newPv - 128))
        g = (newPy - 0.34414 * (newPu - 128) - 0.71414 * (newPv - 128))
        b = (newPy + 1.772 * (newPu - 128))
        r = Image.fromarray(r).convert('L')
        g = Image.fromarray(g).convert('L')
        b = Image.fromarray(b).convert('L')
        image = Image.merge("RGB", (r, g, b))
        image = np.asarray(image)
        return image
