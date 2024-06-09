from ultralytics import YOLO


model = YOLO('yolov8n.pt')
model.predict(source='c.jpg', conf=0.25, save=True)
model.predict(source='b.jpg', conf=0.25, save=True)
model.predict(source='a.jpg', conf=0.25, save=True)





