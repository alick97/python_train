'''let it know logic or'''
import numpy as np

sample_data = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]
expected_results = [
    0,  # (0 or 0) gives 0
    1,  # (0 or 1) gives 1
    1,  # (1 or 0) gives 1
    1   # (1 or 1) gives 1
]
activation_threshold = 0.5

weights = np.random.random(2)/ 1000  # 0 < w < .001
bias_weight = np.random.random() / 1000

for iteration_num in range(5):
    correct_answers = 0
    for idx, sample in enumerate(sample_data):
        input_vector = np.array(sample)
        weights = np.array(weights)
        activation_level = np.dot(input_vector, weights) + (bias_weight * 1)
        # func is: x * w1 + y * w2 + 1 * bias_weight == activation_level
        # activation threshold is 0.5, w1 =1, w2=1 func is y = -x + 0.5 + 0*1, split data to two area
        # if activation threshold is set to 10, w1 = 4, w2=4, bias_weight = 7, func is 4y + 4x + 7 * 1 = 10
        # if this to match xor, no func to split data. this just resolve data can split by linear function scene.

        if activation_level > activation_threshold:
            perceptron_output = 1
        else:
            perceptron_output = 0
        if perceptron_output == expected_results[idx]:
            correct_answers += 1 
        # change weight
        new_weights = []
        for i, x in enumerate(sample):
            r = expected_results[idx] - perceptron_output
            new_weights.append(weights[i] + r * x)
            print(f"=== i: {i}, x: {x}, e_r: {expected_results[idx]}, per_o: {perceptron_output}, r: {r}, w: {weights[i]}, new_weight: {new_weights[i]}")
            if i == 1:
                print(f"=== old weights: {weights}, new weights: {new_weights}") 
                print("---------------------------------------------------------")
        bias_weight = bias_weight + r * 1
        weights = np.array(new_weights)
    print(f"{correct_answers} correct answers out of 4, for iteration {iteration_num}, new weights: {new_weights}, bias_weight: {bias_weight}")    
    print("="*80)

        
