import apiClient from "./apiClient";

const BASE_PATH = "/api/gap-analysis/analyze";
const OPTIONS_PATH = "/api/gap-analysis/options";
const ROADMAP_PATH = "/api/roadmap/generate";

export function getGapAnalysisOptions() {
  return apiClient.get(OPTIONS_PATH).then((response) => response.data);
}

export function analyzeGap(employeeId, projectIds) {
  return apiClient
    .post(BASE_PATH, {
      employee_id: employeeId,
      project_ids: projectIds,
    })
    .then((response) => response.data);
}

export function generateRoadmap(employeeId, gapAnalysis) {
  return apiClient
    .post(ROADMAP_PATH, { ...gapAnalysis, employee_id: employeeId })
    .then((response) => response.data);
}