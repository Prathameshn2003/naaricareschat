

import { supabase } from "@/integrations/supabase/client";

// =======================================================
// META TYPE
// =======================================================

export interface MLPredictionMeta {
  usedAPI: boolean;
  error?: string;
}

// =======================================================
// PCOS TYPES
// =======================================================

export interface PCOSInputData {
  age: number;
  height: number;
  weight: number;
  bmi: number;
  cycleRegular: boolean;
  cycleLength: number;
  weightGain: boolean;
  hairGrowth: boolean;
  skinDarkening: boolean;
  hairLoss: boolean;
  pimples: boolean;
  fastFood: boolean;
  regularExercise: boolean;
  follicleLeft: number;
  follicleRight: number;
  endometrium: number;
  lh: number;
  fsh: number;
  testosterone: number;
  insulin: number;
}

export interface PCOSRecommendations {
  diet: string[];
  exercise: string[];
  lifestyle: string[];
  needsDoctor: boolean;
}

export interface PCOSResult {
  hasPCOS: boolean;
  riskPercentage: number;
  severity: "none" | "low" | "medium" | "high";
  breakdown: {
    cycleScore: number;
    hormonalScore: number;
    ultrasoundScore: number;
    metabolicScore: number;
  };
  recommendations: PCOSRecommendations;
}

// =======================================================
// PCOS LOCAL PREDICTION
// =======================================================

export function predictPCOS(data: PCOSInputData): PCOSResult {

  const cycleScore = data.cycleRegular ? 0 : 1;

  const hormonalScore =
    (data.hairGrowth ? 1 : 0) +
    (data.skinDarkening ? 1 : 0) +
    (data.hairLoss ? 1 : 0) +
    (data.pimples ? 1 : 0);

  const totalFollicles = data.follicleLeft + data.follicleRight;
  const ultrasoundScore = totalFollicles >= 10 ? 1 : 0;

  const metabolicScore = data.bmi >= 25 ? 1 : 0;

  const lifestyleScore =
    (data.weightGain ? 0.5 : 0) +
    (data.fastFood ? 0.5 : 0) +
    (!data.regularExercise ? 0.5 : 0);

  const totalScore =
    2 * cycleScore +
    2 * ultrasoundScore +
    hormonalScore +
    metabolicScore +
    lifestyleScore;

  const hasPCOS = totalScore >= 4;

  let riskPercentage = Math.round((totalScore / 9) * 100);
  riskPercentage = Math.max(hasPCOS ? 30 : 0, riskPercentage);
  riskPercentage = Math.min(100, riskPercentage);

  let severity: "none" | "low" | "medium" | "high";

  if (!hasPCOS) severity = "none";
  else if (riskPercentage < 50) severity = "low";
  else if (riskPercentage < 70) severity = "medium";
  else severity = "high";

  return {
    hasPCOS,
    riskPercentage,
    severity,
    breakdown: {
      cycleScore: cycleScore * 2,
      hormonalScore,
      ultrasoundScore: ultrasoundScore * 2,
      metabolicScore
    },
    recommendations: getPCOSRecommendations(severity)
  };
}

// =======================================================
// PCOS RECOMMENDATIONS
// =======================================================

function getPCOSRecommendations(severity: "none" | "low" | "medium" | "high"): PCOSRecommendations {

  if (severity === "none") {
    return {
      diet: ["Balanced diet", "Fruits & vegetables", "Drink enough water"],
      exercise: ["30 minutes daily exercise"],
      lifestyle: ["Healthy sleep", "Regular checkups"],
      needsDoctor: false
    };
  }

  if (severity === "low") {
    return {
      diet: ["Low glycemic foods", "Green vegetables", "Lean protein"],
      exercise: ["Brisk walking", "Yoga"],
      lifestyle: ["Sleep 7–8 hours", "Reduce stress"],
      needsDoctor: false
    };
  }

  if (severity === "medium") {
    return {
      diet: ["Low GI diet", "High fiber foods"],
      exercise: ["Cardio workouts", "Strength training"],
      lifestyle: ["Track cycle", "Maintain sleep"],
      needsDoctor: true
    };
  }

  return {
    diet: ["Strict low GI diet", "High fiber vegetables"],
    exercise: ["HIIT workouts", "Daily cardio"],
    lifestyle: ["Strict routine"],
    needsDoctor: true
  };
}

