import numpy as np
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from pathlib import Path
import argparse


def ctrl_lim(num):
    # 控制输入的数范围在0~255
    if num < 0:
        return 0
    if num > 255:
        return 255
    return num


def convolve(pic_matrix, new_matrix, kernel):
    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]
    picture_height = pic_matrix.shape[0]
    picture_width = pic_matrix.shape[1]
    r = int((kernel.shape[0] - 1) / 2)
    for j in range(picture_height - kernel_height + 1):
        if j % 20 == 0:
            print("正在执行第" + str(j) + "行像素点")
        for i in range(picture_width - kernel_width + 1):
            raw_color = pic_matrix[j + r][i + r]
            # 卷积
            max_color = 0
            for m in range(kernel_height):
                for n in range(kernel_width):
                    if pic_matrix[j + m][i + n] > max_color:
                        max_color = pic_matrix[j + m][i + n]
            # 反色
            max_color = ctrl_lim(255 - max_color)
            # 颜色减淡
            if raw_color == 255:
                new_color = 255
            elif max_color == 0:
                new_color = raw_color
            else:
                new_color = raw_color / (1 - max_color / 255)

            new_matrix[j][i] = ctrl_lim(new_color)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pic_path", "-i", type=str, help="path of original picture")
    parser.add_argument(
        "--output_folder_path",
        "-o",
        type=str,
        default="result",
        help="path of output folder",
    )
    args = parser.parse_args()

    pic_path = Path(args.pic_path)
    pic_name = pic_path.name
    # translate a color image to greyscale: L = R * 299/1000 + G * 587/1000 + B * 114/1000
    pic = Image.open(pic_path).convert(mode="L")
    width, height = pic.size
    pic_matrix = np.array(pic).reshape((height, width))

    lineart = Image.new("L", (width - 2, height - 2), 255)
    lineart_matrix = np.array(lineart).reshape((height - 2, width - 2))

    print("开始")
    kernel = np.zeros((5, 5))
    convolve(pic_matrix, lineart_matrix, kernel)
    print("完毕")

    lineart = Image.fromarray(lineart_matrix, "L")
    lineart.save(Path(args.output_folder_path, pic_name))
