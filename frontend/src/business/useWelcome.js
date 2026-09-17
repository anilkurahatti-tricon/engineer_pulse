// Business layer: React hook wrapping the Welcome data-service.
import { useEffect, useState } from "react";
import { welcomeDataService } from "../dataservice/welcomeDataService";

export function useWelcome() {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    welcomeDataService
      .get()
      .then((data) => {
        if (!cancelled) setInfo(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return { info, loading, error };
}
