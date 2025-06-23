import cv2

class TrackedFace:
    def __init__(self, tracker, name):
        self.tracker = tracker
        self.name = name

def create_tracker(frame, bbox):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)
    return tracker