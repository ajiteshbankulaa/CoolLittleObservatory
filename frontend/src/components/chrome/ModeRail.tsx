import { MODES } from "@/lib/modes";
import type { Mode } from "@/types/api";


interface ModeRailProps {
  activeMode: Mode;
  onSelectMode: (mode: Mode) => void;
  onPrefetchMode: (mode: Mode) => void;
}


export function ModeRail({ activeMode, onSelectMode, onPrefetchMode }: ModeRailProps) {
  return (
    <nav className="mode-rail" aria-label="Observatory modes">
      {MODES.map((mode) => {
        const active = mode.id === activeMode;
        return (
          <button
            key={mode.id}
            className={`mode-button ${active ? "is-active" : ""}`}
            type="button"
            onClick={() => onSelectMode(mode.id)}
            onMouseEnter={() => onPrefetchMode(mode.id)}
          >
            <span className="mode-button__label">{mode.shortLabel}</span>
            <span className="mode-button__kicker">{mode.kicker}</span>
          </button>
        );
      })}
    </nav>
  );
}