// =======================================================
// MENOPAUSE TYPES
// =======================================================

export interface MenopauseInputData {
  age: number;
  estrogenLevel: number;
  fshLevel: number;
  yearsSinceLastPeriod: number;
  irregularPeriods: boolean;
  missedPeriods: boolean;
  hotFlashes: boolean;
  nightSweats: boolean;
  sleepProblems: boolean;
  vaginalDryness: boolean;
  jointPain: boolean;
}

export interface MenopauseRecommendations {
  diet: string[];
  exercise: string[];
  lifestyle: string[];
  needsDoctor: boolean;
}

export interface MenopauseResult {
  stage: "Pre-Menopause" | "Peri-Menopause" | "Post-Menopause";
  riskPercentage: number;
  hasMenopauseSymptoms: boolean;
  breakdown: {
    ageScore: number;
    hormoneScore: number;
    symptomScore: number;
    periodScore: number;
  };
  recommendations: MenopauseRecommendations;
}

// =======================================================
// MENOPAUSE LOCAL LOGIC
// =======================================================

export function predictMenopause(data: MenopauseInputData): MenopauseResult {

  let stage: MenopauseResult["stage"];

  if (data.yearsSinceLastPeriod >= 1) stage = "Post-Menopause";
  else if (data.age >= 40 && (data.irregularPeriods || data.missedPeriods || data.hotFlashes))
    stage = "Peri-Menopause";
  else stage = "Pre-Menopause";

  const symptomScore =
    (data.irregularPeriods ? 1 : 0) +
    (data.missedPeriods ? 1 : 0) +
    (data.hotFlashes ? 1 : 0) +
    (data.nightSweats ? 1 : 0) +
    (data.sleepProblems ? 1 : 0) +
    (data.vaginalDryness ? 1 : 0) +
    (data.jointPain ? 1 : 0);

  const riskPercentage = Math.min(100, symptomScore * 10);

  return {
    stage,
    riskPercentage,
    hasMenopauseSymptoms: stage !== "Pre-Menopause",
    breakdown: {
      ageScore: data.age > 45 ? 2 : 1,
      hormoneScore: 1,
      symptomScore,
      periodScore: data.yearsSinceLastPeriod > 0 ? 2 : 0
    },
    recommendations: getMenopauseRecommendations(stage)
  };
}

// =======================================================
// MENOPAUSE RECOMMENDATIONS
// =======================================================

function getMenopauseRecommendations(stage: MenopauseResult["stage"]): MenopauseRecommendations {

  if (stage === "Pre-Menopause") {
    return {
      diet: ["Balanced diet", "Calcium rich foods"],
      exercise: ["Regular cardio", "30 min walking"],
      lifestyle: ["Good sleep"],
      needsDoctor: false
    };
  }

  if (stage === "Peri-Menopause") {
    return {
      diet: ["Whole grains", "Protein foods"],
      exercise: ["Walking", "Yoga breathing"],
      lifestyle: ["Maintain weight"],
      needsDoctor: true
    };
  }

  return {
    diet: ["High calcium foods"],
    exercise: ["Weight bearing exercises"],
    lifestyle: ["Regular checkups"],
    needsDoctor: true
  };
}

// =======================================================
// MENSTRUAL CYCLE TYPES
// =======================================================

export interface CycleData {
  cycleHistory: number[];
  lastPeriodStart: Date;
  stressLevel?: number;
  sleepHours?: number;
}

export interface CyclePrediction {
  predictedStartDate: Date;
  confidenceLevel: "high" | "medium" | "low";
  averageCycleLength: number;
  cycleVariability: number;
  isIrregular: boolean;
  pcosRiskFlag: boolean;
  delayAdjustment: number;
}

// =======================================================
// API CONNECTOR FUNCTIONS
// =======================================================

const ML_API_URL = import.meta.env.VITE_ML_API_URL || "http://127.0.0.1:8001";

