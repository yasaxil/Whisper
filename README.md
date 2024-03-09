# Whisper Large-v3

This repository is dedicated to Whisper Large-v3, a powerful tool for high-quality conversion of audio messages to text. It provides unique settings and configurations to ensure accurate and precise conversion of *.ogg or *.mp3 files to *.text format.

|  Configuration | Specifications	Detail | 
|--------------------|--------------------|
| Processor  | Intel® Core™ i9-14900KF @3.20Ghz  |
| Memory  | 128 GB DDR4 4200 Mhz (32+32+32+32)  |
| Disk  | M.2 PCIe SSD Samsung SSD 980 PRO 1000Gb  |
| Disk  | M.2 PCIe SSD XPG GAMMIX S11 Pro 1000Gb |
| Discrete Graphics  | NVIDIA GeForce RTX 4090 24GB  |
| Whisper | Large-v3  |
| CudaToolkit | ver.12.3  |


## Features

- Advanced audio processing algorithms for superior quality transcription
- Customizable settings to fine-tune the conversion process
- Support for various audio formats, including *.ogg and *.mp3
- Easy integration with existing systems and applications

## Installation

To use Whisper Large-v3, follow these steps:

"pip install -U openai-whisper"

"pip install git+https://github.com/openai/whisper.git "

"pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git"

"pip install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html"

"pip install setuptools-rust"

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Configure the settings according to your specific requirements.
4. Run the application and start converting audio messages to text.

## Usage

Here's how you can use Whisper Large-v3 in your projects:

```python
import whisper

# Функция для обработки пакета файлов
def process_files(files, input_dir, output_dir):
    for filename in files:
        try:
            # Путь к исходному файлу .ogg
            ogg_path = os.path.join(input_dir, filename)
            # Путь к конвертированному файлу .wav
            wav_path = os.path.join(output_dir, filename[:-4] + '.wav')
            # Путь к текстовому файлу с результатом
            txt_path = os.path.join(output_dir, filename[:-4] + '.txt')

            with torch.no_grad():

# Инициализация модели Whisper на GPU
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
processor = AutoProcessor.from_pretrained(model_id)

            with torch.no_grad():

                # Конвертируем .ogg в .wav
                audio = AudioSegment.from_ogg(ogg_path)
                audio.export(wav_path, format="wav")

                # Транскрибируем аудиофайл
                result = pipe(wav_path)

                # Записываем результат в текстовый файл
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(filename[:-4] + ': \n"' + result["text"] + '"\n')
```

Make sure to refer to the [documentation](https://github.com/yasaxil) for detailed instructions and additional examples.

## My optimal setting whisper config

```python
# Настройки конфигурации для модели whisper
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    device="cuda:0",
)
```
## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). For more information, please see the [LICENSE](LICENSE) file.

## Author

This repository is maintained by [yasaxil](https://github.com/yasaxil). If you have any questions or suggestions, feel free to reach out.
