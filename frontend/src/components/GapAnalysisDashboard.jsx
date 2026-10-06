import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./GapAnalysisDashboard.css";

const defaultGapAnalysis = {
  employee_name: "Rohan",
  experience_years: 7,
  overall_readiness_score: 55,
  strengths: [
    { skill: "C#", reason: "Core language experience across .NET projects." },
    { skill: ".NET", reason: "Strong foundation in building and maintaining applications." },
    { skill: "SQL", reason: "Comfortable working with relational data and queries." },
    { skill: "REST APIs", reason: "Experience integrating and developing service endpoints." },
  ],
  gaps: [
    {
      skill: "Docker",
      priority: "High",
      reason: "Limited experience packaging applications into containers.",
      recommended_action: "Containerize a small .NET service and add a multi-stage build.",
    },
    {
      skill: "Kubernetes",
      priority: "High",
      reason: "Production orchestration concepts need further development.",
      recommended_action: "Deploy the containerized service to a local Kubernetes cluster.",
    },
    {
      skill: "CI/CD pipelines",
      priority: "Medium",
      reason: "Pipeline ownership and automation experience is limited.",
      recommended_action: "Create a pipeline that runs tests and publishes a build artifact.",
    },
    {
      skill: "Cloud monitoring",
      priority: "Low",
      reason: "Observability practices could be more hands-on.",
      recommended_action: "Add structured logging, health checks, and a basic dashboard.",
    },
  ],
  areas_of_improvement: [
    {
      area: "Containerization & orchestration",
      recommendation: "Build and deploy a containerized .NET service, then practice scaling and rollout strategies.",
    },
    {
      area: "Delivery automation",
      recommendation: "Automate testing and deployment in a CI/CD pipeline with clear quality checks.",
    },
    {
      area: "Cloud operations",
      recommendation: "Add health checks, centralized logs, and actionable alerts to a sample application.",
    },
  ],
  summary:
    "Rohan brings solid .NET experience and a dependable foundation in application development. Focused practice with containers, orchestration, and delivery automation will strengthen readiness for modern cloud-native projects.",
};

const PRIORITIES = [
  { name: "High", color: "#dc5a4b" },
  { name: "Medium", color: "#e3a72f" },
  { name: "Low", color: "#489878" },
];

function getPriorityCounts(gaps) {
  return PRIORITIES.map(({ name }) => ({
    priority: name,
    count: gaps.filter((gap) => gap.priority?.toLowerCase() === name.toLowerCase()).length,
  }));
}

function ReadinessGauge({ score }) {
  const boundedScore = Math.min(100, Math.max(0, Number(score) || 0));
  const gaugeData = [
    { name: "Ready", value: boundedScore },
    { name: "Remaining", value: 100 - boundedScore },
  ];

  return (
    <div className="gap-readiness" aria-label={`Overall readiness score: ${boundedScore} out of 100`}>
      <div className="gap-gauge-chart">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={gaugeData}
              dataKey="value"
              cx="50%"
              cy="92%"
              startAngle={180}
              endAngle={0}
              innerRadius="72%"
              outerRadius="100%"
              paddingAngle={0}
              stroke="none"
            >
              <Cell fill="#73c5a2" />
              <Cell fill="rgba(255,255,255,0.16)" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="gap-gauge-label" aria-hidden="true">
          <strong>{boundedScore}</strong>
          <span>/ 100</span>
        </div>
      </div>
      <span className="gap-readiness-caption">Overall readiness</span>
    </div>
  );
}

