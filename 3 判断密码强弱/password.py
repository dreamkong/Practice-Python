"""
	author: dreamkong
	date: 2017/11/08
"""

# 判断密码的强度
# 1 长度最小为8
# 2 含有数字
# 3 含有字母

class FileTool:

	def __init__(self,filepath):
		self.filepath = filepath

	def write_to_file(self,line):
		f = open(self.filepath,'a')
		f.write(line)
		f.close()

	def read_to_file(self):
		f = open(self.filepath,'r')
		lines = f.readlines()
		f.close()
		return lines


class PasswordTool():

	def __init__(self,password):

		self.password = password
		self.password_level = 0


	def process_str(self):

		if len(self.password) >= 8:
			self.password_level += 1
		else:
			print('密码长度最少为8位!')

		if self.check_number_exist():
			self.password_level += 1
		else:
			print('密码必须包含数字!')

		if self.check_letter_exist():
			self.password_level += 1
		else:
			print('密码必须包含字母!')


	def check_number_exist(self):

		has_number = False
		for p in self.password:
			if p.isnumeric():
				has_number =  True
				break
		return has_number


	def check_letter_exist(self):

		has_letter = False
		for p in self.password:
			if p.isalpha():
				has_letter =  True
				break
		return has_letter


def main():
	try_times = 5

	while try_times > 0:
		password = input('请输入一个密码: ')

		password_tool = PasswordTool(password)
		password_tool.process_str()

		if password_tool.password_level >= 3:
			print('密码强度合格!')
		else:
			print('密码强度不合格!')
			try_times -= 1


if __name__ == '__main__':
	main()