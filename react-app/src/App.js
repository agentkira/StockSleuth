import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./index.css";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [displayedResponse, setDisplayedResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    setResponse("");
    setDisplayedResponse("");

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResponse(data.response);
      fetchHistory();

      // 🔄 Typing animation
      let i = 0;
      const interval = setInterval(() => {
        setDisplayedResponse((prev) => prev + data.response[i]);
        i++;
        if (i >= data.response.length) clearInterval(interval);
      }, 20);
    } catch (err) {
      setDisplayedResponse("❌ Error fetching response.");
    }

    setLoading(false);
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      alert("✅ File uploaded!");
    } catch (err) {
      alert("❌ File upload failed");
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch("http://localhost:8000/conversations");
      const data = await res.json();
      setHistory(data.reverse());
    } catch (err) {
      console.error("Failed to fetch history.");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 px-4 py-6 text-gray-800 dark:text-white">
        <div className="max-w-3xl mx-auto">

          {/* 🌙 Dark mode toggle */}
          <div className="flex justify-end mb-2">
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="text-sm px-3 py-1 border rounded hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
            </button>
          </div>

          <h1 className="text-4xl font-bold text-center text-blue-700 dark:text-blue-300 mb-6">
            💸 StockSleuth
          </h1>

          {/* 🔍 Query input */}
          <div className="flex flex-col sm:flex-row gap-2 items-center justify-center mb-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about $AAPL, interest rates, etc."
              className="border border-gray-300 rounded px-4 py-2 w-full sm:w-2/3 text-lg shadow-sm focus:ring focus:ring-blue-200 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            />
            <button
              onClick={handleQuery}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400 transition"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>

          {/* 📄 Upload PDF */}
          <div className="mb-6 flex flex-col items-center">
            <label className="text-sm font-medium text-gray-600 dark:text-gray-300 mb-2">
              📄 Upload PDF
            </label>
            <div className="ml-6"> 
              <input
                type="file"
                onChange={(e) => uploadFile(e.target.files[0])}
                className="text-sm file:py-2 file:px-4 file:rounded file:border file:border-gray-300 file:bg-white file:text-sm file:font-medium file:cursor-pointer dark:file:bg-gray-700 dark:file:border-gray-600 dark:file:text-white"
              />
            </div>
          </div>
          {/* 🧠 Answer */}
          {displayedResponse && (
            <div className="bg-white dark:bg-gray-800 rounded shadow p-6 my-6">
              <h2 className="text-xl font-semibold mb-2 text-green-700 dark:text-green-300">🧐 Answer</h2>
              <div className="prose dark:prose-invert max-w-none">
                <ReactMarkdown>{displayedResponse}</ReactMarkdown>
              </div>
            </div>
          )}

          {/* 💬 Conversation History */}
          {history.length > 0 && (
            <div className="mt-10">
              <h3 className="text-2xl font-bold text-blue-700 dark:text-blue-300 mb-4">🕓 Conversation History</h3>
              <div className="space-y-4">
                {history.map((item, idx) => (
                  <div
                    key={idx}
                    className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg border dark:border-gray-700"
                  >
                    <p className="font-semibold text-gray-900 dark:text-gray-100">Q: {item.query}</p>
                    <div className="prose dark:prose-invert max-w-none">
                      <ReactMarkdown>{item.response || "No response."}</ReactMarkdown>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default App;
