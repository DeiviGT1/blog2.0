# app/python/supabase_client.py
import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")


def get_client() -> Client:
    """Public client — uses anon key. Good for user-scoped auth operations."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_admin_client() -> Client:
    """Service-role client — bypasses RLS. Use only in trusted server-side code."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# ── Auth helpers ────────────────────────────────────────────────────────────

def sign_up(email: str, password: str, username: str):
    sb = get_client()
    return sb.auth.sign_up({
        "email": email,
        "password": password,
        "options": {"data": {"username": username}},
    })


def sign_in(email: str, password: str):
    sb = get_client()
    return sb.auth.sign_in_with_password({"email": email, "password": password})


def get_user_from_token(access_token: str):
    """Validate a JWT and return the Supabase user, or None if invalid."""
    try:
        sb = get_client()
        response = sb.auth.get_user(access_token)
        return response.user
    except Exception:
        return None


def sign_in_with_google(redirect_to: str):
    """Return the Google OAuth URL to redirect the browser to."""
    sb = get_client()
    response = sb.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": redirect_to},
    })
    return response.url


# ── Profile helpers (use admin client for server-side access) ────────────────

def get_profile(user_id: str) -> dict | None:
    sb = get_admin_client()
    result = sb.table("profiles").select("*").eq("id", user_id).single().execute()
    return result.data


def create_or_update_profile(user_id: str, email: str, username: str,
                              is_admin: bool = False, is_approved: bool = False):
    sb = get_admin_client()
    sb.table("profiles").upsert({
        "id": user_id,
        "email": email,
        "username": username,
        "is_admin": is_admin,
        "is_approved": is_approved,
    }).execute()


def approve_user(user_id: str):
    sb = get_admin_client()
    sb.table("profiles").update({"is_approved": True}).eq("id", user_id).execute()


def set_admin(user_id: str, value: bool = True):
    sb = get_admin_client()
    sb.table("profiles").update({"is_admin": value}).eq("id", user_id).execute()


def get_all_profiles() -> list:
    sb = get_admin_client()
    result = sb.table("profiles").select("*").order("created_at", desc=True).execute()
    return result.data or []


# ── Module permission helpers ────────────────────────────────────────────────

def get_user_permissions(user_id: str) -> set:
    """Return a set of enabled module_ids for a user."""
    sb = get_admin_client()
    result = (
        sb.table("module_permissions")
        .select("module_id")
        .eq("user_id", user_id)
        .eq("enabled", True)
        .execute()
    )
    return {row["module_id"] for row in (result.data or [])}


def get_all_permissions_for_user(user_id: str) -> list:
    sb = get_admin_client()
    result = (
        sb.table("module_permissions")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return result.data or []


def set_module_permission(user_id: str, module_id: str, enabled: bool,
                          granted_by: str | None = None):
    sb = get_admin_client()
    sb.table("module_permissions").upsert({
        "user_id": user_id,
        "module_id": module_id,
        "enabled": enabled,
        "granted_by": granted_by,
    }).execute()


def bulk_set_level_permissions(user_id: str, module_ids: list[str],
                               enabled: bool, granted_by: str | None = None):
    sb = get_admin_client()
    rows = [
        {"user_id": user_id, "module_id": mid,
         "enabled": enabled, "granted_by": granted_by}
        for mid in module_ids
    ]
    sb.table("module_permissions").upsert(rows).execute()


# ── Submission helpers ────────────────────────────────────────────────────────

def create_submission(user_id: str, module_id: str,
                      file_path: str, original_filename: str):
    sb = get_admin_client()
    result = sb.table("submissions").insert({
        "user_id": user_id,
        "module_id": module_id,
        "file_path": file_path,
        "original_filename": original_filename,
    }).execute()
    return result.data


def get_user_submissions(user_id: str) -> list:
    sb = get_admin_client()
    result = (
        sb.table("submissions")
        .select("*")
        .eq("user_id", user_id)
        .order("uploaded_at", desc=True)
        .execute()
    )
    return result.data or []


def get_all_submissions() -> list:
    sb = get_admin_client()
    result = (
        sb.table("submissions")
        .select("*, profiles(email, username)")
        .order("uploaded_at", desc=True)
        .execute()
    )
    return result.data or []


def update_submission_review(submission_id: str, grade: str,
                              feedback: str, reviewed_by: str):
    sb = get_admin_client()
    import datetime
    sb.table("submissions").update({
        "grade": grade,
        "feedback": feedback,
        "reviewed": True,
        "reviewed_by": reviewed_by,
        "reviewed_at": datetime.datetime.utcnow().isoformat(),
    }).eq("id", submission_id).execute()


# ── Storage helpers ───────────────────────────────────────────────────────────

STORAGE_BUCKET = "course-submissions"


def upload_submission_file(user_id: str, module_id: str,
                           filename: str, file_bytes: bytes) -> str:
    """Upload file to Supabase Storage. Returns the storage path."""
    import datetime
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = filename.replace(" ", "_")
    path = f"{user_id}/{module_id}/{ts}_{safe_name}"
    sb = get_admin_client()
    sb.storage.from_(STORAGE_BUCKET).upload(
        path,
        file_bytes,
        {"content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
    )
    return path


def get_submission_download_url(file_path: str) -> str:
    sb = get_admin_client()
    result = sb.storage.from_(STORAGE_BUCKET).create_signed_url(file_path, 3600)
    return result.get("signedURL", "")
