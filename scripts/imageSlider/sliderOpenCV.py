import os
import sys
import cv2

delayImage = 60000
#folderPath = "/home/pi/scripts/imageSlider/"
folderPath = "/home/sneer/Documents/smartBackUp/scripts/imageSlider/"

def handleExitRequests(key):
    if key == ord('q'): # If 'q' pressed (EXIT)
        sys.exit(0)

def makeImageFullScreen(name):
    cv2.namedWindow(name,cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def slideshow():

    window_name = "Slideshow"
    list_image_names = os.listdir(folderPath+'images/')
    quantity_of_images = len(list_image_names)

    image_id = 0
    while(image_id < quantity_of_images):
        key, pause_key = None, None  # to store the key entered by user while slideshow

        img = cv2.imread(folderPath+'images/' + list_image_names[image_id])

        '''
        To add blur effect
        '''
        for blur_amount in range(32,1,-6):  # getting blur values for our blur effect
            cv2.imshow(window_name, cv2.blur(img, (blur_amount,blur_amount) ) ) # showing blurred image
            key = cv2.waitKey(25)
            handleExitRequests(key)

        makeImageFullScreen(window_name)
        cv2.imshow(window_name, img)  # displaying clear image

        key = cv2.waitKey(delayImage)   # taking key from user with 'n' ms delay
        handleExitRequests(key)
        image_id = (image_id+1)%quantity_of_images # If no keys are pressed, then image_id incremented for next image
    cv2.destroyAllWindows() # when work id done, closing windows

def main():
    print('''|| Press 'q' to exit the slideshow ||''')
    slideshow()

if __name__ == "__main__":
    main()
