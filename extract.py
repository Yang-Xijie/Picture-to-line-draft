import argparse
import numpy as np
from PIL import Image  # https://pillow.readthedocs.io/en/stable/reference/Image.html
from pathlib import Path

# [param]
# picture_matrix: numpy.ndarray dtype=np.uint8
#   0-255的灰度输入图像
# kernel_size: int >= 2
#   一个kernel的边长 越小转换出的线条越纤细
#   推荐值3
# contrast_threshold: float (0.0,1.0]
#   kernel内对比度的门限
#   值为1.0时图像的所有变化都经过转换 但变化缓慢处可能会较脏
#   值较小时可能出现全图空白 无法得到线稿
#   推荐值0.96
# [return]
# lineart_matrix: numpy.ndarray dtype=np.uint8
#   0-255的灰度线稿
def picture2lineart(picture_matrix, kernel_size, contrast_threshold):
    assert (
        isinstance(picture_matrix, np.ndarray)
        and np.sum(picture_matrix > 255) == 0
        and np.sum(picture_matrix < 0) == 0
    ), "picture matrix should be a np.ndarray in [0,255]"
    assert isinstance(kernel_size, int) and kernel_size >= 2, "kernel_size should >= 2"
    assert (
        isinstance(contrast_threshold, float)
        and contrast_threshold > 0.0
        and contrast_threshold <= 1.0
    ), "contrast_threshold should in (0.0,1.0]"

    picture_height, picture_width = picture_matrix.shape
    lineart_height = picture_height - kernel_size + 1
    lineart_width = picture_width - kernel_size + 1
    middle_offset = int(kernel_size / 2)  # 中心位置的偏差

    lineart_matrix = np.zeros(shape=(lineart_height, lineart_width), dtype=np.int8)
    for r in range(lineart_height):
        for c in range(lineart_width):
            # 当前kernel中心的颜色
            raw_color = picture_matrix[r + middle_offset][c + middle_offset]
            max_color = np.max(
                picture_matrix[r : (r + kernel_size), c : (c + kernel_size)]
            )

            contrast = raw_color / max_color  # contrast in [0,1]
            if contrast > contrast_threshold:
                new_color = 255  # 图片去脏 差异特别小的时候就直接给255
            else:
                # 颜色减淡: raw_color 与 max_color 越接近 new_color越白
                new_color = np.uint8(255 * raw_color / max_color)
            lineart_matrix[r][c] = new_color

    return lineart_matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--picture_path", "-i", type=str, help="输入图像的路径")
    parser.add_argument(
        "--output_folder_path", "-o", type=str, default="result", help="输出文件夹的路径",
    )
    parser.add_argument(
        "--kernel_size", type=int, default=3, help="int >= 2 单次处理像素块边长 越小得到的线稿线条越纤细"
    )
    parser.add_argument(
        "--contrast_threshold",
        type=float,
        default=0.96,
        help="(0.0,1.0]\nkernel内对比度的门限 推荐值0.96\n值为1.0时图像的所有变化都经过转换 但变化缓慢处可能会较脏\n值较小时可能出现全图空白 无法得到线稿",
    )
    arguments = parser.parse_args()

    # mode="L": translate a color image to greyscale: L = R * 299/1000 + G * 587/1000 + B * 114/1000
    picture = Image.open(arguments.picture_path).convert(mode="L")
    picture_matrix = np.array(picture, dtype=np.uint8)
    lineart_matrix = picture2lineart(
        picture_matrix,
        kernel_size=arguments.kernel_size,
        contrast_threshold=arguments.contrast_threshold,
    )
    lineart = Image.fromarray(lineart_matrix, "L")
    lineart.save(Path(arguments.output_folder_path, Path(arguments.picture_path).name))
