import unittest
import torch
from color_transfer import Conversion_Srgb_LSM
import numpy as np
from PIL import Image
from pathlib import Path


class TestColorTransfer(unittest.TestCase):
    # def __init__(self):

    def test_LMS(self, srgb_img):
        srgb_img = torch.where(srgb_img <= 0.04045, srgb_img/12.92,
                               torch.pow((srgb_img+0.055)/1.055, 2.4))
        lms_img = torch.einsum("whc, mc -> whm", srgb_img, self.srgb_to_lms)
        LMS_img = torch.log(lms_img)
        lms_img = torch.exp(LMS_img)
        srgb_img = torch.einsum("whc, mc -> whm", lms_img, self.lms_to_srgb)
        new_srgb_img = torch.where(srgb_img <= 0.0031308, 12.92 *
                                   srgb_img, 1.055 * torch.pow(srgb_img, 1/2.4) - 0.055)

    # def test_matrix(self):
    #     conversion = Conversion_Srgb_LSM()
    #     tmp = torch.mm(conversion.LMS_to_lab_matrix,
    #                    conversion.LMS_to_lab_matrix)
    #     tmp2 = torch.mm(conversion.lms_to_srgb, conversion.srgb_to_lms)
    #     torch.isclose(tmp, tmp2)


def assertScalarEqual(tensor1, tensor2):
    tmp = torch.abs(tensor1 - tensor2)
    assert tmp.item() <= 0.0001, print(tensor1, tensor2, tmp)
    # assert torch.isclose(tensor1, tensor2), print(tensor1.item(), tensor2)


def check_srgb_matrix():
    """
    srgbでの赤緑青の値をxy平面に写像した値は規格TU-R BT.709で決められている．
    この値のペアを利用して，srgbからXYZ色空間への変換が正しく行われているか確認する関数．
    メモTU-R BT.709はD65を利用している．
    """
    def check(color, x, y):
        color = conversion.from_srgb_gamma(color)
        xyz = torch.mm(conversion.srgb_to_xyz, color)
        cal_x, cal_y = get_xy(xyz)
        x, y = torch.tensor([x]), torch.tensor([y])
        assertScalarEqual(cal_x, x)
        assertScalarEqual(cal_y, y)
    conversion = Conversion_Srgb_LSM()
    red = torch.tensor([1, 0, 0], dtype=torch.float32).reshape((3, 1))
    green = torch.tensor([0, 1, 0], dtype=torch.float32).reshape((3, 1))
    blue = torch.tensor([0, 0, 1], dtype=torch.float32).reshape((3, 1))
    white = torch.tensor([1, 1, 1], dtype=torch.float32).reshape((3, 1))

    red_x, red_y = 0.640, 0.3300
    green_x, green_y = 0.3, 0.6
    blue_x, blue_y = 0.15, 0.060
    white_x, white_y = 0.3127, 0.3290
    check(red, red_x, red_y)
    check(green, green_x, green_y)
    check(blue, blue_x, blue_y)
    check(white, white_x, white_y)


def get_xy(xyz):
    return xyz[0] / torch.sum(xyz), xyz[1] / torch.sum(xyz)


def test2(source_path, target_path, save_dir):
    source_img = np.asarray(Image.open(source_path)) / 255
    source_img = torch.from_numpy((source_img.astype(np.float32)))
    conversion = Conversion_Srgb_LSM()
    new_srgb_img = conversion.test_LMS(source_img)
    img = Image.fromarray(np.uint8(255*new_srgb_img.cpu().float().numpy()))
    save_name = save_dir + "from_test2" + Path(source_path).name
    img.save(save_name)


def test(source_path, target_path, save_dir):
    source_img = np.asarray(Image.open(source_path)) / 255
    source_img = torch.from_numpy((source_img.astype(np.float32)))
    # print(source_img.dtype)
    target_img = np.asarray(Image.open(target_path)) / 255
    target_img = torch.from_numpy(target_img.astype(np.float32))
    conversion = Conversion_Srgb_LSM()
    source_lab_img = conversion.srgb_to_lab(source_img)
    # target_lab_img = conversion.srgb_to_lab(target_img)
    # new_lab_img = color_transfer(source_lab_img, target_lab_img)
    new_srgb_img = conversion.lab_to_srgb(source_lab_img)

    img = Image.fromarray(np.uint8(255*new_srgb_img.cpu().float().numpy()))
    # save_name = save_dir + "source=" + Path(source_path).stem + "target=" + Path(target_path).stem + ".png"
    save_name = save_dir + "from_lab" + Path(source_path).name
    img.save(save_name)


def constract():
    conversion = Conversion_Srgb_LSM()


if __name__ == "__main__":
    # test2("images/雨宮優子2.jpg", "images/天使ちゃん.png", "results/")
    # constract()
    check_srgb_matrix()
