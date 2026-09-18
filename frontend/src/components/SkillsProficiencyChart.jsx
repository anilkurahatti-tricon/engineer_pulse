import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { chartTheme } from "../theme";

const LEVELS = ["Beginner", "Intermediate", "Advanced"];
const LEVEL_COLORS = [chartTheme.barAlt, chartTheme.bar, "#34d399"];

export default function SkillsProficiencyChart({ items, height = 240 }) {
  const counts = LEVELS.map((level) => ({
    level,
    count: items.filter((item) => item.proficiency_level === level).length,
  }));
  const yMax = Math.max(...counts.map((item) => item.count), 4);
  const data = counts.map((item) => ({
    ...item,
    remainder: yMax - item.count,
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 24, right: 12, left: 16, bottom: 20 }}>
        <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
        <XAxis dataKey="level" type="category" interval={0} stroke={chartTheme.tick} tickMargin={8} />
        <YAxis
          allowDecimals={false}
          domain={[0, yMax]}
          width={56}
          stroke={chartTheme.tick}
          tickMargin={8}
          label={{
            value: "Count",
            angle: -90,
            position: "insideLeft",
            offset: 12,
            fill: chartTheme.tick,
          }}
        />
        <Tooltip
          formatter={(value, name) => (name === "remainder" ? [null] : [value, "People"])}
          contentStyle={{
            background: chartTheme.tooltipBackground,
            border: `1px solid ${chartTheme.tooltipBorder}`,
          }}
        />
        <Bar dataKey="count" stackId="level" maxBarSize={64} name="count">
          {data.map((entry) => (
            <Cell key={entry.level} fill={LEVEL_COLORS[LEVELS.indexOf(entry.level)]} />
          ))}
        </Bar>
        <Bar
          dataKey="remainder"
          stackId="level"
          fill="rgba(192, 132, 252, 0.12)"
          radius={[6, 6, 0, 0]}
          maxBarSize={64}
          name="remainder"
          legendType="none"
        >
          <LabelList dataKey="count" position="top" fill={chartTheme.tick} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
