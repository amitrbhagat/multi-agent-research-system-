import QueryInput from "./components/QueryInput";
import TracePanel from "./components/TracePanel";
import { useAgentStream } from "./hooks/useAgentStream";


export default function App() {
  const { trace, isRunning, finalState, runQuery } = useAgentStream();

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Multi-Agent Research System</h2>
      <QueryInput onSubmit={runQuery} disabled={isRunning} />
      <TracePanel trace={trace} />

      {finalState && (
        <div style={{ marginTop: 24, padding: 12, background: "#f5f5f5" }}>
          {finalState.analyst_result?.answer && (
            <p>{finalState.analyst_result.answer}</p>
          )}
          {finalState.draft && (
            <>
              <p>{finalState.draft}</p>
              {finalState.claims?.length > 0 && (
                <ul style={{ fontSize: 12, color: "#666" }}>
                  {finalState.claims.map((c, i) => (
                    <li key={i}>
                      {c.text} — source: {c.source_id ?? "none"}
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
