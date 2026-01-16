# Vertex AI Search for Commerce MCP Server

This project is a Model Context Protocol (MCP) server example that provides the [Vertex AI Search for Commerce](https://cloud.google.com/solutions/vertex-ai-search-commerce?hl=en) API from Google Cloud as a tool, using [FastMCP](https://github.com/fastmcp/fastmcp-py).

Through this server, an AI agent can search a product catalog using natural language queries.

## Key Features

-   Lightweight MCP server based on FastMCP
-   Provides Vertex AI Search for Commerce product search functionality (`search_products`)
-   Easy setup using a `.env` file

## Prerequisites

-   Python 3.8 or higher
-   [uv](https://github.com/astral-sh/uv) (a fast Python package installer and virtual environment manager)
-   [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`)

## Installation and Setup

1.  **Google Cloud Authentication**

    Set up Application Default Credentials (ADC) to access Google Cloud services from your local environment. Run the command below in your terminal and complete the authentication through your browser.

    ```bash
    gcloud auth application-default login
    ```

2.  **Environment Variable Setup**

    Copy the `.env.example` file in the project root directory to a new `.env` file, then modify the contents to match your Google Cloud environment.

    ```bash
    cp .env.example .env
    ```

    **`.env` file contents:**
    ```
    PROJECT_ID="your-gcp-project-id"
    LOCATION="global"
    CATALOG_ID="default_catalog"
    SERVING_CONFIG_ID="default_serving_config"
    ```

3.  **Create Virtual Environment and Install Dependencies**

    Use `uv` to create a virtual environment and install the necessary libraries.

    ```bash
    # Create virtual environment
    uv venv

    # Activate virtual environment (macOS/Linux)
    source .venv/bin/activate
    # (Windows: .venv\Scripts\activate)

    # Install dependencies
    uv pip install -r requirements.txt
    ```

## Running the Server

You can run the Python script directly using `uv`'s execution feature.

```bash
uv run python src/server.py
```

### Running the Server (using fastmcp)

You can also run the server using the CLI provided by the `fastmcp` library. This method automatically finds and runs the `FastMCP` instance.

Specify the module path where the `mcp` instance is located. You can use the `--port` option to specify a different port instead of the default (8080).

```bash
fastmcp run src/server.py --transport http --port 9000
```

When the server starts successfully, you will see a message like this:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
```

## Provided Tools

This MCP server provides the following tool:

### `search_products`

-   **Description**: Searches for products in the product catalog based on a given query. For detailed information on filtering and ordering, see the [official documentation](https://cloud.google.com/retail/docs/filter-and-order).
-   **Parameters**:
    -   `query` (str): The product keyword to search for (e.g., "jeans", "sneakers").
    -   `visitor_id` (str, optional): A unique ID to identify the user. Used for personalized search results. (Default: "guest-user")
    -   `brand` (str, optional): Brand to filter by.
    -   `color_families` (str, optional): Color family to filter by.
    -   `category` (str, optional): Category to filter by.
    -   `size` (str, optional): Size to filter by.
    -   `page_size` (int): The number of results to return per page. (Default: 10)
-   **Returns**: A stream of dictionaries, where each dictionary contains the full details of a found product.

---

## Google Cloud Run Deployment Guide

TBD
---

## Reference

-  [Model Context Protocol (MCP) - Introduction](https://modelcontextprotocol.io/introduction)
-  [FastMCP - Quickstart](https://gofastmcp.com/getting-started/quickstart)
-  [MCP Tools Documentation](https://google.github.io/adk-docs/tools/mcp-tools/)
-  [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector): an interactive developer tool for testing and debugging MCP servers
-  [Importing Catalog Information to Vertex AI Search for Commerce](https://cloud.google.com/retail/docs/retail-api-tutorials#import_catalog_information)
    -  💻 [Sample Code on GitHub](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/retail/interactive-tutorials/product)
-  [Searching for Products with Vertex AI Search for Commerce](https://cloud.google.com/retail/docs/retail-api-tutorials#search_tutorials)
    -  💻 [Sample Code on GitHub](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/retail/interactive-tutorials/search)
