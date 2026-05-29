# -*- coding: utf-8 -*-
import os, shutil

src_files = [
    (r'C:\temp_frames2\frame_042s.jpg', 'video_frame_01_trophy3d.jpg'),
    (r'C:\temp_frames2\frame_018s.jpg', 'video_frame_02_history1970s.jpg'),
    (r'C:\temp_frames2\frame_210s.jpg', 'video_frame_03_map3d.jpg'),
]

base = r'E:\김세희\aeong_claude_code\blog'
dest_dir = None
for root, dirs, files in os.walk(base):
    for d in dirs:
        if d == '영상' and '종자원' in root:
            dest_dir = os.path.join(root, d)

for src, name in src_files:
    dst = os.path.join(dest_dir, name)
    shutil.copy2(src, dst)
    print(f'copied: {name}')

# 이전 잘못 고른 파일 삭제
for old in ['video_frame_01_tomato.jpg', 'video_frame_02_global.jpg', 'video_frame_03_field.jpg']:
    p = os.path.join(dest_dir, old)
    if os.path.exists(p):
        os.remove(p)
        print(f'removed: {old}')
