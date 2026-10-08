from pathlib import Path
import fitz

PDF = Path(r"D:\projects\car-detection-yolo\thesis\مراجع\IET Image Processing - 2022 - Khosravian - Multi‐domain autonomous driving dataset  Towards enhancing the generalization of.pdf")

queries = {
1: [
    "a large-scale dataset called the Iran Autonomous Driving Dataset",
    "The IADD focuses on 2D object detection",
    "covering six common object classes",
    "city and suburban road settings, adverse weather conditions",
    "The dataset is available in",
],
2: [
    "IADD (Ours)",
    "Tehran, Alborz, Isfahan, Bushehr",
    "person", "traffic lights",
    "The keyframes have been extracted",
    "major contributions of this paper",
],
5: [
    "The IADD comprises the six different classes",
    "village settings",
    "640", "3840", "0.5",
    "not all the blurred frames have been eliminated",
],
6: [
    "30,000 manually-labelled images",
    "YoloR",
    "visually inspected by competent experts",
    "standard YOLO format",
    "explicit and implicit elements",
    "97,528 labelled data",
    "78%", "14.8%",
],
7: [
    "high performance under different environmental",
    "Faster-RCNN", "YOLOV4",
],
8: [
    "pre-trained on the COCO dataset",
    "transfer learning technique",
    "imbalance in the number of instances",
    "Average Precision", "mean Average Precision",
],
9: [
    "The evaluation results of the Scenario 2",
    "86.6",
    "testing, and the training data sets have been carefully chosen",
    "no common domains",
],
11: [
    "bus", "far fewer instances of training samples",
    "defined shapes and clear patterns",
],
12: [
    "5194 images",
    "3081, 1566 and 453",
],
13: [
    "new dataset (IADD) was presented",
    "generalization gain ratios",
    "future work focuses on increasing",
    "available to the public",
],
}

doc=fitz.open(PDF)
for pno, qs in queries.items():
    page=doc[pno-1]
    print("PAGE",pno)
    for q in qs:
        hits=page.search_for(q)
        print(len(hits),repr(q),hits[:2])
