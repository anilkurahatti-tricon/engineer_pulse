import { useEffect, useState } from "react";
import {
  Alert,
  Button,
  Checkbox,
  CircularProgress,
  FormControl,
  InputLabel,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Select,
} from "@mui/material";
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
import {
  analyzeGap,
  generateRoadmap,
  getGapAnalysisOptions,
} from "../dataservice/gapAnalysisDataService";
import "./GapAnalysisDashboard.css";

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
  const hasScore = score !== null && score !== undefined && Number.isFinite(Number(score));
  const boundedScore = hasScore ? Math.min(100, Math.max(0, Number(score))) : 0;
  const gaugeData = [
    { name: "Ready", value: boundedScore },
    { name: "Remaining", value: 100 - boundedScore },
  ];

  return (
    <div
      className="gap-readiness"
      aria-label={hasScore ? `Overall readiness score: ${boundedScore} out of 100` : "Overall readiness score pending"}
    >
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
          <strong>{hasScore ? boundedScore : "--"}</strong>
          {hasScore && <span>/ 100</span>}
        </div>
      </div>
      <span className="gap-readiness-caption">Overall readiness</span>
    </div>
  );
}

function getApiErrorMessage(error) {
  const detail = error.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg).join("; ");
  return error.message || "Unable to identify skill gaps. Please try again.";
}

