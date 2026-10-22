from app.generators.subtitle_generator import Word
from app.generators.subtitle_generator import format_time
from app.generators.subtitle_generator import generate_subtitle
from app.generators.subtitle_generator import restore_punctuation
from app.generators.subtitle_generator import segment_words


def test_format_time_never_produces_1000_ms():
    assert format_time(1.9996) == "00:00:02,000"
    assert format_time(0) == "00:00:00,000"
    assert format_time(3661.5) == "01:01:01,500"


def test_restore_punctuation_brings_back_script_spelling():
    text = "Did you know? The well-known Moon is drifting away, slowly."

    words = [
        Word("Did", 0.0, 0.2),
        Word("you", 0.2, 0.3),
        Word("know", 0.3, 0.6),
        Word("The", 0.8, 0.9),
        Word("well", 0.9, 1.1),
        Word("known", 1.1, 1.4),
        Word("Moon", 1.4, 1.7),
        Word("is", 1.7, 1.8),
        Word("drifting", 1.8, 2.2),
        Word("away", 2.2, 2.5),
        Word("slowly", 2.6, 3.0),
    ]

    restored = restore_punctuation(words, text)

    assert [w.text for w in restored] == [
        "Did", "you", "know?", "The", "well-known",
        "Moon", "is", "drifting", "away,", "slowly.",
    ]

    # The merged "well-known" spans both spoken tokens.
    well_known = restored[4]
    assert (well_known.start, well_known.end) == (0.9, 1.4)


def test_captions_split_at_sentence_end():
    words = [
        Word("First", 0.0, 0.4),
        Word("sentence", 0.4, 0.9),
        Word("ends", 0.9, 1.3),
        Word("here.", 1.3, 1.8),
        Word("Then", 2.0, 2.3),
        Word("another", 2.3, 2.8),
        Word("sentence", 2.8, 3.3),
        Word("follows.", 3.3, 3.9),
    ]

    captions = segment_words(words)

    assert len(captions) == 2
    assert captions[0].text.endswith("here.")
    assert captions[1].start == 2.0


def test_generate_subtitle_from_word_timings(tmp_path):
    words_path = tmp_path / "1.words.json"
    words_path.write_text(
        '[{"text": "Hello", "start": 0.1, "end": 0.5},'
        ' {"text": "world", "start": 0.5, "end": 1.0},'
        ' {"text": "again", "start": 1.0, "end": 1.6}]',
        encoding="utf-8",
    )

    output = tmp_path / "1.srt"

    generate_subtitle(
        tmp_path / "missing.mp3",
        output,
        words_path=words_path,
        text="Hello, world again!",
    )

    srt = output.read_text(encoding="utf-8")

    assert srt.startswith("1\n00:00:00,100 --> 00:00:01,600\nHello, world again!\n")
