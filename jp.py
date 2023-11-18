from moviepy.editor import VideoFileClip, concatenate_videoclips
from pymediainfo import MediaInfo
import os
import sys

INPUT_VIDEOS_DIR = "input/"
OUTPUT_DIR = "output/"

FINAL_VIDEO_RES_WIDTH = 1920
FINAL_VIDEO_RES_HEIGHT = 1080

file_list = os.listdir(INPUT_VIDEOS_DIR)

def rescale(aa, bb, maxAA, maxBB):
    """
    Scale a rectangle with 'aa' x 'bb' size to 'maxAA' x 'maxBB', while keeping the orignal ratio
    """
    # Compute the scale ratios and keep the minimum one
    factor_escala = min(maxAA / aa, maxBB / bb)

    # Apply to each of the dimensions
    aa_esc = aa * factor_escala
    bb_esc = bb * factor_escala

    return aa_esc, bb_esc


# Select only the first N items

num_videos = 30
video_clips = []

for file_name in file_list[1000:1200]:
    full_path = INPUT_VIDEOS_DIR + file_name

    # Check if video is rotated
    media_info = MediaInfo.parse(full_path)
    video_info = media_info.video_tracks[0].to_data()

    rotation = int(float(video_info['rotation']))
    is_rotated = (rotation == 90) or (rotation == 270)

    height = video_info["height"]
    width = video_info["width"]
    
    # Invert resolution
    if is_rotated:
        height, width = width, height
        
    # Scale to 4K 
    target_height, target_width = rescale(height, width, FINAL_VIDEO_RES_HEIGHT,FINAL_VIDEO_RES_WIDTH)

    target_resolution = [int(target_height), int(target_width)]
    print("File: " + full_path + ". Resolution: " + str([video_info["height"], video_info["width"]]) +". Is rotated? " + str(is_rotated) + ", loading with resolution: " + str(target_resolution))

    # Try to open it 
    try:
        clip = VideoFileClip(full_path, target_resolution=target_resolution, fps_source='fps')
        #video_clips.append(VideoFileClip(full_path, target_resolution=target_resolution, fps_source='fps'))
        video_clips.append(clip)
        clip.close_video_reader()
    except:
        print(f"ERROR: video {file_name} could not be opened. Skipped file.")
        continue

    #video_clips.append(clip)


parameters=['-probesize', '500M']

final_clip = concatenate_videoclips(video_clips, method="compose", bg_color=(0,0,0))

outputFilePath = OUTPUT_DIR + "out.mp4"

final_clip.write_videofile(filename=outputFilePath, bitrate="10000000", write_logfile=True, preset="slow",audio_codec="libvorbis", ffmpeg_params=parameters)

