# EMG in gaming applications
For this project we are using MYO armband to get raw EMG data from the forearm's
muscles. 
## Gesture recognition
For now we are able to identify 5 gestures: 
1. Wave left
2. Wave right
3. Clenched fist
4. Pinky finger
5. Relaxed

![alt text](Assets/2018-10-18-18.38.40.gif)
![alt text](Assets/2018-10-18-18.39.22.gif)

The gesture recognition is done real-time using LDA classifier. The gesture is then mapped to a specific keyboard input and can be used in a game.

```json
{
  "classes": {
    "1" : "palm_left",
    "2" : "palm_right",
    "3" : "palm_rest",
    "4" : "fist",
    "5" : "pinky"
  },
  "bindings": {
    "1" : "left",
    "2" : "right",
    "3" : "",
    "4" : "",
    "5" : ""
  }
}
```
![alt text](Assets/2018-10-18-18.39.32.gif)
![alt text](Assets/2018-10-18-18.39.39.gif)

## Continuous output
For continuous output from the MYO we are using Kernel Ridge Regression with an RBF kernel. The training data was obtained by recording periodic palm movements from left to right. The y-values were obtained from the sine wave that was fitted over the dataset’s peaks.

![alt text](Assets/Screen%20Shot%202018-10-18%20at%2019.43.00.png)

![alt text](Assets/2018-10-18-19.27.50.gif)