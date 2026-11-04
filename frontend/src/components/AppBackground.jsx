import { Box } from "@mui/material";
import theme, { chartTheme } from "../theme";

const PRIMARY = theme.palette.primary.main;
const SECONDARY = theme.palette.secondary.main;

// Neural-network layers (AI motif): input -> hidden -> hidden -> output
const NEURAL_LAYERS = [
  { x: 90, ys: [60, 140, 220, 300] },
  { x: 230, ys: [40, 110, 180, 250, 320] },
  { x: 370, ys: [90, 180, 270] },
  { x: 490, ys: [140, 220] },
];

// Gear teeth as short radial lines around a circle (machine/hardware motif)
function gearTeeth(cx, cy, r, toothLen, count) {
  return Array.from({ length: count }, (_, i) => {
    const angle = (i / count) * Math.PI * 2;
    return {
      x1: cx + Math.cos(angle) * r,
      y1: cy + Math.sin(angle) * r,
      x2: cx + Math.cos(angle) * (r + toothLen),
      y2: cy + Math.sin(angle) * (r + toothLen),
    };
  });
}

const GEAR_BIG = { cx: 340, cy: 470, r: 36, teeth: gearTeeth(340, 470, 36, 13, 10) };
const GEAR_SMALL = { cx: 405, cy: 508, r: 22, teeth: gearTeeth(405, 508, 22, 10, 8) };

const SPARKLE_SPOTS = [
  { x: 560, y: 300, scale: 1, color: SECONDARY },
  { x: 840, y: 480, scale: 1.3, color: PRIMARY },
  { x: 1545, y: 210, scale: 0.9, color: SECONDARY },
  { x: 300, y: 420, scale: 0.8, color: PRIMARY },
];

