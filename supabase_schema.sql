-- ============================================================
-- Supabase schema for josedavidgt.com — Excel 365 Course
-- Run this in your Supabase project → SQL Editor → New Query
-- ============================================================

-- ── Tables ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS public.profiles (
    id          UUID        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email       TEXT        NOT NULL,
    username    TEXT,
    is_admin    BOOLEAN     NOT NULL DEFAULT FALSE,
    is_approved BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.module_permissions (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    module_id   TEXT        NOT NULL,
    enabled     BOOLEAN     NOT NULL DEFAULT FALSE,
    granted_by  UUID        REFERENCES public.profiles(id),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, module_id)
);

CREATE TABLE IF NOT EXISTS public.submissions (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID        NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    module_id         TEXT        NOT NULL,
    file_path         TEXT        NOT NULL,
    original_filename TEXT        NOT NULL,
    uploaded_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    grade             TEXT,
    feedback          TEXT,
    reviewed          BOOLEAN     NOT NULL DEFAULT FALSE,
    reviewed_by       UUID        REFERENCES public.profiles(id),
    reviewed_at       TIMESTAMPTZ
);

-- ── Row Level Security ───────────────────────────────────────
-- The Flask backend uses the SERVICE ROLE key which bypasses
-- RLS entirely. RLS is here as a safety net.

ALTER TABLE public.profiles           ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.module_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.submissions        ENABLE ROW LEVEL SECURITY;

-- Service role bypasses RLS automatically. No extra policies needed
-- for server-side operations. Add policies below if you ever want
-- direct Supabase client access from the browser.

-- ── Auto-create profile on user signup ───────────────────────
-- This trigger fires whenever a new user is created in auth.users
-- (covers both email/password signup AND Google OAuth).

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (id, email, username)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(
            NEW.raw_user_meta_data->>'username',
            NEW.raw_user_meta_data->>'full_name',
            split_part(NEW.email, '@', 1)
        )
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- ── Supabase Storage bucket ───────────────────────────────────
-- Run this only once. If the bucket already exists, skip it.

INSERT INTO storage.buckets (id, name, public)
VALUES ('course-submissions', 'course-submissions', FALSE)
ON CONFLICT (id) DO NOTHING;

-- Storage policies (server-side uploads via service role bypass these,
-- but they protect direct client access)
CREATE POLICY "Users upload to own folder" ON storage.objects
    FOR INSERT
    WITH CHECK (
        bucket_id = 'course-submissions'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "Users read own files" ON storage.objects
    FOR SELECT
    USING (
        bucket_id = 'course-submissions'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

-- ============================================================
-- After running this script:
-- 1. Go to Authentication → Providers → Google → enable it
--    and add your Google OAuth credentials.
-- 2. In Authentication → URL Configuration, add:
--    http://localhost:5001/curso/auth/callback  (dev)
--    https://josedavidgt.com/curso/auth/callback (prod)
-- 3. Copy your Project URL and anon/service_role keys to .env
-- ============================================================
