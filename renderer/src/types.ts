export interface TimelineClip {

    index: number;

    image: string;

    startTime: number;

    startFrame: number;

    duration: number;

    durationFrames: number;

}

export interface Timeline {

    videoId: number;

    width: number;

    height: number;

    fps: number;

    totalDuration: number;

    totalFrames: number;

    audio: string;

    subtitle: string;

    clips: TimelineClip[];

}