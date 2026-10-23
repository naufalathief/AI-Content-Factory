import {
    CalculateMetadataFunction,
    Composition,
} from "remotion";

import {
    Props,
    Video,
} from "./video";

const defaultProps: Props = {

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

    },

};

// Size, fps and length come from the timeline, so the video is exactly as
// long as the narration instead of a fixed 30 seconds.
const calculateMetadata: CalculateMetadataFunction<Props> = ({ props }) => {

    const { timeline } = props;

    return {

        durationInFrames: Math.max(1, Math.round(timeline.totalFrames)),

        fps: timeline.fps,

        width: timeline.width,

        height: timeline.height,

    };

};

export const RemotionRoot = () => {

    return (

        <Composition

            id="AIContentFactory"

            component={Video}

            width={1080}

            height={1920}

            fps={30}

            durationInFrames={900}

            defaultProps={defaultProps}

            calculateMetadata={calculateMetadata}

        />

    );

};
