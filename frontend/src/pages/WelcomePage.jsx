import { Alert, Box, Card, CardActionArea, CardContent, CircularProgress, Stack, Typography } from "@mui/material";
import ChatIcon from "@mui/icons-material/Chat";
import RateReviewIcon from "@mui/icons-material/RateReview";
import ScienceIcon from "@mui/icons-material/Science";
import WorkspacePremiumIcon from "@mui/icons-material/WorkspacePremium";
import { Link } from "react-router-dom";
import { useWelcome } from "../business/useWelcome";

const FALLBACK_FEATURES = [
  { title: "Employee Feedback", description: "Capture and review feedback for every engineer.", path: "/employee-feedback" },
  { title: "Employee Skills", description: "Track skills and proficiency levels across the team.", path: "/employee-skills" },
  { title: "AI Chatbot", description: "Ask questions and get AI-assisted answers.", path: "/chatbot" },
  { title: "Demo Sandbox", description: "Full CRUD playground used to validate the layered setup.", path: "/demo" },
];

const FEATURE_ICONS = {
  "/employee-feedback": <RateReviewIcon color="primary" />,
  "/employee-skills": <WorkspacePremiumIcon color="primary" />,
  "/chatbot": <ChatIcon color="primary" />,
  "/demo": <ScienceIcon color="primary" />,
};

export default function WelcomePage() {
  const { info, loading, error } = useWelcome();
  const features = info?.features?.length ? info.features : FALLBACK_FEATURES;

  return (
    <Stack spacing={4} sx={{ alignItems: "center" }}>
      <Box sx={{ textAlign: "center", maxWidth: 640 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {info?.app_name || "Engineer Pulse"}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          {info?.tagline || "Understand, support, and grow your engineering team."}
        </Typography>
        {info?.description && (
          <Typography color="text.secondary">{info.description}</Typography>
        )}
      </Box>

      {loading && <CircularProgress />}
      {error && <Alert severity="warning">Couldn&apos;t reach the API: {error}</Alert>}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
          gap: 2,
          width: "100%",
        }}
      >
        {features.map((feature) => (
          <Card
            key={feature.title}
            sx={{ bgcolor: "#f8fafc", color: "#1f2933" }}
          >
            <CardActionArea component={Link} to={feature.path} sx={{ height: "100%" }}>
              <CardContent>
                <Stack direction="row" spacing={1} sx={{ mb: 1, alignItems: "center" }}>
                  {FEATURE_ICONS[feature.path] || <ScienceIcon color="primary" />}
                  <Typography variant="h6" component="h2" sx={{ color: "#1f2933" }}>
                    {feature.title}
                  </Typography>
                </Stack>
                <Typography variant="body2" sx={{ color: "#52606d" }}>
                  {feature.description}
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        ))}
      </Box>
    </Stack>
  );
}
