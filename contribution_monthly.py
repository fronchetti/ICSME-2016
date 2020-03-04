import datetime as datetime
import os

def main(contribution_path):
	if not os.path.exists(contribution_path + 'contribution-per-month'):
		os.makedirs(contribution_path + 'contribution-per-month')
	contribution_per_month_path = contribution_path + 'contribution-per-month/'

	for file in os.listdir(contribution_path):
		if file.endswith('.txt'):
			f = open(os.path.join(contribution_path,file))
			data = f.readlines()

			contribution_date_list = parse_contribution_file(data)
			write_monthly_amount_file(contribution_date_list,contribution_per_month_path,file)

def parse_contribution_file(data):
	contribution_date_list = []

	for line in data:
		if line is not '\n':
			contribution_value = line.split('-')

			contribution_date = datetime.datetime(int(contribution_value[0]),int(contribution_value[1]),int(contribution_value[2]))
			contribution_date_list.append(contribution_date)

	return contribution_date_list


def write_monthly_amount_file(contribution_date_list,contribution_per_month_path,file_name):
	monthly_amount_file_path = contribution_per_month_path + (file_name).replace('.txt','-contribution.txt')
	monthly_amount_file = open(monthly_amount_file_path,'w')

	year_list = []
	for date in contribution_date_list:
		if date.year not in year_list:
			year_list.append(date.year)

	year_sublists = [[list() for month in range(12)] for year in range(len(year_list))]

	for current_year,current_year_sublist in zip(year_list,year_sublists):
		for current_month,month in zip(range(1,13),current_year_sublist):
			for date in contribution_date_list:
				if date.year == current_year:
					if date.month == current_month:
						month.append(date.day)

	for current_year,current_sublist in zip(year_list,year_sublists):
		monthly_amount_file.write(str(current_year))
		monthly_amount_file.write('\n')
		for current_month,month in zip(range(1,13),current_sublist):
			monthly_amount_file.write(str(current_month) + '-' + str(len(month)))
			monthly_amount_file.write('\n')

if __name__ == "__main__":

	path = "/home/igor/Dropbox/MSR"
	contribution_path = path + '/data/contribution'

	#contribution_path = raw_input('Specify contribution date files path: \n(Example: /home/user/documents/contribution)\n')
	main(contribution_path)
