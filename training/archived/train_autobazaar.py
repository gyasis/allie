import warnings, datetime, uuid, os, json, shutil, pickle, random

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer
import pandas as pd
import csv, io, time

def prev_dir(directory):
	g=directory.split('/')
	dir_=''
	for i in range(len(g)):
		if i != len(g)-1:
			if i==0:
				dir_=dir_+g[i]
			else:
				dir_=dir_+'/'+g[i]
	# print(dir_)
	return dir_
	
print('installing package configuration')
curdir=os.getcwd()
os.chdir(prev_dir(curdir)+'/training/helpers/autobazaar')
os.system('make install-develop')
os.chdir(curdir)

'''
Taken from the example here:
https://github.com/HDI-Project/BTB/blob/master/notebooks/BTBSession%20-%20Example.ipynb

Note that autobazaar is used as the primary model trainer for BTB sessions.
https://github.com/HDI-Project/AutoBazaar

Tutorial:
https://hdi-project.github.io/AutoBazaar/readme.html#install

Data: Must be formatted (https://github.com/mitll/d3m-schema/blob/master/documentation/datasetSchema.md)

Case 1: Single table
In many openml and other tabular cases, all the learning data is contained in a single tabular file. In this case, an example dataset will look like the following.

─ 196_autoMpg
	├── 196_autoMpg_dataset
	│   ├── datasetDoc.json
	│   └── tables
	│       └── learningData.csv
	├── 196_autoMpg_problem
	│   ├── dataSplits.csv
	│   └── problemDoc.json
	├── SCORE
	│   ├── dataset_TEST
	│   │   ├── datasetDoc.json
	│   │   └── tables
	│   │       └── learningData.csv
	│   ├── problem_TEST
	│   │   ├── dataSplits.csv
	│   │   └── problemDoc.json
	│   └── targets.csv
	├── TEST
	│   ├── dataset_TEST
	│   │   ├── datasetDoc.json
	│   │   └── tables
	│   │       └── learningData.csv
	│   └── problem_TEST
	│       ├── dataSplits.csv
	│       └── problemDoc.json
	└── TRAIN
		├── dataset_TRAIN
		│   ├── datasetDoc.json
		│   └── tables
		│       └── learningData.csv
		└── problem_TRAIN
			├── dataSplits.csv
			└── problemDoc.json
'''

def convert_(X_train, y_train, labels):

	feature_list=labels
	data=dict()

	print(len(feature_list))
	print(len(X_train[0]))
	# time.sleep(50)

	indices=list()
	for i in range(len(X_train)):
		indices.append(i)
		for j in range(len(feature_list)-1):
			if i > 0:
				try:
					data[feature_list[j]]=data[feature_list[j]]+[X_train[i][j]]
				except:
					pass
			else:
				data[feature_list[j]]=[X_train[i][j]]
				print(data)

	data['class_']=y_train
	data['d3mIndex']=indices

	data=pd.DataFrame(data, columns = list(data))
	print(data)
	print(list(data))

	return data

def split_data(data):

	# get training and testing numbers 
	train_num=int(0.80*len(data))
	test_num=len(data)-train_num

	print('TRAINING SAMPLES')
	print(train_num)
	print('TESTING SAMPLES')
	print(test_num)

	# now write the rows 
	rows=list()
	train_count=0
	test_count=0
	train_rows=list()
	test_rows=list()
	i=0

	totalcount=train_num+test_num

	# randomize the numbers of i
	i_list=list()
	for i in range(totalcount):
		i_list.append(i)

	random.shuffle(i_list)

	for i in range(len(i_list)):

		if train_num > train_count:
			rows.append([i_list[i], 'TRAIN', 0, 0])
			train_rows.append(i_list[i])
			i=i+1
			train_count=train_count+1
			print(train_count)
			# print(train_num)

		elif test_num > test_count:
			rows.append([i_list[i], 'TEST', 0, 0])
			test_rows.append(i_list[i])
			i=i+1
			test_count=test_count+1
			# print(len(rows))

		print([test_num, test_count, train_num, train_count])
	# field names  
	fields = ['d3mIndex', 'type', 'repeat', 'fold']  
		
	# name of csv file  
	filename = "dataSplits.csv"

	# writing to csv file  
	with open(filename, 'w') as csvfile:  
		# creating a csv writer object  
		csvwriter = csv.writer(csvfile)  
		# writing the fields  
		csvwriter.writerow(fields)  
		# writing the data rows  
		csvwriter.writerows(rows) 

	# now split this data into another csv 
	print(train_rows)
	train_data=data.iloc[train_rows,:]
	train_data.to_csv('train.csv')
	print(test_rows)
	test_data=data.iloc[test_rows,:]
	test_data.to_csv('test.csv')

	return filename


