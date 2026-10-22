from app.schemas import Script
from app.timeline.timeline_builder import TimelineBuilder
from app.timeline.timeline_builder import block_start_times
from app.timeline.timeline_builder import scene_windows

SCRIPT = Script.from_dict(
    {
        "title": "Test",
        "scenes": [
            {
                "text": "One two three.",
                "keyword": "a",
                "visuals": [{"prompt": "a", "duration": 1.0}, {"prompt": "b", "duration": 1.0}],
            },
            {
                "text": "Four five.",
                "keyword": "b",
                "visuals": [{"prompt": "c", "duration": 2.0}],
            },
        ],
        "cta": "Follow!",
    }
)

WORDS = [
    {"text": "One", "start": 0.0, "end": 0.4},
    {"text": "two", "start": 0.4, "end": 0.8},
    {"text": "three", "start": 0.8, "end": 1.3},
    {"text": "Four", "start": 2.0, "end": 2.5},
    {"text": "five", "start": 2.5, "end": 3.0},
    {"text": "Follow", "start": 3.5, "end": 4.0},
]


def test_blocks_start_when_their_first_word_is_spoken():
    assert block_start_times(SCRIPT.narration(), WORDS) == [0.0, 2.0, 3.5]


def test_scene_windows_follow_the_voice_and_cover_the_cta():
    windows = scene_windows(SCRIPT, 4.6, WORDS)

    assert windows == [(0.0, 2.0), (2.0, 4.6)]


def test_scene_windows_without_timings_are_proportional():
    windows = scene_windows(SCRIPT, 10.0, None)

    assert windows[0][0] == 0.0
    assert windows[-1][1] == 10.0
    assert windows[0][1] == windows[1][0]


def test_clips_fill_the_whole_video_without_gaps():
    metadata = [
        {"scene": 1, "visual": 1, "file": "001.png", "duration": 1.0},
        {"scene": 1, "visual": 2, "file": "002.png", "duration": 1.0},
        {"scene": 2, "visual": 1, "file": "003.png", "duration": 2.0},
    ]

    clips = TimelineBuilder().place_clips(
        7,
        metadata,
        [(0.0, 2.0), (2.0, 4.6)],
        4.6,
    )

    assert [c["startFrame"] for c in clips] == [0, 30, 60]

    for current, following in zip(clips, clips[1:]):
        assert current["startFrame"] + current["durationFrames"] == following["startFrame"]

    last = clips[-1]
    assert last["startFrame"] + last["durationFrames"] == round(4.6 * 30)

    # Motion never repeats back to back and is the same on every render.
    names = [c["motion"]["name"] for c in clips]
    assert all(a != b for a, b in zip(names, names[1:]))
    assert names == [
        c["motion"]["name"]
        for c in TimelineBuilder().place_clips(7, metadata, [(0.0, 2.0), (2.0, 4.6)], 4.6)
    ]
