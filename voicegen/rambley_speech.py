from rvc_python.infer import infer_file, infer_files
import asyncio
import edge_tts
import subprocess
from voicegen.text_to_speech import speechGeneration
def VoiceGeneration(TEXT):
    speechGeneration(TEXT)
    # To process a single file:
    result = infer_file(
        input_path="voicegen/tts_speech.mp3",
        model_path="voicegen/Rambley-RVC/Rambley.pth",
        index_path="voicegen/Rambley-RVC/Rambley.index",  # Optional: specify path to index file if available
        device="cuda:0", # Use cpu or cuda  
        f0method="rmvpe",  # Choose between 'harvest', 'crepe', 'rmvpe', 'pm'
        f0up_key=0,  # Transpose setting
        opt_path="voicegen/Rambley.wav",
        index_rate=1.0,
        filter_radius=3,
        resample_sr=0,  # Set to desired sample rate or 0 for no resampling.
        rms_mix_rate=0.25,
        protect=0.50,
        version="v2"
    )


    print("Inference completed. Output saved to:", result)

