import { useState } from "react";

export default function QueryInput({ onSubmit, disabled }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSubmit(query.trim());
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8 }}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a research question..."
        disabled={disabled}
        style={{ flex: 1, padding: 8 }}
      />
      <button type="submit" disabled={disabled || !query.trim()}>
        {disabled ? "Running..." : "Ask"}
      </button>
    </form>
  );
}