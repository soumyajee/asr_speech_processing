from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from inference import ASRModelONNX
from utils import load_and_validate_audio, waveform_to_logmels

app = FastAPI()
model = ASRModelONNX("asr_model_fixed.onnx")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")
    file_bytes = await file.read()
    try:
        audio, sr = load_and_validate_audio(file_bytes)
        logmels = waveform_to_logmels(audio, sr)
        print("logmels shape:", logmels.shape)  # Debug
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    text = model.infer(logmels)
    return JSONResponse({"transcription": text})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
