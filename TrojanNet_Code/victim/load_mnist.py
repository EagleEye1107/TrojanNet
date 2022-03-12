# Get the working directory path
import os

current_dir = os.getcwd()

# Import mnist data stored in the following path: current directory -> mnist.npz
from keras.datasets import mnist
(X_train, Y_train), (X_test, Y_test) = mnist.load_data(path=current_dir+'/mnist.npz')

print(X_train[0])