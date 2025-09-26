from pydantic import BaseModel, Field
from typing import List, Optional
from llama_cloud import ExtractConfig, ExtractMode
from llama_cloud_services import LlamaExtract
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

LLAMA_KEY = os.getenv("LLAMA_KEY")

# Initialize the extractor client
extractor = LlamaExtract(api_key=LLAMA_KEY)


# Nested schema for irrigation details
class IrrigationDetail(BaseModel):
    duration: str = Field(description="Duration of irrigation")
    fields_watered: Optional[List[str]] = Field(description="Which fields or crops were watered")
    method: Optional[str] = Field(description="Irrigation method used (drip, sprinkler, flood)")
    water_source: Optional[str] = Field(description="Source of water for irrigation")


# Nested schema for soil and fertilizer info
class SoilFertilizer(BaseModel):
    soil_condition: str = Field(description="Current soil condition")
    soil_tests: Optional[str] = Field(description="Soil pH or nutrient test results")
    fertilizers_applied: Optional[List[str]] = Field(description="List of fertilizers or compost applied")


# Nested schema for pest and disease
class PestDisease(BaseModel):
    observed: Optional[List[str]] = Field(description="Observed pests or diseases")
    treatment_applied: Optional[List[str]] = Field(description="Treatment applied for pests/diseases")
    damage_notes: Optional[str] = Field(description="Any crop damage observed")


# Nested schema for labor or operations
class LaborOperations(BaseModel):
    tasks_completed: Optional[List[str]] = Field(description="Tasks done today like weeding, pruning")
    labor_hours: Optional[float] = Field(description="Number of hours spent on tasks")
    workers: Optional[List[str]] = Field(description="People involved in farm operations")


# Nested schema for machinery info
class Machinery(BaseModel):
    equipment_used: Optional[List[str]] = Field(description="Machinery or tools used")
    maintenance_notes: Optional[str] = Field(description="Repairs or maintenance done")
    fuel_used: Optional[str] = Field(description="Fuel consumption for machinery")


# Nested schema for weather info
class Weather(BaseModel):
    temperature: Optional[str] = Field(description="Temperature today (min/max)")
    rainfall: Optional[str] = Field(description="Rainfall amount")
    humidity: Optional[str] = Field(description="Humidity level")
    wind: Optional[str] = Field(description="Wind speed/direction")
    sunlight_hours: Optional[str] = Field(description="Hours of sunlight or cloud cover")


# Main farm log schema
class FarmLog(BaseModel):
    date: Optional[str] = Field(description="Date of the log")
    irrigation: Optional[IrrigationDetail] = Field(description="Irrigation info")
    soil_fertilizer: Optional[SoilFertilizer] = Field(description="Soil and fertilizer info")
    pest_disease: Optional[PestDisease] = Field(description="Pest and disease info")
    labor_operations: Optional[LaborOperations] = Field(description="Labor and operations info")
    machinery: Optional[Machinery] = Field(description="Machinery and equipment info")
    weather: Optional[Weather] = Field(description="Weather and environmental info")
    crops: Optional[List[str]] = Field(description="List of crops grown by the farmer")
    additional_notes: Optional[str] = Field(description="Any other observations or notes")


# Configure extraction settings
config = ExtractConfig(extraction_mode=ExtractMode.FAST)

# Extract data from farm log file
farm_log_file = "C:\SIH_BACKEND\Log_data\sample.txt"  # replace with your file
result = extractor.extract(FarmLog, config, farm_log_file)

# Print structured metadata
print(result.data)