import torch
from PIL import Image
import numpy as np
from pathlib import Path


class Conversion_Srgb_LSM:
    def __init__(self):
        self.srgb_to_xyz = torch.tensor([
            [0.412453, 0.357580, 0.180423],
            [0.212671, 0.715160, 0.072169],
            [0.019334, 0.119193, 0.950227]])
        self.modify_matrix = False
        if self.modify_matrix:
            one = torch.ones(3, dtype=torch.float32).reshape((3, 1))
            x = torch.mm(self.srgb_to_xyz.inverse(), one)
            self.srgb_to_xyz = self.srgb_to_xyz * x.T

        # # 論文に乗っている変換式．
        # rgb_to_xyz = torch.tensor([
        #     [0.5141, 0.3239, 0.1604],
        #     [0.2651, 0.6702, 0.0641],
        #     [0.0241, 0.1228, 0.8444]])
        # rgb_to_lms = torch.tensor([
        #     [0.3811, 0.5783, 0.0402],
        #     [0.1967, 0.7244, 0.0782],
        #     [0.0241, 0.1288, 0.8444]])
        xyz_to_lms = torch.tensor([
            [0.3897, 0.6890, -0.0787],
            [-0.2298, 1.1834, 0.0464],
            [0.0000, 0.0000, 1.0000]])
        self.srgb_to_lms = torch.mm(xyz_to_lms, self.srgb_to_xyz)
        # self.srgb_to_lms = rgb_to_lms
        self.lms_to_srgb = self.srgb_to_lms.inverse()
        # self.lms_to_srgb = torch.tensor([
        #     [4.4679, -3.5873, 0.1193],
        #     [-1.2186, 2.3809, -0.1624],
        #     [0.0497, -0.2439, 1.2045]
        # ])

        m1 = torch.tensor(
            [[1, 1, 1], [1, 1, -2], [1, -1, 0]], dtype=torch.float32)
        vec = torch.rsqrt(torch.tensor([3.0, 6.0, 2.0]))
        m2 = torch.diag(vec)
        self.LMS_to_lab_matrix = torch.einsum("mc, cd ->md", m2, m1)

        m1 = m1.T
        vec = torch.div(torch.sqrt(torch.tensor(
            [3.0, 6.0, 2.0])), torch.tensor([3, 6, 2], dtype=torch.float32))
        m2 = torch.diag(vec)
        self.lab_to_LMS_matrix = torch.einsum("mc, cd->md", m1, m2)

    def from_srgb_gamma(self, srgb_img):
        """
        srgb -> xyzにする時のガンマ補正
        input (non) srgb_img tensor[0, 1]
        output (linear) srgb_img tensor
        """
        linear_srgb = torch.where(srgb_img <= 0.04045, srgb_img/12.92,
                                  torch.pow((srgb_img+0.055)/1.055, 2.4))
        return linear_srgb

    def to_srgb_gamma(self, srgb_img):
        """
        xyz -> srgbにする時のガンマ補正
        input （linear) srgb_img tensor
        output (non) srgb_img tensor[0, 1]

        """
        srgb_img = torch.where(srgb_img <= 0.0031308, 12.92 *
                               srgb_img, 1.055 * torch.pow(srgb_img, 1/2.4) - 0.055)
        return srgb_img

    def srgb_to_lab(self, srgb_img):
        """
        input srgb_img tensor [0, 1]
        return lab_img tensor
        """
        if not self.modify_matrix:
            srgb_img = self.from_srgb_gamma(srgb_img)
        lms_img = torch.einsum("whc, mc -> whm", srgb_img, self.srgb_to_lms)
        LMS_img = torch.log(lms_img)
        lab_img = torch.einsum("whc, mc-> whm", LMS_img,
                               self.LMS_to_lab_matrix)
        return lab_img

    def lab_to_srgb(self, lab_img):
        """
        input lab tensor
        return srgb tensor[0, 1]
        """
        LMS_img = torch.einsum("whc, mc -> whm", lab_img,
                               self.lab_to_LMS_matrix)
        lms_img = torch.exp(LMS_img)
        srgb_img = torch.einsum("whc, mc -> whm", lms_img, self.lms_to_srgb)
        if not self.modify_matrix:
            srgb_img = self.to_srgb_gamma(srgb_img)
        srgb_img = torch.clamp(srgb_img, min=0, max=1)
        return srgb_img


def color_transfer(source_img, target_img):
    """
    source_img: lab image tensor
    target_img: lab image tensor

    return:参照画像（target img）の色に変換した入力画像(source img)
    """
    source_mean = torch.mean(source_img, dim=[0, 1])
    target_mean = torch.mean(target_img, dim=[0, 1])
    source_std = torch.std(source_img, dim=[0, 1], unbiased=False)
    target_std = torch.std(target_img, dim=[0, 1], unbiased=False)
    new_lab_img = torch.div(target_std, source_std) * \
        (source_img - source_mean) + target_mean
    return new_lab_img


def main(source_path, target_path, save_dir):
    source_img = np.asarray(Image.open(source_path)) / 255
    # αチャネルがあった場合は削除
    if source_img.shape[2] == 4:
        source_img = source_img[:, :, :3]
    source_img = torch.from_numpy((source_img.astype(np.float32)))
    target_img = np.asarray(Image.open(target_path)) / 255
    if target_img.shape[2] == 4:
        target_img = target_img[:, :, :3]
    target_img = torch.from_numpy(target_img.astype(np.float32))
    conversion = Conversion_Srgb_LSM()
    source_lab_img = conversion.srgb_to_lab(source_img)
    target_lab_img = conversion.srgb_to_lab(target_img)
    new_lab_img = color_transfer(source_lab_img, target_lab_img)
    new_srgb_img = conversion.lab_to_srgb(new_lab_img)
    img = Image.fromarray(np.uint8(255*new_srgb_img.cpu().float().numpy()))
    save_name = Path(save_dir).joinpath(
        "source=" + Path(source_path).stem + "target=" + Path(target_path).stem + ".png")
    img.save(save_name)


def main2(source_path, target_path, save_dir):
    source_img = Image.open(source_path)
    target_img = Image.open(target_path)
    source_img = source_img.resize((192, 165))
    target_img = target_img.resize((192, 165))
    source_img = np.asarray(source_img) / 255
    # αチャネルがあった場合は削除
    if source_img.shape[2] == 4:
        source_img = source_img[:, :, :3]
    source_img = source_img[:450, :, :]
    target_img = np.asarray(target_img) / 255
    if target_img.shape[2] == 4:
        target_img = target_img[:, :, :3]
    source_img = torch.from_numpy((source_img.astype(np.float32)))
    target_img = torch.from_numpy(target_img.astype(np.float32))
    conversion = Conversion_Srgb_LSM()
    source_lab_img = conversion.srgb_to_lab(source_img)
    target_lab_img = conversion.srgb_to_lab(target_img)
    new_lab_img = color_transfer(source_lab_img, target_lab_img)
    new_srgb_img = conversion.lab_to_srgb(new_lab_img)
    img = Image.fromarray(np.uint8(255*new_srgb_img.cpu().float().numpy()))
    save_name = Path(save_dir).joinpath(
        "source=" + Path(source_path).stem + "target=" + Path(target_path).stem + ".png")
    img.save(save_name)


if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) != 4:
        print("color_tranfer.py 入力画像へのパス 参照画像へのパス 保存するディレクトリへのパス")
        print("と実行してください")
        sys.exit()
    main(args[1], args[2], args[3])
