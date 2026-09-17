import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#c084fc" },
    secondary: { main: "#67e8f9" },
    background: {
      default: "#16171d",
      paper: "#1f2028",
    },
    text: {
      primary: "#f3f4f6",
      secondary: "#9ca3af",
    },
    divider: "#2e303a",
    error: { main: "#f87171" },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: "Roboto, system-ui, 'Segoe UI', sans-serif",
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#1f2933",
          backgroundImage: "none",
        },
      },
    },
    MuiButton: {
      defaultProps: { variant: "contained" },
    },
  },
});

export const chartTheme = {
  grid: "#2e303a",
  tick: "#9ca3af",
  tooltipBackground: "#1f2028",
  tooltipBorder: "#2e303a",
  bar: "#c084fc",
  barAlt: "#67e8f9",
};

export default theme;
