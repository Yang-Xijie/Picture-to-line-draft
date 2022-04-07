import numpy as np
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from pathlib import Path
import argparse


# pic_matrix 0-255的灰度图像
# new_matrix 
def convolve(pic_matrix, new_matrix, kernel):
    print((pic_matrix < 0).sum())
    print(pic_matrix.dtype)
    kernel_height, kernel_width = kernel.shape
    picture_height, picture_width = pic_matrix.shape
    r = int((kernel_height - 1) / 2)  # 找到中心位置
    for j in range(picture_height - kernel_height + 1):
        if j % 20 == 0:
            print("正在执行第" + str(j) + "行像素点")
        for i in range(picture_width - kernel_width + 1):
            raw_color = pic_matrix[j + r][i + r]  # 这个kernel中心的颜色
            # 卷积 在当前的这个kernel中寻找最大的灰度值
            max_color = 0
            for m in range(kernel_height):
                for n in range(kernel_width):
                    if pic_matrix[j + m][i + n] > max_color:
                        max_color = pic_matrix[j + m][i + n]

            # 颜色减淡
            new_color = 255 * raw_color / max_color # raw_color 与 max_color 越接近 new_color越白

            new_matrix[j][i] = new_color


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pic_path", "-i", type=str, help="输入图像的路径")
    parser.add_argument(
        "--output_folder_path", "-o", type=str, default="result", help="输出文件夹的路径",
    )
    args = parser.parse_args()

    pic_path = Path(args.pic_path)
    pic_name = pic_path.name
    # translate a color image to greyscale: L = R * 299/1000 + G * 587/1000 + B * 114/1000
    pic = Image.open(pic_path).convert(mode="L")
    width, height = pic.size
    print(pic.size)
    pic_matrix = np.array(pic).reshape((height, width))

    kernel = np.zeros((5, 5))
    lineart_matrix = np.zeros(shape=(height - 2, width - 2), dtype=np.int8)
    convolve(pic_matrix, lineart_matrix, kernel)
    lineart = Image.fromarray(lineart_matrix, "L")
    lineart.save(Path(args.output_folder_path, pic_name))

