FastAPI-based Automatic Speech Recognition (ASR) Application
Overview
This application provides a FastAPI-based server for transcribing 5–10 second Hindi audio clips using the NVIDIA NeMo stt_hi_conformer_ctc_medium model, optimized with ONNX for efficient inference. The application is containerized with Docker for easy deployment and includes input validation, audio preprocessing, and comprehensive documentation.
Features

Model: NVIDIA NeMo stt_hi_conformer_ctc_medium model converted to ONNX, supporting transcription of 16kHz Hindi audio clips.
API: FastAPI server with a /transcribe POST endpoint for uploading .wav files and returning JSON transcriptions.
Input Validation: Ensures uploaded files are .wav format, 5–10 seconds long, and sampled at 16kHz.
Containerization: Dockerized application using python:3.9-slim, running on port 8000 with uvicorn.
Preprocessing: Audio resampling and normalization to ensure compatibility with the model.
Documentation: Detailed README with setup, build, and usage instructions, including a sample curl command.

Installation and Setup
Prerequisites

Docker: Installed on your system.
Audio File: A 16kHz mono .wav file (5–10 seconds) for testing.
Tools: Basic familiarity with HTTP requests (e.g., using curl or Postman).

Steps

Clone the Repository:
git clone <repository-url>
cd <repository-directory>


Build the Docker Image:
docker build -t asr-fastapi .


Run the Docker Container:
docker run -p 8000:8000 asr-fastapi


Verify the Server:Access the interactive API documentation at http://localhost:8000/docs in a browser.


Usage
Transcribing Audio
Send a .wav file to the /transcribe endpoint using curl:
curl -X POST -F "file=@/path/to/audio.wav" http://localhost:8000/transcribe

Example Response:
{
  "transcription": "नमस्ते, यह एक परीक्षण है"
}

Converting Non-.wav Files
Convert other audio formats (e.g., MP3) to 16kHz mono .wav using ffmpeg:
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav

Notes

Ensure audio files are 5–10 seconds, 16kHz, mono, and in Hindi with clear pronunciation.
Test the API using the Swagger UI at http://localhost:8000/docs.

Technical Details
Application Flow

Audio Upload: User sends a .wav file to the /transcribe endpoint.
Preprocessing: Audio is resampled to 16kHz and normalized using pydub.
Inference: ONNX runtime processes the audio with the NeMo model and CTC decoder.
Response: Transcribed text is returned as JSON.

API Documentation
The FastAPI server provides interactive documentation at http://localhost:8000/docs, where users can test the /transcribe endpoint.
Model Preparation
The NVIDIA NeMo stt_hi_conformer_ctc_medium model was converted to ONNX format for optimized inference. The vocabulary is stored in vocab.txt and supports Hindi transcription.
Challenges and Solutions



Challenge
Impact
Solution



ONNX Conversion
Unsupported CTC decoder operations caused export errors.
Resized token size to 128 to match decoder classes; consulted NeMo GitHub.


Dependency Conflicts
PyTorch version mismatches with NeMo and FastAPI caused runtime errors.
Used a requirements.txt with pinned versions (e.g., torch==1.12.0, nemo_toolkit==1.18.0).


Empty Transcription
Noisy or non-Hindi audio led to empty or incorrect transcriptions.
Validated audio for Hindi, 16kHz, and no background noise using pydub.


Audio Validation
Inconsistent .wav formats caused validation failures.
Integrated pydub for robust audio parsing.


Large Docker Image
~2GB image size due to NeMo and ONNX dependencies.
Explored multi-stage builds and python:3.9-alpine (not fully implemented).


Limitations

Audio Format: Supports only 16kHz mono .wav files. Other formats require preprocessing.
Model Accuracy: ONNX conversion may slightly reduce accuracy compared to the original NeMo model.
Scalability: Synchronous inference limits performance under high concurrency.
Image Size: The Docker image (~2GB) is larger than ideal due to dependencies.

Workarounds:

Use ffmpeg to convert non-.wav files (see Usage).
Optimize Docker image with multi-stage builds for production.
Explore async inference for improved scalability.

Assumptions

Environment: Deployment system has sufficient CPU/GPU resources for ONNX inference.
Input Audio: Audio clips are 5–10 seconds, 16kHz, mono, and in Hindi with clear pronunciation.
User Knowledge: Users have Docker installed and basic familiarity with HTTP requests.

Future Improvements

Async Inference: Implement asynchronous inference with onnxruntime or aiofiles for better scalability.
Model Optimization: Explore quantization or pruning to reduce model size and latency.
CI/CD Pipeline: Set up GitHub Actions for automated testing and deployment.
Unit Tests: Add pytest tests for the /transcribe endpoint and preprocessing logic.
Multi-format Support: Extend preprocessing to handle MP3, stereo, or other formats natively.
Image Optimization: Use multi-stage Docker builds or python:3.9-alpine to reduce image size.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/xyz).
Commit your changes (git commit -m 'Add xyz feature').
Push to the branch (git push origin feature/xyz).
Open a pull request.

Please include tests and update this README for new features.
License
MIT License
Resources

NVIDIA NeMo Documentation
FastAPI Documentation






