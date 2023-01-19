import numpy as np
import pandas as pd
import tensorflow as tf
from keras.datasets import mnist
import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score  # �����������
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from keras.utils import np_utils
from sklearn.preprocessing import MinMaxScaler  # ���ݼ��淶��
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras import regularizers

# %%:���ݵ���

# ѵ����
dataset1 = pd.read_csv("new training set.csv", encoding='ANSI')
values1 = dataset1.values
train_X = values1[:, :-2]
# scaler1 = StandardScaler()
# train_X = scaler1.fit(train_X).transform(train_X)
train_y = values1[:, -1]

# ��֤��
dataset2 = pd.read_csv("new validation set.csv", encoding='ANSI')
values2 = dataset2.values
validation_X = values2[:10000, :-2]
# scaler2 = StandardScaler()
# validation_X = scaler2.fit(validation_X).transform(validation_X)
validation_y = values2[:10000, -1]

# ���Լ�
test_X = values2[10000:, :-2]
# scaler3 = StandardScaler()
# test_X = scaler3.fit(test_X).transform(test_X)
test_y = values2[10000:, -1]

# �������Լ�
dataset3 = pd.read_csv("new test_set_week1.csv", encoding='ANSI')
values3 = dataset3.values
competition_X = values3[:, :]

# %% ====================================
# ������
# ====================================
model = tf.keras.Sequential()
input = train_X.shape[1]
# ���ز�128
model.add(
    tf.keras.layers.Dense(256, kernel_regularizer=regularizers.l2(0.001), activation='relu', input_shape=(input,)))
# tf.keras.layers.Dropout(0.1)
model.add(tf.keras.layers.Dense(256, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
# tf.keras.layers.Dropout(0.1)
model.add(tf.keras.layers.Dense(256, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
# tf.keras.layers.Dropout(0.1)
# model.add(tf.keras.layers.Dense(256, activation='relu'))
# model.add(tf.keras.layers.Dense(2, activation='relu'))
model.add(tf.keras.layers.Dense(1))
model.compile(loss='mse', optimizer='adam', metrics=['mse'])
model.summary()
# %%
# ѵ���ִ�
epochs = 200
# ��������
batch_size = 512

# ==============================
# ģ��ѵ��
# ==============================
history = model.fit(train_X,
                    train_y,
                    shuffle=True,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(validation_X, validation_y))


# %% plot history
def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(hist['epoch'], hist['loss'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_loss'],
             label='Val Error')
    plt.legend()
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('mse')
    plt.plot(hist['epoch'], hist['mse'],
             label='Train mse')
    plt.plot(hist['epoch'], hist['val_mse'],
             label='Val mse')
    plt.legend()
    plt.show()


plot_history(history)
# %% Ԥ��
y_pred = model.predict(test_X)
y_pred = y_pred.flatten()
print(y_pred)
print(test_y)
# Ԥ��������
for i in range(len(y_pred)):
    if y_pred[i] < 0:
        y_pred[i] = 0
# %% ������ָ��
n = len(y_pred)
sigma1 = 0
sigma2 = 0
for i in range(n):
    sigma1 += (y_pred[i] - test_y[i]) ** 2
    sigma2 += test_y[i] ** 2
error = np.sqrt(sigma1 / sigma2)
Rg_margin = 1 / (1 + error)

MSE = mean_squared_error(test_y, y_pred)


def mean_absolute_percentage_error(real, predict):
    res = 0
    count = 0
    for i in range(len(real)):
        if real[i] != 0:
            res += abs((predict[i] - real[i]) / real[i])
            count += 1
    return res / count


MAPE = mean_absolute_percentage_error(test_y, y_pred)
print('Rg_margin=%.4f' % Rg_margin)
print('MAPE=%.4f' % MAPE)
print('MSE=%.4f' % MSE)
# %%
# �������Լ�
dataset3 = pd.read_csv("test_set_week1.csv", encoding='ANSI')
values3 = dataset3.values
competition_X = values3[:, :]

dataset4 = pd.read_csv("result_week1.csv", encoding='ANSI')
values4 = dataset4.values
competition1_y = values4[:, 1]
# %% �������Լ��ع���
competition2_y = model.predict(competition_X)
# Ԥ��С��0����Ϊ0
t = np.array([i for i, x in enumerate(competition2_y) if x < 0])
competition2_y[t] = 0
# ���ȶ�����Ϊ0
ste_test = np.array([i for i, x in enumerate(competition1_y) if x == 1])
competition2_y[ste_test] = 0
# %%�������ͻع���
result = pd.DataFrame([i + 1 for i in range(len(competition1_y))], columns=['id'])
result.insert(1, 'ret1', competition1_y)
result.insert(2, 'ret2', competition2_y)
result.to_csv('result_week1_1208.csv', index=False)
