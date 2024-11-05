import cv2
import numpy as np
from ColorByClick import get_color_by_click


def get_green_to_yellow_mask(im: np.ndarray) -> np.ndarray:
    """
        Если компонента g наибольшая, то приравниваем к ней r,
        тем самым получая желтый. Для яркости домножим эти
        компоненты на коэффициенты
    """
    yellow_brightness = 1.4
    green_brightness = 1.1

    # Параметры регулирующие преобразование серого в желтый
    min_g_r_diff = -20
    min_g_b_diff = 20

    mask_im = im.copy()
    for h in range(im.shape[0]):
        for w in range(im.shape[1]):
            b, g, r = im[h][w]
            if (g > r and g > b) or (int(g) - int(r) > min_g_r_diff and int(g) - int(b) > min_g_b_diff):
                new_r = min(int(g) * yellow_brightness, 255)
                new_g = min(int(g) * green_brightness, 255)
                new_b = b
                mask_im[h][w] = [new_b, new_g, new_r]
            else:
                mask_im[h][w] = [255, 255, 255]
    return mask_im


def get_erode_mask(mask_im: np.ndarray) -> np.ndarray:
    kernel_size = 8
    img = mask_im.copy()
    kernel = np.ones((kernel_size, kernel_size), 'uint8')
    dilate_img = cv2.dilate(img, kernel, iterations=3)
    erode_mask = cv2.erode(dilate_img, kernel, cv2.BORDER_REFLECT, iterations=2)
    return erode_mask


def check_for_white_pix(pix) -> bool:
    for color_ind in range(3):
        if pix[color_ind] != 255:
            return False
    return True


def apply_mask(mask_im: np.ndarray, erode_mask: np.ndarray, im: np.ndarray) -> np.ndarray:
    for h in range(erode_mask.shape[0]):
        for w in range(erode_mask.shape[1]):
            is_empty_erode_pix = check_for_white_pix(erode_mask[h][w])
            is_empty_mask_pix = check_for_white_pix(mask_im[h][w])

            if not is_empty_erode_pix and not is_empty_mask_pix:
                im[h][w] = mask_im[h][w]
    return im


def green_to_yellow(orig_im_name: str, res_im_name: str) -> None:
    im = cv2.imread(orig_im_name)
    mask_im = get_green_to_yellow_mask(im)
    erode_mask = get_erode_mask(mask_im)
    im = apply_mask(mask_im, erode_mask, im)
    cv2.imwrite(res_im_name, im)


def main():
    # 'images\\0053.png'
    green_to_yellow('images\\0053.png', 'res002.png')
    # get_color_by_click('res002.png')


if __name__ == '__main__':
    main()
