from nemo.collections.asr.models import EncDecCTCModel

model = EncDecCTCModel.restore_from("stt_hi_conformer_ctc_medium.nemo")
with open("vocab.txt", "w", encoding="utf-8") as f:
    for token in model.decoder.vocabulary:
        f.write(token + "\n")
print("Vocab size:", len(model.decoder.vocabulary))
