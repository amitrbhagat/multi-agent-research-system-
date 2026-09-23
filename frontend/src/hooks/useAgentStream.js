import { useState, useCallback } from "react";


export function useAgentStream() {
  const [trace, setTrace] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [finalState, setFinalState] = useState(null);

  const runQuery = useCallback(async (query) => {
    setTrace([]);
    setFinalState(null);
    setIsRunning(true);

    const response = await fetch("http://localhost:8000/query/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const frames = buffer.split("\n\n");
      buffer = frames.pop(); // keep incomplete frame for next chunk

      for (const frame of frames) {
        if (!frame.startsWith("data: ")) continue;
        const payload = JSON.parse(frame.slice(6));

        if (payload.node === "__end__") {
          setIsRunning(false);
          continue;
        }

        setTrace((prev) => [...prev, payload]);
        setFinalState(payload.state);
      }
    }

    setIsRunning(false);
  }, []);

  return { trace, isRunning, finalState, runQuery };
}
