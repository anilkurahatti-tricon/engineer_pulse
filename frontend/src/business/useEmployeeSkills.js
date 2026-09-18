// Business layer: React hook wrapping the Employee Skills data-service.
import { useCallback, useEffect, useState } from "react";
import { employeeSkillsDataService } from "../dataservice/employeeSkillsDataService";

function toErrorMessage(err) {
  const detail = err.response?.data?.detail;
  if (typeof detail === "string") return detail;
  return err.message || "Request failed";
}

export function useEmployeeSkills() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await employeeSkillsDataService.getAll());
    } catch (err) {
      setError(toErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createItems = useCallback(async (payloads) => {
    setSubmitting(true);
    setError(null);
    try {
      for (const payload of payloads) {
        await employeeSkillsDataService.create(payload);
      }
      setItems(await employeeSkillsDataService.getAll());
    } catch (err) {
      setError(toErrorMessage(err));
      throw err;
    } finally {
      setSubmitting(false);
    }
  }, []);

  const deleteItem = useCallback(
    async (id) => {
      await employeeSkillsDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, submitting, error, refresh, createItems, deleteItem };
}
