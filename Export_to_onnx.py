from nemo.collections.asr.models import EncDecCTCModel
# Load the model
asr_model = EncDecCTCModel.restore_from("stt_hi_conformer_ctc_medium.nemo")
# Force vocabulary size to 128
asr_model.cfg.decoder.num_classes = 128
asr_model.decoder.num_classes = 128

# Export to ONNX
try:
    asr_model.export("asr_model_fixed.onnx", onnx_opset_version=13, check_trace=True)
except Exception as e:
    print(f"Export failed: {e}")

