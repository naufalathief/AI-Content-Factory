import {
    Composition,
} from "remotion";

import {
    Video,
} from "./video";

import {
    Timeline,
} from "./types";

export const RemotionRoot = () => {

    return (

        <Composition

            id="AIContentFactory"

            component={Video}

            width={1080}

            height={1920}

            fps={30}

            durationInFrames={900}

            defaultProps={

                {

                    timeline: {

                        videoId: 0,

                        width: 1080,

                        height: 1920,

                        fps: 30,

                        totalDuration: 30,

                        totalFrames: 900,

                        audio: "",

                        subtitle: "",

                        clips: [],

                    }

                }

            }

        />

    );

};