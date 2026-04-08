"""Typed response schemas for prediction APIs."""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PredictionModelScores(BaseModel):
    xgboost: float
    random_forest: float


class PredictionResultSchema(BaseModel):
    delay_probability: float
    estimated_delay_minutes: int
    confidence: str
    risk_band: str
    severity_band: str
    recommendations: List[str] = Field(default_factory=list)
    explanations: List["PredictionExplanationItemSchema"] = Field(default_factory=list)
    model_scores: Optional[PredictionModelScores] = None
    error: Optional[str] = None


class PredictionResponseSchema(BaseModel):
    success: bool
    data: PredictionResultSchema
    message: str


class PredictionInputSchema(BaseModel):
    airline: str
    origin: str
    destination: str
    departure_datetime: str
    weather_condition: Optional[str] = None


class BatchPredictionItemSchema(BaseModel):
    input: PredictionInputSchema
    prediction: PredictionResultSchema


class BatchPredictionResponseSchema(BaseModel):
    success: bool
    data: List[BatchPredictionItemSchema]
    message: str


class FeatureImportanceItemSchema(BaseModel):
    feature: str
    importance: float


class PredictionExplanationItemSchema(BaseModel):
    factor: str
    impact: str
    message: str


class ModelMetricSummarySchema(BaseModel):
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None


class ModelInfoDataSchema(BaseModel):
    model_config = ConfigDict(extra="allow")

    status: str
    xgboost: Optional[ModelMetricSummarySchema] = None
    random_forest: Optional[ModelMetricSummarySchema] = None
    ensemble: Optional[ModelMetricSummarySchema] = None
    feature_importance: List[FeatureImportanceItemSchema] = Field(default_factory=list)
    dataset_size: Optional[int] = None
    train_size: Optional[int] = None
    test_size: Optional[int] = None
    trained_at: Optional[str] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    features: List[str] = Field(default_factory=list)


class ModelInfoResponseSchema(BaseModel):
    success: bool
    data: ModelInfoDataSchema
    message: str


class PredictionHistoryItemSchema(BaseModel):
    id: int
    created_at: Optional[str] = None
    airline: str
    origin: str
    destination: str
    departure_datetime: Optional[str] = None
    delay_probability: float
    estimated_delay_minutes: int
    risk_band: str
    severity_band: str
    confidence: str


class PredictionHistoryListSchema(BaseModel):
    items: List[PredictionHistoryItemSchema] = Field(default_factory=list)
    page: int
    limit: int
    total: int
    total_pages: int


class PredictionHistoryResponseSchema(BaseModel):
    success: bool
    data: PredictionHistoryListSchema
    message: str


PredictionResultSchema.model_rebuild()
