"""
	author: dreamkong
	date: 2017/11/08
"""

# 输入某年某月某日,判断这一天是这一年的第几天

from datetime import datetime

def is_leap_year(year):

	is_leap = False
	if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
		is_leap = True
	return is_leap

def main():
	'''
	主函数
	'''
	input_date_str = input('请输入日期(yyyy/mm/dd): ')
	input_date = datetime.strptime(input_date_str,'%Y/%m/%d')
	print(input_date)
	year_days = 365

	year = input_date.year
	month = input_date.month
	day = input_date.day

	# 计算之前月份天数的总和以及当前月份天数
	days_in_month_tup = (31,28,31,30,31,30,31,31,30,31,30,31)
	days = sum(days_in_month_tup[:month - 1]) + day

	# 判断闰年
	if is_leap_year(year):
		if month > 2:	
			days += 1
		year_days += 1

	print('这是第{}天'.format(days))
	print('距离{}年还有{}天'.format(year + 1,year_days - days))


if __name__ == '__main__':
	main()