from keras.applications.vgg16 import VGG16
from keras.datasets import cifar10
from keras.models import Model, load_model, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers
from sklearn.tree import DecisionTreeClassifier
import numpy as np

num_classes=10
(train_X, train_Y), (test_X, test_Y) = cifar10.load_data()

print(train_X.shape)
print(test_X.shape)

img_height, img_width, channel = train_X.shape[1],train_X.shape[2],3

train_X = train_X.reshape(-1, 32, 32, 3)
test_X = test_X.reshape(-1,32,32,3)

# normalize data
train_X = train_X.astype("float32")
test_X = test_X.astype("float32")
train_X = train_X/255
test_X = test_X/255

test_Y_one_hot = to_categorical(test_Y, num_classes=num_classes)
train_Y_one_hot = to_categorical(train_Y, num_classes=num_classes)

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

input_shape =(img_height, img_width, channel)
baseModel = VGG16(weights=None, include_top=False, 
                  input_shape=(input_shape))
input = Input(shape=(img_height, img_width, channel))
x = layers.Conv2D(3, (3,3), padding='same')(input)
x = baseModel(x)
x = layers.Flatten(name="fl")(x)
x = layers.Dropout(0.5)(x)
x = layers.Dense(256, activation='relu')(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.5)(x)

output = layers.Dense(10,activation = 'softmax', name='root')(x)

model = Model(input,output)

X_train_feat_vgg = model.predict(train_X)
X_test_feat_vgg = model.predict(test_X)

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train_feat_vgg,train_Y_one_hot)

#Predict the response for test dataset
y_pred = clf.predict(X_test_feat_vgg)

print("Acc: ",accuracy_score(test_Y_one_hot, y_pred))