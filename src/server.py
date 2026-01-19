#!/usr/bin/env python3
import os
import logging
import sys
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from google.api_core.exceptions import InvalidArgument
from google.cloud import retail_v2
from google.api_core.client_options import ClientOptions

# 1. 
# Ensure .env is loaded from the script's actual directory
# ADK runs this as a subprocess, so relative paths often fail.
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 2. Redirect logs to stderr. 
# Stdio transport uses stdout for the MCP protocol. 
# If a logger prints to stdout, the ADK will see it as a "malformed JSON" error.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Explicitly force logs to stderr
)
logger = logging.getLogger(__name__)

# --- Google Cloud Settings ---
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION", "global")
CATALOG_ID = os.getenv("CATALOG_ID")
SERVING_CONFIG_ID = os.getenv("SERVING_CONFIG_ID", "default_serving_config")

# --- FastMCP Server Setup ---
mcp = FastMCP(
    "MCP for Vertex AI Search for Commerce")

@mcp.tool
def search_products(
    query: str,
    visitor_id: str = "guest-user",
    brand: str = "",          
    color_families: str = "", 
    category: str = "",        
    size: str = "",            
    gender: str = "",          
    min_price: float = None,   
    max_price: float = None,   
    page_size: int = 5,
):
  """
  Searches the product catalog for a given query and returns product details.

  Args:
    query: The search term (e.g., "running shoes").
    brand: Filter by brand name.
    color_families: Filter by color.
    category: Filter by product category.
    size: Filter by size. ONLY use the raw value (e.g., "42", "M"). DO NOT include units or parenthetical text like "(EU size)".
    gender: Filter by gender (e.g., "Hombre", "Mujer", "Unisex").
    min_price: Minimum price filter.
    max_price: Maximum price filter.
    page_size: Number of results to return.
  """
  # 5 Lazy Initialization
  client_options = ClientOptions(quota_project_id=PROJECT_ID)
  search_client = retail_v2.SearchServiceClient(client_options=client_options)
  product_client = retail_v2.ProductServiceClient(client_options=client_options)

  placement = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/"
    f"catalogs/{CATALOG_ID}/servingConfigs/{SERVING_CONFIG_ID}"
  )
  
  try:
    filter_conditions = []
    if brand: filter_conditions.append(f'(brand: ANY("{brand}"))')
    if color_families: filter_conditions.append(f'(colorFamilies: ANY("{color_families}"))')
    if category: filter_conditions.append(f'(categories: ANY("{category}"))')
    if size: filter_conditions.append(f'(attributes.sizes: ANY("{size.strip()}"))')
    if gender: filter_conditions.append(f'(attributes.gender: ANY("{gender}"))')
    
    if min_price is not None: filter_conditions.append(f'(price >= {min_price})')
    if max_price is not None: filter_conditions.append(f'(price <= {max_price})')

    filter_str = " AND ".join(filter_conditions) if filter_conditions else ""
    logger.info(f"Searching with query: '{query}' and filter: '{filter_str}'")

    search_request = retail_v2.SearchRequest(
      placement=placement,
      query=query,
      visitor_id=visitor_id,
      filter=filter_str,
      page_size=page_size,
    )

    search_response = search_client.search(request=search_request)

    results = []
    for result in search_response.results:
      product_name = result.product.name
      logger.info(f"Fetching details for: {product_name}")

      product_detail = product_client.get_product(name=product_name)
      product_dict = retail_v2.Product.to_dict(product_detail)
      results.append(product_dict)
    
    return results

  except Exception as e:
    logger.error(f"Error: {e}")
    return {"error": str(e)}

if __name__ == "__main__":
  # 7 Default to Stdio.
  # Not using transport="http".
  # When the ADK launches this script, it expects to talk via stdin/stdout.
  mcp.run()