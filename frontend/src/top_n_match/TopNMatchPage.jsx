import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  CircularProgress,
  Chip,
  Alert,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import PeopleAltOutlinedIcon from "@mui/icons-material/PeopleAltOutlined";
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import CheckCircleOutlinedIcon from "@mui/icons-material/CheckCircleOutlined";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";

import { topNMatchService } from "./topNMatchService";
import GapAnalysisPanel from "./GapAnalysisPanel";
import RecommenderView from "./RecommenderView";
import "./topNMatch.css";

export default function TopNMatchPage() {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [topN, setTopN] = useState("");
  const [matchData, setMatchData] = useState(null);
  const [loadingMatches, setLoadingMatches] = useState(false);

  // Gap Analysis states
  // Map of employeeId -> gap analysis result. Recommender button is visible ONLY if analyzedGaps[employeeId] exists!
  const [analyzedGaps, setAnalyzedGaps] = useState({});
  const [analyzingEmployeeId, setAnalyzingEmployeeId] = useState(null);
  const [activeEmployee, setActiveEmployee] = useState(null);
  const [gapAnalysisError, setGapAnalysisError] = useState(null);

  // Recommender Roadmap states
  const [recommenderMap, setRecommenderMap] = useState({});
  const [recommenderLoadingId, setRecommenderLoadingId] = useState(null);
  const [activeRoadmap, setActiveRoadmap] = useState(null);
  const [recommenderModalOpen, setRecommenderModalOpen] = useState(false);

  // Notification / Alert
  const [alertInfo, setAlertInfo] = useState(null);

  // Load available projects on mount
  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await topNMatchService.getProjects();
        setProjects(data || []);
      } catch (err) {
        console.error("Could not fetch projects:", err);
      }
    }
    loadProjects();
  }, []);

  // Fetch top N matches
  const handleFindMatches = async () => {
    if (!selectedProjectId) {
      setAlertInfo({
        type: "warning",
        text: "Please select a target project from the dropdown first.",
      });
      return;
    }
    setLoadingMatches(true);
    setAlertInfo(null);
    try {
      const data = await topNMatchService.matchTopNEmployees(selectedProjectId, topN || 5);
      setMatchData(data);
      // Reset current active gap view if project changed
      setActiveEmployee(null);
    } catch (err) {
      setAlertInfo({ type: "error", text: "Failed to rank candidates. Please try again." });
    } finally {
      setLoadingMatches(false);
    }
  };

  // Matches are triggered when the user clicks "Find Matches" (or optionally on initial user action)


  // Click Handler for "Analyse Gap"
  const handleAnalyzeGap = async (employee) => {
    setActiveEmployee(employee);
    setAnalyzingEmployeeId(employee.employee_id);
    setGapAnalysisError(null);

    try {
      const gapResult = await topNMatchService.analyzeGap(
        employee.employee_id,
        [selectedProjectId]
      );
      // Store analyzed gap result for this employee
      setAnalyzedGaps((prev) => ({
        ...prev,
        [employee.employee_id]: gapResult,
      }));
      setAlertInfo({
        type: "success",
        text: `Gap analysis completed for ${employee.employee_name}! Recommender is now available.`,
      });
    } catch (err) {
      setGapAnalysisError("Failed to run gap analysis for this employee.");
    } finally {
      setAnalyzingEmployeeId(null);
    }
  };

  // Click Handler for "Recommendor"
  const handleOpenRecommender = async (employee) => {
    if (!employee) return;
    const gapResult = analyzedGaps[employee.employee_id];
    if (!gapResult) return;

    // Check if roadmap is already cached for this employee
    if (recommenderMap[employee.employee_id]) {
      setActiveRoadmap(recommenderMap[employee.employee_id]);
      setRecommenderModalOpen(true);
      return;
    }

    setRecommenderLoadingId(employee.employee_id);
    try {
      const roadmapResult = await topNMatchService.generateRecommenderRoadmap(
        gapResult,
        employee.employee_id
      );
      setRecommenderMap((prev) => ({
        ...prev,
        [employee.employee_id]: roadmapResult,
      }));
      setActiveRoadmap(roadmapResult);
      setRecommenderModalOpen(true);
    } catch (err) {
      setAlertInfo({
        type: "error",
        text: "Could not generate recommender roadmap at this moment.",
      });
    } finally {
      setRecommenderLoadingId(null);
    }
  };

  const currentProject = projects.find((p) => p.id === Number(selectedProjectId)) || {
    project_name: matchData?.project_name || "Project",
    tech_stack_summary: ".NET & Cloud",
  };

  return (
    <Box className="top-n-container">
      {/* Header and Filter Card */}
      <Box className="top-n-header-card">
        <div className="top-n-hero-copy">
          <span className="top-n-eyebrow">AI Talent Matching</span>
          <Typography className="top-n-title">
            <PeopleAltOutlinedIcon sx={{ fontSize: 28, color: "#a8d9c0" }} />
            Top-N Employee Match
          </Typography>
          <Typography className="top-n-subtitle">
            Rank and match candidate engineers for project allocations based on technical readiness, experience, and skill alignment.
          </Typography>
        </div>

        {/* Project Selector & Top N Controls */}
        <Box className="top-n-controls">
          <FormControl fullWidth size="small" sx={{ bgcolor: "white", borderRadius: 1.5 }}>
            <Select
              value={selectedProjectId}
              onChange={(e) => setSelectedProjectId(e.target.value)}
              displayEmpty
              sx={{
                borderRadius: 1.5,
                bgcolor: "white",
                color: "#000000",
                "& .MuiSelect-select": {
                  color: "#000000",
                  py: 1,
                },
              }}
              renderValue={(selected) => {
                if (!selected) {
                  return <span style={{ color: "#000000", fontWeight: 600 }}>Target Project</span>;
                }
                const proj = projects.find((p) => p.id === Number(selected));
                return proj ? (
                  <span style={{ color: "#000000", fontWeight: 600 }}>
                    {proj.project_name}{" "}
                    <span style={{ color: "#334155", fontWeight: 400, fontSize: "0.85em" }}>
                      ({proj.technologies || proj.tech_stack_summary || ""})
                    </span>
                  </span>
                ) : (
                  <span style={{ color: "#000000", fontWeight: 600 }}>Target Project</span>
                );
              }}
            >
              <MenuItem value="" disabled sx={{ color: "#000000" }}>
                <span style={{ color: "#000000", fontWeight: 600 }}>Target Project</span>
              </MenuItem>
              {projects.map((proj) => (
                <MenuItem key={proj.id} value={proj.id} sx={{ color: "#000000" }}>
                  <strong>{proj.project_name}</strong> &nbsp;
                  <span style={{ color: "#64748b", fontSize: "0.85em" }}>
                    ({proj.technologies || proj.tech_stack_summary || ""})
                  </span>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ bgcolor: "white", borderRadius: 1.5, minWidth: 150 }}>
            <Select
              value={topN}
              onChange={(e) => setTopN(e.target.value)}
              displayEmpty
              sx={{
                borderRadius: 1.5,
                bgcolor: "white",
                color: "#000000",
                "& .MuiSelect-select": {
                  color: "#000000",
                  py: 1,
                },
              }}
              renderValue={(selected) => {
                if (!selected) {
                  return <span style={{ color: "#000000", fontWeight: 600 }}>Top Matches</span>;
                }
                return <span style={{ color: "#000000", fontWeight: 600 }}>Top {selected}</span>;
              }}
            >
              <MenuItem value="" disabled sx={{ color: "#000000" }}>
                <span style={{ color: "#000000", fontWeight: 600 }}>Top Matches</span>
              </MenuItem>
              <MenuItem value={3} sx={{ color: "#000000" }}>Top 3</MenuItem>
              <MenuItem value={5} sx={{ color: "#000000" }}>Top 5</MenuItem>
              <MenuItem value={8} sx={{ color: "#000000" }}>Top 8</MenuItem>
              <MenuItem value={10} sx={{ color: "#000000" }}>Top 10</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="contained"
            onClick={handleFindMatches}
            disabled={loadingMatches}
            startIcon={loadingMatches ? <CircularProgress size={18} color="inherit" /> : <SearchIcon />}
            sx={{
              bgcolor: "#28785c",
              px: 3,
              py: 1,
              fontWeight: 700,
              textTransform: "none",
              borderRadius: 1,
              whiteSpace: "nowrap",
              "&:hover": { bgcolor: "#20664d" },
            }}
          >
            {loadingMatches ? "Matching..." : "Find Matches"}
          </Button>
        </Box>
      </Box>

      {/* Alert message if any */}
      {alertInfo && (
        <Alert
          severity={alertInfo.type}
          onClose={() => setAlertInfo(null)}
          sx={{ borderRadius: 2 }}
        >
          {alertInfo.text}
        </Alert>
      )}

      {/* Main Grid: Left = Top N Matches list, Right = Gap Analysis display */}
      <Box className="top-n-main-grid">
        {/* Left Column: Ranked Employees */}
        <Box className="employees-list">
          <Typography variant="h6" sx={{ fontWeight: 600, color: "#ffffff", mb: 0.5 }}>
            Ranked Candidate Shortlist ({matchData?.employees?.length || 0})
          </Typography>

          {loadingMatches ? (
            <Box sx={{ p: 6, textAlign: "center", bgcolor: "white", borderRadius: 2, border: "1px solid #e5ebe6" }}>
              <CircularProgress size={36} sx={{ color: "#28785c" }} />
              <Typography sx={{ mt: 2, color: "#697770" }}>
                AI is scoring employees against project skill requirements...
              </Typography>
            </Box>
          ) : matchData?.employees?.length > 0 ? (
            matchData.employees.map((emp) => {
              const rank = emp.rank || 1;
              const rankClass = rank === 1 ? "rank-1" : rank === 2 ? "rank-2" : rank === 3 ? "rank-3" : "rank-other";
              const score = Math.round(emp.overall_readiness_score || 0);
              const scoreClass = score >= 70 ? "high" : score >= 50 ? "medium" : "low";
              const isSelected = activeEmployee?.employee_id === emp.employee_id;
              const isAnalyzing = analyzingEmployeeId === emp.employee_id;
              const isRecommenderLoading = recommenderLoadingId === emp.employee_id;

              // KEY REQUIREMENT:
              // Has gap analysis been completed for this employee?
              const hasGapAnalysis = Boolean(analyzedGaps[emp.employee_id]);

              return (
                <Box
                  key={emp.employee_id}
                  className={`employee-card ${isSelected ? "selected" : ""}`}
                >
                  <Box className="employee-card-header">
                    <Box className="employee-info-box">
                      <div className={`rank-badge ${rankClass}`}>
                        #{rank}
                      </div>
                      <Box>
                        <h3 className="employee-name">{emp.employee_name}</h3>
                        <p className="employee-role">
                          {emp.role || "Software Engineer"} • {emp.experience_years} yrs exp
                        </p>
                      </Box>
                    </Box>

                    <div className="readiness-score-pill">
                      <span className={`readiness-score-value ${scoreClass}`}>
                        {score}%
                      </span>
                      <span className="readiness-score-label">Readiness</span>
                    </div>
                  </Box>

                  {/* Skills summary */}
                  <Box className="employee-skills-section">
                    <Box className="skills-row">
                      <span className="skills-label">Matched:</span>
                      <Box className="skills-chips-wrapper">
                        {emp.matched_skills && emp.matched_skills.length > 0 ? (
                          emp.matched_skills.map((skill, sIdx) => (
                            <span key={sIdx} className="skill-chip matched">
                              <CheckCircleOutlinedIcon sx={{ fontSize: 13 }} />
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span style={{ color: "#697770", fontSize: "0.75rem" }}>None</span>
                        )}
                      </Box>
                    </Box>

                    <Box className="skills-row">
                      <span className="skills-label">Missing:</span>
                      <Box className="skills-chips-wrapper">
                        {emp.missing_skills && emp.missing_skills.length > 0 ? (
                          emp.missing_skills.map((skill, sIdx) => (
                            <span key={sIdx} className="skill-chip missing">
                              <HighlightOffIcon sx={{ fontSize: 13 }} />
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span style={{ color: "#28785c", fontSize: "0.75rem" }}>Fully Matched!</span>
                        )}
                      </Box>
                    </Box>
                  </Box>

                  {/* 2 Buttons:
                      1. Analyse Gap (always available)
                      2. Recommendor:
                         "first the recommendor should be hidden when we click the analyse gap
                          the gap analyses api should work and at the right end side it should
                          display it and then the recommendor button should be available"
                  */}
                  <Box className="employee-actions-row">
                    <Button
                      className="btn-analyze-gap"
                      onClick={() => handleAnalyzeGap(emp)}
                      disabled={isAnalyzing}
                      startIcon={
                        isAnalyzing ? (
                          <CircularProgress size={15} color="inherit" />
                        ) : (
                          <AssessmentOutlinedIcon sx={{ fontSize: 17 }} />
                        )
                      }
                    >
                      {isAnalyzing ? "Analyzing..." : "Analyse Gap"}
                    </Button>

                    {/* Recommendor Button is ONLY displayed when hasGapAnalysis is true! */}
                    {hasGapAnalysis && (
                      <Button
                        className="btn-recommender"
                        onClick={() => handleOpenRecommender(emp)}
                        disabled={isRecommenderLoading}
                        startIcon={
                          isRecommenderLoading ? (
                            <CircularProgress size={15} color="inherit" />
                          ) : (
                            <AutoAwesomeIcon sx={{ fontSize: 17 }} />
                          )
                        }
                      >
                        {isRecommenderLoading ? "Loading..." : "Recommendor"}
                      </Button>
                    )}
                  </Box>
                </Box>
              );
            })
          ) : (
            <Box sx={{ p: 5, textAlign: "center", bgcolor: "#f6f8f5", borderRadius: 2, border: "1px dashed #cbd8ce" }}>
              <PeopleAltOutlinedIcon sx={{ fontSize: 48, color: "#7bb396", mb: 1.5 }} />
              <Typography variant="h6" sx={{ fontWeight: 600, color: "#20342d", mb: 0.5 }}>
                Ready to Find Top Matches
              </Typography>
              <Typography variant="body2" sx={{ color: "#697770", maxWidth: 360, mx: "auto", mb: 2 }}>
                Select your target project and desired number of matches above, then click <strong>&quot;Find Matches&quot;</strong> to view AI-ranked candidates.
              </Typography>
              <Button
                variant="contained"
                onClick={handleFindMatches}
                startIcon={<SearchIcon />}
                sx={{ bgcolor: "#28785c", textTransform: "none", fontWeight: 600, "&:hover": { bgcolor: "#20664d" } }}
              >
                Find Matches Now
              </Button>
            </Box>
          )}
        </Box>

        {/* Right Column: Real-time Gap Analysis Display */}
        <Box>
          <GapAnalysisPanel
            gapData={activeEmployee ? analyzedGaps[activeEmployee.employee_id] : null}
            loading={analyzingEmployeeId !== null}
            error={gapAnalysisError}
            projectName={currentProject.project_name}
            hasRecommender={Boolean(activeEmployee && analyzedGaps[activeEmployee.employee_id])}
            onOpenRecommender={() => handleOpenRecommender(activeEmployee)}
            recommenderLoading={recommenderLoadingId === activeEmployee?.employee_id}
          />
        </Box>
      </Box>

      {/* Recommender Roadmap Dialog */}
      <RecommenderView
        open={recommenderModalOpen}
        onClose={() => setRecommenderModalOpen(false)}
        roadmapData={activeRoadmap}
      />
    </Box>
  );
}
