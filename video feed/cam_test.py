import cv2

def show_video_feed():
    # Create a VideoCapture object to capture video from the camera
    cap = cv2.VideoCapture(0)  # 0 represents the default camera index

    while True:
        # Read the current frame from the camera
        ret, frame = cap.read()
        
        # Lower the image resolution by resizing the frame
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Display the frame in a window named "Video Feed"
        cv2.imshow("Video Feed", frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start showing the video feed
show_video_feed()
