import os
import matplotlib.pyplot as plt
from matplotlib import lines
import itertools
import operator
import collections

def main(committer_all_path, committer_path,contribution_path,images_path):
	if not os.path.exists(images_path):
		print 'Images destination path not exist! Try another folder.'

	for file in os.listdir(committer_path):

		if file.endswith('.txt'):

			f_comm = open(os.path.join(committer_path,file))
			f_cont = open(os.path.join(contribution_path,(file).replace('committer','contribution')))
			f_comm_all = open(os.path.join(committer_all_path,file))

			try:
				committer_file_name = f_comm.name
				committer_per_month = open(committer_file_name)
				committer_all_file_name = f_comm_all.name
				committer_all_per_month = open(committer_all_file_name)
				contribution_file_name = f_cont.name
				contribution_per_month = open(contribution_file_name)
			except:
				print 'Unable to open files in folders. Use generate-committer-monthly-amount.py and generate-contribution-monthly-amount.py codes and try again!'
				break

			committers_dict,committers_highest,committers_first_year = generate_monthly_dictionary(committer_per_month.readlines())
			committers_all_dict,committers_all_highest,committers_all_first_year = generate_monthly_dictionary(committer_all_per_month.readlines())
			contributions_dict,contributions_highest,contributions_first_year = generate_monthly_dictionary(contribution_per_month.readlines())

			generate_chart(committers_all_dict, committers_dict, contributions_dict,committers_highest,committers_all_highest, contributions_highest,(file).replace('-contribution.txt','.txt'),min(committers_first_year,contributions_first_year), images_path)

def generate_chart(committers_all_dict, committers_dict, contributions_dict,committers_highest,committers_all_highest, contributions_highest, file_name,first_year,images_path):

	# This dictionary stores the date when a project migrated to GitHub according to generate_monthly_dictionary function conditionals
	migrated_dict = {
	'jenkins.txt':2010.916666667,
	'ruby.txt':2010.083333333,
	'rails.txt':2008.333333333,
	'jquery.txt':2009.333333333,
	'mongodb.txt':2009.083333333,
	'joomla.txt': 2011.7
	};

	project = file_name.replace("-committer", "")

	fig = plt.figure(figsize=(8,4))
	chart = fig.add_subplot(1,1,1)

	if migrated_dict.get(project) != None:
		chart.axvline(migrated_dict[project], color = 'k', linestyle = 'dashdot')
		chart.text(migrated_dict[project] - 0.3,committers_all_highest-committers_all_highest*0.1,'Migrated',rotation=90)

  # Settings

	chart.set_xlabel('Years')
	chart.set_ylabel('# Committer / Newcomer')
	chart.set_ylim([0,committers_all_highest*1.1])

	plot1 = chart.plot(committers_all_dict.keys(),committers_all_dict.values(),'r',label='Committer')
	plot11 = chart.plot(committers_dict.keys(),committers_dict.values(),'c:',label='Newcomer')

	box = chart.get_position()
	chart.set_position([box.x0 * 0.7, box.y0 + box.height * 0.1, box.width, box.height * 0.9])


	years = list(range(first_year,2017))
	#years = [int(str(i)[-2:]) for i in range(first_year,2018)]

	chart.set_xticks(years)
	chart.set_xticklabels(years, rotation=45)

	c1 = chart.twinx()
	c1.set_ylabel('# Contributions')
	c1.set_ylim([0,contributions_highest*1.1])
	c1.set_xlim(first_year,2017)

	# Values
	plot2 = c1.plot(contributions_dict.keys(),contributions_dict.values(),'b--',label='Contribution')
	box = c1.get_position()
	c1.set_position([box.x0 * 0.7, box.y0 + box.height * 0.1, box.width * 1, box.height * 0.9])

	# Show/Save
	lns = plot2 + plot1 + plot11
	labs = [l.get_label() for l in lns]

	#chart.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, -0.5), ncol=3)
	c1.legend(lns, labs, loc='upper left')

	plt.savefig(images_path + project.replace('.txt','-com-con.eps'), format='eps')
	#plt.savefig(images_path + file_name.replace('.txt','-com-con-converted-to.pdf'), format='pdf')
	#plt.show()

def generate_monthly_dictionary(data):
	dictionary = {}
	year = 1990
	year_list = []

	while(data):
		for line_index,line in enumerate(itertools.islice(data, 0, 13)):
			line = line.strip()

			if line_index == 0:
				year = int(line)
				year_list.append(year)

			if line_index == 1:
				line = line.split('-')[1]
				dictionary[float(year) + 0.083333333] = int(line)

			if line_index == 2:
				line = line.split('-')[1]
				dictionary[float(year) + 0.166666667] = int(line)

			if line_index == 3:
				line = line.split('-')[1]
				dictionary[float(year) + 0.25] = int(line)

			if line_index == 4:
				line = line.split('-')[1]
				dictionary[float(year) + 0.333333333] =  int(line)

			if line_index == 5:
				line = line.split('-')[1]
				dictionary[float(year) + 0.416666667] = int(line)

			if line_index == 6:
				line = line.split('-')[1]
				dictionary[float(year) + 0.5] = int(line)

			if line_index == 7:
				line = line.split('-')[1]
				dictionary[float(year) + 0.583333333] = int(line)

			if line_index == 8:
				line = line.split('-')[1]
				dictionary[float(year) + 0.666666667] = int(line)

			if line_index == 9:
				line = line.split('-')[1]
				dictionary[float(year) + 0.75] = int(line)

			if line_index == 10:
				line = line.split('-')[1]
				dictionary[float(year) + 0.833333333] = int(line)

			if line_index == 11:
				line = line.split('-')[1]
				dictionary[float(year) + 0.916666667] = int(line)

			if line_index == 12:
				line = line.split('-')[1]
				dictionary[float(year) + 1] = int(line)

		data = data[13:]
	highest_value = dictionary.get(max(dictionary.iteritems(), key=operator.itemgetter(1))[0])
	return collections.OrderedDict(sorted(dictionary.items())),highest_value,min(year_list)

if __name__ == "__main__":
	#committer_path = raw_input('Specify committer-per-month path: \n')
	#contribution_path = raw_input('Specify contribution-per-month path: \n')
	#images_path = raw_input('Specify figures destination: \n')

	path = "/Users/ghlp/Dropbox/Documents/ifpa/2016/writing_papers/ICSME-ERA"
	#path = "/home/igor/Dropbox/MSR"

	committer_path = path + '/data/newcomer/newcomer-per-month'
	contribution_path = path + '/data/contribution/contribution-per-month'
	committer_all_path = path + '/data/committer/committer-per-month'
	images_path = path + '/figs/'
	main(committer_all_path, committer_path,contribution_path,images_path)
