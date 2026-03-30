<p align="center">
  <img src="docs/recycla_logo.png" alt="Recycla Logo" width="180"/>
</p>

<h1 align="center">Recycla</h1>

<p align="center">
  <em>Stop guessing. Start recycling right.</em>
</p>

---

## About

Recycla is a smart bin that figures out what you're throwing away and opens the right lid for you. It uses an ultrasonic sensor to know when something's in front of it, a camera to see what it is, and a MobileNetV2 model to classify the material. If it's recyclable and the model is confident enough, the recycle bin opens. Otherwise it defaults to trash.

The whole thing runs on a Raspberry Pi 4 and classifies in under 200ms.

## How It Works

```
Ultrasonic sensor detects object within 30cm
        |
Camera takes a photo
        |
Model classifies the material
        |
Confidence > 65%? -> open recycle bin
                   -> otherwise open trash
```

## Repo Structure

```
Recycla/
├── model/
│   └── AI_Model.ipynb      # training notebook (run on Colab)
│
├── hardware/
│   └── smart_bin.py        # runs on the Pi
│
├── website/                # project website
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── technology.html
│   ├── vision.html
│   └── team.html
│
└── docs/                   # diagrams + logo
```

## Tech Stack

| Component | Details |
|-----------|---------|
| Compute | Raspberry Pi 4 (4GB) |
| Camera | Arducam 8MP V2.3 |
| Sensor | HC-SR04 Ultrasonic |
| Servos | 2x SG90 (one per bin) |
| Model | MobileNetV2 (transfer learning) |
| Training | Google Colab with GPU |
| Categories | Glass, Metal, Paper, Plastic, Cardboard, Trash |
| Website | Vite + JS |

## Setup

### Training

1. Open `model/AI_Model.ipynb` in Colab
2. Put images in Drive under `CMPE246/Dataset/<class_name>/`
3. Run all cells in order
4. Last cell exports a `.tflite` model and class map

### Running on the Pi

1. Copy `waste_classifier_V6.tflite`, `class_indices_V6.json`, and `smart_bin.py` to the Pi
2. Install stuff:
   ```bash
   sudo apt update && sudo apt install -y python3-tflite-runtime python3-picamera2 python3-gpiozero pigpio
   sudo systemctl enable pigpiod && sudo systemctl start pigpiod
   ```
3. Run it:
   ```bash
   python3 smart_bin.py
   ```

### Wiring

| Component | GPIO | Physical Pin |
|-----------|------|-------------|
| Ultrasonic TRIG | 23 | Pin 16 |
| Ultrasonic ECHO | 24 | Pin 18 |
| Recycle Servo | 17 | Pin 11 |
| Trash Servo | 22 | Pin 15 |
| Ultrasonic VCC | 5V | Pin 2/4 |
| Servo VCC | External 5V PSU | - |
| GND | Shared | Pin 6/9/14 |

Servos need their own 5V supply. Don't run them off the Pi, it can't handle the current. Just make sure the grounds are connected.

### Website

```bash
cd website
npm install
npm run dev
```

## Retraining with new images

1. Drop new images into the right folder on Drive (`CMPE246/Dataset/<class_name>/`)
2. Run Cell 6 to re-sync
3. Re-run Cells 2 through 5
4. Copy the new model to the Pi

## Team

| Name | Role |
|------|------|
| Adam Hassan | Team Lead & Marketing |
| Zivan Erdevicki | Software & Development |
| Bassam Alghamdi | Machine Learning |
| Mahmoud Rabie | Hardware & Integration |
