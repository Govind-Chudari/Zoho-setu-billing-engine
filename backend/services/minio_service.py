from minio import Minio
from minio.error import S3Error
from config import Config
import io

minio_client = Minio(
    Config.MINIO_ENDPOINT,
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    secure=Config.MINIO_SECURE
)


def get_bucket_name(username):
    """
    Each user gets their own bucket.
    MinIO bucket names must be lowercase and no special characters.
    Example: username "Rahul_K" becomes bucket "user-rahul-k"
    """
    clean = username.lower().replace("_", "-").replace(" ", "-")
    return f"user-{clean}"


def create_user_bucket(username):
    """
    Called when a new user registers.
    Creates a private bucket just for them.
    """
    bucket_name = get_bucket_name(username)
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"✅ Bucket created: {bucket_name}")
        else:
            print(f"ℹ️  Bucket already exists: {bucket_name}")
        return True
    except S3Error as e:
        print(f"❌ Error creating bucket: {e}")
        return False


def upload_file(username, file_data, filename, content_type, file_size):
    """
    Uploads a file to the user's bucket.
    
    username     - who is uploading
    file_data    - the actual file bytes
    filename     - what to name the file in storage
    content_type - e.g. "image/png", "application/pdf"
    file_size    - size in bytes
    """
    bucket_name = get_bucket_name(username)
    try:
        minio_client.put_object(
            bucket_name,
            filename,
            io.BytesIO(file_data),
            length=file_size,
            content_type=content_type
        )
        print(f"✅ File uploaded: {filename} to bucket {bucket_name}")
        return True
    except S3Error as e:
        print(f"❌ Upload error: {e}")
        return False


def download_file(username, filename):
    """
    Downloads a file from the user's bucket.
    Returns the file data as bytes, or None if not found.
    """
    bucket_name = get_bucket_name(username)
    try:
        response = minio_client.get_object(bucket_name, filename)
        file_data = response.read()
        response.close()
        response.release_conn()
        return file_data
    except S3Error as e:
        print(f"❌ Download error: {e}")
        return None


def delete_file(username, filename):
    """
    Deletes a file from the user's bucket.
    """
    bucket_name = get_bucket_name(username)
    try:
        minio_client.remove_object(bucket_name, filename)
        print(f"✅ File deleted: {filename} from {bucket_name}")
        return True
    except S3Error as e:
        print(f"❌ Delete error: {e}")
        return False


def list_files(username):
    """
    Lists all files in the user's bucket.
    Returns a list of file info dictionaries.
    """
    bucket_name = get_bucket_name(username)
    files = []
    try:
        objects = minio_client.list_objects(bucket_name)
        for obj in objects:
            files.append({
                "filename": obj.object_name,
                "size_bytes": obj.size,
                "size_kb": round(obj.size / 1024, 2),
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None
            })
        return files
    except S3Error as e:
        print(f"❌ List error: {e}")
        return []


def get_file_size(username, filename):
    """
    Returns the size of a specific file in bytes.
    """
    bucket_name = get_bucket_name(username)
    try:
        stat = minio_client.stat_object(bucket_name, filename)
        return stat.size
    except S3Error:
        return 0


def get_total_storage_used(username):
    """
    Calculates total storage used by a user across all their files.
    Returns size in bytes.
    """
    files = list_files(username)
    return sum(f["size_bytes"] for f in files)