def create_dataset_json(foldername, trainingcsv):

	# create the template .JSON file necessary for the featurization
	dataset_name=foldername
	dataset_id="%s_dataset"%(foldername)
	columns=list()

	colnames=list(pd.read_csv(trainingcsv))

	for i in range(len(colnames)):
		if colnames[i] != 'class_':
			columns.append({"colIndex": i,
						"colName": colnames[i],
						"colType": "real",
						"role": ["attribute"]})
		else:
			columns.append({"colIndex": i,
						"colName": 'class_',
						"colType": "real",
						"role": ["suggestedTarget"]})	
			i1=i


	data={"about": 
	  {
	  "datasetID": dataset_id,
	  "datasetName":dataset_name,
	  "humanSubjectsResearch": False,
	  "license":"CC",
	  "datasetSchemaVersion":"3.0",
	  "redacted":False
	  },
	"dataResources":
	  [
		{
		  "resID": "0",
		  "resPath": 'tables/learningData.csv',
		  "resType": "table",
		  "resFormat": ["text/csv"],
		  "isCollection": False,
		  "columns":columns,
		}
	  ]
	}

	filename='datasetDoc.json'
	jsonfile=open(filename,'w')
	json.dump(data,jsonfile)
	jsonfile.close()

	return dataset_id, filename, i1

def create_problem_json(mtype, folder,i1):

	if mtype == 'c':
		data = {
		  "about": {
			"problemID": "%s_problem"%(folder),
			"problemName": "%s_problem"%(folder),
			"problemDescription": "not applicable",
			"taskType": "classification",
			"taskSubType": "multiClass",
			"problemVersion": "1.0",
			"problemSchemaVersion": "3.0"
		  },
		  "inputs": {
			"data": [
			  {
				"datasetID": "%s"%(folder),
				"targets": [
				  {
					"targetIndex": 0,
					"resID": "0",
					"colIndex": i1,
					"colName": 'class_',
				  }
				]
			  }
			],
			"dataSplits": {
			  "method": "holdOut",
			  "testSize": 0.2,
			  "stratified": True,
			  "numRepeats": 0,
			  "randomSeed": 42,
			  "splitsFile": "dataSplits.csv"
			},
			"performanceMetrics": [
			  {
				"metric": "accuracy"
			  }
			]
		  },
		  "expectedOutputs": {
			"predictionsFile": "predictions.csv"
		  }
		}

	elif mtype == 'r':
		data={"about": {
				"problemID": "%s_problem"%(folder),
				"problemName": "%s_problem"%(folder),
				"problemDescription": "not applicable",
				"taskType": "regression",
				"taskSubType": "univariate",
				"problemVersion": "1.0",
				"problemSchemaVersion": "3.0"
			  },
			  "inputs": {
				"data": [
				  {
					"datasetID": "%s_dataset"%(folder),
					"targets": [
					  {
						"targetIndex": 0,
						"resID": "0",
						"colIndex": i1,
						"colName": "class_"
					  }
					]
				  }
				],
				"dataSplits": {
				  "method": "holdOut",
				  "testSize": 0.2,
				  "stratified": True,
				  "numRepeats": 0,
				  "randomSeed": 42,
				  "splitsFile": "dataSplits.csv"
				},
				"performanceMetrics": [
				  {
					"metric": "meanSquaredError"
				  }
				]
			  },
			  "expectedOutputs": {
				"predictionsFile": "predictions.csv"
			  }
			}

	jsonfile=open('problemDoc.json','w')
	json.dump(data,jsonfile)
	jsonfile.close()

