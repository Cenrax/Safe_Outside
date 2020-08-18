# Note
Due to unavailabilty of live CCTV footages I break the code into two parts. The first part focus on detection mask along with uncovered mouth and nose. The code was tested using live streaming from the webcam of my computer (which can be compared with the CCTV footages) but for social distancing I did't get any possible opportunity for deploying it live but the live streaming can be done easily by pipelining the CCTV footage with the Social_Distancing/src/social_distanciation_video_detection.py file. The working video can be accessed from the following link: https://drive.google.com/file/d/1Wn1tsz0sE5_Lk6Y9KCKwAA4Sq5TEEPxs/view?usp=sharing. For any 


## Mask_WithFacial_Checker

This folder is focused on detecting whether a person is wearing mask or not. If also wearing a mask, whether he/she is covering his/her mouth is also detected. Along with that if the person is not wearing a correct mask then also our model can detect it.

Apart from that, Sometimes a person opens his/her mouth without his/her sense. This model can also detect that part and it can notify the user through a app named Masky which I have developed along with this project.

The last part of the project is the android app which is developed using AndroidStudio and Java.

### Running Steps
Open Spyder or any python editor like Sublime3 or Visual Studio code and then run the following codes.
Run 
```bash
python detect_mask_video.py
```
What is happening in the above code can be summarized by the following points:

- First the model i.e. mask_detector.model is loaded and then the live streaming begin
- There are two parallel task going one is detecting the whether the person is wearing a mask or not and secondly another task is going whether the person's mouth and nose is exposed to the environment directly.
- As soon as the detection is done to ensure any miscalculation from the model we consider the average of the every 10 seconds and then the result is sent to the cloud i.e Firestore.
- From firestore there is a direct connection with the user's phone with a push notification system accordingly:
      - The user will get a notification " **Wear your Mask** " if he/she is not wearing a mask.
          - He/She will get a notification " **Cover your mouth** " if his/her mouth is exposed to the atmosphere.
          - He/She will also get a notification **Close your Mouth** his/her mouth is kept opent for a long time.

## Social_Distancing

This is the second part of the project. For running the project go to the second folder named Social_Distancing and then execute the following instructions.

![](/img/result.gif)

### Running Steps 


```bash
pip install -r requirements.txt
```

#### Download Tensorflow models

In my project I used the faster_rcnn_inception_v2_coco model. I could not upload it to github because it is to heavy. You can download this model and several others from the [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). 
Just download all the models you want to try out, put them in the models folder and unzip them. For example :
```bash
tar -xvzf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
```

#### Calibrate
Run 
```bash
python calibrate_with_mouse.py
```
You will be asked as input the name of the video and the size of the frame you want to work with. The default values are PETS2009.avi and 800 pixels.

Note : It is important to start with the top right corner, than the bottom right, then bottom left, than end by top left corner !

You can add any video to the video folder and work with that.

#### Start social distancing detection
Run 
```bash
python social_distanciation_video_detection.py
```
You will be asked as inputs :
- The tensorflow model you want to use (default value faster_rcnn_inception_v2_coco_2018_01_28).
- The name of the video (default value PETS2009.avi).
- The distance (in pixels between 2 persons).

The running process can be understood from the following process.
In this as soon as the social index violence is above the threshold a warning will be sent to the nearby local administration about the social-distancing violence with corresponding latitute and longitude of the position where the CCTV camera is placed.

## Android Application

The android app has been developed using Android Studio and Java programming language. The app has a simple  UI providing us the notification about the proper put up of mask and as well as the nearby crowded areas near us.





