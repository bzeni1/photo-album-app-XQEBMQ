import os
from supabase import create_client

def get_supabase_admin():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SupaBase URL or Supabase Role Key")
    return create_client(url, key)