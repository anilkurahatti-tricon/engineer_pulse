import { AppBar, Box, Button, Toolbar, Typography } from "@mui/material";
import ChatIcon from "@mui/icons-material/Chat";
import HomeIcon from "@mui/icons-material/Home";
import RateReviewIcon from "@mui/icons-material/RateReview";
import ScienceIcon from "@mui/icons-material/Science";
import WorkspacePremiumIcon from "@mui/icons-material/WorkspacePremium";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Welcome", icon: <HomeIcon fontSize="small" />, end: true },
  { to: "/employee-feedback", label: "Feedback", icon: <RateReviewIcon fontSize="small" /> },
  { to: "/employee-skills", label: "Employee Skills", icon: <WorkspacePremiumIcon fontSize="small" /> },
  { to: "/chatbot", label: "Chatbot", icon: <ChatIcon fontSize="small" /> },
  { to: "/demo", label: "Demo", icon: <ScienceIcon fontSize="small" /> },
];

export default function NavBar() {
  return (
    <AppBar position="sticky" component="header">
      <Toolbar sx={{ gap: 1, flexWrap: "wrap" }}>
        <Typography variant="h6" sx={{ mr: 2, fontWeight: 700 }}>
          Engineer Pulse
        </Typography>
        <Box component="nav" sx={{ display: "flex", gap: 0.5, flexWrap: "wrap" }}>
          {links.map((link) => (
            <Button
              key={link.to}
              component={NavLink}
              to={link.to}
              end={link.end}
              color="inherit"
              variant="text"
              startIcon={link.icon}
              sx={{
                "&.active": {
                  fontWeight: 700,
                  borderBottom: "2px solid currentColor",
                  borderRadius: 0,
                },
              }}
            >
              {link.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
}
