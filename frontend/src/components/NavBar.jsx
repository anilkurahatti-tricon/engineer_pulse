import { AppBar, Box, Button, Toolbar, Typography } from "@mui/material";
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined";
import ChatIcon from "@mui/icons-material/Chat";
import HomeIcon from "@mui/icons-material/Home";
import PeopleAltOutlinedIcon from "@mui/icons-material/PeopleAltOutlined";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Welcome", icon: <HomeIcon fontSize="small" />, end: true },
  { to: "/top-n-match", label: "Top-N Match", icon: <PeopleAltOutlinedIcon fontSize="small" /> },
  { to: "/gap-analysis", label: "Skill Match", icon: <AssessmentOutlinedIcon fontSize="small" /> },
  { to: "/chatbot", label: "Chatbot", icon: <ChatIcon fontSize="small" /> },
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
