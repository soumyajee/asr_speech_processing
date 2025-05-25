import numpy as np
import onnxruntime

class ASRModelONNX:
    def __init__(self, model_path):
        self.session = onnxruntime.InferenceSession(model_path)
        self.input_names = [i.name for i in self.session.get_inputs()]
        self.output_name = self.session.get_outputs()[0].name
        self.vocab = self._load_vocab()

    def _load_vocab(self):
        try:
            with open("vocab.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            # Dummy vocab; replace with real vocab for real output!
            return [str(i) for i in range(100)]

    def infer(self, logmels):
        # logmels: [n_mels, time]
        if not isinstance(logmels, np.ndarray):
            logmels = np.array(logmels, dtype=np.float32)
        if logmels.ndim != 2:
            raise ValueError(f"logmels must be 2D, got shape {logmels.shape}")
        features = np.expand_dims(logmels, axis=0)  # [1, 80, time]
        length = np.array([features.shape[-1]], dtype=np.int64)  # [1]
        inputs = {
            self.input_names[0]: features.astype(np.float32),
            self.input_names[1]: length
        }
        logits = self.session.run([self.output_name], inputs)[0]  # [1, time, vocab]
        pred_ids = np.argmax(logits, axis=-1)[0]  # [time]
        print("pred_ids:", pred_ids)  # Debug
        tokens = self._greedy_decode(pred_ids)
        print("tokens:", tokens)  # Debug
        text = self._tokens_to_text(tokens)
        print("text:", text)  # Debug
        print("vocab[128]:", self.vocab[128] if len(self.vocab) > 128 else "Index 128 missing!")
        return text

    def _greedy_decode(self, pred_ids, blank_id=0):
        tokens = []
        prev = blank_id
        for idx in pred_ids:
            if idx != prev and idx != blank_id:
                tokens.append(idx)
            prev = idx
        return tokens

    def _tokens_to_text(self, tokens):
        if self.vocab:
            chars = [self.vocab[t] for t in tokens if t < len(self.vocab)]
            return "".join(chars)
        else:
            return str(tokens)