// Decorative, low-opacity backdrop rendered once behind every page: soft color
// glows plus an AI/ML motif (neural network, sparkles) alongside an abstract
// "readiness score / skill match / roadmap" visual made of a bar chart, a
// sparkline, a skill-matching node graph and a milestone path.
export default function AppBackground() {
  return (
    <Box
      aria-hidden="true"
      sx={{
        position: "fixed",
        inset: 0,
        zIndex: -1,
        overflow: "hidden",
        bgcolor: "background.default",
        backgroundImage: `
          radial-gradient(640px circle at 6% 8%, ${PRIMARY}29, transparent 60%),
          radial-gradient(760px circle at 94% 14%, ${SECONDARY}24, transparent 60%),
          radial-gradient(900px circle at 50% 105%, ${PRIMARY}1f, transparent 65%)
        `,
      }}
    >
      <Box
        component="svg"
        viewBox="0 0 1600 900"
        preserveAspectRatio="xMidYMid slice"
        sx={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
      >
        <defs>
          <pattern id="ep-dot-grid" width="42" height="42" patternUnits="userSpaceOnUse">
            <circle cx="1.5" cy="1.5" r="1.5" fill={chartTheme.tick} opacity="0.18" />
          </pattern>
          <path
            id="ep-sparkle"
            d="M0,-11 C1,-3 3,-1 11,0 C3,1 1,3 0,11 C-1,3 -3,1 -11,0 C-3,-1 -1,-3 0,-11 Z"
          />
        </defs>

        <rect width="1600" height="900" fill="url(#ep-dot-grid)" opacity="0.35" />

        {/* AI neural network */}
        <g opacity="0.26" stroke={SECONDARY} strokeWidth="1.2">
          {NEURAL_LAYERS.slice(0, -1).flatMap((layer, i) => {
            const next = NEURAL_LAYERS[i + 1];
            return layer.ys.flatMap((y1) =>
              next.ys.map((y2) => (
                <line key={`${layer.x}-${y1}-${next.x}-${y2}`} x1={layer.x} y1={y1} x2={next.x} y2={y2} />
              ))
            );
          })}
        </g>
        <g opacity="0.45" fill={PRIMARY}>
          {NEURAL_LAYERS.flatMap((layer) =>
            layer.ys.map((y) => <circle key={`${layer.x}-${y}`} cx={layer.x} cy={y} r="7" />)
          )}
        </g>

        {/* AI robot/machine icon */}
        <g opacity="0.28" stroke={PRIMARY} strokeWidth="2.5" fill="none" strokeLinejoin="round">
          <rect x="105" y="420" width="90" height="75" rx="16" />
          <rect x="115" y="495" width="70" height="18" rx="6" />
          <rect x="98" y="440" width="10" height="24" rx="3" />
          <rect x="192" y="440" width="10" height="24" rx="3" />
          <line x1="150" y1="420" x2="150" y2="398" />
          <rect x="125" y="472" width="50" height="8" rx="4" />
        </g>
        <g opacity="0.4" fill={SECONDARY}>
          <circle cx="150" cy="394" r="5" />
          <circle cx="130" cy="450" r="6" />
          <circle cx="170" cy="450" r="6" />
        </g>

        {/* interlocking gears (machine motif) */}
        <g opacity="0.22" stroke={SECONDARY} strokeWidth="2" fill="none" strokeLinecap="round">
          <circle cx={GEAR_BIG.cx} cy={GEAR_BIG.cy} r={GEAR_BIG.r} />
          {GEAR_BIG.teeth.map((t) => (
            <line key={`${t.x1}-${t.y1}`} x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2} strokeWidth="6" />
          ))}
          <circle cx={GEAR_BIG.cx} cy={GEAR_BIG.cy} r="9" />
          <circle cx={GEAR_SMALL.cx} cy={GEAR_SMALL.cy} r={GEAR_SMALL.r} />
          {GEAR_SMALL.teeth.map((t) => (
            <line key={`${t.x1}-${t.y1}`} x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2} strokeWidth="5" />
          ))}
          <circle cx={GEAR_SMALL.cx} cy={GEAR_SMALL.cy} r="6" />
        </g>

        {/* AI sparkle accents */}
        <g>
          {SPARKLE_SPOTS.map((s) => (
            <use
              key={`${s.x}-${s.y}`}
              href="#ep-sparkle"
              x={s.x}
              y={s.y}
              fill={s.color}
              opacity="0.4"
              transform={`scale(${s.scale})`}
            />
          ))}
        </g>

        {/* readiness score bar chart */}
        <g opacity="0.22">
          {[120, 180, 90, 220, 150, 260, 110].map((h, i) => (
            <rect
              key={h + i}
              x={48 + i * 54}
              y={840 - h}
              width="34"
              height={h}
              rx="6"
              fill={PRIMARY}
            />
          ))}
        </g>

        {/* trend sparkline */}
        <g opacity="0.3" fill="none" stroke={SECONDARY} strokeWidth="3" strokeLinecap="round">
          <polyline points="680,170 780,120 880,150 980,80 1080,110 1180,55 1280,90 1380,40 1480,70" />
          {[680, 880, 1080, 1280, 1480].map((x, i) => (
            <circle
              key={x}
              cx={x}
              cy={[170, 150, 110, 90, 70][i]}
              r="5"
              fill={SECONDARY}
              stroke="none"
            />
          ))}
        </g>

        {/* skill-matching node graph */}
        <g opacity="0.2" stroke={PRIMARY} strokeWidth="1.5">
          <line x1="1120" y1="330" x2="1250" y2="400" />
          <line x1="1250" y1="400" x2="1200" y2="520" />
          <line x1="1250" y1="400" x2="1400" y2="440" />
          <line x1="1400" y1="440" x2="1480" y2="340" />
          <line x1="1200" y1="520" x2="1350" y2="580" />
          <line x1="1400" y1="440" x2="1350" y2="580" />
        </g>
        <g opacity="0.35" fill={SECONDARY}>
          <circle cx="1120" cy="330" r="7" />
          <circle cx="1250" cy="400" r="9" />
          <circle cx="1200" cy="520" r="6" />
          <circle cx="1400" cy="440" r="8" />
          <circle cx="1480" cy="340" r="6" />
          <circle cx="1350" cy="580" r="7" />
        </g>

        {/* roadmap milestone path */}
        <g opacity="0.25">
          <path
            d="M 980 760 Q 1120 700 1260 760 T 1540 760"
            fill="none"
            stroke={PRIMARY}
            strokeWidth="2.5"
            strokeDasharray="2 14"
            strokeLinecap="round"
          />
          {[980, 1190, 1400, 1540].map((x, i) => (
            <circle
              key={x}
              cx={x}
              cy={i % 2 === 0 ? 760 : 724}
              r="8"
              fill="none"
              stroke={SECONDARY}
              strokeWidth="2.5"
            />
          ))}
        </g>
      </Box>
    </Box>
  );
}
