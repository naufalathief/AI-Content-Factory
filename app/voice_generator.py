import asyncio

import edge_tts

VOICE = "id-ID-ArdiNeural"


async def _generate(text: str, output_path: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
    )

    await communicate.save(output_path)


def generate_voice(text: str, output_path: str):
    asyncio.run(
        _generate(
            text=text,
            output_path=output_path,
        )
    )
