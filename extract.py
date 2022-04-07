import argparse
import numpy as np
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from pathlib import Path


# pic_matrix 0-255的灰度图像 numpy数组 类型np.uint8
# kernel_size int 表示一个运算核的大小
# new_matrix 0-255的灰度图像 numpy数组 类型np.uint8
def convolve(pic_matrix, new_matrix, kernel_size=5):
    picture_height, picture_width = pic_matrix.shape
    result_height = picture_height - kernel_size + 1
    result_width = picture_width - kernel_size + 1
    mid_offset = int(kernel_size / 2)  # 中心位置的偏差

    for r in range(result_height):
        print(r)
        for c in range(result_width):
            raw_color = pic_matrix[r + mid_offset][c + mid_offset]  # 这个kernel中心的颜色
            max_color = np.max(pic_matrix[r:(r+kernel_size),c:(c+kernel_size)])
            # 颜色减淡: raw_color 与 max_color 越接近 new_color越白
            new_color = 255 * raw_color / max_color
            new_matrix[r][c] = new_color


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

    
    lineart_matrix = np.zeros(shape=(height - 2, width - 2), dtype=np.int8)
    convolve(pic_matrix, lineart_matrix)
    lineart = Image.fromarray(lineart_matrix, "L")
    lineart.save(Path(args.output_folder_path, pic_name))

