import argparse
import numpy as np
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from pathlib import Path

# [param]
# picture_matrix numpy数组 类型np.uint8 0-255的灰度图像
# kernel_size int 一个运算核的边长 越小转换出的线条越纤细
# [return]
# lineart_matrix 0-255的灰度图像 numpy数组 类型np.uint8
def picture2lineart(picture_matrix, kernel_size=1):
    assert isinstance(kernel_size, int) and kernel_size >= 2, "kernel_size should >= 2"
    assert (
        isinstance(picture_matrix, np.ndarray)
        and np.sum(picture_matrix > 255) == 0
        and np.sum(picture_matrix < 0) == 0
    ), "picture matrix should be a np.ndarray in [0,255]"

    picture_height, picture_width = picture_matrix.shape
    lineart_height = picture_height - kernel_size + 1
    lineart_width = picture_width - kernel_size + 1
    middle_offset = int(kernel_size / 2)  # 中心位置的偏差

    lineart_matrix = np.zeros(shape=(lineart_height, lineart_width), dtype=np.int8)
    for r in range(lineart_height):
        for c in range(lineart_width):
            # raw_color: 当前kernel中心的颜色
            raw_color = picture_matrix[r + middle_offset][c + middle_offset]
            max_color = np.max(
                picture_matrix[r : (r + kernel_size), c : (c + kernel_size)]
            )
            # 颜色减淡: raw_color 与 max_color 越接近 new_color越白
            new_color = 255 * raw_color / max_color
            lineart_matrix[r][c] = new_color
    return lineart_matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--picture_path", "-i", type=str, help="输入图像的路径")
    parser.add_argument(
        "--output_folder_path", "-o", type=str, default="result", help="输出文件夹的路径",
    )
    parser.add_argument(
        "--kernel_size", type=int, default=3, help="单次处理像素块边长 越小得到的线稿线条越纤细"
    )
    arguments = parser.parse_args()

    # mode="L": translate a color image to greyscale: L = R * 299/1000 + G * 587/1000 + B * 114/1000
    picture = Image.open(arguments.picture_path).convert(mode="L")
    picture_matrix = np.array(picture, dtype=np.uint8)
    lineart_matrix = picture2lineart(picture_matrix, kernel_size=arguments.kernel_size)
    lineart = Image.fromarray(lineart_matrix, "L")
    lineart.save(Path(arguments.output_folder_path, Path(arguments.picture_path).name))
