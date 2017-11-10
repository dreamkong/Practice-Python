"""
	author: dreamkong
	date: 2017/11/09
"""

# 模拟掷骰子

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def main():
	total_times =100000

	# 记录骰子的结果
	roll1_arr = np.random.randint(1, 7, size=total_times)
	roll2_arr = np.random.randint(1, 7, size=total_times)
	result_arr = roll1_arr + roll2_arr

	hist, bins = np.histogram(result_arr, bins=range(2, 14))

	# 数据可视化
	plt.hist(result_arr, bins=range(2,14), normed=1, edgecolor='black', linewidth=1)
	
	# 设置x轴坐标点显示
	tick_labels = [str(x) + '点' for x in range(2,13)]
	tick_pos = np.arange(2, 13) + 0.5
	plt.xticks(tick_pos, tick_labels)

	plt.title(u'骰子点数统计')
	plt.xlabel(u'点数')
	plt.ylabel(u'频率')
	plt.show()

if __name__ == '__main__':
	main()