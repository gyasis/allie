import os, json, sys

# go to the proper directory
directory=sys.argv[1]
os.chdir(directory)

# now get current directory 
curdir=os.getcwd()
listdir=os.listdir()

if 'settings.json' in listdir:
	settings=json.load(open('settings.json'))
	settings_g='## Settings \n'
	settings_g=settings_g+'```\n'
	settings_g=settings_g+str(settings)+'\n'
	settings_g=settings_g+'```\n'
	settings_g=settings_g+'\n'
else:
	settings=''

if 'visualizations' in listdir:
	vis='## Visualizations \n'
	vis=vis+'### Clustering \n'
	vis=vis+'![](./visualizations/clustering/pca.png)\n'
	vis=vis+'![](./visualizations/clustering/tsne.png)\n'
	vis=vis+'### Feature ranking \n'
	vis=vis+'![](./visualizations/feature_ranking/feature_importance.png)\n'
	vis=vis+'![](./visualizations/feature_ranking/heatmap_clean.png)\n'
	vis=vis+'![](./visualizations/model_selection/outliers.png)'
else:
	vis=''

os.chdir('model')
listdir=os.listdir()

# get visualizations for model training 
if 'confusion_matrix.png' in listdir:
	confusion_matrix=True
else:
	confusion_matrix=False
if 'roc_curve.png' in listdir:
	roc_curve=True
else:
	roc_curve=False

for i in range(len(listdir)):
	if listdir[i].endswith('.json'):
		statsfile=listdir[i]
		stats=json.load(open(listdir[i]))
		break

os.chdir(curdir)
common_name=statsfile.split('_')[0]

readme_file=open('readme.md','w')
readme_file.write('# %s model \n'%(common_name.upper()))
readme_file.write('This is a %s model created on %s classifying %s. It was trained using the %s script, and achieves the following accuracy scores: \n```\n%s\n```\n'%(common_name, stats['created date'], str(stats['classes']), stats['model type'],str(stats['metrics'])))  
readme_file.write(vis)
readme_file.write('\n')
if roc_curve==True:
	readme_file.write('![](./model/roc_curve.png)\n')
if confusion_matrix==True:
	readme_file.write('![](./model/confusion_matrix.png)\n')
readme_file.write(settings_g)
