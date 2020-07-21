# Mask_Detector

This is an tensor-flow and computer vision based model on detection of mask from real-time video stream. Any cctv camera footage can be pipelined to our model and help in mask-classification. This is a part of the project FIGHT-O-MIC smart hospital.







## covid-social-distancing-detection

This is the second part of the project. For running the project go to the second folder named Social_Distancing and then execute the following instructions.

![](/img/result.gif)

# Installation

### Other requirements
All the other requirements can be installed via the command : 
```bash
pip install -r requirements.txt
```

# Download Tensorflow models

In my project I used the faster_rcnn_inception_v2_coco model. I could not upload it to github because it is to heavy. You can download this model and several others from the [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). 
Just download all the models you want to try out, put them in the models folder and unzip them. For example :
```bash
tar -xvzf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```

# Run project

### Calibrate
Run 
```bash
python calibrate_with_mouse.py
```
You will be asked as input the name of the video and the size of the frame you want to work with. The default values are PETS2009.avi and 800 pixels.

Note : It is important to start with the top right corner, than the bottom right, then bottom left, than end by top left corner !

You can add any video to the video folder and work with that.

### Start social distancing detection
Run 
```bash
python social_distanciation_video_detection.py
```
You will be asked as inputs :
- The tensorflow model you want to use (default value faster_rcnn_inception_v2_coco_2018_01_28).
- The name of the video (default value PETS2009.avi).
- The distance (in pixels between 2 persons).

## Outputs
Both video outputs (normal frame and bird eye view) will be stored in the outputs file.

# Note
Due to unavailabilty of live CCTV footages I break the code into two parts. The first part focussed on detection mask along with uncovered mouth and nose. The code was tested uising live streaming from the webcam of my computer (which can be compared with the CCTV footages) but for social distancing I did't get any possible opportunity for deploying it live but the live streaming can be done easily by pipelining the CCTV footage with the main.py file. The following steps will illustrate the process more clearly:

- 
