# -*- coding: utf-8 -*-
import cv2, os

base = r'E:\김세희\aeong_claude_code\blog'
video_path = None
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.mp4') and '종자원' in f:
            video_path = os.path.join(root, f)

tmp_dir = r'C:\temp_frames2'
os.makedirs(tmp_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

# 연혁 3D 구간(10~80s) + 3D지도 구간(190~215s) 촘촘하게
timestamps = list(range(10, 82, 8)) + list(range(190, 216, 5))

for t in timestamps:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ret, frame = cap.read()
    if ret:
        path = os.path.join(tmp_dir, f'frame_{t:03d}s.jpg')
        cv2.imwrite(path, frame)
        print(f'saved: {t}s')

cap.release()
print('완료')
