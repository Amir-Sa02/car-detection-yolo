# -*- coding: utf-8 -*-
"""Single global bibliography for the whole thesis.

The آیین‌نامه requires ONE reference list at the end of the thesis, numbered
from 1 and ordered alphabetically (Persian sources first, then Latin, then web
sources), with the title of each work in italic.

Chapters never hard-code a number: they call ref("key") and get the correct
Persian numeral, so inserting a new source renumbers everything automatically.
"""

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

# key -> (sort surname, authors, title, venue-and-rest)
# `title` is rendered in italic; the rest is plain, comma separated.
SOURCES = {
    # the copy we hold is the 2025 review of YOLOv4, not Bochkovskiy's original
    "yolov4": (
        "Sundaresan Geetha",
        "Sundaresan Geetha, A.",
        "YOLOv4: A Breakthrough in Real-Time Object Detection",
        "arXiv preprint arXiv:2502.04161, 2025"),
    "adas_yolov11": (
        "Chaman A",
        "Chaman, M., El Maliki, A., El Yanboiy, H., Dahou, H., Laamari, H., and Hadjoudja, A.",
        "A Real-Time Vehicle Detection System for ADAS in Autonomous Vehicles Using "
        "YOLOv11 Deep Neural Network on Embedded Edge Platforms",
        "Engineering, Technology and Applied Science Research, vol. 15, no. 5, 2025, pp. 28077-28082"),
    "v11_vs_v12": (
        "Chaman B",
        "Chaman, M., El Maliki, A., El Yanboiy, H., Dahou, H., Laamari, H., and Hadjoudja, A.",
        "Comparative Analysis of Deep Neural Networks YOLOv11 and YOLOv12 for "
        "Real-Time Vehicle Detection in Autonomous Vehicles",
        "International Journal of Transport Development and Integration, vol. 9, no. 1, 2025, pp. 39-48"),
    "yolov11": (
        "Khanam",
        "Khanam, R., and Hussain, M.",
        "YOLOv11: An Overview of the Key Architectural Enhancements",
        "arXiv preprint arXiv:2410.17725, 2024"),
    "iadd": (
        "Khosravian",
        "Khosravian, A., Amirkhani, A., Masih-Tehrani, M., and Yazdanijoo, A.",
        "Multi-domain autonomous driving dataset: Towards enhancing the generalization "
        "of the convolutional neural networks in new environments",
        "IET Image Processing, vol. 17, 2023, pp. 1253-1266"),
    "yolo11_coop": (
        "Liang",
        "Liang, E., Wei, D., Li, F., Lv, H., and Li, S.",
        "Object detection model of vehicle-road cooperative autonomous driving based on "
        "improved YOLO11 algorithm",
        "Scientific Reports, vol. 15, 2025, article 32348"),
    "coco": (
        "Lin A",
        "Lin, T.-Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., "
        "Dollar, P., and Zitnick, C. L.",
        "Microsoft COCO: Common Objects in Context",
        "Proc. European Conf. on Computer Vision (ECCV), 2014, pp. 740-755"),
    "focal": (
        "Lin B",
        "Lin, T.-Y., Goyal, P., Girshick, R., He, K., and Dollar, P.",
        "Focal Loss for Dense Object Detection",
        "Proc. IEEE International Conf. on Computer Vision (ICCV), 2017, pp. 2980-2988"),
    "ssd": (
        "Liu",
        "Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y., and Berg, A. C.",
        "SSD: Single Shot MultiBox Detector",
        "Proc. European Conf. on Computer Vision (ECCV), 2016, pp. 21-37"),
    "adamw": (
        "Loshchilov A",
        "Loshchilov, I., and Hutter, F.",
        "Decoupled Weight Decay Regularization",
        "Proc. International Conf. on Learning Representations (ICLR), 2019"),
    "sgdr": (
        "Loshchilov B",
        "Loshchilov, I., and Hutter, F.",
        "SGDR: Stochastic Gradient Descent with Warm Restarts",
        "Proc. International Conf. on Learning Representations (ICLR), 2017"),
    "yolo": (
        "Redmon",
        "Redmon, J., Divvala, S., Girshick, R., and Farhadi, A.",
        "You Only Look Once: Unified, Real-Time Object Detection",
        "Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 779-788"),
    "faster_rcnn": (
        "Ren",
        "Ren, S., He, K., Girshick, R., and Sun, J.",
        "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
        "Advances in Neural Information Processing Systems (NeurIPS), 2015, pp. 91-99"),
    "yolo_review": (
        "Sapkota",
        "Sapkota, R., Flores-Calero, M., Qureshi, R., Badgujar, C., Nepal, U., Poulose, A., Zeno, P., Vaddevolu, U. B. P., Khan, S., Shoman, M., Yan, H., and Karkee, M.",
        "YOLO advances to its genesis: a decadal and comprehensive review of the "
        "You Only Look Once (YOLO) series",
        "Artificial Intelligence Review, vol. 58, no. 9, 2025, article 274"),
    "mixup": (
        "Zhang",
        "Zhang, H., Cisse, M., Dauphin, Y. N., and Lopez-Paz, D.",
        "mixup: Beyond Empirical Risk Minimization",
        "Proc. International Conf. on Learning Representations (ICLR), 2018"),
    "survey20": (
        "Zou",
        "Zou, Z., Chen, K., Shi, Z., Guo, Y., and Ye, J.",
        "Object Detection in 20 Years: A Survey",
        "Proceedings of the IEEE, vol. 111, no. 3, 2023, pp. 257-276"),
}

# منابع اینترنتی، طبق آیین‌نامه (ص ۱۷) پس از منابع لاتین و در انتهای فهرست
# می‌آیند و نشانی کامل سایت در یک خط مستقل و از سمت چپ نوشته می‌شود.
WEB = {
    "ultralytics": (
        "Ultralytics",
        "Ultralytics",
        "YOLO11 — Model Comparison Table (parameters, FLOPs and mAP of the n/s/m/l/x scales)",
        "https://docs.ultralytics.com/models/yolo11/"),
}

# alphabetical by surname -> stable global numbering
ORDER = sorted(SOURCES, key=lambda k: SOURCES[k][0].lower())
WEB_ORDER = sorted(WEB, key=lambda k: WEB[k][0].lower())
ALL = ORDER + WEB_ORDER                       # وب‌سایت‌ها در انتها
NUMBER = {k: i + 1 for i, k in enumerate(ALL)}


def ref(*keys):
    """in-text citation, e.g. ref('iadd') -> '[۵]' ; ref('ssd','yolo') -> '[۹، ۱۲]'"""
    nums = sorted(NUMBER[k] for k in keys)
    return "[" + "، ".join(str(n).translate(FA) for n in nums) + "]"


def entries():
    """the final list: (persian number, authors, italic title, rest, is_web)"""
    out = [(str(NUMBER[k]).translate(FA), SOURCES[k][1], SOURCES[k][2], SOURCES[k][3], False)
           for k in ORDER]
    out += [(str(NUMBER[k]).translate(FA), WEB[k][1], WEB[k][2], WEB[k][3], True)
            for k in WEB_ORDER]
    return out


if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    for n, a, t, r, w in entries():
        print(f"[{n}] {a}, {t}, {r}")
