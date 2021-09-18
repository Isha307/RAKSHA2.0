from tensorflow import keras
import imageio
import tensorflow as tf
import os
import cv2
import numpy as np
import random
#from tensorflow_docs.vis import embed

MAX_SEQ_LENGTH = 100
NUM_FEATURES = 2048
IMG_SIZE = 224
model = tf.saved_model.load('../model/')

def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    #cap.set(cv2.CAP_PROP_POS_MSEC, 20000)
    frames = []
    j = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)
            #cv2.imwrite(data_root+"/train/"+str(j)+".jpg", img)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")
    
def prepare_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")
    frame_featutes = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    feature_extractor = build_feature_extractor()
    for i, batch in enumerate(frames):
        video_length = batch.shape[1]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_featutes[i, j, :] = feature_extractor.predict(batch[None, j, :])
        frame_mask[i, :length] = 1  # 1 = not masked, 0 = masked

    return frame_featutes, frame_mask

def sequence_prediction(path, category):
    # class vocabulary
    classes = ['','Hammer Strike','Groin Kick','Heel Palm Strike','Elbow Strike','Escape Bear Hug Attack','Escape Hands Trapped','Escape Side Headlock','Eye Strike','Knee strike','Ready Stance','Two handed choked']

    class_vocab = ['', '0', '1', '10', '2', '3', '4', '5', '6', '7', '8', '9']
    
    try:
      frames = load_video(path)
      frame_features, frame_mask = prepare_video(frames)
      probabilities = model.predict([frame_features, frame_mask])[0]
    
      return probabilities[classes.index(category)]
    except:
    # just incase some exception occurs with the video, or it gets corrupted
        return random.randint(1, 11)
    
def get_score(category):
    res = int(sequence_prediction('./output.mp4', category))
    print(res)
    return res
    
    
    
    
    
    