import edge_tts
import asyncio
from rvc_python.infer import infer_file, infer_files

def speechGeneration(ai_response):
    VOICE = "en-US-AvaNeural"   # Model voice
    OUTPUT_FILE = "voicegen/tts_speech.mp3"  # Output file path

    async def amain() -> None:
        """Main function"""
        communicate = edge_tts.Communicate(ai_response, VOICE)
        await communicate.save(OUTPUT_FILE)

    asyncio.run(amain())

    # После генерации tts_speech.mp3 запускаем процесс преобразования речи
    result = infer_file(
        input_path=OUTPUT_FILE,
        model_path="voicegen/Rambley-RVC/Rambley.pth",
        index_path="voicegen/Rambley-RVC/Rambley.index",  # Optional: specify path to index file if available
        device="cuda:0",  # Use cpu or cuda
        f0method="rmvpe",  # Choose between 'harvest', 'crepe', 'rmvpe', 'pm'
        f0up_key=0,  # Transpose setting
        opt_path="voicegen/Rambley.wav",  # Output path
        index_rate=1.0,
        filter_radius=3,
        resample_sr=0,  # Set to desired sample rate or 0 for no resampling.
        rms_mix_rate=0.25,
        protect=0.50,
        version="v2"
    )

    print("Inference completed. Output saved to:", result)
