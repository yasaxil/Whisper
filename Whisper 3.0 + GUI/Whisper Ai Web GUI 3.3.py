import os
import time
import logging
import subprocess
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
import streamlit as st

def setup_logging(output_dir):
    log_filename = os.path.join(output_dir, 'processing.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return log_filename

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, codec='pcm_s16le')
    audio.close()
    video.close()

def process_audio(filepath, output_dir):
    filename = os.path.basename(filepath)
    try:
        audio = AudioSegment.from_file(filepath)
        temp_audio_path = os.path.join(output_dir, f"temp_{filename}.wav")
        audio.export(temp_audio_path, format="wav")
        result = pipe(temp_audio_path)
        text = result["text"]
        txt_path = os.path.join(output_dir, filename[:-4] + '.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        os.remove(temp_audio_path)
        logging.info(f"Файл {filename} успешно обработан.")
        return os.path.getsize(filepath)
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {filename}: {str(e)}")
        return 0

def process_video(filepath, output_dir):
    try:
        audio_filepath = os.path.splitext(filepath)[0] + '.wav'
        extract_audio_from_video(filepath, audio_filepath)
        return process_audio(audio_filepath, output_dir)
    except Exception as e:
        logging.error(f"Ошибка при обработке видео файла {os.path.basename(filepath)}: {str(e)}")
        return 0

def clean_path(path):
    return path.strip().strip('"')

def kill_process():
    subprocess.call(["taskkill", "/F", "/T", "/PID", str(os.getppid())])

model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    device="cuda:0"
)

st.title('Whisper Ai Web GUI 3.3')

input_directories = st.text_input("Введите пути к папкам через запятую:")
directories = [clean_path(dir_path) for dir_path in input_directories.split(',') if dir_path] if input_directories else []

if st.button('Завершить работу'):
    kill_process()

if st.button('Посмотреть лог', key='view_log'):
    log_filename = setup_logging('')  # Укажите корректный путь до лог файла
    try:
        with open(log_filename, 'r') as file:
            st.text_area('Лог:', value=file.read(), height=300)
    except Exception as e:
        st.error(f"Не удалось открыть лог-файл: {e}")

if directories:
    all_accessible = True
    for directory in directories:
        if not (os.path.exists(directory) and os.access(directory, os.R_OK)):
            st.error(f"Указанный путь {directory} не существует или к нему нет доступа.")
            all_accessible = False
    if all_accessible and st.button('Начать обработку'):
        for input_directory in directories:
            output_directory = os.path.join(input_directory, 'processed')
            os.makedirs(output_directory, exist_ok=True)
            log_filename = setup_logging(output_directory)
            # Обработка файлов
            files_to_process = []
            total_size = 0
            for root, dirs, files in os.walk(input_directory):
                for file in files:
                    if file.endswith(".ogg") or file.endswith(".mp4"):
                        full_path = os.path.join(root, file)
                        files_to_process.append(full_path)
                        total_size += os.path.getsize(full_path)

            total_size_mb = total_size / (1024 * 1024)
            processed_size_mb = 0
            start_time = time.time()
            progress_bar = st.progress(0)
            status_text = st.empty()
            for i, filepath in enumerate(files_to_process):
                file_size = os.path.getsize(filepath)
                file_size_mb = file_size / (1024 * 1024)
                processed_size_mb += file_size_mb
                if filepath.endswith(".ogg"):
                    process_audio(filepath, output_directory)
                elif filepath.endswith(".mp4"):
                    process_video(filepath, output_directory)
                progress_bar.progress((i + 1) / len(files_to_process))
                status_text.text(f"Обработка файла {i+1}/{len(files_to_process)}. Обработано {processed_size_mb:.2f} MB из {total_size_mb:.2f} MB")

            end_time = time.time()
            total_time = end_time - start_time
            num_files = len(files_to_process)
            logging.info(f"Обработка завершена для {input_directory}. Время работы: {total_time:.2f} секунд. Обработано файлов: {num_files}. Обработано {processed_size_mb:.2f} MB из {total_size_mb:.2f} MB")
            st.write(f"Обработка завершена для {input_directory}. Время работы: {total_time:.2f} секунд. Обработано файлов: {num_files}. Обработано {processed_size_mb:.2f} MB из {total_size_mb:.2f} MB")
