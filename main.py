import cv2
import numpy as np
from ColorByClick import get_color_by_click


def get_green_to_yellow_mask(im: np.ndarray, param_dict: dict) -> np.ndarray:
    """
        Если компонента g наибольшая, то приравниваем к ней r,
        тем самым получая желтый. Для яркости домножим эти
        компоненты на коэффициенты
    """
    yellow_brightness = param_dict['yellow_brightness']
    green_brightness = param_dict['green_brightness']
    threshold_g_r_diff = param_dict['threshold_g_r_diff']
    threshold_g_b_diff = param_dict['threshold_g_b_diff']

    mask_im = im.copy()
    for h in range(im.shape[0]):
        for w in range(im.shape[1]):
            b, g, r = im[h][w]
            if ((int(g) - int(r) > 5 and int(g) - int(b) > 5) or
                    (int(g) - int(r) > threshold_g_r_diff and int(g) - int(b) > threshold_g_b_diff)):
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


def green_to_yellow(orig_im_name: str, res_im_name: str, param_dict: dict) -> None:
    im = cv2.imread(orig_im_name)
    mask_im = get_green_to_yellow_mask(im, param_dict)
    erode_mask = get_erode_mask(mask_im)
    im = apply_mask(mask_im, erode_mask, im)
    cv2.imwrite(res_im_name, im)


def main():
    param_dict = {'yellow_brightness': 1.4, 'green_brightness': 1.1,  # отвечают за яркость желтого
                  'threshold_g_r_diff': -20, 'threshold_g_b_diff': 20}  # мин допустимая разница соответств. компонент

    # im_name = 'images\\0109.png'
    im_name = 'im3.jpg'
    green_to_yellow(im_name, 'res002.png', param_dict)
    get_color_by_click('res002.png')


if __name__ == '__main__':
    main()
