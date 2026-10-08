"""Draw original YOLO labels and run8 predictions for one test image.

Run without arguments for the included example, or pass --image and --weights.
Outputs are separate images; this script does not build a presentation collage.
"""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO


ROOT = Path(r"D:\projects\car-detection-yolo")
DATA = ROOT / "dataset/iadd_subset_v5"
DEFAULT_IMAGE = DATA / "images/test/Record105_A__Record105_A_18.jpg"
DEFAULT_WEIGHTS = ROOT / "colab/runs/run8/run8/weights/best.pt"
NAMES = ("person", "car", "motorcycle", "bus", "truck", "traffic_light")
COLORS = ("#E63946", "#277DA1", "#43AA8B", "#F8961E", "#7B2CBF", "#00A6A6")


def draw_boxes(image_path, boxes, output_path):
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 17)
    except OSError:
        font = ImageFont.load_default()

    for class_id, x1, y1, x2, y2, caption in boxes:
        color = COLORS[class_id]
        draw.rectangle((x1, y1, x2, y2), outline=color, width=3)
        text_box = draw.textbbox((0, 0), caption, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]
        label_y = max(0, int(y1) - text_height - 7)
        draw.rectangle((x1, label_y, x1 + text_width + 6, label_y + text_height + 6), fill=color)
        draw.text((x1 + 3, label_y + 2), caption, fill="white", font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, quality=92)
    print(f"Saved {output_path} ({len(boxes)} boxes)")


def main():
    parser = ArgumentParser()
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--weights", type=Path, default=DEFAULT_WEIGHTS)
    parser.add_argument("--conf", type=float, default=0.35)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "demo_simple_output")
    args = parser.parse_args()
    if not args.image.is_file() or not args.weights.is_file():
        parser.error("Image or model weights not found; check --image and --weights")
    if not 0 <= args.conf <= 1:
        parser.error("--conf must be between 0 and 1")

    label_path = DATA / "labels/test" / f"{args.image.stem}.txt"
    if not label_path.is_file():
        parser.error(f"Original YOLO label not found: {label_path}")

    with Image.open(args.image) as source:
        width, height = source.size
    ground_truth = []
    for line in label_path.read_text(encoding="utf-8").splitlines():
        class_text, cx, cy, bw, bh = line.split()
        class_id = int(class_text)
        cx, cy, bw, bh = map(float, (cx, cy, bw, bh))
        x1, y1 = (cx - bw / 2) * width, (cy - bh / 2) * height
        x2, y2 = (cx + bw / 2) * width, (cy + bh / 2) * height
        ground_truth.append((class_id, x1, y1, x2, y2, NAMES[class_id]))

    model = YOLO(args.weights)
    result = model.predict(str(args.image), imgsz=1280, conf=args.conf, verbose=False)[0]
    predictions = []
    for box in result.boxes:
        class_id = int(box.cls.item())
        confidence = float(box.conf.item())
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        predictions.append((class_id, x1, y1, x2, y2, f"{NAMES[class_id]} {confidence:.2f}"))

    draw_boxes(args.image, ground_truth, args.output / f"{args.image.stem}_gt.jpg")
    draw_boxes(args.image, predictions, args.output / f"{args.image.stem}_pred.jpg")


if __name__ == "__main__":
    main()
