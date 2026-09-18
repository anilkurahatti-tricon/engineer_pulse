import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { chartTheme } from "../theme";

const LEVELS = ["Beginner", "Intermediate", "Advanced"];
const LEVEL_COLORS = [chartTheme.barAlt, chartTheme.bar, "#34d399"];

export default function SkillsProficiencyChart({ items }) {
  const data = LEVELS.map((level) => ({
    level,
    count: items.filter((item) => item.proficiency_level === level).length,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data}>
        <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
        <XAxis dataKey="level" stroke={chartTheme.tick} />
        <YAxis
          allowDecimals={false}
          stroke={chartTheme.tick}
          label={{ value: "Engineers", angle: -90, position: "insideLeft", fill: chartTheme.tick }}
        />
        <Tooltip
          contentStyle={{
            background: chartTheme.tooltipBackground,
            border: `1px solid ${chartTheme.tooltipBorder}`,
          }}
        />
        <Bar dataKey="count" radius={[6, 6, 0, 0]} name="People">
          {data.map((entry) => (
            <Cell key={entry.level} fill={LEVEL_COLORS[LEVELS.indexOf(entry.level)]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
