from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

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
            # Special handling for GitHub camo
            if "github-camo" in user_agent.lower():
                visitor_id = f"{username}_github_camo" if username else "anonymous_github_camo"
            else:
                # Regular visitor identification
                visitor_id = f"{ip}_{user_agent}"
                if username:
                    visitor_id = f"{username}_{visitor_id}"
            
            current_time = datetime.now(timezone.utc)
            print(f"Debug - Current time (UTC): {current_time}")
            
            result = self.database.list_documents(
                database_id=self.database_id,
                collection_id=os.getenv('IP_COLLECTION_ID'),
                queries=[Query.equal('visitor_id', visitor_id)]
            )
            
            if result['total'] == 0:
                print(f"Debug - New visitor: {visitor_id}")
                self.database.create_document(
                    database_id=self.database_id,
                    collection_id=os.getenv('IP_COLLECTION_ID'),
                    document_id='unique()',
                    data={
                        'visitor_id': visitor_id,
                        'ip': ip,
                        'username': username,
                        'user_agent': user_agent,
                        'referrer': referrer,
                        'last_visit': current_time.isoformat()
                    }
                )
                return True
            else:
                last_visit = datetime.fromisoformat(result['documents'][0]['last_visit'])
                if last_visit.tzinfo is None:
                    last_visit = last_visit.replace(tzinfo=timezone.utc)
                
                time_diff = current_time - last_visit
                seconds_passed = time_diff.total_seconds()
                print(f"Debug - Last visit: {last_visit}")
                print(f"Debug - Time difference in seconds: {seconds_passed}")
                print(f"Debug - Required seconds: {rate_limit_minutes * 60}")
                
                if seconds_passed >= (rate_limit_minutes * 60):
                    print(f"Debug - Updating last visit for: {visitor_id}")
                    self.database.update_document(
                        database_id=self.database_id,
                        collection_id=os.getenv('IP_COLLECTION_ID'),
                        document_id=result['documents'][0]['$id'],
                        data={
                            'last_visit': current_time.isoformat(),
                            'referrer': referrer
                        }
                    )
                    return True
                print(f"Debug - Rate limited: {visitor_id}")
                return False
                
        except Exception as e:
            print(f"Error in can_increment_view: {e}")
            return False