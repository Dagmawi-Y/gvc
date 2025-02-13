from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from urllib.parse import urlparse

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

    def _is_valid_github_profile(self, referrer: str, username: str) -> bool:
        if not referrer:
            return False
            
        parsed = urlparse(referrer)
        path_parts = parsed.path.strip('/').split('/')
        
        return (parsed.netloc == "github.com" and 
                len(path_parts) == 1 and
                path_parts[0].lower() == username.lower() and
                not parsed.query)

    async def can_increment_view(self, username: str, referrer: str, rate_limit_minutes: int = 60) -> bool:
        try:
            if not self._is_valid_github_profile(referrer, username):
                return False

            current_time = time.time()
            cache_key = username
            
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=self.ip_collection_id,
                queries=[Query.equal('cache_key', cache_key)]
            )

            if result['total'] > 0:
                doc = result['documents'][0]
                last_view_time = float(doc['last_view_time'])
                
                if current_time - last_view_time < rate_limit_minutes * 60:
                    return False
                
                self.database.update_document(
                    database_id=self.database_id,
                    collection_id=self.ip_collection_id,
                    document_id=doc['$id'],
                    data={'last_view_time': str(current_time)}
                )
            else:
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
            print(f"Error checking cache: {e}")
            return False 