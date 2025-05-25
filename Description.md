Description of FastAPI-based ASR Application
Features Successfully Implemented

Model Preparation: Successfully loaded the NVIDIA NeMo stt_hi_conformer_ctc_medium model and converted it to ONNX format for optimized inference. The model supports transcription of 5–10 second audio clips sampled at 16kHz.
FastAPI Application: Implemented a FastAPI server with a /transcribe POST endpoint that accepts .wav files and returns transcribed text as JSON. Added input validation to check file type (.wav) and duration (5–10 seconds).
Containerization: Created a Dockerfile based on python:3.9-slim to containerize the application. The FastAPI server runs on port 8000 using uvicorn.
Documentation: Provided a README.md with instructions to build and run the Docker container, along with a sample curl command to test the /transcribe endpoint.
Preprocessing/Inference: Implemented audio preprocessing to resample and normalize input audio, and integrated ONNX runtime for model inference.

Issues Encountered During Development

ONNX Conversion: Faced challenges converting the NeMo model to ONNX due to unsupported CTC decoder operations, which requires 129 token size after conversion of .onnx format so i have to resized the token size to 128 as per the no of decoder classes.
Dependency Conflicts: Installing NeMo alongside FastAPI dependencies caused version mismatches with PyTorch, leading to runtime errors.
Empty Transcription: While extraction of vocabulary or word from original nemo extension file all words are hindi alphabet only that has saved imside vocab.txt file so it requires the correct hindi audio with proper tone and no background noise with 5-10 seconds duration then only it should get proper transcription Hindi.And the transcription word that go is mimsatch with original audio content of speaker.
Audio Validation: Validating audio duration was tricky due to varying file formats, requiring additional libraries like pydub for robust parsing.
Docker Image Size: The Docker image size was larger than desired due to the inclusion of NeMo and ONNX runtime dependencies.

Reasons for Not Implementing Certain Components

Async Inference: Did not implement async model inference due to time constraints and limited familiarity with async-compatible ONNX runtimes. The synchronous inference pipeline was prioritized to ensure functionality.
Bonus Features (CI/CD, Testing): Lacked time to set up a CI/CD pipeline or comprehensive unit tests. Focused on core functionality to meet the deadline.
Model Optimization Limitations: While ONNX conversion was achieved, further optimizations (e.g., quantization) were not explored due to complexity and lack of documentation for NeMo-specific workflows.

How to Overcome the Challenges

ONNX Conversion: Consult NVIDIA NeMo’s GitHub issues or forums for updated ONNX export scripts. Alternatively, explore TorchScript as a fallback if ONNX issues persist.
Dependency Conflicts: Use a requirements.txt file with pinned versions (e.g., torch==1.12.0, nemo_toolkit==1.18.0) and test in a virtual environment to isolate conflicts.
Audio Validation: Leverage librosa or soundfile for more robust audio processing and validation, ensuring compatibility with various .wav formats.
Docker Image Size: Use multi-stage builds in the Dockerfile to reduce image size by excluding unnecessary build dependencies. Explore lighter base images like python:3.9-alpine if compatible with NeMo.
Async Inference: Study onnxruntime’s async capabilities or use aiofiles for async file handling. Allocate time to test async performance with sample audio files.
Bonus Features: Set up a basic GitHub Actions workflow for CI/CD and write unit tests using pytest for the FastAPI endpoint and preprocessing logic.

Known Limitations and Assumptions

Limitations:
The application assumes input audio is 16kHz mono .wav files. Other formats (e.g., MP3, stereo) require additional preprocessing.
The ONNX model may have slight accuracy degradation compared to the original NeMo model due to conversion trade-offs.
The Docker image size is approximately 2GB due to large dependencies, which could be optimized further.
The inference pipeline is synchronous, which may limit scalability under high concurrency.


Assumptions:
The deployment environment has sufficient CPU/GPU resources for ONNX inference.
Input audio clips are 5–10 seconds long, as specified in the requirements.
Users have Docker installed and basic knowledge of running containers and sending HTTP requests.
The NeMo model is suitable for the target language (Hindi) and generalizes well to typical audio inputs.




