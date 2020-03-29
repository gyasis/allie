import scipy.io.wavfile as wav
import numpy as np
import pyworld as pw
import os, sys
import numpy as np

# get statistical features in numpy
def stats(matrix, label):

	labels=list()

	# extract features
	if label in ['smoothed_spectrogram', 'aperiodicity']:
		mean=np.mean(matrix, axis=0)
		for i in range(len(mean)):
			labels.append(label+'_mean_'+str(i))
		std=np.std(matrix, axis=0)
		for i in range(len(std)):
			labels.append(label+'_std_'+str(i))
		maxv=np.amax(matrix, axis=0)
		for i in range(len(maxv)):
			labels.append(label+'_max_'+str(i))
		minv=np.amin(matrix, axis=0)
		for i in range(len(minv)):
			labels.append(label+'_min_'+str(i))
		median=np.median(matrix, axis=0)
		for i in range(len(median)):
			labels.append(label+'_median_'+str(i))
	else:
		mean=np.mean(matrix)
		std=np.std(matrix)
		maxv=np.amax(matrix)
		minv=np.amin(matrix)
		median=np.median(matrix)
		labels=[label+'_mean',label+'_std',label+'_max'+label+'_min',label, '_median']

	features=np.append(mean, std)
	features=np.append(features, maxv)
	features=np.append(features, minv)
	features=np.append(features, median)

	return features, labels

def pyworld_featurize(audiofile):

	fs, x = wav.read(audiofile)
	print(x)
	print(fs)
	# corrects for 2 channel audio
	try:
		x= x[:,0]
	except:
		pass
	x=np.array(np.ascontiguousarray(x), dtype=np.double)
	print(fs)
	print(x)

	_f0, t = pw.dio(x, fs)    # raw pitch extractor
	f0 = pw.stonemask(x, _f0, t, fs)  # pitch refinement
	sp = pw.cheaptrick(x, f0, t, fs)  # extract smoothed spectrogram
	ap = pw.d4c(x, f0, t, fs)         # extract aperiodicity)

	features_0, labels_0 = stats(_f0, 'pitch')
	features_1, labels_1 = stats(_f0, 'pitch_refinement')
	features_2, labels_2 = stats(sp, 'smoothed_spectrogram')
	features_3, labels_3 = stats(ap, 'aperiodicity')

	features_0=list(features_0)
	features_1=list(features_1)
	features_2=list(features_2)
	features_3=list(features_3)

	features=features_0+features_1+features_2+features_3
	labels=labels_0+labels_1+labels_2+labels_3

	return features, labels

# file_name = sys.argv[1]
# features, labels = pyworld_featurize(file_name)
# print(features)
# print(labels)
# print(features)
# print(labels)
# print(len(features))
# print(len(labels))