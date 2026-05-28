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

## Production Thinking

### How would you schedule this pipeline to run automatically?
I would use Google Cloud Scheduler to trigger the pipeline once 
daily at 6am IST. It would send an HTTP request to a Cloud Function 
that runs pipeline.py. Alternatively, if the team already uses 
Apache Airflow, I would wrap this in a DAG and schedule it there 
instead, keeping it consistent with existing tools.

### How would you know if it failed?
Two ways:
1. At the end of every run, the pipeline writes a status record 
   (success/fail, row count, timestamp, error message if any) to 
   a separate BigQuery table called pipeline_runs. This gives a 
   full audit trail of every execution.
2. A Cloud Monitoring alert checks that table every morning. If 
   no successful run is recorded by 7am, it sends an email alert 
   to the team. Currently the pipeline already logs INFO and ERROR 
   messages using Python's logging module, so failures are visible 
   in Cloud Function logs immediately.

### What would you add or change if this pipeline needed to scale to 10x the data volume?
Three main changes:
1. Switch from loading directly from a dataframe to staging data 
   in Google Cloud Storage first, then loading from GCS into 
   BigQuery. More reliable and efficient for larger volumes.
2. Partition the BigQuery table by date so queries only scan 
   the relevant date range — faster and cheaper at scale.
3. Use async requests to fetch data for multiple locations in 
   parallel rather than one at a time.

---

## Walkthrough

### What I built and why
I chose the Open-Meteo API because it requires no API key, returns 
clean structured JSON, and works immediately with no setup friction. 
This let me focus on building the pipeline well rather than spending 
time on authentication.

The pipeline fetches 7-day weather forecast data for Chennai, 
transforms it into a clean tabular format with two derived fields 
(temperature range and rainy day flag), and loads it into BigQuery.

### Decisions I made
- Used WRITE_TRUNCATE in BigQuery so each run replaces previous 
  data rather than appending duplicates. For a forecast pipeline 
  this makes sense since yesterday's forecast is no longer relevant.
- Added temp_range_c as a derived field because raw max/min 
  temperatures alone don't show the day's variability clearly.
- Kept all config in a single CONFIG dictionary at the top so 
  anyone can change location or BigQuery settings without touching 
  the logic.
- Used Python's logging module throughout so the pipeline is 
  transparent at every step.

### What I would do differently with more time
- Add a pipeline_runs audit table in BigQuery to track every 
  execution automatically.
- Pull data for multiple cities to make the dataset more useful 
  for cross-location analysis.
- Write unit tests for the transform function to catch data 
  quality issues early.
- Add a data validation step after loading to check row count, 
  null values, and date ranges.
