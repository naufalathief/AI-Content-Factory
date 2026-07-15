import {
    AbsoluteFill,
    Html5Audio,
    Img,
    Sequence,
    staticFile,
} from "remotion";

import { Timeline } from "./types";

type Props = {

    timeline: Timeline;

};

export const Video = (
    {
        timeline,
    }: Props,
) => {

    return (

        <AbsoluteFill
            style={{
                backgroundColor: "black",
            }}
        >

            <Html5Audio
                src={staticFile(
                    timeline.audio.replace(/^\/+/, "")
                )}
            />

            {

                timeline.clips.map(

                    clip => (

                        <Sequence
                            key={clip.index}
                            from={clip.startFrame}
                            durationInFrames={
                                clip.durationFrames
                            }
                        >

                            <Img
                                src={staticFile(
                                    clip.image.replace(/^\/+/, "")
                                )}
                                style={{
                                    width: "100%",
                                    height: "100%",
                                    objectFit: "cover",
                                }}
                            />

                        </Sequence>

                    )

                )

            }

        </AbsoluteFill>

    );

};