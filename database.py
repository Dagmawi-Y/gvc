from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from urllib.parse import urlparse
import hashlib

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

    def _hash_ip(self, ip: str) -> str:
        """Hash IP address for privacy"""
        return hashlib.sha256(ip.encode()).hexdigest()[:16]

    def _is_valid_github_profile(self, referrer: str, username: str) -> bool:
        if not referrer:
            return False
            
        parsed = urlparse(referrer)
        path_parts = parsed.path.strip('/').split('/')
        
        return (parsed.netloc == "github.com" and 
                len(path_parts) == 1 and
                path_parts[0].lower() == username.lower() and
                not parsed.query and
                not parsed.fragment)

    def _is_bot(self, user_agent: str) -> bool:
        """Check if request is from a bot"""
        bot_strings = ['bot', 'crawler', 'spider', 'curl', 'wget', 'python', 'http']
        user_agent = user_agent.lower()
        return any(bot in user_agent for bot in bot_strings)

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

    async def can_increment_view(self, username: str, ip: str, referrer: str, user_agent: str, rate_limit_minutes: int = 60) -> bool:
        try:
            if self._is_bot(user_agent):
                return False

            if not self._is_valid_github_profile(referrer, username):
                return False

            current_time = time.time()
            hashed_ip = self._hash_ip(ip)
            cache_key = f"{hashed_ip}:{username}"
            
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=self.ip_collection_id,
                queries=[Query.equal('cache_key', cache_key)]
            )

            if result['total'] > 0:
                doc = result['documents'][0]
                last_view_time = float(doc['last_view_time'])
                attempts = int(doc.get('attempts', 0))
                
                if current_time - last_view_time < rate_limit_minutes * 60:
                    self.database.update_document(
                        database_id=self.database_id,
                        collection_id=self.ip_collection_id,
                        document_id=doc['$id'],
                        data={'attempts': attempts + 1}
                    )
                    return False
                
                self.database.update_document(
                    database_id=self.database_id,
                    collection_id=self.ip_collection_id,
                    document_id=doc['$id'],
                    data={
                        'last_view_time': str(current_time),
                        'attempts': 0
                    }
                )
            else:
                self.database.create_document(
                    database_id=self.database_id,
                    collection_id=self.ip_collection_id,
                    document_id='unique()',
                    data={
                        'cache_key': cache_key,
                        'last_view_time': str(current_time),
                        'attempts': 0
                    }
                )
            
            return True
            
        except Exception as e:
            print(f"Error checking cache: {e}")
            return False 