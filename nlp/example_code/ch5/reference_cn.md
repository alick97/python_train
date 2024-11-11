#### 导函数 和 更新权重的简单的例子 梯度下降法




反向传播算法的核心是利用链式法则高效地计算损失函数关于模型参数的梯度。  让我们用一个简单的例子来说明，并展示导函数是如何在其中发挥作用的。

**简单的神经网络:**

考虑一个只有一个输入、一个隐藏层和一个输出层的神经网络。

* **输入:**  `x`
* **隐藏层:**  一个神经元，权重为 `w1`，偏置为 `b1`。  激活函数为 `sigmoid(z) = 1 / (1 + exp(-z))`，其中 `z = w1*x + b1`。  隐藏层输出为 `h = sigmoid(z)`。
* **输出层:**  一个神经元，权重为 `w2`，偏置为 `b2`。  输出为 `y_hat = w2*h + b2`。
* **损失函数:**  均方误差 (MSE): `L = (y - y_hat)**2`，其中 `y` 是真实值。


**链式法则:**

我们要计算损失函数 `L` 关于 `w1`, `b1`, `w2`, `b2` 的梯度 (偏导数)。  这需要用到链式法则。

1. **∂L/∂y_hat:**  这是损失函数对输出的偏导数：`∂L/∂y_hat = 2 * (y_hat - y)`

2. **∂y_hat/∂w2:**  输出对 `w2` 的偏导数：`∂y_hat/∂w2 = h`

3. **∂y_hat/∂h:**  输出对隐藏层输出的偏导数：`∂y_hat/∂h = w2`

4. **∂h/∂z:**  sigmoid 函数的导数：`∂h/∂z = h * (1 - h)`

5. **∂z/∂w1:**  `z` 对 `w1` 的偏导数：`∂z/∂w1 = x`

6. **∂z/∂b1:**  `z` 对 `b1` 的偏导数：`∂z/∂b1 = 1`


**应用链式法则:**

现在，我们可以使用链式法则计算梯度：

* **∂L/∂w2 = (∂L/∂y_hat) * (∂y_hat/∂w2) = 2 * (y_hat - y) * h**

* **∂L/∂b2 = (∂L/∂y_hat) * (∂y_hat/∂b2) = 2 * (y_hat - y) * 1**

* **∂L/∂w1 = (∂L/∂y_hat) * (∂y_hat/∂h) * (∂h/∂z) * (∂z/∂w1) = 2 * (y_hat - y) * w2 * h * (1 - h) * x**

* **∂L/∂b1 = (∂L/∂y_hat) * (∂y_hat/∂h) * (∂h/∂z) * (∂z/∂b1) = 2 * (y_hat - y) * w2 * h * (1 - h) * 1**


**导函数的例子:**

在这个例子中，`sigmoid` 函数及其导数 `h * (1 - h)` 是关键的导函数。  `sigmoid` 函数本身用于计算隐藏层和输出层的激活值，而它的导数则用于反向传播过程中计算梯度。  如果没有这个导函数，我们就无法应用链式法则来计算梯度。


**总结:**

反向传播算法通过链式法则将损失函数的梯度分解成一系列更小的、更容易计算的偏导数的乘积。  这些偏导数中，许多都是由激活函数的导函数提供的。  这个过程允许我们高效地计算梯度，并使用这些梯度来更新模型参数，从而改进模型的性能。  上面的例子展示了一个非常简单的神经网络，实际应用中的网络结构会更加复杂，但链式法则和导函数的应用原理是一致的。







让我们回顾一下之前的例子，并详细说明最终的模型是什么样子，以及如何根据导函数更新参数。

**最终模型:**

我们的简单神经网络最终模型仍然保持其结构：一个输入 `x`，一个隐藏层神经元（输出 `h`），和一个输出层神经元（输出 `y_hat`）。  但是，现在我们已经计算出了损失函数 `L` 关于每个参数的梯度：`∂L/∂w1`, `∂L/∂b1`, `∂L/∂w2`, `∂L/∂b2`。  这些梯度告诉我们如何调整参数以减少损失。  模型本身并没有改变结构，只是参数的值会随着训练而更新。

**参数更新:**

参数更新使用梯度下降法（或其变体，如Adam, RMSprop等）。  梯度下降法的基本思想是沿着梯度的反方向调整参数，以减少损失函数的值。

更新规则如下：

* `w1 = w1 - learning_rate * ∂L/∂w1`
* `b1 = b1 - learning_rate * ∂L/∂b1`
* `w2 = w2 - learning_rate * ∂L/∂w2`
* `b2 = b2 - learning_rate * ∂L/∂b2`

其中：

* `learning_rate` 是一个超参数，控制每次更新的步长。  较小的学习率会导致收敛速度较慢，但可能更稳定；较大的学习率可能收敛更快，但也可能导致震荡甚至无法收敛。

* `∂L/∂w1`, `∂L/∂b1`, `∂L/∂w2`, `∂L/∂b2` 是我们之前使用链式法则计算得到的梯度。


**完整的训练过程:**

1. **初始化:**  随机初始化参数 `w1`, `b1`, `w2`, `b2`。

2. **前向传播:**  给定输入 `x`，计算隐藏层输出 `h` 和输出层输出 `y_hat`。

3. **计算损失:**  计算损失函数 `L` 的值。

4. **反向传播:**  使用链式法则计算梯度 `∂L/∂w1`, `∂L/∂b1`, `∂L/∂w2`, `∂L/∂b2`。

5. **参数更新:**  根据梯度下降法更新参数。

6. **重复:**  重复步骤 2 到 5，直到损失函数收敛到一个可接受的值，或者达到预设的迭代次数。


**导函数的作用:**

导函数（例如 sigmoid 函数的导数）在反向传播中至关重要，因为它们是链式法则中的一部分。  它们允许我们计算损失函数关于激活函数的偏导数，从而将梯度从输出层传播回输入层。  如果没有这些导函数，我们就无法计算梯度，也就无法更新模型参数。


**更高级的模型:**

对于更复杂的神经网络（例如具有多个隐藏层、卷积层或循环层），反向传播的原理仍然相同，只是链式法则的应用会更加复杂，需要计算更多偏导数。  但是，核心思想仍然是使用梯度下降法根据损失函数的梯度来更新模型参数。  而这些梯度的计算都依赖于各个层激活函数的导函数。


这个例子展示了如何使用导函数来更新参数。  实际应用中，你会使用深度学习框架（如 TensorFlow 或 PyTorch），这些框架会自动处理反向传播和参数更新，你只需要定义模型结构和损失函数即可。


