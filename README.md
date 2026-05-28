# Tacheon Assessment — Data & AI Product Engineer

## Repository Structure
- `task1-product-scoping/` — Product brief and scoping decisions
- `task2-pipeline/` — Python data pipeline (Open-Meteo → BigQuery)

---

## Task 2: Pipeline

### API Choice: Open-Meteo
Chosen because it requires no API key, returns clean structured 
JSON, and weather data is relevant to marketing use cases such as 
correlating campaign performance with weather conditions.

### How to Run
1. Install dependencies:
   pip install requests pandas google-cloud-bigquery pandas-gbq db-dtypes
2. Authenticate with Google:
   gcloud auth application-default login
3. Run the pipeline:
   python task2-pipeline/pipeline.py

### BigQuery Setup
- Go to console.cloud.google.com/bigquery
- Note your Project ID
- Create dataset: weather_pipeline
- Update bq_project in pipeline.py with your Project ID
- Run the pipeline — forecasts table is created automatically

### SQL Summary Query
See task2-pipeline/queries/summary.sql

### Query Output
| date | location | max_temp_c | min_temp_c | temp_range_c | rainfall_mm |
|------|----------|------------|------------|--------------|-------------|
| 2026-05-28 | Chennai | 39.3 | 29.7 | 9.6 | 0.0 |
| 2026-05-29 | Chennai | 39.8 | 29.0 | 10.8 | 0.0 |
| 2026-05-30 | Chennai | 37.5 | 28.5 | 9.0 | 1.2 |
| 2026-05-31 | Chennai | 37.9 | 28.1 | 9.8 | 4.9 |
| 2026-06-01 | Chennai | 35.5 | 26.8 | 8.7 | 0.0 |
| 2026-06-02 | Chennai | 36.8 | 27.1 | 9.7 | 3.3 |
| 2026-06-03 | Chennai | 35.7 | 26.3 | 9.4 | 5.4 |

### Production Thinking

**Scheduling:** Use Google Cloud Scheduler to trigger a Cloud 
Function running this pipeline daily at 6am IST.

**Failure alerting:** Pipeline writes status logs to a 
pipeline_runs BigQuery table. A Cloud Monitoring alert emails 
the team if no successful run is logged by 7am.

**Scaling to 10x volume:** Switch to GCS-staged loads instead 
of loading directly from dataframe. Partition the BigQuery table 
by date. Add pagination to the API fetch layer. Use async 
requests if pulling data for multiple locations in parallel.
