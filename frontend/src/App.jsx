import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  // 1. Handle picking the image from your computer
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setPrediction(""); // Reset prediction when a new photo is picked
    }
  };

  // 2. The POST request to your FastAPI Backend
  const uploadImage = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file); // Must match 'file: UploadFile' in FastAPI

    setLoading(true);
    try {
      // Note: Use 127.0.0.1 or localhost (FastAPI default port is 8000)
      const response = await axios.post("http://127.0.0.1:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error("Error:", error);
      alert("Cannot connect to Backend. Make sure main.py is running on port 8000!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white font-sans flex flex-col items-center py-12 px-4">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600 mb-2">
          PlantScan AI
        </h1>
        <p className="text-slate-400">Instant disease detection for your crops</p>
      </div>

      {/* Main Card */}
      <div className="w-full max-w-md bg-slate-800 rounded-3xl shadow-2xl border border-slate-700 p-8">
        
        {/* Upload Area */}
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-2xl p-6 hover:border-green-500 transition-colors cursor-pointer relative">
          <input 
            type="file" 
            onChange={handleFileChange} 
            accept="image/*"
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          <div className="text-center">
            <span className="text-4xl mb-2 block">📸</span>
            <p className="text-sm text-slate-300">
              {file ? file.name : "Click to upload leaf image"}
            </p>
          </div>
        </div>

        {/* Preview and Button */}
        {preview && (
          <div className="mt-8 space-y-6">
            <div className="relative group">
              <img 
                src={preview} 
                alt="Preview" 
                className="w-full h-64 object-cover rounded-xl shadow-lg border-2 border-slate-700" 
              />
            </div>

            <button 
              onClick={uploadImage}
              disabled={loading}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all transform active:scale-95 ${
                loading 
                ? "bg-slate-700 cursor-not-allowed" 
                : "bg-green-600 hover:bg-green-500 shadow-lg shadow-green-900/20"
              }`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3 border-t-2 border-white rounded-full" viewBox="0 0 24 24"></svg>
                  Analyzing...
                </span>
              ) : "Identify Disease"}
            </button>
          </div>
        )}

        {/* Result Display */}
        {prediction && (
          <div className="mt-8 p-6 bg-green-900/20 border border-green-500/30 rounded-2xl animate-fade-in">
            <h3 className="text-green-400 text-xs font-bold uppercase tracking-widest mb-1">Results</h3>
            <p className="text-2xl font-semibold capitalize">
              {prediction.replace(/___/g, " ").replace(/_/g, " ")}
            </p>
          </div>
        )}
      </div>

      <footer className="mt-auto pt-10 text-slate-500 text-sm">
        FastAPI + React + PyTorch Integration
      </footer>
    </div>
  );
}

export default App;