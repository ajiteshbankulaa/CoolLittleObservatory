import type { Mode } from "@/types/api";


interface TimelineBarProps {
  activeMode: Mode;
  playing: boolean;
  speed: number;
  follow: boolean;
  currentTimeLabel: string;
  onTogglePlaying: () => void;
  onCycleSpeed: () => void;
  onToggleFollow: () => void;
}


export function TimelineBar({
  activeMode,
  playing,
  speed,
  follow,
  currentTimeLabel,
  onTogglePlaying,
  onCycleSpeed,
  onToggleFollow,
}: TimelineBarProps) {
  const hidden = activeMode === "deep-space" || activeMode === "featured-tours";
  if (hidden) {
    return null;
  }

  return (
    <footer className="timeline-bar panel-shell">
      <div className="timeline-bar__summary">
        <span className="eyebrow">Timeline</span>
        <strong>{currentTimeLabel}</strong>
      </div>
      <div className="timeline-bar__actions">
        <button type="button" onClick={onTogglePlaying}>
          {playing ? "Pause" : "Play"}
        </button>
        <button type="button" onClick={onCycleSpeed}>
          {speed}x speed
        </button>
        <button type="button" onClick={onToggleFollow} className={follow ? "is-active" : ""}>
          {follow ? "Following target" : "Free camera"}
        </button>
      </div>
    </footer>
  );
}
