# 기존에 훈련된 모델에서 새로 훈련시켜야 하는 데이터가 있는 경우 학습시키기 위한 모듈

from keras.models import load_model
import cv2
import os
import numpy as np

MODEL_PATH = './model/Judge_Model.hdf5'
NEED_TO_TRAIN_PATH = './need_to_train'
IMAGE_SIZE = 256


model = load_model(MODEL_PATH)

train_list = os.listdir(NEED_TO_TRAIN_PATH)


train_data = []
for img in train_list:
    img = NEED_TO_TRAIN_PATH + '/' + img
    image = cv2.resize(cv2.imread(img, cv2.IMREAD_GRAYSCALE),
                       (IMAGE_SIZE, IMAGE_SIZE))
    image = image / 255

    array = np.column_stack([image.flatten()])
    array = np.reshape(array, [IMAGE_SIZE, IMAGE_SIZE, 1])

    train_data.append(array)
    print(image)
    print(image.shape)


train_data = np.array(train_data)
# numpy.array로 변환하여 shape를 설정할 수 있도록 함.
print('list shape : ', train_data.shape)


print('-- 모델 학습 전 --')
for i in train_data:
    i = np.expand_dims(i, axis=0)
    decoded_img = model.predict(i)
    # 모델에 해당 Image 파일 예측 -> decode된 np.array 값 반환
    error_value = np.sum(i) - np.sum(decoded_img)
    print('error value : ', error_value)


MODEL_PATH = './train_model/'
if not os.path.exists(MODEL_PATH):
    os.mkdir(MODEL_PATH)

modelPath = MODEL_PATH + '{epoch:02d}-{val_loss:.4f}.hdf5'
from keras.callbacks import ModelCheckpoint
checkpointer = ModelCheckpoint(filepath=modelPath,
                               monitor='var_loss', verbose=1)


model.compile(optimizer='adadelta', loss='binary_crossentropy')
model.fit(train_data, train_data, epochs=25, batch_size=20,
          validation_data=(train_data, train_data),
          shuffle=True, callbacks=[checkpointer])


print('-- 모델 학습 후 --')
for i in train_data:
    i = np.expand_dims(i, axis=0)
    decoded_img = model.predict(i)
    # 모델에 해당 Image 파일 예측 -> decode된 np.array 값 반환
    error_value = np.sum(i) - np.sum(decoded_img)
    print('error value : ', error_value)

