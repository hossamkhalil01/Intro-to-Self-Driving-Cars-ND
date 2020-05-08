import cv2 
import helpers 

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 


#############################
##1.Loading and Visualizing##
#############################

# Image data directories
IMAGE_DIR_TRAINING = "traffic_light_images/training/"
IMAGE_DIR_TEST = "traffic_light_images/test/"

# Using the load_dataset function in helpers.py
# Load training data
IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAINING)


# Visualize the Data

im_num = 500
selected_image = IMAGE_LIST[im_num][0]
selected_label = IMAGE_LIST[im_num][1]

plt.imshow(selected_image)
plt.show()

print("Shape: ",selected_image.shape)
print ("Label: ",selected_label)


#####################
##2.Pre-Processing###
#####################

# This function should take in an RGB image and return a new, standardized version
def standardize_input(image):
    
    #Create a copy of the image
    standard_im = np.copy(image)
    
    
    #Crop the image to cut out all irrelevant pixels
    #cut off 30% of the image from each side
    #cut off 15% of the image from top and bottom
    portion_x =0.3 
    portion_y =0.15 
    
    
    x1 = int(portion_x*image.shape[1])
    x2 = int((1-portion_x)*image.shape[1])

    y1 = int(portion_y*image.shape[0])
    y2 = int((1-portion_y)*image.shape[0])
    
    #Slice the original image to get the new cropped image
    standard_im = standard_im[y1:y2,x1:x2]    
    
    
    #Resize the image to the standard size (32x32)
    standard_im = cv2.resize(standard_im,(32,32))
    
    
    return standard_im

# Given a label - "red", "green", or "yellow" - return a one-hot encoded label
def one_hot_encode(label):

    #Define all classes
    label_types = ['red','yellow','green']
    
    #Create a list of zeroes with the same length
    one_hot_encoded = [0]*len(label_types)
    
    #Assign a value of 1 at the index of the label type
    one_hot_encoded[label_types.index(label)] = 1
    
    return one_hot_encoded


#Testing the encoding function
# Importing the tests
import test_functions
tests = test_functions.Tests()

# Test for one_hot_encode function
tests.test_one_hot(one_hot_encode)


# Construct a Standardized list of the input images

def standardize(image_list):
    
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)

        # One-hot encode the label
        one_hot_label = one_hot_encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, one_hot_label))
        
    return standard_list

# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)

#Visualize the Standardized data
im_num = 900
plt.imshow(STANDARDIZED_LIST[im_num][0])
plt.show()

print ("Label: ",STANDARDIZED_LIST[im_num][1])
print("Standardized Shape:  ",STANDARDIZED_LIST[im_num][0].shape)



##########################
###3.Feature Extraction###
##########################

# Convert and image to HSV colorspace
# Visualize the individual color channels

image_num = 798
test_im = STANDARDIZED_LIST[image_num][0]
test_label = STANDARDIZED_LIST[image_num][1]

# Convert to HSV
hsv = cv2.cvtColor(test_im, cv2.COLOR_RGB2HSV)

# Print image label
print('Label [red, yellow, green]: ' + str(test_label))

# HSV channels
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]


# Plot the original image and the three channels
f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20,10))
ax1.set_title('Standardized image')
ax1.imshow(test_im)
ax2.set_title('H channel')
ax2.imshow(h, cmap='gray')
ax3.set_title('S channel')
ax3.imshow(s, cmap='gray')
ax4.set_title('V channel')
ax4.imshow(v, cmap='gray')

#Create features
## This feature should use HSV colorspace values
def create_feature(rgb_image):

    
    hsv = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2HSV)
    
    #Extract the v channel
    v = hsv[:,:,2]

    #The image is divided into 3 regions in height for each of the color (To determine the average v values) of the pixels
    #the red region is from height = 5 to 9 , yellow from 13 to 18 , and green from 24 to 32
    
    
    #Slicing the image in width for the seperated regions
    r_region = v[5:9,:]
    y_region = v[13:18,:]
    g_region = v[24:32,:]
    
    #Compute the average v value over each region 
    r_region = np.sum(r_region) /(r_region.shape[0]*r_region.shape[1])
    y_region = np.sum(y_region)/(y_region.shape[0]*y_region.shape[1])
    g_region = np.sum(g_region)/(g_region.shape[0]*g_region.shape[1])
    
    
    feature = [r_region,y_region,g_region]
    
    return feature


#####################
##4.Classification###
#####################
# Analyze that image using your feature creation code and output a one-hot encoded label
def estimate_label(rgb_image):
    
    ## classify the image and output a one-hot encoded label
  
    features = create_feature(rgb_image)
    
    #features is a list with 3 elements 
    #average number of pixels in the v channel for red region , yellow region and green region respectively 

    r_region = features[0]
    y_region = features[1]
    g_region = features[2]
    
    

    #use the region separation to classify
    

    if y_region>r_region and y_region>g_region:  #Yellow region detected
        return one_hot_encode('yellow')
    
    if r_region > g_region:  #Red region detected
        return one_hot_encode('red')
    
    
    if g_region > r_region: #Green region detected
        return one_hot_encode('green')

    
    #The default value should be red over a green
    return one_hot_encode('red')



#############################
##4.Testing the Classifier###
#############################

# Using the load_dataset function in helpers.py
# Load test data
TEST_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TEST)

# Standardize the test data
STANDARDIZED_TEST_LIST = standardize(TEST_IMAGE_LIST)

# Shuffle the standardized test data
random.shuffle(STANDARDIZED_TEST_LIST)

#Determine the Accuracy

# Constructs a list of misclassified images given a list of test images and their labels
# This will throw an AssertionError if labels are not standardized (one-hot encoded)

def get_misclassified_images(test_images):
    # Track misclassified images by placing them into a list
    misclassified_images_labels = []

    # Iterate through all the test images
    # Classify each image and compare to the true label
    for image in test_images:

        # Get true data
        im = image[0]
        true_label = image[1]
        assert(len(true_label) == 3), "The true_label is not the expected length (3)."

        # Get predicted label from your classifier
        predicted_label = estimate_label(im)
        assert(len(predicted_label) == 3), "The predicted_label is not the expected length (3)."

        # Compare true and predicted labels 
        if(predicted_label != true_label):
            # If these labels are not equal, the image has been misclassified
            misclassified_images_labels.append((im, predicted_label, true_label))
            
    # Return the list of misclassified [image, predicted_label, true_label] values
    return misclassified_images_labels


# Find all misclassified images in a given test set
MISCLASSIFIED = get_misclassified_images(STANDARDIZED_TEST_LIST)

# Accuracy calculations
total = len(STANDARDIZED_TEST_LIST)
num_correct = total - len(MISCLASSIFIED)
accuracy = num_correct/total

print('Accuracy: ' + str(accuracy))
print("Number of misclassified images = " + str(len(MISCLASSIFIED)) +' out of '+ str(total))


#Visualize the misclassified images
im_num = 0
plt.imshow(MISCLASSIFIED[im_num][0])
plt.show()
print("Predicted label: ",MISCLASSIFIED[im_num][1])
print("Ture label: ",MISCLASSIFIED[im_num][2])

###################################################
###Test if you classify any red lights as green####
###################################################
# Importing the tests
import test_functions
tests = test_functions.Tests()

if(len(MISCLASSIFIED) > 0):
    # Test code for one_hot_encode function
    tests.test_red_as_green(MISCLASSIFIED)
else:
    print("MISCLASSIFIED may not have been populated with images.")