def train_autobazaar(X_train,X_test,y_train,y_test,mtype,common_name_model,problemtype,classes,default_featurenames,transform_model,settings,model_session):
	# create file names
	model_name=common_name_model+'.pickle'
	folder=common_name_model

	# this should be the model directory
	hostdir=os.getcwd()

	# make a temporary folder for the training session
	try:
		os.mkdir(folder)
		os.chdir(folder)
	except:
		shutil.rmtree(folder)
		os.mkdir(folder)
		os.chdir(folder)

	# make the data arrays 
	print('creating training data...')
	if transform_model != '':
		csvfilename=common_name_model+'_all.csv'
		shutil.copy(hostdir+'/'+model_session+'/data/'+common_name_model.split('_')[0]+'_all.csv', os.getcwd()+'/'+csvfilename)
	else:
		csvfilename=common_name_model+'_all_transformed.csv'
		shutil.copy(hostdir+'/'+model_session+'/data/'+common_name_model.split('_')[0]+'_all_transformed.csv', os.getcwd()+'/'+csvfilename)

	# create required .JSON files
	data=pd.read_csv(csvfilename)
	dataset_id, dataset_filename, i1=create_dataset_json(folder, csvfilename)
	problem_filename=create_problem_json(mtype, folder, i1)
	split_data(data)

	# get the current directory
	abz_dir=os.getcwd()

	# make necessary directories 
	# now create proper tree structure
	'''
	─ 196_autoMpg
		├── 196_autoMpg_dataset
		│   ├── datasetDoc.json
		│   └── tables
		│       └── learningData.csv
		├── 196_autoMpg_problem
		│   ├── dataSplits.csv
		│   └── problemDoc.json
		├── SCORE
		│   ├── dataset_TEST
		│   │   ├── datasetDoc.json
		│   │   └── tables
		│   │       └── learningData.csv
		│   ├── problem_TEST
		│   │   ├── dataSplits.csv
		│   │   └── problemDoc.json
		│   └── targets.csv
		├── TEST
		│   ├── dataset_TEST
		│   │   ├── datasetDoc.json
		│   │   └── tables
		│   │       └── learningData.csv
		│   └── problem_TEST
		│       ├── dataSplits.csv
		│       └── problemDoc.json
		└── TRAIN
			├── dataset_TRAIN
			│   ├── datasetDoc.json
			│   └── tables
			│       └── learningData.csv
			└── problem_TRAIN
				├── dataSplits.csv
				└── problemDoc.json
	'''

	dataset_folder=folder+'_dataset'
	problem_folder=folder+'_problem'

	# make datasets folder
	os.mkdir(dataset_folder)
	os.chdir(dataset_folder)
	os.mkdir('tables')
	shutil.copy(abz_dir+'/datasetDoc.json', os.getcwd()+'/datasetDoc.json')	
	shutil.copy(abz_dir+'/'+csvfilename, os.getcwd()+'/tables/'+csvfilename)
	os.chdir('tables')
	os.rename(csvfilename, 'learningData.csv')

	# make problem folder
	os.chdir(abz_dir)
	os.mkdir(problem_folder)
	os.chdir(problem_folder)
	shutil.copy(abz_dir+'/problemDoc.json', os.getcwd()+'/problemDoc.json')
	shutil.copy(abz_dir+'/dataSplits.csv', os.getcwd()+'/dataSplits.csv')

	os.chdir(abz_dir)
	os.mkdir('TEST')
	os.chdir('TEST')
	os.mkdir('dataset_TEST')
	shutil.copy(abz_dir+'/'+dataset_folder+'/datasetDoc.json', os.getcwd()+'/dataset_TEST/datasetDoc.json')
	os.mkdir('problem_TEST')
	shutil.copy(abz_dir+'/'+problem_folder+'/problemDoc.json',os.getcwd()+'/problem_TEST/problemDoc.json')
	shutil.copy(abz_dir+'/'+problem_folder+'/dataSplits.csv', os.getcwd()+'/problem_TEST/dataSplits.csv')
	os.chdir('dataset_TEST')
	os.mkdir('tables')
	shutil.copy(abz_dir+'/test.csv', os.getcwd()+'/tables/test.csv')
	os.chdir('tables')
	os.rename('test.csv', 'learningData.csv')
	
	os.chdir(abz_dir)
	os.mkdir('TRAIN')
	os.chdir('TRAIN')
	os.mkdir('dataset_TRAIN')
	os.chdir('dataset_TRAIN')
	os.mkdir('tables')
	shutil.copy(abz_dir+'/datasetDoc.json', os.getcwd()+'/datasetDoc.json')
	shutil.copy(abz_dir+'/train.csv', os.getcwd()+'/tables/train.csv')
	os.chdir('tables')
	os.rename('train.csv','learningData.csv')
	os.chdir(abz_dir+'/TRAIN')
	os.mkdir('problem_TRAIN')
	shutil.copy(abz_dir+'/'+problem_folder+'/problemDoc.json',os.getcwd()+'/problem_TRAIN/problemDoc.json')
	shutil.copy(abz_dir+'/'+problem_folder+'/dataSplits.csv', os.getcwd()+'/problem_TRAIN/dataSplits.csv')

	os.chdir(abz_dir)
	os.mkdir('SCORE')
	os.chdir('SCORE')
	shutil.copytree(abz_dir+'/TEST/dataset_TEST',os.getcwd()+'/dataset_SCORE')
	shutil.copytree(abz_dir+'/TEST/problem_TEST', os.getcwd()+'/problem_SCORE')
	os.chdir(hostdir)

	# this works for really any input configuration - regression or classificatoin (as this is covered in config files)
	try:
		os.mkdir('input')
	except:
		pass
	
	# remove if file exists
	try:
		shutil.copytree(folder, os.getcwd()+'/input/'+folder)
	except:
		shutil.rmtree(os.getcwd()+'/input/'+folder)
		shutil.copytree(folder, os.getcwd()+'/input/'+folder)

	print(os.getcwd())
	time.sleep(30)
	os.system('abz search %s -c20,30,40 -b10'%(folder))

	# now go to output folder 
	os.chdir('output')
	listdir=os.listdir()
	for i in range(len(listdir)):
		if listdir[i].endswith('.json'):
			g=json.load(open(listdir[i]))
			# os.remove(listdir[i])
		elif listdir[i].endswith('.pkl'):
			picklefile=folder+'.pickle'
			shutil.copy(os.getcwd()+'/'+listdir[i],hostdir+'/'+model_name)

	files.append(model_name)
	model_dir=hostdir

	return model_name, model_dir, files
