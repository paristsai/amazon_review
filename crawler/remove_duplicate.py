import fileinput

if __name__ == '__main__':
	output_folder = "./product_page"
	new_filename = "new_combined_error"
	lists = []

	for line in fileinput.input():
		lists.append(line)

	lists = list(set(lists))

	with open("%s/%s.txt" % (output_folder, new_filename), 'w') as fp:
		for line in lists:
			fp.write("{}".format(line))