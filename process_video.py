# Returns a list of timestamps and their frame match scores
import cv2

SHOW_FRAMES = False
def process_video(file_path, on_frame, intervals=15):
    print(f'Reading {file_path}')
    cap = cv2.VideoCapture(f'{file_path}.mp4')
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_no = 0
    match_scores_and_timestamps = []
    while (cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            if SHOW_FRAMES:
                cv2.imshow('Frame', curr_frame)

                # press q on keyboard to exit
                if cv2.waitKey(10) & 0xFF == ord('q'): 
                    break
            on_frame(curr_frame, frame_no)
            
            # skip to next frame
            num_frames_to_skip = int(video_fps * intervals)
            frame_no += num_frames_to_skip
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        else:
            break
        frame_no += 1
    cap.release()

    match_scores = [datum[1]
                          for datum in match_scores_and_timestamps]
    timestamps = [datum[0] for datum in match_scores_and_timestamps]
    return match_scores, timestamps