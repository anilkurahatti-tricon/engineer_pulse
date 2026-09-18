import { useState } from "react";
import {
  Alert,
  Box,
  Button,
  Chip,
  LinearProgress,
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { useEmployeeSkills } from "../business/useEmployeeSkills";
import SkillsProficiencyChart from "../components/SkillsProficiencyChart";

const LEVELS = ["Beginner", "Intermediate", "Advanced"];

const chipColor = {
  Beginner: "default",
  Intermediate: "info",
  Advanced: "success",
};

export default function EmployeeSkillsPage() {
  const { items, loading, error, createItem, deleteItem } = useEmployeeSkills();
  const [employeeName, setEmployeeName] = useState("");
  const [skillName, setSkillName] = useState("");
  const [proficiencyLevel, setProficiencyLevel] = useState("Beginner");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!employeeName || !skillName) return;
    await createItem({
      employee_id: Math.floor(Math.random() * 1000),
      employee_name: employeeName,
      skill_name: skillName,
      proficiency_level: proficiencyLevel,
    });
    setEmployeeName("");
    setSkillName("");
    setProficiencyLevel("Beginner");
  };

  return (
    <Stack spacing={3}>
      <Box>
        <Typography variant="h4" component="h1">
          Employee Skills
        </Typography>
        <Typography color="text.secondary">
          {items.length} skill records across the team
        </Typography>
      </Box>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
          <TextField
            label="Employee name"
            value={employeeName}
            onChange={(e) => setEmployeeName(e.target.value)}
            required
            fullWidth
          />
          <TextField
            label="Skill"
            value={skillName}
            onChange={(e) => setSkillName(e.target.value)}
            required
            fullWidth
          />
          <TextField
            select
            label="Proficiency"
            value={proficiencyLevel}
            onChange={(e) => setProficiencyLevel(e.target.value)}
            sx={{ minWidth: 180 }}
          >
            {LEVELS.map((level) => (
              <MenuItem key={level} value={level}>
                {level}
              </MenuItem>
            ))}
          </TextField>
          <Button type="submit" sx={{ whiteSpace: "nowrap" }}>
            Add
          </Button>
        </Stack>
      </Paper>

      {loading && <LinearProgress />}
      {error && <Alert severity="error">{error}</Alert>}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1.2fr" },
          gap: 2,
        }}
      >
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Proficiency mix
          </Typography>
          <SkillsProficiencyChart items={items} />
        </Paper>

        <Paper sx={{ overflow: "auto" }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Employee</TableCell>
                <TableCell>Skill</TableCell>
                <TableCell>Proficiency</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.employee_name}</TableCell>
                  <TableCell>{item.skill_name}</TableCell>
                  <TableCell>
                    <Chip
                      size="small"
                      label={item.proficiency_level}
                      color={chipColor[item.proficiency_level] || "default"}
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Button
                      color="error"
                      variant="text"
                      startIcon={<DeleteOutlinedIcon />}
                      onClick={() => deleteItem(item.id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </Box>
    </Stack>
  );
}
