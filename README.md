# Low-Light Video Enhancement and Number Plate Recognition System

## Step 1: Low-Light Video Enhancement

The first step of the project focuses on enhancing low-light CCTV videos to improve visibility and increase the accuracy of further processing tasks.

### Available Enhancement Methods
1. EnlightenGAN  
2. Retinex Mamba  
3. ZeroDCE++

You can select any of the above algorithms. Update the input path of the video inside the enhancement code before running it.

### Training the Enhancement Model
You can train your selected enhancement model using both images and videos.

### Datasets for Training
LOL Dataset (Low-Light Enhancement Training):
- https://www.kaggle.com/datasets/soumikrakshit/lol-dataset
- https://github.com/Li-Chongyi/Lighting-the-Darkness-in-the-Deep-Learning-Era-Open

Additionally, CCTV feed samples are provided in the project for testing purposes.


## Step 2: Number Plate Recognition

After enhancing the video, the next step is number plate detection and recognition.

### Training the ANPR Model
Use the following dataset to train your number plate detection model:
- https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e

This model detects the license plate from frames and extracts the alphanumeric plate number.


## Step 3: Run the Backend Server

Once models are trained and integrated:

Run the backend API server:

python server.py

## Step 4: Expose the Server Using Ngrok

To make your local server publicly accessible:

1. Download Ngrok from https://ngrok.com  
2. Open a new terminal  
3. Run:
ngrok http 5000
4. Ngrok will generate a public URL which can be used to access the API over the internet.

## Step 5: MySQL Database Setup

Open MySQL and run the required SQL queries to create the database and tables.

## Step 6: Connect MySQL Database to QGIS

To visualize detected vehicle coordinates on a map, integrate the MySQL database with QGIS.

Steps:
1. Open QGIS  
2. Go to Layers → Add Layer → Add Vector Layer  
3. Select Database  
4. Choose MySQL  
5. Enter hostname, port, username, password  
6. Select the database `anpr_mysql`  
7. Load the table `numberplate`

This will display:
- Points based on latitude and longitude
- Vehicle movement paths (if multiple points exist)

## Project Workflow Summary

1. Perform low-light video enhancement  
2. Run Number_plate_recognition.ipynb to detect and extract license plates  
3. Start server using `server.py`  
4. Use Ngrok to expose the server  
5. Insert results into MySQL  
6. Visualize coordinates through QGIS  

