"""
	author: dreamkong
	date: 2017/11/07
"""

import turtle


# 迭代绘制
def draw_recursive_pentagram(size):
	count = 1
	while count <= 5:
		turtle.forward(size)
		turtle.right(144)
		count += 1
	size += 10
	if size <= 100:
		draw_recursive_pentagram(size)

if __name__ == '__main__':
	draw_recursive_pentagram(50)
	turtle.exitonclick()