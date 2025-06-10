from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions,ContentSettings
import azure.cosmos.cosmos_client as cosmos_client
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest,DocumentContentFormat

import urllib.parse

from datetime import datetime, timedelta

import logging

from utils.config import (
   AZURE_STORAGE_CONNECTION_STRING,
AZURE_STORAGE_CONTAINER_NAME,
COSMOS_ACCOUNT_URI ,
COSMOS_MASTER_KEY,
COSMOS_DATABASE_ID,
COSMOS_CONTAINER_EMPLOYEE,
DI_ENDPOINT,
DI_KEY
)


def extract_markdown_doc_intel(pdf_bytes):
    try:
        document_intelligence_client = DocumentIntelligenceClient(endpoint=DI_ENDPOINT, credential=AzureKeyCredential(DI_KEY))
        logging.info("CALLED: Document Intelligence")
        poller = document_intelligence_client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=AnalyzeDocumentRequest(bytes_source=pdf_bytes),
            output_content_format=DocumentContentFormat.MARKDOWN
        )
        return poller.result()
    except Exception as e:
        logging.error(f"Document Intelligence processing failed: {e}")


def generate_sas_token(blob_service_client: BlobServiceClient, container_name: str, blob_name: str) -> str:
    """Generate a SAS token for blob access."""
    try:
        # Generate SAS token with read permission that expires in 5 hours
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now() + timedelta(hours=5)
        )
        return sas_token
    except Exception as e:
        logging.error(f"Failed to generate SAS token: {str(e)}")
        return ""

def generate_document_link(blob_name: str, page_number: int) -> str:
    """Generate a SAS URL for a specific document with page reference."""
    # Input validation
    if not blob_name:
        logging.warning("Empty blob name provided to generate_document_link")
        return ""
    
    logging.info(f"Generating document link: blob_name='{blob_name}', page={page_number}")
        
    try:
        # Get environment variables
        connection_string = AZURE_STORAGE_CONNECTION_STRING
        container_name = AZURE_STORAGE_CONTAINER_NAME
        
        if not connection_string or not container_name:
            logging.error("Required environment variables are missing")
            return ""

        # Create blob service client
        try:
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        except Exception as e:
            logging.error(f"Failed to create blob service client: {str(e)}")
            return ""
            
        # Generate SAS token using the new function
        sas_token = generate_sas_token(blob_service_client, container_name, blob_name)
        if not sas_token:
            return ""

        # Encode the blob name to handle special characters
        encoded_blob_name = urllib.parse.quote(blob_name)

        # Construct full URL
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{encoded_blob_name}?{sas_token}"

        # Add page reference
        if page_number is not None and page_number > 0:
            blob_url += f"#page={page_number}"

        # Log the full URL for debugging (but mask part of the SAS token for security)
        masked_url = blob_url.replace(sas_token, sas_token[:10] + "...")
        
        return blob_url
    except Exception as e:
        logging.error(f"Error generating document link: {str(e)}", exc_info=True)
        return ""
    

def get_cosmos_client(host, master_key):
    return cosmos_client.CosmosClient(host, {'masterKey': master_key}, user_agent="CosmosDBNDDatabase", user_agent_overwrite=True)

def get_container_client(client, database_id, container_id):
    db = client.get_database_client(database_id)
    return db.get_container_client(container_id)

def get_container():
    client = get_cosmos_client(COSMOS_ACCOUNT_URI, COSMOS_MASTER_KEY)
    return get_container_client(client, COSMOS_DATABASE_ID, COSMOS_CONTAINER_EMPLOYEE)


def read_items(container):
    return list(container.read_all_items(max_item_count=300)) #max item count still load everything but the sdk will do paginated behind the scene

# ### for file management
def add_item(container, item_data): 
    container.create_item(body=item_data)

def upload_file_to_blob(blob_file, file_name):
    try:
         
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=file_name)
        blob_client.upload_blob(blob_file, overwrite=True)

        # set blob properties Content-type
        content_settings = ContentSettings(content_type='application/pdf')
        blob_client.set_http_headers(content_settings)
        # Add metadata to the uploaded blob
        metadata = {"isDeleted": "False"}
        blob_client.set_blob_metadata(metadata)
    except Exception as err:
        logging.error(f"Something went wrong: {err}")