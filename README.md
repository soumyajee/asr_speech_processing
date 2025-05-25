FastAPI ASR Application (Hindi) – NVIDIA NeMo

This project is a containerized FastAPI application for Hindi Automatic Speech Recognition (ASR) using an NVIDIA NeMo model, optimized with ONNX. It transcribes 5–10 second, 16kHz mono .wav audio clips via a simple HTTP API.
🚀 Quickstart
1. Build the Docker Image

bash
docker build -t fastapi-asr .

2. Run the Container

bash
docker run -p 8000:8000 fastapi-asr
🎤 Test the /transcribe Endpoint
Sample cURL Request

bash
curl -X POST "http://localhost:8000/transcribe" -F "file=@test_hindi.wav"
Sample Postman Request

    Method: POST

    URL: http://localhost:8000/transcribe

    Body: form-data

        Key: file

        Type: File

        Value: (select your .wav file)

Expected Response:

json
{
  "transcription": "नमस्ते, यह एक परीक्षण ऑडियो क्लिप है।"
}

