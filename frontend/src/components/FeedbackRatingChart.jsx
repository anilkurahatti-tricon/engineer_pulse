import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { chartTheme } from "../theme";

export default function FeedbackRatingChart({ items }) {
  const data = [1, 2, 3, 4, 5].map((rating) => ({
    rating: `${rating}`,
    count: items.filter((item) => Number(item.rating) === rating).length,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data}>
        <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
        <XAxis dataKey="rating" stroke={chartTheme.tick} label={{ value: "Rating", position: "insideBottom", offset: -2, fill: chartTheme.tick }} />
        <YAxis allowDecimals={false} stroke={chartTheme.tick} label={{ value: "Count", angle: -90, position: "insideLeft", fill: chartTheme.tick }} />
        <Tooltip
          contentStyle={{
            background: chartTheme.tooltipBackground,
            border: `1px solid ${chartTheme.tooltipBorder}`,
          }}
        />
        <Bar dataKey="count" fill={chartTheme.bar} radius={[6, 6, 0, 0]} name="Feedback count" />
      </BarChart>
    </ResponsiveContainer>
  );
}
