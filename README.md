# API Harbor

API Harbor is a modular and scalable system designed for fetching, translating, and storing data from various APIs. The system is divided into two main components: `server` and `worker`.

### Components

1. **Server:**
   - Responsible for handling API configurations, scheduling tasks, and serving API endpoints.
   - Ensures essential environment variables are set before processing.
   - Uses FastAPI for building API endpoints.
   - Utilizes `loguru` for logging and `dotenv` for handling environment variables.

2. **Worker:**
   - Focuses on the asynchronous fetching of data, translation, and storage.
   - Runs scheduled tasks to periodically fetch and store data from configured APIs.
   - Separated from the server for scalability, allowing the system to handle a large number of APIs concurrently.

### Key Features

- Dynamic API configuration: APIs are configured via environment variables, providing flexibility.
- Asynchronous Processing: Utilizes asynchronous programming to efficiently handle multiple API requests concurrently.
- Elasticsearch Integration: Stores fetched data in Elasticsearch for easy retrieval and analysis.

### Usage

1. **Environment Variables:**
   - Essential configuration parameters such as API URLs, API keys, and Elasticsearch settings are set using environment variables.

2. **API Configuration:**
   - APIs are configured in the `create_api_handler` function, specifying details such as API URLs, keys, and parsing functions.

3. **Scheduling:**
   - Scheduled tasks are defined in the `scheduled_tasks` list, specifying the APIs to fetch data from and the interval.

4. **Logging:**
   - Logging is done using `loguru` with different log levels to facilitate debugging and monitoring.

### Recommendations

- Consider enhancing modularity by using dependency injection, especially for components like the Elasticsearch client.
- Continuously document code to improve readability for maintainers and collaborators.
- Regularly update and review dependencies to ensure compatibility and security.

### Future Improvements

- Implement a more sophisticated workflow orchestrator, such as Temporal, for enhanced task scheduling and management.
- Explore options for handling API configuration dynamically, allowing runtime modifications without restarting the server.

# Setup

```sh
docker-compose exec opensearch bash -c "chmod +x plugins/opensearch-security/tools/securityadmin.sh && bash plugins/opensearch-security/tools/securityadmin.sh -cd config/opensearch-security -icl -nhnv -cacert config/certificates/ca/ca.pem -cert config/certificates/ca/admin.pem -key config/certificates/ca/admin.key -h localhost"
```

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
