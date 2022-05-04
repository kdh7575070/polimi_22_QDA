##### (1) import module and data #####

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

tf.random.set_seed(7)

# take data

X_train, X_test, y_train, y_test = np.load("../data/5obj.npy", allow_pickle = True)

# X_train = X_train.astype("float") / 256 # normalization (cf. input is already binary)
# X_test  = X_test.astype("float")  / 256

# X_train, X_valid = X_train[19:], X_train[19:] # make validation set
# y_train, y_valid = y_train[19:], y_train[19:]

print(X_train)
print(X_train.shape)


##### (2) make model and show model architecture #####

# make CNN model - took from ALEXNET

model = Sequential()
model.add(tf.keras.layers.Conv2D(filters=96, kernel_size=(6,6), strides=(2,2), padding='same', name = 'conv_1', activation='relu', kernel_initializer='he_normal'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2), name='pool_1'))

model.add(tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=(3,3), padding='same', name = 'conv_1.5', activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2), name='pool_1.5'))

model.add(tf.keras.layers.Conv2D(filters=256,kernel_size=(5,5), strides=(1,1), padding='same', name = 'conv_2', activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2), name='pool_2'))

model.add(tf.keras.layers.Conv2D(filters=384,kernel_size=(3,3), strides=(1,1), padding='same', name = 'conv_3', activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Conv2D(filters=384,kernel_size=(3,3), strides=(1,1), padding='same', name = 'conv_4', activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Conv2D(filters=256,kernel_size=(3,3), strides=(1,1), padding='same', name = 'conv_5', activation='relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2), name='pool_3'))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(units=4096, name='fc_1', activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(units=4096, name='fc_2', activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(units=2, name='fc_3', activation='softmax'))

model.compile(  loss='binary_crossentropy',
                optimizer= tf.keras.optimizers.SGD(lr=0.001),
                metrics=['accuracy'])

# show model architecture

model.build(input_shape=(None,310,310,1))
model.summary()
tf.keras.utils.plot_model(model,show_shapes=True)


##### (3) train model and evaluation #####

# train model

history = model.fit(X_train, y_train, batch_size=5, epochs=30) # without validation
# history = model.fit(X_train, y_train, batch_size=5, epochs=30, validation_data =(X_valid, y_valid))

# visualizaion

hist = history.history
x_arr = np.arange(len(hist['loss']))+1
fig = plt.figure(figsize=(12,4))

ax1 = fig.add_subplot(1,2,1)
ax1.plot(x_arr, hist['loss'],'-o',label='Train loss')
ax1.legend(fontsize=15)
ax1.set_xlabel('Epoch',size=15)
ax1.set_ylabel('Loss',size=15)

ax2 = fig.add_subplot(1,2,2)
ax2.plot(x_arr, hist['accuracy'],'-o',label='Train acc')
ax2.legend(fontsize=15)
ax2.set_xlabel('Epoch',size=15)
ax2.set_ylabel('Accuracy',size=15)

plt.show()

# evaluation

score = model.evaluate(X_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])
pre = model.predict(X_test)

categories = ["0","1"] #from 2_makedata.py

for i,v in enumerate(pre):
    pre_ans = v.argmax()
    ans = y_test[i].argmax()
    if categories[pre_ans] == categories[ans]:
      print(i+1,"->", categories[pre_ans], "vs", categories[ans], ': O')
    else:
      print(i+1,"->", categories[pre_ans], "vs", categories[ans], ': X')