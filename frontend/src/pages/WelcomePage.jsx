import { Alert, Box, Card, CardActionArea, CardContent, CircularProgress, Stack, Typography } from "@mui/material";
import ChatIcon from "@mui/icons-material/Chat";
import RateReviewIcon from "@mui/icons-material/RateReview";
import ScienceIcon from "@mui/icons-material/Science";
import WorkspacePremiumIcon from "@mui/icons-material/WorkspacePremium";
import { Link } from "react-router-dom";
import { useWelcome } from "../business/useWelcome";

const FALLBACK_FEATURES = [
  { title: "Top N Match", description: "Find the best matches for your project.", path: "/top-n-match" },
  { title: "Skill Match", description: "Match skills to project requirements.", path: "/gap-analysis" },
  { title: "AI Chatbot", description: "Ask questions and get AI-assisted answers.", path: "/chatbot" },
  // { title: "Demo Sandbox", description: "Full CRUD playground used to validate the layered setup.", path: "/demo" },
];

const FEATURE_ICONS = {
  "/top-n-match": <RateReviewIcon color="primary" />,
  "/gap-analysis": <WorkspacePremiumIcon color="primary" />,
  "/chatbot": <ChatIcon color="primary" />,  
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
        <Typography variant="subtitle1" color="text.secondary">
          {info?.tagline || "Understand, support, and grow your engineering team."}
        </Typography>
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
          <Card key={feature.title}>
            <CardActionArea component={Link} to={feature.path} sx={{ height: "100%" }}>
              <CardContent>
                <Stack direction="row" spacing={1} sx={{ mb: 1, alignItems: "center" }}>
                  {FEATURE_ICONS[feature.path] || <ScienceIcon color="primary" />}
                  <Typography variant="h6" component="h2">
                    {feature.title}
                  </Typography>
                </Stack>
                <Typography variant="body2" color="text.secondary">
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
