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

        (srgb_img - new_srgb_img)

    def assertTochEqual(tensor1, tensor2):
        tmp = tensor1 - tensor2

    def test_matrix(self):
        conversion = Conversion_Srgb_LSM()
        tmp = torch.mm(conversion.LMS_to_lab_matrix,
                       conversion.LMS_to_lab_matrix)
        tmp2 = torch.mm(conversion.lms_to_srgb, conversion.srgb_to_lms)


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
    constract()