import apiClient from "../dataservice/apiClient";

/**
 * Service integrating frontend with the actual backend APIs:
 * - GET /api/projects/       -> ProjectService -> ProjectRepository -> DB (employee_projects)
 * - GET /api/employees/      -> EmployeeService -> EmployeeRepository -> DB (employees + employee_skills)
 * - POST /api/top-n-match/   -> TopNMatchService -> Groq/LangChain AI Agent -> Ranked Employees
 * - POST /api/gap-analysis/analyze -> GapAnalysisService -> AI Gap Analysis Agent
 * - POST /api/roadmap/generate     -> RoadmapService -> AI Upskilling Roadmap Agent
 */
export const topNMatchService = {
  /**
   * Fetch all projects from GET /api/projects/
   */
  async getProjects() {
    const response = await apiClient.get("/api/projects/");
    return response.data;
  },

  /**
   * Fetch all employees from GET /api/employees/
   */
  async getEmployees() {
    const response = await apiClient.get("/api/employees/");
    return response.data;
  },

  /**
   * Get an employee by ID from GET /api/employees/:id
   */
  async getEmployeeById(employeeId) {
    const response = await apiClient.get(`/api/employees/${employeeId}`);
    return response.data;
  },

  /**
   * Get a project by ID from GET /api/projects/:id
   */
  async getProjectById(projectId) {
    const response = await apiClient.get(`/api/projects/${projectId}`);
    return response.data;
  },

  /**
   * Rank employees for a project using POST /api/top-n-match/
   */
  async matchTopNEmployees(projectId, topN = 5) {
    const response = await apiClient.post("/api/top-n-match/", {
      project_id: Number(projectId),
      top_n: Number(topN),
    });
    return response.data;
  },

  /**
   * Run Gap Analysis using POST /api/gap-analysis/analyze
   */
  async analyzeGap(employeeId, projectIds, overallReadinessScore = null) {
    const payload = {
      employee_id: Number(employeeId),
      project_ids: Array.isArray(projectIds) ? projectIds.map(Number) : [Number(projectIds)],
      ...(overallReadinessScore !== null && overallReadinessScore !== undefined
        ? { overall_readiness_score: Number(overallReadinessScore) }
        : {}),
    };
    const response = await apiClient.post("/api/gap-analysis/analyze", payload);
    return response.data;
  },

  /**
   * Generate Recommender / 6-Month Upskilling Roadmap using POST /api/roadmap/generate
   */
  async generateRecommenderRoadmap(gapAnalysisData, employeeId = null) {
    const payload = {
      employee_name: gapAnalysisData.employee_name || "Employee",
      experience_years: Number(gapAnalysisData.experience_years || 0),
      overall_readiness_score: Number(gapAnalysisData.overall_readiness_score || 0),
      strengths: gapAnalysisData.strengths || [],
      gaps: gapAnalysisData.gaps || [],
      areas_of_improvement: gapAnalysisData.areas_of_improvement || [],
      summary: gapAnalysisData.summary || "",
      employee_id: employeeId ? Number(employeeId) : null,
    };

    const response = await apiClient.post("/api/roadmap/generate", payload);
    return response.data;
  },
};
