
// This blueprint represents the structured JSON dictionary our FastAPI model returns.
export interface PredictionResult {
  disease_name: string;
  chemical_treatment: string;
  organic_remedy: string;
  prevention: string; 
}