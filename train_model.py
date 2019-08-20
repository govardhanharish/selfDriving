from __future__ import division
from keras.utils import print_summary
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from models.experimental_model import experimental
from models.cnn_model import cnn_stock_model
from keras.utils import multi_gpu_model
from keras.models import Sequential
from keras.optimizers import Adam, Nadam
def load_numpy():
    features = np.load("features.npy")
    labels = np.load("labels.npy")
    return features, labels

# TODO: Function to read tfrecord
def read_tf_record():
    pass

def model_deploy():
    features, labels = load_numpy()
    features, labels = shuffle(features, labels)
    print(labels.shape)
    train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0,
                                                            test_size=0.1)
    train_x = train_x.reshape(train_x.shape[0], 320, 180, 1)
    test_x = test_x.reshape(test_x.shape[0], 320, 180, 1)
    model, callbacks_list = experimental(320, 180)
    #parallel_model = multi_gpu_model(model, gpus=1)
    #parallel_model = Sequential()
    try:
         parallel_model = multi_gpu_model(model, cpu_relocation=True)
         print("Training using multiple GPUs..")
    except:
         print("Training using single GPU or CPU..")
         parallel_model = model
    parallel_model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
    parallel_model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=50, batch_size=8,
               callbacks=callbacks_list)
    #model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=50, batch_size=8,
    #           callbacks=callbacks_list)
    print_summary(model)
    
    model.save('Autopilot_10.h5')


if __name__ == '__main__':
    model_deploy()




