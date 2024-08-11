import edge_tts
import asyncio

def speechGeneration(TEXT):
    VOICE = "en-US-AvaNeural"   # Model voice, CHANGE CAREFUL!
    OUTPUT_FILE = "tts_speech.mp3" # Output directory
    async def amain() -> None:
        """Main function"""
        communicate = edge_tts.Communicate(TEXT, VOICE)
        await communicate.save(OUTPUT_FILE)


    if __name__ == "__main__":
        asyncio.run(amain())
speechGeneration(TEXT)