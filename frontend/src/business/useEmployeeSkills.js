// Business layer: React hook wrapping the Employee Skills data-service.
import { useCallback, useEffect, useState } from "react";
import { employeeSkillsDataService } from "../dataservice/employeeSkillsDataService";

export function useEmployeeSkills() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setItems(await employeeSkillsDataService.getAll());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const createItem = useCallback(
    async (payload) => {
      await employeeSkillsDataService.create(payload);
      await refresh();
    },
    [refresh]
  );

  const deleteItem = useCallback(
    async (id) => {
      await employeeSkillsDataService.remove(id);
      await refresh();
    },
    [refresh]
  );

  return { items, loading, error, refresh, createItem, deleteItem };
}
