

import React, { useState, ChangeEvent, FormEvent } from 'react';
import { PredictionResult } from './types';

export default function App() {
  // We explicitly tell these states what data types they are allowed to manage inside <brackets>
  const [file, setFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // ChangeEvent<HTMLInputElement> ensures this function only triggers from an HTML file/text input element
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null); // Clear errors when a new file is picked
    }
  };

  // FormEvent ensures this function is wired specifically to a submission behavior
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a leaf image first!");
      return;
    }

    setLoading(true);
    setError(null);

    // Prepare our binary image file to travel across the network HTTP stream
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Fixed: Pointing exactly to the 127.0.0.1 loopback IP whitelisted by CORS
        const response = await fetch('http://127.0.0.1:8000/api/v1/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server responded with status code: ${response.status}`);
      }

      // We explicitly map the raw json response to our strict TypeScript interface structure
      const data: PredictionResult = await response.json();
      setPrediction(data);
    } catch (err: any) {
      setError(err.message || "An error occurred while connecting to the AI backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6 border border-slate-100">
        <h1 className="text-2xl font-bold text-slate-800 mb-2 text-center">Plant Disease Scanner</h1>
        <p className="text-slate-500 text-sm text-center mb-6">Upload a leaf picture to diagnose health issues.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="border-2 border-dashed border-slate-300 rounded-xl p-4 text-center hover:bg-slate-50 transition">
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange} 
              className="text-sm text-slate-500 w-full"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-3 bg-emerald-600 text-white font-semibold rounded-xl hover:bg-emerald-700 disabled:bg-slate-300 transition"
          >
            {loading ? "Analyzing Image Layers..." : "Scan Leaf Data"}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">
            ⚠️ {error}
          </div>
        )}

        {prediction && (
          <div className="mt-6 p-4 bg-emerald-50 rounded-xl border border-emerald-100 space-y-3">
            <h3 className="font-bold text-lg text-emerald-900 border-b border-emerald-200 pb-2">AI Diagnostic Report</h3>
            <div className="text-sm text-emerald-800 space-y-1">
              <p><strong>Condition:</strong> {prediction.disease_name}</p>
              <p><strong>Organic Remedy:</strong> {prediction.organic_remedy}</p>
              <p><strong>Chemical Option:</strong> {prediction.chemical_treatment}</p>
              {/* Fixed: Added missing closing </p> tag below */}
              <p className="bg-white p-3 rounded-lg border border-emerald-100 mt-2 text-xs text-slate-600 leading-relaxed">
                <strong>Prevention Plan:</strong> {prediction.prevention}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}