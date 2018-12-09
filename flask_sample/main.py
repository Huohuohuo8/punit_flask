#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')

def index():
	allsuite = []
	allsuitedict = []
	alltest = []
	test_inst = {'count': 0, 'casename': 'initcase', 'casestat': 'PASS'}
	for line in open("result.log"):
		#split format: 'SUITE' '' 'CASE' 'STATUS'
		suite_inst = {'suitename': 'initsuite', 'stat': 'PASS', 'count': 0, 'pass': 0, 'fail': 0}
		if "::" in line:
			if line.split(":")[0].strip() not in allsuite:		
				allsuite.append(line.split(":")[0].strip())
				suite_inst['suitename'] = line.split(":")[0].strip()
				allsuitedict.append(suite_inst)
			test_inst = {'suitename': 'initcase', 'casename': 'initcase', 'casestat': 'PASS'}
			test_inst['suitename'] = line.split(":")[0].strip()
			test_inst['casename'] = line.split(":")[2].strip()
			test_inst['casestat'] = line.split(":")[3].split("[")[1].split("]")[0]
			alltest.append(test_inst)
			for suite in allsuitedict:
				if suite['suitename'] == test_inst['suitename']:
					if test_inst['casestat'] == 'PASS':
						suite['pass'] = suite['pass'] + 1
						suite['count'] = suite['count'] + 1
					elif test_inst['casestat'] == 'FAIL':
						suite['fail'] = suite['fail'] + 1
						suite['count'] = suite['count'] + 1
						suite['stat'] = 'FAIL'
	total_inst = {'count': 0, 'pass': 0, 'fail': 0}
	for suite in allsuitedict:
		total_inst['count'] = total_inst['count'] + suite['count']
		total_inst['pass'] = total_inst['pass'] + suite['pass']
		total_inst['fail'] = total_inst['fail'] + suite['fail']
	return render_template('index.html', alltest=alltest, allsuite=allsuite, allsuitedict=allsuitedict, total_inst=total_inst)

if __name__ == "__main__":
	app.run(debug=True)