import json
from datetime import timedelta
import traceback

from couchbase.exceptions import CouchbaseException
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions

# --- Couchbase Connection ---
endpoint = "couchbases://cb.1rsxs0hrd0ojm0pu.cloud.couchbase.com"  # Replace with your Capella endpoint
username = "SIH-2025"   # Replace with your cluster username
password = "Sih-2025"   # Replace with your cluster password
bucket_name = "travel-sample"   # You can use another bucket if needed
scope_name = "tenant_agent_00"   # Use default scope unless you created a custom one
collection_name = "bookings"   # Use default collection unless you created a custom one

# --- Load your combined JSON file ---
combined_json_path = r"C:\SIH_BACKEND\combined_data.json"
with open(combined_json_path, "r", encoding="utf-8") as f:
    combined_data = json.load(f)

# --- Connect to Couchbase ---
auth = PasswordAuthenticator(username, password)
options = ClusterOptions(auth)
options.apply_profile("wan_development")

try:
    cluster = Cluster(endpoint, options)
    cluster.wait_until_ready(timedelta(seconds=10))

    # Get bucket, scope, and collection
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)

    # Key for your document (unique ID in Couchbase)
    key = "combined_json_2025"

    # Insert combined JSON into Couchbase
    try:
        result = cb_coll.insert(key, combined_data)
        print("\n✅ Inserted combined JSON into Couchbase. CAS:", result.cas)
    except CouchbaseException as e:
        print("\n⚠️ Insert failed:", e)

    # Retrieve it back
    try:
        result = cb_coll.get(key)
        print("\n📥 Retrieved JSON from Couchbase:")
        print(json.dumps(result.content_as[dict], indent=4, ensure_ascii=False))
    except CouchbaseException as e:
        print("\n⚠️ Fetch failed:", e)

except Exception as e:
    traceback.print_exc()
