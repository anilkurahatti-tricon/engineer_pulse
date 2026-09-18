import { useState } from "react";
import {
  Alert,
  Autocomplete,
  Box,
  Button,
  Chip,
  IconButton,
  LinearProgress,
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { useEmployeeSkills } from "../business/useEmployeeSkills";
import SkillsProficiencyChart from "../components/SkillsProficiencyChart";
import { formatSystemDate } from "../utils/formatSystemDate";
import ConfirmDialog from "../components/ConfirmDialog";

const LEVELS = ["Beginner", "Intermediate", "Advanced"];

const chipColor = {
  Beginner: "default",
  Intermediate: "info",
  Advanced: "success",
};

const EMPTY_FORM = {
  employeeId: "",
  employeeName: "",
  skills: [],
  proficiencyLevel: "Beginner",
};

export default function EmployeeSkillsPage() {
  const { items, loading, submitting, error, createItems, deleteItem } = useEmployeeSkills();
  const [form, setForm] = useState(EMPTY_FORM);
  const [skillInput, setSkillInput] = useState("");
  const [recordedAt, setRecordedAt] = useState(() => new Date());
  const [success, setSuccess] = useState("");
  const [confirm, setConfirm] = useState(null);

  const skillOptions = [...new Set(items.map((item) => item.skill_name).filter(Boolean))];

  const isFormDirty =
    Boolean(form.employeeId) ||
    Boolean(form.employeeName.trim()) ||
    form.skills.length > 0 ||
    Boolean(skillInput.trim()) ||
    form.proficiencyLevel !== "Beginner";

  const resetForm = () => {
    setForm(EMPTY_FORM);
    setSkillInput("");
    setRecordedAt(new Date());
    setSuccess("");
  };

  const addSkillChips = (rawValues) => {
    const next = rawValues
      .map((value) => value.replace(/,/g, "").trim())
      .filter(Boolean)
      .filter(
        (value) =>
          !form.skills.some((skill) => skill.toLowerCase() === value.toLowerCase())
      );
    if (!next.length) return;
    setForm((prev) => ({ ...prev, skills: [...prev.skills, ...next] }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const pendingSkills = skillInput
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);
    const skills = [...form.skills];
    pendingSkills.forEach((skill) => {
      if (!skills.some((existing) => existing.toLowerCase() === skill.toLowerCase())) {
        skills.push(skill);
      }
    });
    if (!form.employeeId || !form.employeeName.trim() || skills.length === 0) return;
    if (pendingSkills.length) {
      setForm((prev) => ({ ...prev, skills }));
      setSkillInput("");
    }
    setConfirm({ type: "submit", skills });
  };

  const handleCancelClick = () => {
    if (!isFormDirty) {
      resetForm();
      return;
    }
    setConfirm({ type: "cancel" });
  };

  const handleConfirm = async () => {
    if (!confirm) return;
    if (confirm.type === "cancel") {
      resetForm();
      setConfirm(null);
      return;
    }
    if (confirm.type === "delete") {
      await deleteItem(confirm.item.id);
      setConfirm(null);
      return;
    }
    setSuccess("");
    try {
      const skills = confirm.skills?.length ? confirm.skills : form.skills;
      await createItems(
        skills.map((skill_name) => ({
          employee_id: Number(form.employeeId),
          employee_name: form.employeeName.trim(),
          skill_name,
          proficiency_level: form.proficiencyLevel,
        }))
      );
      resetForm();
      setSuccess(skills.length > 1 ? `${skills.length} skills submitted.` : "Skill submitted.");
      setConfirm(null);
    } catch {
      setConfirm(null);
    }
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4" component="h1">
        Employee Skills
      </Typography>

      <Paper component="form" onSubmit={handleSubmit} sx={{ p: { xs: 2, sm: 3 } }}>
        <Stack spacing={2.5}>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
            <TextField
              label="Employee ID"
              type="number"
              value={form.employeeId}
              onChange={(e) => setForm((prev) => ({ ...prev, employeeId: e.target.value }))}
              required
              fullWidth
            />
            <TextField
              label="Employee name"
              value={form.employeeName}
              onChange={(e) => setForm((prev) => ({ ...prev, employeeName: e.target.value }))}
              required
              fullWidth
            />
          </Stack>

          <Autocomplete
            multiple
            freeSolo
            filterSelectedOptions
            options={skillOptions}
            value={form.skills}
            inputValue={skillInput}
            onInputChange={(_, value) => {
              if (value.includes(",")) {
                const parts = value.split(",");
                const remainder = parts.pop() || "";
                addSkillChips(parts);
                setSkillInput(remainder.trimStart());
                return;
              }
              setSkillInput(value);
            }}
            onChange={(_, skills) => setForm((prev) => ({ ...prev, skills }))}
            slotProps={{
              paper: {
                sx: {
                  mt: 0.5,
                  bgcolor: "background.paper",
                  backgroundImage: "none",
                  border: "1px solid",
                  borderColor: "divider",
                },
              },
              listbox: {
                sx: {
                  py: 0.5,
                  "& .MuiAutocomplete-option": {
                    mx: 0.5,
                    my: 0.25,
                    borderRadius: 1,
                  },
                  "& .MuiAutocomplete-option.Mui-focused": {
                    bgcolor: "rgba(192, 132, 252, 0.12)",
                  },
                  "& .MuiAutocomplete-option[aria-selected='true']": {
                    bgcolor: "transparent",
                  },
                },
              },
            }}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => {
                const { key, ...tagProps } = getTagProps({ index });
                return (
                  <Chip
                    key={key}
                    label={option}
                    size="small"
                    variant="outlined"
                    color="primary"
                    {...tagProps}
                  />
                );
              })
            }
            renderInput={(params) => (
              <TextField
                {...params}
                label="Skills"
                placeholder={form.skills.length ? "Add another" : "Type a skill, then press Enter or comma"}
                helperText="Each skill wraps in a chip. Add as many as you need."
              />
            )}
          />
          <TextField
            select
            label="Proficiency"
            value={form.proficiencyLevel}
            onChange={(e) => setForm((prev) => ({ ...prev, proficiencyLevel: e.target.value }))}
            sx={{ minWidth: 180, maxWidth: { sm: 280 } }}
          >
            {LEVELS.map((level) => (
              <MenuItem key={level} value={level}>
                {level}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            label="Recorded date"
            value={formatSystemDate(recordedAt)}
            fullWidth
            disabled
            helperText="Filled automatically from this computer."
          />

          <Stack direction="row" spacing={1} sx={{ justifyContent: "flex-end" }}>
            <Button type="button" variant="outlined" onClick={handleCancelClick} disabled={submitting}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting}>
              {submitting ? "Submitting..." : "Submit"}
            </Button>
          </Stack>
        </Stack>
      </Paper>

      {loading && <LinearProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      {success && <Alert severity="success">{success}</Alert>}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1.35fr" },
          gap: 2,
          alignItems: "stretch",
        }}
      >
        <Paper sx={{ p: { xs: 2, sm: 3 }, minHeight: 320 }}>
          <Typography variant="h6" gutterBottom>
            Proficiency mix
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {items.length} skill records
          </Typography>
          <SkillsProficiencyChart items={items} height={240} />
        </Paper>

        <Paper sx={{ overflow: "hidden", display: "flex", flexDirection: "column" }}>
          <Box sx={{ px: { xs: 2, sm: 3 }, pt: { xs: 2, sm: 3 }, pb: 1 }}>
            <Typography variant="h6">Submitted skills</Typography>
          </Box>
          <TableContainer sx={{ flex: 1 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Employee</TableCell>
                  <TableCell>Skill</TableCell>
                  <TableCell>Proficiency</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {items.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4}>
                      <Typography color="text.secondary">No skills yet.</Typography>
                    </TableCell>
                  </TableRow>
                )}
                {items.map((item) => (
                  <TableRow key={item.id} hover>
                    <TableCell>
                      <Typography variant="body2">{item.employee_name}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        ID {item.employee_id}
                      </Typography>
                    </TableCell>
                    <TableCell>{item.skill_name}</TableCell>
                    <TableCell>
                      <Chip
                        size="small"
                        label={item.proficiency_level}
                        color={chipColor[item.proficiency_level] || "default"}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        aria-label={`Delete skill for ${item.employee_name}`}
                        color="error"
                        onClick={() => setConfirm({ type: "delete", item })}
                      >
                        <DeleteOutlinedIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>

      <ConfirmDialog
        open={Boolean(confirm)}
        title={
          confirm?.type === "delete"
            ? "Delete this skill?"
            : confirm?.type === "cancel"
              ? "Clear this form?"
              : confirm?.skills?.length > 1
                ? `Submit ${confirm.skills.length} skills?`
                : "Submit this skill?"
        }
        message={
          confirm?.type === "delete"
            ? `The skill for ${confirm.item?.employee_name || "this employee"} will be removed.`
            : confirm?.type === "cancel"
              ? "Unsaved text will be lost."
              : confirm?.skills?.length > 1
                ? "Each skill will be saved as its own record for this employee."
                : "This will send the skill to the server."
        }
        confirmLabel={
          confirm?.type === "delete" ? "Delete" : confirm?.type === "cancel" ? "Clear" : "Submit"
        }
        confirmColor={confirm?.type === "submit" ? "primary" : "error"}
        busy={submitting}
        onCancel={() => setConfirm(null)}
        onConfirm={handleConfirm}
      />
    </Stack>
  );
}
