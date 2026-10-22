export interface Motion {

    name: string;

    zoomStart: number;

    zoomEnd: number;

    xStart: number;

    xEnd: number;

    yStart: number;

    yEnd: number;

}

export interface TimelineClip {

    index: number;

    scene?: number;

    image: string;

    startTime: number;

    startFrame: number;

    duration: number;

    durationFrames: number;

    // Optional so timelines built before motion support still render.
    motion?: Motion;

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
