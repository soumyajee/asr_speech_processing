import onnxruntime
session = onnxruntime.InferenceSession("asr_model_fixed.onnx")
for out in session.get_outputs():
    print(out.name, out.shape)
