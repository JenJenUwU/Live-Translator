from faster_whisper import WhisperModel
def model_init(size="small",device="cuda",compute_type="float16"):
    model = WhisperModel(size,device=device,compute_type=compute_type)
    return model