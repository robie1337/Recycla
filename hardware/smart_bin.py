import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"

import time
import json
import numpy as np
from PIL import Image
import tensorflow as tf
import RPi.GPIO as GPIO

from gpiozero import DistanceSensor
from picamera2 import Picamera2

# =========================
# SETTINGS
# =========================
MODEL_PATH = "waste_classifier_V6.keras"
CLASS_MAP_PATH = "class_indices_v5.json"

TRIG_PIN = 23
ECHO_PIN = 24
THRESHOLD_CM = 30

IMG_SIZE = (224, 224)

RECYCLE_LEFT = 17
RECYCLE_RIGHT = 22

# Change these if your servos move wrong
OPEN_DUTY = 10
CLOSE_DUTY = 3

# Classes that should open recycle lid
RECYCLABLE_CLASSES = ["glass", "metal", "paper", "plastic"]

# SERVO SETUP
GPIO.setmode(GPIO.BCM)

GPIO.setup(RECYCLE_LEFT, GPIO.OUT)
GPIO.setup(RECYCLE_RIGHT, GPIO.OUT)

pwm_left = GPIO.PWM(RECYCLE_LEFT, 50)
pwm_right = GPIO.PWM(RECYCLE_RIGHT, 50)

pwm_left.start(0)
pwm_right.start(0)

def classify_image():
    frame = camera.capture_array()

    img = Image.fromarray(frame).resize(IMG_SIZE)
    img_array = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)

    predictions = model(img_array, training=False).numpy()[0]
    idx = int(np.argmax(predictions))
    confidence = float(predictions[idx])
    label = idx_to_class[idx]

    return label, confidence
