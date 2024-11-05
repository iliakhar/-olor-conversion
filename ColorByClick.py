import cv2

def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        color = param[y, x]
        print(f"Цвет пикселя: R={color[2]}, G={color[1]}, B={color[0]}")

def get_color_by_click(im_name: str):
    img = cv2.imread(im_name)
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', get_color, param=img)

    while True:
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()