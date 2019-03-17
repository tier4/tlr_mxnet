# Installation
## Autoware
#### Source build
https://github.com/CPFL/Autoware/wiki/Source-Build

## MXNet
#### Source build
https://github.com/CPFL/Autoware/tree/master/ros/src/computing/perception/detection/trafficlight_recognizer/nodes/region_tlr_mxnet
#### Install Python module
```
$ cd mxnet/python
$ sudo pip install -e .
```

## ApexAI/mxnet-ssd
```
$ git clone https://github.com/ApexAI/mxnet-ssd <apex-mxnet-dir>
```

# Dataset generation
#### Extract traffic light images
```
## Launch Autoware (map, sensors, calibration, feat_proj)
$ roslaunch trafficlight_recognizer roi_extractor.launch similarity_threshold:=0.95
```

#### Prepare dataset directory strucrture
```
$ mkdir -p <dataset-dir>/raw
$ mv $HOME/.autoware/tlr_TrainingDataSet/Images/* <dataset-dir>/raw
$ tree <dataset-dir>

<dataeset-dir>
├── raw
│   ├── 0.png
│   ├── 1.png
│   ├── 2.png
```
#### Annotate by keyboard (Keyboard configuration -> green: 1, yellow: 2, red: 3, off: 4, nouse: space)
```
$ python simple_annotator.py <dataset-dir>
$ tree <dataset-dir>

<dataeset-dir>
├── green
├── yellow
├── red
├── off
├── nouse
├── raw
```
#### Generate `lst/idx/rec` file (Generated label -> green: 0, yellow: 1, red: 2, off: 3)
```
$ python lst_generator.py <dataset-dir>
$ cd <dataset-dir>
$ python <apex-mxnet-dir>/traffic_light_classification/im2rec.py ./ ./ --resize 100
```

# Training
```
$ tree <model-dir>

<model-dir>
├── densenet30-symbol.json

$ cd <apex-mxnet-dir>
$ python train_nexar.py --prefix <model-dir>/densenet30 --net densenet30 --train_rec <dataset-dir>/train.rec --val_rec <dataset-dir>/test.rec

```
#### Fine-tuning
```
$ tree <model-dir>

<model-dir>
├── densenet30-symbol.json
├── densenet30-<epoch>.params

$ cd <apex-mxnet-dir>
$ python train_nexar.py --resume <epoch> --prefix <model-dir>/densenet30 --net densenet30 --train_rec <dataset-dir>/train.rec --val_rec <dataset-dir>/test.rec --freeze True

```

# Inference
```
$ cd <apex-mxnet-dir>
$ python traffic_light_classifier.py --network densenet30 --modelpath <model-dir> --image_path <image-path>
```
