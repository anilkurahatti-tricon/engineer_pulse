import React from "react";
import {
  Box,
  Typography,
  CircularProgress,
  Chip,
  Button,
  LinearProgress,
  Divider,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import PsychologyIcon from "@mui/icons-material/Psychology";
import LightbulbOutlinedIcon from "@mui/icons-material/LightbulbOutlined";

export default function GapAnalysisPanel({
  gapData,
  employeeScore,
  loading,
  error,
  projectName,
  onOpenRecommender,
  hasRecommender,
  recommenderLoading,
}) {
  if (loading) {
    return (
      <Box className="right-panel-card">
        <Box className="panel-placeholder" sx={{ minHeight: 380 }}>
          <CircularProgress size={44} thickness={4} sx={{ color: "#28785c", mb: 2 }} />
          <Typography variant="h6" sx={{ fontWeight: 600, color: "#20342d" }}>
            Running AI Gap Analysis...
          </Typography>
          <Typography variant="body2" sx={{ color: "#697770", maxWidth: 300 }}>
            Analyzing candidate skills, target project requirements, and identifying prioritized technical gaps.
          </Typography>
        </Box>
      </Box>
    );
  }

  if (error) {
    return (
      <Box className="right-panel-card">
        <Box className="panel-placeholder" sx={{ minHeight: 250 }}>
          <WarningAmberIcon sx={{ fontSize: 48, color: "#9f332c" }} />
          <Typography variant="h6" sx={{ color: "#9f332c", fontWeight: 600 }}>
            Analysis Error
          </Typography>
          <Typography variant="body2" sx={{ color: "#697770" }}>
            {error}
          </Typography>
        </Box>
      </Box>
    );
  }

  if (!gapData) {
    return (
      <Box className="right-panel-card">
        <Box className="panel-placeholder" sx={{ minHeight: 380 }}>
          <PsychologyIcon className="placeholder-icon" />
          <Typography variant="h6" sx={{ fontWeight: 600, color: "#20342d" }}>
            Select an Employee
          </Typography>
          <Typography variant="body2" sx={{ color: "#697770", maxWidth: 300, lineHeight: 1.6 }}>
            Click the <strong>&quot;Analyse Gap&quot;</strong> button on any employee to generate a real-time skills gap analysis and unlock the AI Recommender.
          </Typography>
        </Box>
      </Box>
    );
  }

  const rawScore =
    employeeScore !== undefined && employeeScore !== null
      ? employeeScore
      : gapData.overall_readiness_score;
  const score = Math.round(rawScore || 0);
  const scoreClass = score >= 70 ? "high" : score >= 50 ? "medium" : "low";

  return (
    <Box className="right-panel-card">
      {/* Header */}
      <Box className="panel-header">
        <Box>
          <Typography className="panel-header-title">
            {gapData.employee_name || "Employee"}
          </Typography>
          <Typography className="panel-header-subtitle">
            Gap Analysis for <strong>{projectName || "Target Project"}</strong> • {gapData.experience_years || 0} yrs experience
          </Typography>
        </Box>
        <Box className="readiness-score-pill">
          <span className={`readiness-score-value ${scoreClass}`}>{score}%</span>
          <span className="readiness-score-label">Readiness</span>
        </Box>
      </Box>

      {/* Readiness Bar */}
      <Box sx={{ mb: 2 }}>
        <LinearProgress
          variant="determinate"
          value={score}
          sx={{
            height: 8,
            borderRadius: 4,
            backgroundColor: "#dce8df",
            "& .MuiLinearProgress-bar": {
              backgroundColor: score >= 70 ? "#28785c" : score >= 50 ? "#8a6112" : "#9f332c",
              borderRadius: 4,
            },
          }}
        />
      </Box>

      {/* AI Summary */}
      {gapData.summary && (
        <Box className="gap-summary-quote">
          <Typography variant="body2" sx={{ fontStyle: "italic" }}>
            &ldquo;{gapData.summary}&rdquo;
          </Typography>
        </Box>
      )}

      {/* Unlock Recommender Banner if available */}
      {hasRecommender && (
        <Box
          sx={{
            background: "#f6f8f5",
            border: "1px solid #b5cebe",
            borderLeft: "3px solid #28785c",
            borderRadius: 1,
            p: 1.5,
            mb: 2.5,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 1.5,
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <AutoAwesomeIcon sx={{ color: "#459474", fontSize: 20 }} />
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 700, color: "#20342d" }}>
                Recommender Ready
              </Typography>
              <Typography variant="caption" sx={{ color: "#697770" }}>
                Generate a custom 6-month upskilling roadmap for {gapData.employee_name}
              </Typography>
            </Box>
          </Box>
          <Button
            className="btn-recommender"
            onClick={onOpenRecommender}
            disabled={recommenderLoading}
            startIcon={recommenderLoading ? <CircularProgress size={16} color="inherit" /> : <AutoAwesomeIcon />}
            sx={{ whiteSpace: "nowrap" }}
          >
            {recommenderLoading ? "Generating..." : "Recommendor"}
          </Button>
        </Box>
      )}

      {/* Strengths */}
      {gapData.strengths && gapData.strengths.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography className="section-title">
            <CheckCircleIcon sx={{ color: "#28785c", fontSize: 18 }} />
            Key Strengths ({gapData.strengths.length})
          </Typography>
          <Box sx={{ display: "flex", flexWrap: "wrap" }}>
            {gapData.strengths.map((item, idx) => {
              const skillName = typeof item === "string" ? item : item.skill;
              const reason = typeof item === "object" ? item.reason : "";
              return (
                <Chip
                  key={idx}
                  icon={<CheckCircleIcon sx={{ fontSize: "14px !important", color: "#059669 !important" }} />}
                  label={reason ? `${skillName}: ${reason}` : skillName}
                  sx={{
                    m: 0.3,
                    bgcolor: "#dff0e5",
                    color: "#267451",
                    border: "1px solid #b8dfcb",
                    fontWeight: 500,
                    fontSize: "0.8rem",
                    maxWidth: "100%",
                    height: "auto",
                    py: 0.4,
                    "& .MuiChip-label": {
                      whiteSpace: "normal",
                      display: "block",
                    },
                  }}
                />
              );
            })}
          </Box>
        </Box>
      )}

      <Divider sx={{ my: 1.5 }} />

      {/* Skill Gaps */}
      {gapData.gaps && gapData.gaps.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography className="section-title">
            <WarningAmberIcon sx={{ color: "#8a6112", fontSize: 18 }} />
            Identified Skill Gaps ({gapData.gaps.length})
          </Typography>
          {gapData.gaps.map((gap, idx) => {
            const skill = typeof gap === "string" ? gap : gap.skill;
            const priority = (gap.priority || "Medium").toLowerCase();
            return (
              <Box key={idx} className="gap-item-card">
                <Box className="gap-item-header">
                  <span className="gap-item-skill">{skill}</span>
                  <span className={`gap-item-priority ${priority}`}>{gap.priority || "Medium"}</span>
                </Box>
                {gap.reason && <p className="gap-item-reason">{gap.reason}</p>}
                {gap.recommended_action && (
                  <p className="gap-item-action">
                    <strong>Action:</strong> {gap.recommended_action}
                  </p>
                )}
              </Box>
            );
          })}
        </Box>
      )}

      {/* Areas of Improvement */}
      {gapData.areas_of_improvement && gapData.areas_of_improvement.length > 0 && (
        <Box sx={{ mb: 1 }}>
          <Typography className="section-title">
            <LightbulbOutlinedIcon sx={{ color: "#459474", fontSize: 18 }} />
            Areas of Improvement
          </Typography>
          {gapData.areas_of_improvement.map((areaItem, idx) => (
            <Box key={idx} sx={{ mb: 1, p: 1.2, bgcolor: "#f6f8f5", borderRadius: 1, border: "1px solid #e5ebe6" }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 600, color: "#20342d", fontSize: "0.825rem" }}>
                {areaItem.area}
              </Typography>
              <Typography variant="body2" sx={{ color: "#697770", fontSize: "0.8rem", mt: 0.25 }}>
                {areaItem.recommendation}
              </Typography>
            </Box>
          ))}
        </Box>
      )}
    </Box>
  );
}