export default function GapAnalysisDashboard({ data = defaultGapAnalysis }) {
  const strengths = data.strengths ?? [];
  const gaps = data.gaps ?? [];
  const areas = data.areas_of_improvement ?? [];
  const priorityCounts = getPriorityCounts(gaps);

  return (
    <main className="gap-dashboard">
      <header className="gap-hero">
        <div className="gap-hero-copy">
          <span className="gap-eyebrow">TALENT DEVELOPMENT / GAP ANALYSIS</span>
          <h1>{data.employee_name ?? "Employee"}</h1>
          <p>{data.experience_years ?? 0} years of experience</p>
        </div>
        <ReadinessGauge score={data.overall_readiness_score} />
      </header>

      <section className="gap-summary gap-panel" aria-labelledby="gap-summary-title">
        <div className="gap-section-heading">
          <span className="gap-section-index">01</span>
          <h2 id="gap-summary-title">At a glance</h2>
        </div>
        <p>{data.summary}</p>
      </section>

      <section className="gap-panel" aria-labelledby="gap-strengths-title">
        <div className="gap-section-heading">
          <span className="gap-section-index">02</span>
          <div>
            <h2 id="gap-strengths-title">Core strengths</h2>
            <p className="gap-section-subtitle">Skills already contributing to role readiness</p>
          </div>
          <span className="gap-count">{strengths.length} skills</span>
        </div>
        <div className="gap-strength-grid">
          {strengths.map((strength) => (
            <article className="gap-strength" key={strength.skill}>
              <span className="gap-strength-mark" aria-hidden="true">+</span>
              <div>
                <h3>{strength.skill}</h3>
                <p>{strength.reason}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="gap-panel" aria-labelledby="gap-gaps-title">
        <div className="gap-section-heading">
          <span className="gap-section-index">03</span>
          <div>
            <h2 id="gap-gaps-title">Priority gaps</h2>
            <p className="gap-section-subtitle">Focus areas ranked by urgency</p>
          </div>
          <span className="gap-count">{gaps.length} gaps</span>
        </div>

        <div className="gap-chart-wrap" role="img" aria-label="Bar chart showing gap counts by priority">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={priorityCounts} margin={{ top: 12, right: 12, bottom: 0, left: -18 }}>
              <CartesianGrid vertical={false} stroke="#e8ece8" />
              <XAxis dataKey="priority" tickLine={false} axisLine={false} tick={{ fill: "#66736d", fontSize: 12 }} />
              <YAxis allowDecimals={false} tickLine={false} axisLine={false} tick={{ fill: "#87918c", fontSize: 11 }} />
              <Tooltip
                cursor={{ fill: "#f3f6f3" }}
                contentStyle={{ border: "1px solid #e2e8e3", borderRadius: 8, fontSize: 12 }}
                formatter={(value) => [`${value} ${value === 1 ? "gap" : "gaps"}`, "Count"]}
              />
              <Bar dataKey="count" name="Gaps" radius={[5, 5, 0, 0]} maxBarSize={64}>
                {PRIORITIES.map((priority) => <Cell key={priority.name} fill={priority.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="gap-list" role="list" aria-label="Gap details">
          {gaps.map((gap) => (
            <article className="gap-row" role="listitem" key={gap.skill}>
              <div className="gap-row-main">
                <div className="gap-row-title">
                  <h3>{gap.skill}</h3>
                  <span className={`gap-priority gap-priority-${gap.priority?.toLowerCase() ?? "low"}`}>
                    {gap.priority ?? "Unranked"}
                  </span>
                </div>
                <p className="gap-reason">{gap.reason}</p>
                <p className="gap-action"><strong>Recommended action</strong>{gap.recommended_action}</p>
              </div>
            </article>
          ))}
          {gaps.length === 0 && <p className="gap-empty">No priority gaps identified.</p>}
        </div>
      </section>

      <section className="gap-panel" aria-labelledby="gap-improvement-title">
        <div className="gap-section-heading">
          <span className="gap-section-index">04</span>
          <div>
            <h2 id="gap-improvement-title">Areas of improvement</h2>
            <p className="gap-section-subtitle">Practical next steps for continued growth</p>
          </div>
        </div>
        <div className="gap-improvement-grid">
          {areas.map((item, index) => (
            <article className="gap-improvement" key={item.area}>
              <span className="gap-improvement-number">0{index + 1}</span>
              <h3>{item.area}</h3>
              <p>{item.recommendation}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
