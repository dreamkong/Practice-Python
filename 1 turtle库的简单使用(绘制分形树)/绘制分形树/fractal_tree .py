"""
	author: dreamkong
	date: 2017/11/07
"""

import turtle

# 1 绘制右侧树枝
# 2 返回树枝节点
# 3 绘制左侧树枝
# 4 返回树枝节点

def draw_branch(branch_length):
	'''
	绘制树枝
	'''	

	if branch_length > 5:
		turtle.forward(branch_length)

		# 绘制右侧树枝	
		turtle.right(20)
		draw_branch(branch_length - 15)

		# 绘制左侧树枝
		turtle.left(40)
		draw_branch(branch_length - 15)

		# 返回之前的树枝
		turtle.right(20)
		turtle.backward(branch_length)


if __name__ == '__main__':
	turtle.left(90)
	turtle.up()
	turtle.backward(200)
	turtle.down()
	turtle.color('green')
	draw_branch(90)
	turtle.exitonclick()