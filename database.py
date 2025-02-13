from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

class AppwriteDB:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
        self.client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
        self.client.set_key(os.getenv('APPWRITE_API_KEY'))
        
        self.database = Databases(self.client)
        self.database_id = os.getenv('DATABASE_ID')
        self.collection_id = os.getenv('COLLECTION_ID')
        self.ip_collection_id = os.getenv('IP_COLLECTION_ID')

    async def get_views(self, repo: str) -> int:
        try:
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=self.collection_id,
                queries=[Query.equal('repository', repo)]
            )
            if result['total'] == 0:
                return 0
            return result['documents'][0]['count']
        except Exception:
            return 0

    async def increment_views(self, repo: str) -> int:
        try:
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=self.collection_id,
                queries=[Query.equal('repository', repo)]
            )
            
            current_time = datetime.now().isoformat()
            
            if result['total'] == 0:
                # Create new document
                doc = self.database.create_document(
                    database_id=self.database_id,
                    collection_id=self.collection_id,
                    document_id='unique()',
                    data={
                        'repository': repo,
                        'count': 1,
                        'last_updated': current_time
                    }
                )
                return 1
            else:
                # Update existing document
                doc = result['documents'][0]
                new_count = doc['count'] + 1
                self.database.update_document(
                    database_id=self.database_id,
                    collection_id=self.collection_id,
                    document_id=doc['$id'],
                    data={
                        'count': new_count,
                        'last_updated': current_time
                    }
                )
                return new_count
        except Exception as e:
            print(f"Error: {e}")
            return 0

    async def can_increment_view(self, ip: str, username: str, rate_limit_minutes: int = 60) -> bool:
        try:
            cache_key = f"{ip}:{username}"
            current_time = time.time()
            
            # Check existing record
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=self.ip_collection_id,
                queries=[Query.equal('cache_key', cache_key)]
            )

            if result['total'] > 0:
                doc = result['documents'][0]
                last_view_time = float(doc['last_view_time'])
                
                # Check if enough time has passed
                if current_time - last_view_time < rate_limit_minutes * 60:
                    return False
                
                # Update last view time
                self.database.update_document(
                    database_id=self.database_id,
                    collection_id=self.ip_collection_id,
                    document_id=doc['$id'],
                    data={'last_view_time': str(current_time)}
                )
            else:
                # Create new record
                self.database.create_document(
                    database_id=self.database_id,
                    collection_id=self.ip_collection_id,
                    document_id='unique()',
                    data={
                        'cache_key': cache_key,
                        'last_view_time': str(current_time)
                    }
                )
            
            return True
            
        except Exception as e:
            print(f"Error checking IP cache: {e}")
            return False  # On error, don't increment to be safe 