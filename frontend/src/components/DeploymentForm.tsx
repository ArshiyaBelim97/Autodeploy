import React, { useState } from "react";

export const DeploymentForm: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState("");
  const [nlDesc, setNlDesc] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    setMessage("Deploying... (mock)");
    setTimeout(() => setMessage("Deployment successful! URL: https://mock-url.com"), 2000);
  };

  return (
    <div>
      <input placeholder="GitHub URL" value={repoUrl} onChange={e => setRepoUrl(e.target.value)} />
      <input placeholder="Deployment Description" value={nlDesc} onChange={e => setNlDesc(e.target.value)} />
      <button onClick={handleSubmit}>Deploy</button>
      <p>{message}</p>
    </div>
  );
};
