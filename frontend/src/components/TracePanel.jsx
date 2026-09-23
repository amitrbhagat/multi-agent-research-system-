export default function TracePanel({ trace }) {
  const nodeLabels = {
    planner: "Planner",
    data_analyst: "Data Analyst",
    researcher: "Researcher",
    writer: "Writer",
    critic: "Critic",
    retry: "Retry (looping back)",
    fallback: "Fallback",
  };

  return (
    <div style={{ marginTop: 16 }}>
      {trace.map((step, i) => (
        <div
          key={i}
          style={{
            padding: 8,
            borderLeft: "3px solid #4caf50",
            marginBottom: 4,
          }}
        >
          <strong>{nodeLabels[step.node] || step.node}</strong>
          {step.node === "critic" && step.state.critique && (
            <div style={{ fontSize: 12, color: "#555" }}>
              score: {step.state.critique.score} | feedback:{" "}
              {step.state.critique.feedback}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}