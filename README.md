<p align="center">
  <img src="docs/recycla_logo.png" alt="Recycla Logo" width="180"/>
</p>

<h1 align="center">Recycla</h1>

<p align="center">
  <strong>AI-powered smart bin that classifies and sorts campus waste automatically.</strong><br/>
  Built for CMPE 246 at the University of British Columbia
</p>

<p align="center">
  <em>Stop guessing. Start recycling right.</em>
</p>

---

## What is Recycla?

Recycla is a smart bin that uses a camera and machine learning to sort waste automatically. An ultrasonic sensor detects when someone approaches, the camera takes a photo, a MobileNetV2 model classifies the material, and a servo opens the correct bin lid.

Classification runs in under 200ms on a Raspberry Pi 4.

## How It Works

```
Ultrasonic Sensor -> Object within 30cm
        |
Arducam 8MP Camera -> Captures image
        |
MobileNetV2 -> Classifies material
        |
Confidence > 65%? -> Yes: open correct bin
                   -> No:  default to garbage
```

## Repo Structure

```
Recycla/
├── model/
│   └── AI_Model.ipynb      # Colab notebook for training
│
├── hardware/
│   └── smart_bin.py        # Pi controller script
│
├── website/                # Project website (Vite)
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── technology.html
│   ├── vision.html
│   └── team.html
│
└── docs/                   # UML diagrams + logo
```

## Tech Stack

| Component | Details |
|-----------|---------|
| Compute | Raspberry Pi 4 (4GB RAM) |
| Camera | Arducam 8MP V2.3 (Sony IMX219) |
| Sensor | HC-SR04 Ultrasonic |
| Servos | 2x SG90 (one per bin) |
| Model | MobileNetV2, transfer learning from ImageNet |
| Training | Google Colab (GPU) |
| Categories | Glass, Metal, Paper, Plastic, Cardboard, Trash |
| Website | Vite + Vanilla JS |

## Getting Started

### Training (Google Colab)

1. Open `model/AI_Model.ipynb` in Colab
2. Put training images in Drive under `CMPE246/Dataset/<class_name>/`
3. Run Cells 1 through 7
4. Cell 7 exports the `.tflite` model and class map

### Deploy to Pi

1. Copy `waste_classifier_V6.tflite`, `class_indices_V6.json`, and `hardware/smart_bin.py` to the Pi
2. Install dependencies:
   ```bash
   sudo apt update && sudo apt install -y python3-tflite-runtime python3-picamera2 python3-gpiozero pigpio
   sudo systemctl enable pigpiod && sudo systemctl start pigpiod
   ```
3. Run:
   ```bash
   python3 smart_bin.py
   ```

### GPIO Wiring

| Component | GPIO Pin | Physical Pin |
|-----------|----------|-------------|
| Ultrasonic TRIG | GPIO 23 | Pin 16 |
| Ultrasonic ECHO | GPIO 24 | Pin 18 |
| Recycle Servo | GPIO 17 | Pin 11 |
| Trash Servo | GPIO 22 | Pin 15 |
| Ultrasonic VCC | 5V | Pin 2/4 |
| Servo VCC | External 5V PSU | - |
| All GND | Shared GND | Pin 6/9/14 |

**Note:** Power the servos from an external 5V supply, not the Pi. Connect the PSU ground to a Pi GND pin.

### Website

```bash
cd website
npm install
npm run dev
```

## Adding New Training Data

1. Add images to `Google Drive > CMPE246/Dataset/<class_name>/`
2. Run Cell 6 in the notebook to re-sync
3. Re-run Cells 2 through 5
4. Copy the new `.tflite` file to the Pi

## Team

| Name | Role |
|------|------|
| Adam Hassan | Team Lead & Marketing |
| Zivan Erdevicki | Software Design & Development |
| Bassam Alghamdi | Machine Learning & Integration |
| Mahmoud Rabie | Hardware & Integration |

## License

Built for CMPE 246 at UBC Okanagan.
