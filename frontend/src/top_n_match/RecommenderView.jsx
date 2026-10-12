import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import SchoolIcon from "@mui/icons-material/School";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";
import FlagIcon from "@mui/icons-material/Flag";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CloseIcon from "@mui/icons-material/Close";

export default function RecommenderView({ open, onClose, roadmapData }) {
  if (!roadmapData) return null;

  const startScore = roadmapData.starting_readiness_score || 0;
  const targetScore = roadmapData.target_readiness_score || 95;

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        },
      }}
    >
      <DialogTitle
        sx={{
          background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)",
          color: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          pb: 2,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
          <AutoAwesomeIcon sx={{ color: "#a78bfa", fontSize: 28 }} />
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 700, color: "white" }}>
              AI Recommender: 6-Month Upskilling Roadmap
            </Typography>
            <Typography variant="body2" sx={{ color: "#c7d2fe" }}>
              Tailored growth plan for <strong>{roadmapData.employee_name}</strong> ({roadmapData.role || "Software Engineer"})
            </Typography>
          </Box>
        </Box>
        <Button
          onClick={onClose}
          sx={{ color: "#c7d2fe", minWidth: 36, p: 0.5 }}
          aria-label="close"
        >
          <CloseIcon />
        </Button>
      </DialogTitle>

      <DialogContent sx={{ p: 3, bgcolor: "#f8fafc" }}>
        {/* Goal Card & Readiness Progression */}
        <Box
          sx={{
            bgcolor: "white",
            p: 2.5,
            borderRadius: 2.5,
            border: "1px solid #e2e8f0",
            mb: 3,
            boxShadow: "0 2px 4px rgba(0,0,0,0.03)",
          }}
        >
          <Typography variant="subtitle2" sx={{ color: "#6b21a8", fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, mb: 0.5 }}>
            Overall Upskilling Objective
          </Typography>
          <Typography variant="body1" sx={{ color: "#1e293b", fontWeight: 500, lineHeight: 1.6, mb: 2 }}>
            {roadmapData.overall_goal}
          </Typography>

          <Divider sx={{ my: 1.5 }} />

          <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-around", flexWrap: "wrap", gap: 2 }}>
            <Box sx={{ textAlign: "center" }}>
              <Typography variant="caption" sx={{ color: "#64748b", fontWeight: 600 }}>
                CURRENT READINESS
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 800, color: "#f59e0b" }}>
                {startScore}%
              </Typography>
            </Box>

            <Typography variant="h5" sx={{ color: "#94a3b8", fontWeight: 300 }}>
              ➔
            </Typography>

            <Box sx={{ textAlign: "center" }}>
              <Typography variant="caption" sx={{ color: "#64748b", fontWeight: 600 }}>
                TARGET READINESS
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 800, color: "#10b981" }}>
                {targetScore}%
              </Typography>
            </Box>

            <Box sx={{ textAlign: "center" }}>
              <Typography variant="caption" sx={{ color: "#64748b", fontWeight: 600 }}>
                DURATION
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 800, color: "#6366f1" }}>
                {roadmapData.roadmap_duration_months || 6} Mo
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Monthly Plan Accordions */}
        <Typography variant="h6" sx={{ fontWeight: 700, color: "#0f172a", mb: 1.5, display: "flex", alignItems: "center", gap: 1 }}>
          <SchoolIcon sx={{ color: "#4f46e5" }} />
          Curated Monthly Learning Curriculum
        </Typography>

        <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
          {roadmapData.monthly_plan?.map((monthPlan, idx) => (
            <Accordion
              key={idx}
              defaultExpanded={idx === 0}
              sx={{
                borderRadius: "10px !important",
                border: "1px solid #e2e8f0",
                "&:before": { display: "none" },
                boxShadow: "0 1px 3px rgba(0,0,0,0.03)",
                overflow: "hidden",
              }}
            >
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                sx={{
                  bgcolor: "white",
                  "&:hover": { bgcolor: "#f8fafc" },
                  borderLeft: "5px solid #6366f1",
                }}
              >
                <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, flexWrap: "wrap", width: "100%", pr: 1 }}>
                  <Chip
                    label={`Month ${monthPlan.month}`}
                    size="small"
                    sx={{
                      bgcolor: "#ede9fe",
                      color: "#5b21b6",
                      fontWeight: 700,
                      borderRadius: 1.5,
                    }}
                  />
                  <Typography sx={{ fontWeight: 700, color: "#1e293b", fontSize: "0.95rem" }}>
                    {monthPlan.title}
                  </Typography>
                  <Box sx={{ ml: "auto", display: "flex", alignItems: "center", gap: 0.5, color: "#64748b" }}>
                    <AccessTimeIcon sx={{ fontSize: 16 }} />
                    <Typography variant="caption" sx={{ fontWeight: 600 }}>
                      ~{monthPlan.estimated_weekly_hours || 5}h / week
                    </Typography>
                  </Box>
                </Box>
              </AccordionSummary>

              <AccordionDetails sx={{ bgcolor: "#fafafa", p: 2.5, borderTop: "1px solid #f1f5f9" }}>
                {/* Focus Skills */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" sx={{ fontWeight: 700, color: "#475569", textTransform: "uppercase" }}>
                    Focus Skills:
                  </Typography>
                  <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mt: 0.5 }}>
                    {monthPlan.focus_skills?.map((skill, sIdx) => (
                      <Chip
                        key={sIdx}
                        label={skill}
                        size="small"
                        sx={{ bgcolor: "#e0e7ff", color: "#3730a3", fontWeight: 600, fontSize: "0.75rem" }}
                      />
                    ))}
                  </Box>
                </Box>

                {/* Objectives */}
                {monthPlan.objectives && monthPlan.objectives.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: "#475569", textTransform: "uppercase" }}>
                      Key Objectives:
                    </Typography>
                    <Box component="ul" sx={{ pl: 2.5, m: "0.35rem 0 0 0", color: "#334155", fontSize: "0.85rem" }}>
                      {monthPlan.objectives.map((obj, oIdx) => (
                        <li key={oIdx} style={{ marginBottom: "0.25rem" }}>{obj}</li>
                      ))}
                    </Box>
                  </Box>
                )}

                {/* Recommended Resources */}
                {monthPlan.learning_resources && monthPlan.learning_resources.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: "#475569", textTransform: "uppercase" }}>
                      Recommended Resources:
                    </Typography>
                    <Box sx={{ display: "flex", flexDirection: "column", gap: 0.75, mt: 0.5 }}>
                      {monthPlan.learning_resources.map((res, rIdx) => (
                        <Box
                          key={rIdx}
                          sx={{
                            p: 1.25,
                            bgcolor: "white",
                            borderRadius: 1.5,
                            border: "1px solid #e2e8f0",
                            display: "flex",
                            alignItems: "flex-start",
                            gap: 1,
                          }}
                        >
                          <Chip
                            label={res.type}
                            size="small"
                            sx={{
                              bgcolor: "#f1f5f9",
                              color: "#475569",
                              fontSize: "0.7rem",
                              fontWeight: 700,
                              textTransform: "uppercase",
                              height: 22,
                            }}
                          />
                          <Box>
                            <Typography variant="subtitle2" sx={{ fontWeight: 700, color: "#0f172a", fontSize: "0.85rem" }}>
                              {res.title}
                            </Typography>
                            {res.description && (
                              <Typography variant="caption" sx={{ color: "#64748b" }}>
                                {res.description}
                              </Typography>
                            )}
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  </Box>
                )}

                {/* Practical Tasks */}
                {monthPlan.practical_tasks && monthPlan.practical_tasks.length > 0 && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" sx={{ fontWeight: 700, color: "#475569", textTransform: "uppercase" }}>
                      Hands-on Practical Tasks:
                    </Typography>
                    <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5, mt: 0.5 }}>
                      {monthPlan.practical_tasks.map((task, tIdx) => (
                        <Box key={tIdx} sx={{ display: "flex", alignItems: "flex-start", gap: 1 }}>
                          <AssignmentTurnedInIcon sx={{ color: "#10b981", fontSize: 16, mt: 0.3 }} />
                          <Typography variant="body2" sx={{ color: "#334155", fontSize: "0.825rem" }}>
                            {task}
                          </Typography>
                        </Box>
                      ))}
                    </Box>
                  </Box>
                )}

                {/* Milestone */}
                {monthPlan.milestone && (
                  <Box
                    sx={{
                      p: 1.25,
                      bgcolor: "#ecfdf5",
                      border: "1px solid #a7f3d0",
                      borderRadius: 1.5,
                      display: "flex",
                      alignItems: "center",
                      gap: 1,
                    }}
                  >
                    <FlagIcon sx={{ color: "#059669", fontSize: 18 }} />
                    <Typography variant="body2" sx={{ color: "#065f46", fontWeight: 600, fontSize: "0.825rem" }}>
                      <strong>Milestone:</strong> {monthPlan.milestone}
                    </Typography>
                  </Box>
                )}
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2, bgcolor: "white", borderTop: "1px solid #e2e8f0" }}>
        <Button onClick={onClose} variant="contained" sx={{ bgcolor: "#4f46e5", px: 3 }}>
          Done
        </Button>
      </DialogActions>
    </Dialog>
  );
}
