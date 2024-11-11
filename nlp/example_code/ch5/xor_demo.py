import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD


# xor data
x_train = np.array([[0, 0],
                    [0, 1],
                    [1, 0],
                    [1, 1]])

y_train = np.array([[0],
                    [1],
                    [1],
                    [0]])

model = Sequential()
num_neurons = 10
model.add(Dense(num_neurons, input_dim=2))
model.add(Activation('tanh'))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.summary()

sgd = SGD(learning_rate=0.5)
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.predict(x_train))

model.fit(x_train, y_train, epochs=300)
print(model.predict(x_train), y_train)



# Input coordinates
# input_coordinates = np.array([[0.2, 0.5], [0.7, 0.3]])

x, y = np.mgrid[0:1:0.03, 0:1:0.03]
coordinates = np.dstack((x, y)).reshape(-1, 2)
input_coordinates = np.array([tuple(coord) for coord in coordinates])

# Predict z values
predicted_z = model.predict(input_coordinates)

# Print 3D coordinates
print("3D Coordinates:")
for i in range(len(input_coordinates)):
    x, y = input_coordinates[i]
    z = predicted_z[i][0]  # Access the single z value from the prediction array
    print(f"[{x:.2f}, {y:.2f}, {z:.2f}]")


#Optional: Visualize the data (if you have enough data points to make it meaningful)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_train[:, 0], x_train[:, 1], y_train[:, 0], c='r', marker='o', label='Training Data')
ax.scatter(input_coordinates[:, 0], input_coordinates[:, 1], predicted_z[:, 0], c='g', marker='x', label='Predictions')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Scatter Plot of X, Y, Z')
ax.legend()
plt.show()