export async function predictPCOSFromAPI(
  data: PCOSInputData
): Promise<PCOSResult & { _meta: MLPredictionMeta }> {

  // Try direct API call first (for production)
  if (ML_API_URL && ML_API_URL !== "http://127.0.0.1:8001") {
    try {
      const response = await fetch(`${ML_API_URL}/ml-predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_type: "pcos", input_data: data }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.prediction) {
          return { ...result.prediction, _meta: { usedAPI: true } };
        }
      }
    } catch (err) {
      console.warn("Direct API call failed, falling back to Supabase:", err);
    }
  }

  // Fallback to Supabase functions
  try {
    const { data: response, error } =
      await supabase.functions.invoke("ml-predict", {
        body: { model_type: "pcos", input_data: data }
      });

    if (error) throw error;

    if (response?.prediction) {
      return { ...response.prediction, _meta: { usedAPI: true } };
    }

    const local = predictPCOS(data);
    return { ...local, _meta: { usedAPI: false } };

  } catch (err: any) {
    const local = predictPCOS(data);
    return {
      ...local,
      _meta: { usedAPI: false, error: err.message }
    };
  }
}

// =======================================================
// MENOPAUSE API
// =======================================================

export async function predictMenopauseFromAPI(
  data: MenopauseInputData
): Promise<MenopauseResult & { _meta: MLPredictionMeta }> {

  // Try direct API call first (for production)
  if (ML_API_URL && ML_API_URL !== "http://127.0.0.1:8001") {
    try {
      const response = await fetch(`${ML_API_URL}/ml-predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_type: "menopause", input_data: data }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.prediction) {
          return { ...result.prediction, _meta: { usedAPI: true } };
        }
      }
    } catch (err) {
      console.warn("Direct API call failed, falling back to Supabase:", err);
    }
  }

  // Fallback to Supabase functions
  try {

    const { data: response, error } =
      await supabase.functions.invoke("ml-predict", {
        body: { model_type: "menopause", input_data: data }
      });

    if (error) throw error;

    if (response?.prediction) {
      return { ...response.prediction, _meta: { usedAPI: true } };
    }

    const local = predictMenopause(data);
    return { ...local, _meta: { usedAPI: false } };

  } catch (err: any) {

    const local = predictMenopause(data);

    return {
      ...local,
      _meta: { usedAPI: false, error: err.message }
    };
  }
}

// =======================================================
// CYCLE API
// =======================================================

export async function predictCycleFromAPI(
  data: CycleData
): Promise<CyclePrediction & { _meta: MLPredictionMeta }> {

  // Try direct API call first (for production)
  if (ML_API_URL && ML_API_URL !== "http://127.0.0.1:8001") {
    try {
      const response = await fetch(`${ML_API_URL}/ml-predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model_type: "cycle",
          input_data: {
            ...data,
            lastPeriodStart: data.lastPeriodStart.toISOString()
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        const p = result.prediction;
        return {
          predictedStartDate: new Date(p.predictedStartDate),
          confidenceLevel: p.confidenceLevel,
          averageCycleLength: p.averageCycleLength,
          cycleVariability: p.cycleVariability,
          isIrregular: p.isIrregular,
          pcosRiskFlag: false,
          delayAdjustment: 0,
          _meta: { usedAPI: true }
        };
      }
    } catch (err) {
      console.warn("Direct API call failed, falling back to Supabase:", err);
    }
  }

  // Fallback to Supabase functions
  try {

    const { data: response, error } =
      await supabase.functions.invoke("ml-predict", {
        body: {
          model_type: "cycle",
          input_data: {
            ...data,
            lastPeriodStart: data.lastPeriodStart.toISOString()
          }
        }
      });

    if (error) throw error;

    const p = response.prediction;

    return {
      predictedStartDate: new Date(p.predictedStartDate),
      confidenceLevel: p.confidenceLevel,
      averageCycleLength: p.averageCycleLength,
      cycleVariability: p.cycleVariability,
      isIrregular: p.isIrregular,
      pcosRiskFlag: false,
      delayAdjustment: 0,
      _meta: { usedAPI: true }
    };

  } catch (err: any) {

    return {
      predictedStartDate: new Date(),
      confidenceLevel: "low",
      averageCycleLength: 28,
      cycleVariability: 0,
      isIrregular: false,
      pcosRiskFlag: false,
      delayAdjustment: 0,
      _meta: { usedAPI: false, error: err.message }
    };
  }
}
