# API Harbor

This project provides a system to fetch, translate, and store data from an external API into Elasticsearch. It includes a backend implemented using FastAPI, Elasticsearch for data storage, and a potential frontend using ChartJS for visualizing the stored data.

# API Usage

Welcome to the API documentation for [Your Project Name]! This API provides information from Exchangerates and Weather APIs.

## Base URL

The base URL for the API is: `http://localhost:8000/api`

## Endpoints

### Exchangerates API

#### Fetch, Translate, and Store Data

- **Endpoint:**
  - Method: GET
  - Path: `/exchangerates`

This endpoint fetches data from the Exchangerates API, translates it, and stores it in Elasticsearch.

#### Get Data from Elasticsearch

- **Endpoint:**
  - Method: GET
  - Path: `/data/exchangerates`

This endpoint retrieves data from Elasticsearch that was previously fetched from the Exchangerates API.

### Weather API

#### Fetch, Translate, and Store Data

- **Endpoint:**
  - Method: GET
  - Path: `/weather`

This endpoint fetches data from the Weather API, translates it, and stores it in Elasticsearch.

#### Get Data from Elasticsearch

- **Endpoint:**
  - Method: GET
  - Path: `/data/weather`

This endpoint retrieves data from Elasticsearch that was previously fetched from the Weather API.

## How to Use

1. **Fetch Exchangerates Data:**

   ```bash
   curl -X GET http://localhost:8000/api/exchangerates