export default function SkillMatchPage() {
  const [employees, setEmployees] = useState([]);
  const [projects, setProjects] = useState([]);
  const [employeeId, setEmployeeId] = useState("");
  const [projectIds, setProjectIds] = useState([]);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [optionsError, setOptionsError] = useState("");
  const [gapData, setGapData] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");
  const [isRoadmapView, setIsRoadmapView] = useState(false);
  const [roadmapData, setRoadmapData] = useState(null);
  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [roadmapError, setRoadmapError] = useState("");

  useEffect(() => {
    let isCurrent = true;
    getGapAnalysisOptions()
      .then((options) => {
        if (!isCurrent) return;
        setEmployees(options.employees ?? []);
        setProjects(options.projects ?? []);
      })
      .catch((requestError) => {
        if (isCurrent) setOptionsError(getApiErrorMessage(requestError));
      })
      .finally(() => {
        if (isCurrent) setOptionsLoading(false);
      });
    return () => { isCurrent = false; };
  }, []);

  const handleIdentifyGaps = async () => {
    if (!employeeId || projectIds.length === 0) return;
    setAnalysisLoading(true);
    setAnalysisError("");
    setRoadmapError("");
    setGapData(null);
    setRoadmapData(null);
    setIsRoadmapView(false);
    try {
      const result = await analyzeGap(Number(employeeId), projectIds);
      setGapData(result);
    } catch (requestError) {
      setAnalysisError(getApiErrorMessage(requestError));
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleGenerateRoadmap = async () => {
    if (!gapData) return;
    setIsRoadmapView(true);
    setRoadmapLoading(true);
    setRoadmapError("");
    try {
      const result = await generateRoadmap(Number(employeeId), gapData);
      setRoadmapData(result);
    } catch (requestError) {
      setRoadmapError(getApiErrorMessage(requestError));
    } finally {
      setRoadmapLoading(false);
    }
  };

  const strengths = gapData?.strengths ?? [];
  const gaps = gapData?.gaps ?? [];
  const areas = gapData?.areas_of_improvement ?? [];
  const priorityCounts = getPriorityCounts(gaps);
  const selectedEmployee = employees.find((employee) => employee.id === Number(employeeId));

  return (
    <main className={`gap-dashboard${isRoadmapView ? " gap-dashboard--roadmap" : ""}`}>
      <section className="gap-controls gap-panel" aria-labelledby="skill-match-title">
        <div className="gap-controls-copy">
          <span className="gap-eyebrow gap-eyebrow-light">SKILL MATCH</span>
          <h1 id="skill-match-title">Skill Match</h1>
          <p>Select an employee and target projects to assess role readiness.</p>
        </div>
        {optionsError && <Alert severity="error">{optionsError}</Alert>}
        <div className="gap-selectors">
          <FormControl fullWidth size="small" disabled={optionsLoading}>  
            <InputLabel id="skill-match-employee-label">Employee</InputLabel>
            <Select
              labelId="skill-match-employee-label"
              value={employeeId}
              label="Employee"
              onChange={(event) => {
                setEmployeeId(event.target.value);
                setGapData(null);
                setRoadmapData(null);
                setIsRoadmapView(false);
              }}
            >
              {employees.map((employee) => (
                <MenuItem key={employee.id} value={String(employee.id)}>
                  {employee.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth size="small" disabled={optionsLoading}>
            <InputLabel id="skill-match-projects-label">Projects</InputLabel>
            <Select
              multiple
              labelId="skill-match-projects-label"
              value={projectIds}
              onChange={(event) => {
                setProjectIds(event.target.value.map(Number));
                setGapData(null);
                setRoadmapData(null);
                setIsRoadmapView(false);
              }}
              input={<OutlinedInput label="Projects" />}
              renderValue={(selected) => selected
                .map((id) => projects.find((project) => project.id === id)?.name)
                .filter(Boolean)
                .join(", ")}
            >
              {projects.map((project) => (
                <MenuItem key={project.id} value={project.id}>
                  <Checkbox checked={projectIds.includes(project.id)} />
                  <ListItemText primary={project.name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          {optionsLoading && <CircularProgress size={22} aria-label="Loading employees and projects" />}
        </div>
      </section>

      <div className={`gap-workspace${isRoadmapView ? " gap-workspace--roadmap" : ""}`}>
          <div className="gap-results">
            <header className="gap-hero">
              <div className="gap-hero-copy">
                <span className="gap-eyebrow">SKILL MATCH</span>
                <h2>{gapData?.employee_name ?? selectedEmployee?.name ?? "Select an employee"}</h2>
                {gapData && <p>{gapData.experience_years ?? 0} years of experience</p>}
              </div>
              <ReadinessGauge score={gapData?.overall_readiness_score} />
            </header>

            <div className="gap-workflow-actions">
              <Button
                variant="contained"
                onClick={handleIdentifyGaps}
                disabled={!employeeId || projectIds.length === 0 || analysisLoading || optionsLoading}
              >
                {analysisLoading ? "Identifying..." : "Identify Gaps"}
              </Button>
              <Button
                variant="outlined"
                onClick={handleGenerateRoadmap}
                disabled={!gapData || analysisLoading || roadmapLoading}
              >
                {roadmapLoading ? "Generating Roadmap..." : "Generate Roadmap"}
              </Button>
            </div>
            {analysisError && <Alert severity="error">{analysisError}</Alert>}
            {analysisLoading && (
              <div className="gap-status" role="status" aria-live="polite">
                <CircularProgress size={20} />
                <span>Analyzing skills against selected projects...</span>
              </div>
            )}

            {gapData && <>
            <section className="gap-summary gap-panel" aria-labelledby="gap-summary-title">
              <div className="gap-section-heading">
                <span className="gap-section-index">01</span>
                <h2 id="gap-summary-title">At a glance</h2>
              </div>
              <p>{gapData.summary}</p>
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
                    <div><h3>{strength.skill}</h3><p>{strength.reason}</p></div>
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
                    <div className="gap-row-title">
                      <h3>{gap.skill}</h3>
                      <span className={`gap-priority gap-priority-${gap.priority?.toLowerCase() ?? "low"}`}>
                        {gap.priority ?? "Unranked"}
                      </span>
                    </div>
                    <p className="gap-reason">{gap.reason}</p>
                    <p className="gap-action"><strong>Recommended action</strong>{gap.recommended_action}</p>
                  </article>
                ))}
                {gaps.length === 0 && <p className="gap-empty">No priority gaps identified.</p>}
              </div>
            </section>

            {areas.length > 0 && (
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
            )}
            </>}
          </div>
          {isRoadmapView && (
            <aside className="gap-roadmap-panel gap-panel" aria-labelledby="roadmap-title">
              <div className="gap-roadmap-person">
                <div>
                  <span className="gap-section-index">ROADMAP FOR</span>
                  <h2>{gapData.employee_name || selectedEmployee?.name || "Employee"}</h2>
                </div>
                <div className="gap-roadmap-score">
                  <span>Readiness</span>
                  <strong>{gapData.overall_readiness_score}<small>/100</small></strong>
                </div>
              </div>
              <div className="gap-roadmap-content">
                <h2 id="roadmap-title">Learning roadmap</h2>
                {roadmapLoading && (
                  <div className="gap-roadmap-placeholder" role="status">
                    <CircularProgress size={24} />
                    <span>Building a personalized roadmap...</span>
                  </div>
                )}
                {roadmapError && <Alert severity="error">{roadmapError}</Alert>}
                {!roadmapLoading && !roadmapData && !roadmapError && (
                  <div className="gap-roadmap-placeholder">
                    <span className="gap-roadmap-placeholder-mark" aria-hidden="true">+</span>
                    <p>Your roadmap will appear here.</p>
                    <span>Generate a learning plan from the identified gaps.</span>
                  </div>
                )}
                {roadmapData && <RoadmapDetails roadmap={roadmapData} />}
              </div>
            </aside>
          )}
      </div>
    </main>
  );
}

function RoadmapDetails({ roadmap }) {
  const months = roadmap.monthly_plan ?? [];
  return (
    <div className="gap-roadmap-details">
      {roadmap.overall_goal && <p className="gap-roadmap-goal">{roadmap.overall_goal}</p>}
      {roadmap.target_readiness_score != null && (
        <p className="gap-roadmap-target">Target readiness: <strong>{roadmap.target_readiness_score}/100</strong></p>
      )}
      {months.map((month) => (
        <article className="gap-roadmap-month" key={month.month}>
          <span>MONTH {month.month}</span>
          <h3>{month.title}</h3>
          {month.focus_skills?.length > 0 && <p><strong>Focus:</strong> {month.focus_skills.join(", ")}</p>}
          {month.milestone && <p><strong>Milestone:</strong> {month.milestone}</p>}
          {month.practical_tasks?.length > 0 && (
            <ul>{month.practical_tasks.map((task) => <li key={task}>{task}</li>)}</ul>
          )}
        </article>
      ))}
      {roadmap.summary && <p className="gap-roadmap-summary">{roadmap.summary}</p>}
    </div>
  );
}
