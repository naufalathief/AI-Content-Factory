import {
    AbsoluteFill,
    Easing,
    Html5Audio,
    Img,
    Sequence,
    interpolate,
    staticFile,
    useCurrentFrame,
    useVideoConfig,
} from "remotion";

import {
    Motion,
    Timeline,
    TimelineClip,
} from "./types";

export type Props = {

    timeline: Timeline;

};

// Frames each clip overlaps the next one for a crossfade.
const CROSSFADE_FRAMES = 8;

const STILL: Motion = {

    name: "still",

    zoomStart: 1.04,

    zoomEnd: 1.04,

    xStart: 0,

    xEnd: 0,

    yStart: 0,

    yEnd: 0,

};

const asset = (path: string) => staticFile(path.replace(/^\/+/, ""));

const KenBurns = (
    {
        clip,
        length,
        fadeIn,
    }: {
        clip: TimelineClip;
        length: number;
        fadeIn: boolean;
    },
) => {

    const frame = useCurrentFrame();

    const { width, height } = useVideoConfig();

    const motion = clip.motion ?? STILL;

    const progress = interpolate(
        frame,
        [0, Math.max(1, length - 1)],
        [0, 1],
        {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.inOut(Easing.quad),
        },
    );

    const zoom = interpolate(progress, [0, 1], [motion.zoomStart, motion.zoomEnd]);

    // Never move further than the zoom margin, so no black edge shows.
    const maxX = ((zoom - 1) * width) / 2;

    const maxY = ((zoom - 1) * height) / 2;

    const clamp = (value: number, max: number) => Math.max(-max, Math.min(max, value));

    const x = clamp(interpolate(progress, [0, 1], [motion.xStart, motion.xEnd]), maxX);

    const y = clamp(interpolate(progress, [0, 1], [motion.yStart, motion.yEnd]), maxY);

    const opacity = fadeIn
        ? interpolate(frame, [0, CROSSFADE_FRAMES], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
        })
        : 1;

    return (

        <AbsoluteFill style={{ opacity }}>

            <Img
                src={asset(clip.image)}
                style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `translate(${x}px, ${y}px) scale(${zoom})`,
                }}
            />

        </AbsoluteFill>

    );

};

export const Video = (
    {
        timeline,
    }: Props,
) => {

    const lastIndex = timeline.clips.length - 1;

    return (

        <AbsoluteFill
            style={{
                backgroundColor: "black",
            }}
        >

            {
                timeline.audio
                    ? <Html5Audio src={asset(timeline.audio)} />
                    : null
            }

            {

                timeline.clips.map(

                    (clip, i) => {

                        // Each clip stays on screen a little longer while the
                        // next one fades in on top of it.
                        const length = clip.durationFrames
                            + (i < lastIndex ? CROSSFADE_FRAMES : 0);

                        return (

                            <Sequence
                                key={clip.index}
                                from={clip.startFrame}
                                durationInFrames={length}
                            >

                                <KenBurns
                                    clip={clip}
                                    length={length}
                                    fadeIn={i > 0}
                                />

                            </Sequence>

                        );

                    },

                )

            }

        </AbsoluteFill>

    );

};
