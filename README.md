# voice_modeling
Master repository for modeling voice files. Transformed from NLX-model.

1. Get dataset
2. feature selection (https://machinelearningmastery.com/feature-selection-machine-learning-python/) 
3. modeling (if < 1000 then simple classification, if >1000 deep learning techniques - iterate through various architectures).
4. apply models. 

## types of data

Load folders and data script type based on principal type of file.

* Audio --> .WAV / .MP3
* Text --> .TXT / .PPT / .DOCX
* Images --> .PNG / .JPG 
* Video --> .MP4 / .M4A

## Features to add
### Videos 
* [Semantic video features](https://github.com/JunweiLiang/Semantic_Features)
* [GMM Video features](https://github.com/jonasrothfuss/videofeatures)
### Text
* [BERT](https://github.com/huggingface/pytorch-pretrained-BERT)
* [AllenNLP](https://github.com/allenai/allennlp)

## problems looked at 
* accent detection
* race detection 
* gender detection
* age detection
* stress detection
* emotion detection (face images) 
* number of speakers 
* image transcription

## list of all applicable models now
* accuracies, standard deviations (TPOT) 

## labeling
* [sound_event_detection]

## featurization scripts (parallel)
### Audio
* [DisVoice](https://github.com/jcvasquezc/DisVoice)
* [AudioOwl](https://github.com/dodiku/AudioOwl)

### Text
* []()

### Image
* []()

### Video 
* []()

## modeling 
* [TPOT]()
* [Ludwig]()

## visualization
* [Yellowbrick]()
