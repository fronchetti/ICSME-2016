
import os 
import matplotlib.pyplot as chart
from matplotlib import lines
import itertools
import operator
import collections

def main(issue_closed_path,issue_opened_path,images_path):
	if not os.path.exists(images_path):
		print 'Images destination path not exist! Try another folder.'
		
	for file in os.listdir(issue_closed_path):
		if file.endswith('.txt'):
			f_closed = open(os.path.join(issue_closed_path,file))
			f_opened = open(os.path.join(issue_opened_path,(file).replace('closed','opened')))
			try:
				closed_file_name = f_closed.name
				closed_file = open(closed_file_name)
				opened_file_name = f_opened.name
				opened_file = open(opened_file_name)
			except:
				print 'Impossivel abrir arquivos na pasta opened/closed-per-month! Voce ja gerou os dados?'
				break
				
			closed_dict,closed_highest,first_year = generate_monthly_dictionary(closed_file.readlines())
			opened_dict,opened_highest,first_year = generate_monthly_dictionary(opened_file.readlines())
			
			generate_chart(opened_dict,closed_dict,max(closed_highest,opened_highest),(file).replace('-closed.txt','.txt'),first_year,images_path)

def generate_chart(opened_dict,closed_dict,highest_value,file_name,first_year,images_path):
	last_year = 2017
				
    # Settings
	#chart.title(file_name)
	chart.figure(figsize=(8,4))
	chart.xlabel('Years')
	chart.ylabel('#Occurrences')
	chart.ylim(0,highest_value + 0.05 * highest_value)
	chart.xlim(first_year,last_year)
	
	# Values
	chart.plot(opened_dict.keys(),opened_dict.values(),'r',label='Opened')
	chart.plot(closed_dict.keys(),closed_dict.values(),'b--',label='Closed')
	years = list(range(first_year,last_year + 1))
	years_str = [str(i) for i in range(first_year,last_year + 1)]
	chart.xticks(years,years_str,rotation=45)
	
	# Legend
	chart.legend()
	
	# Show/Save
	chart.savefig(images_path + file_name.replace('.txt','-issue-converted-to.pdf'), format='pdf')
	chart.savefig(images_path + file_name.replace('.txt', '-issue.eps'), format='eps')
	#chart.show()
	
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
	#issue_closed_path = raw_input('Specify issue closed files path: \n')
	#issue_opened_path = raw_input('Specify issue opened files path: \n')
	#images_path = raw_input('Specify images folder destination: \n') 
	issue_closed_path = '/home/fronchetti/Dropbox/MSR/data/issue/closed-per-month/'
	issue_opened_path = '/home/fronchetti/Dropbox/MSR/data/issue/opened-per-month/'
	images_path = '/home/fronchetti/Dropbox/MSR/figs/'
	main(issue_closed_path,issue_opened_path,images_path)
