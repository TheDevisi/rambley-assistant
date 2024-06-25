from rvc_python.infer import infer_file, infer_files
import asyncio

import edge_tts

with open("voicegen/answer.txt" , 'r') as f:
    TEXT = f.readline()


VOICE = "en-US-AvaNeural"   # Model voice, CHANGE CAREFUL!
OUTPUT_FILE = "voicegen/tts_speech.mp3" # Output directory


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

if __name__ == "__main__":
    asyncio.run(amain())

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

