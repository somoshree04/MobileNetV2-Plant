
// This blueprint represents the structured JSON dictionary our FastAPI model returns.
export interface PredictionResult {
  class_name: string;
  confidence: number;
}