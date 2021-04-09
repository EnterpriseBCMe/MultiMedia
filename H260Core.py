import numpy as np


class H260Core:
    def __init__(self):
        self.a = 0

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

    def intraCoding(self, iFrame, pFrame):
        self.height = iFrame.shape[0]
        self.width = iFrame.shape[1]
        # 先对图像进行填充
        iFrame = self.__Fill(iFrame)
        pFrame = self.__Fill(pFrame)
        # 减少for循环语句，利用numpy的自带函数来提升算法效率
        # 参考吴恩达的公开课视频，numpy的函数自带并行处理，不用像for循环一样串行处理
        shape = (self.height // 8, self.width // 8, 8, 8)
        strides = iFrame.itemsize * np.array([self.width * 8, 8, self.width, 1])
        pBlocks = np.lib.stride_tricks.as_strided(pFrame, shape=shape, strides=strides)
