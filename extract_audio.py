import ffmpeg

def get_audio(video_path, audio_output_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_output_path)
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f'Audio extracted to {audio_output_path}')
    except ffmpeg.Error as e:
        print('Error occurred:')
        print(e)
        print('stderr output:')
        print(e.stderr.decode('utf-8'))

# Gọi hàm get_audio với đường dẫn đến video và đường dẫn để lưu file âm thanh
video_path = 'D:\\Course\\CodeWithMosh - React 18 for Beginners\\02 - Getting Started with React\\2- Setting Up the Development Environment.mp4'
audio_output_path = 'D:\\Course\\CodeWithMosh - React 18 for Beginners\\02 - Getting Started with React\\2- Setting Up the Development Environment.mp3'

get_audio(video_path, audio_output_path)
