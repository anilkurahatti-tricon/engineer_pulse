import { Box, Typography } from "@mui/material";

export default function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        mt: "auto",
        px: 2,
        py: 2,
        textAlign: "center",
        borderTop: "1px solid",
        borderColor: "divider",
        bgcolor: "background.paper",
      }}
    >
      <Typography variant="body2" color="text.secondary">
        Engineer Pulse · draft application
      </Typography>
    </Box>
  );
}
