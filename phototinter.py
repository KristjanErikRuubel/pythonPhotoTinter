import cv2
from PIL import Image

from transforms import RGBTransform


def image_tint(img1, img2, img3):
    """
    Function that adds red, green and grayish tint to images.
    :param img1: image 1
    :param img2: image 2
    :param img3: image 3
    :return: list of tinted images
    """
    red = RGBTransform().mix_with((255, 0, 0), factor=.30).applied_to(img3)
    green = RGBTransform().mix_with((0, 255, 0), factor=.30).applied_to(img1)
    white = RGBTransform().mix_with((189, 190, 191), factor=.30).applied_to(img2)
    return [green, white, red]


def split_image(input_image_path):
    """
    Function that splits image vertically to 3 different slices.

    :param input_image_path: image path
    :return: Cropped images
    """
    image = cv2.imread(input_image_path)
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)

    height, width, channels = image.shape[:3]
    print(image.shape)

    witdthdividedby3 = width / 3

    # Let's get the starting pixel coordiantes (top left of cropped top)
    start_row, start_col = int(0), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped top)
    end_row, end_col = int(height), int(witdthdividedby3)
    cropped_right = image[start_row:end_row, start_col:end_col]
    cv2.imshow("Cropped right", cropped_right)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    end_row, end_col = int(height), int(witdthdividedby3 * 2)
    start_row, start_col = int(0), int(witdthdividedby3)
    cropped_mid = image[start_row:end_row, start_col:end_col]
    cv2.imshow("Cropped mid", cropped_mid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    end_row, end_col = int(height), int(witdthdividedby3 * 3)
    start_row, start_col = int(0), int(witdthdividedby3 * 2)
    cropped_left = image[start_row:end_row, start_col:end_col]
    cv2.imshow("Cropped left", cropped_left)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return cropped_right, cropped_mid, cropped_left


def combine_pictures(images):
    """
    Function that combines pictures together.

    :param images: (List of pictures)
    :return: True
    """
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save('test.jpg')

    return True


if __name__ == '__main__':
    # input img
    input_image_path = 'myimg.jpg'
    # splited image
    crop_right, crop_mid, crop_left = split_image(input_image_path)

    # convert open cv to PIL
    img1 = cv2.cvtColor(crop_right, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img1)
    img2 = cv2.cvtColor(crop_mid, cv2.COLOR_BGR2RGB)
    img_pil2 = Image.fromarray(img2)
    img3 = cv2.cvtColor(crop_left, cv2.COLOR_BGR2RGB)
    img_pil3 = Image.fromarray(img3)
    # Add tint to img
    result = image_tint(img_pil, img_pil2, img_pil3)

    # Add pictures with different tint together
    combine_pictures(result)
