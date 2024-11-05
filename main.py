import cv2

def green_to_yellow(img_name: str, new_img_name: str):
    """
        Если компонента g наибольшая, то приравниваем к ней r,
        тем самым получая желтый. Для яркости домножим эти
        компоненты на коэффициенты
    """
    yellow_brightness = 1.4
    green_brightness = 1.1

    im = cv2.imread(img_name)
    for h in range(im.shape[0]):
        for w in range(im.shape[1]):
            b, g, r = im[h][w]
            if int(g) > int(r) and int(g) > int(b):
                new_r = min(int(g * yellow_brightness), 255)
                new_g = min(int(g * green_brightness), 255)
                new_b = b
                im[h][w] = [new_b, new_g, new_r]
    cv2.imwrite(new_img_name, im)


def main():
    green_to_yellow('images\\0109.png', 'res4.png')


if __name__ == '__main__':
    main()
