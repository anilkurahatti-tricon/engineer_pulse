import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { chartTheme } from "../theme";

export default function FeedbackRatingChart({ items, height = 240 }) {
  const counts = [1, 2, 3, 4, 5].map((rating) => ({
    rating: String(rating),
    count: items.filter((item) => Number(item.rating) === rating).length,
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
        <XAxis
          dataKey="rating"
          type="category"
          interval={0}
          stroke={chartTheme.tick}
          tickMargin={8}
          label={{ value: "Rating", position: "insideBottom", offset: -12, fill: chartTheme.tick }}
        />
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
          formatter={(value, name) => (name === "remainder" ? [null] : [value, "Feedback count"])}
          contentStyle={{
            background: chartTheme.tooltipBackground,
            border: `1px solid ${chartTheme.tooltipBorder}`,
          }}
        />
        <Bar
          dataKey="count"
          stackId="rating"
          fill={chartTheme.bar}
          maxBarSize={64}
          name="count"
        />
        <Bar
          dataKey="remainder"
          stackId="rating"
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
