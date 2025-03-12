import React, { useState } from "react";
import axios from "axios";
import "./styles.css"; // Import custom styles

const App = () => {
  const [education, setEducation] = useState("");
  const [interest, setInterest] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/get-career-guidance", {
        education_level: education,
        interest_area: interest,
      });

      if (response.data.message) {
        setError(response.data.message);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError("Error fetching career guidance. Try again.");
    }
  };

  return (
    <div className="container">
      <h2>🎓 Career Guidance System</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Education Level (e.g., Bachelor's, Intermediate)"
          value={education}
          onChange={(e) => setEducation(e.target.value)}
          required
          className="input-field"
        />
        <input
          type="text"
          placeholder="Enter Interest Area (e.g., Engineering, Business)"
          value={interest}
          onChange={(e) => setInterest(e.target.value)}
          required
          className="input-field"
        />
        <button type="submit" className="btn">Get Career Guidance</button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="results">
          <h3>📌 Career Recommendations:</h3>
          {result.map((item, index) => (
            <div key={index} className="card">
              <p><strong>📚 Suggested Subjects:</strong> {item["Suggested Subjects"]}</p>
              <p><strong>🎓 Recommended Courses:</strong> {item["Recommended Courses"]}</p>
              <p><strong>💼 Career Options:</strong> {item["Career Options"]}</p>
              <p><strong>🏛️ Govt Job Options:</strong> {item["Govt Job Options"]}</p>
              <p><strong>🚀 Business Ideas:</strong> {item["Business/Startup Ideas"]}</p>
              <p><strong>🏛️ Political Career Paths:</strong> {item["Political Career Paths"]}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
