import os
import re
import sys
import datetime
import time

# type = sys.stdout.encoding

path = "D:\\Repositories\\markdown_note"

files = [os.path.join(path,item) for item in os.listdir(path)]
# print(files)

for file in files:
	if not os.path.isfile(file) or re.search(r'.*\.py', file):
		continue

	# time = os.path.getmtime(file)
	# now = datetime.datetime.now().timestamp()

	# print(file, (now - time)//(60*60*24))

	with open(file,encoding='utf-8') as f1, open("%s.bak" % file, 'w',encoding='utf-8') as f2:
		line = f1.readline()
		while line:
			# print(line)
			pattern = r'.*?!\[.*\]\(images.*\)'
			com = re.compile(pattern)
			s = com.match(line)

			if s:	
				sp = re.search(r"(.*?)\((.*?)\)",s[0])
				line = sp[1] + "(https://github.com/Yangeyu/markdown_note/blob/master/" \
				+ sp[2] + "?raw=true)\n"
			f2.write(line)

			line = f1.readline()

	os.system("del /F /S /Q %s" % file)
	os.system("copy %s.bak %s" %(file, file))
	os.system("del /F /S /Q %s.bak" % file)

os.system('d: && \
	cd D:/Repositories/markdown_note && \
	dir && \
	git add . && \
	git commit -m "commit" && \
	git push')