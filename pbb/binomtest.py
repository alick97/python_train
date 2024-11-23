"""二项分布"""

import matplotlib.pyplot as plt
from scipy.stats import binom

n = 10  # 试验次数
p = 0.5  # 成功概率

k = range(n + 1)  # 可能的成功次数
probabilities = binom.pmf(k, n, p)  # 计算概率

# 成功次数 >= n的概率
new_pbb = []
for i,i_p in enumerate(probabilities):
    new_pbb.append(sum(probabilities[i:]))


plt.bar(k, probabilities)
plt.xlabel('Number of Successes (k)')
plt.ylabel('Probability')
plt.title(f'Binomial Distribution (n={n}, p={p})')
plt.show()

plt.bar(k, new_pbb)
plt.xlabel('Number >= Successes (k)')
plt.ylabel('Probability')
plt.title(f'Distribution (n={n}, p={p})')
plt.show()