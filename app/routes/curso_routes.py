# app/routes/curso_routes.py
import os
import re
import functools
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, abort, send_from_directory, current_app,
)
from werkzeug.utils import secure_filename

curso_bp = Blueprint("curso", __name__, url_prefix="/curso")

# ── Course module registry ────────────────────────────────────────────────────

LEVELS = {
    "nivel0": {
        "level_num": 0,
        "title": "Nivel 0 — Fundamentos",
        "short": "Fundamentos",
        "color": "#7B1D32",
        "accent": "#F9EAED",
        "modules": [
            {"id": "nivel0_modulo01_interfaz",   "title": "La interfaz de Excel 365"},
            {"id": "nivel0_modulo02_shortcuts",   "title": "Atajos esenciales"},
            {"id": "nivel0_modulo03_estructura",  "title": "Estructura de datos"},
            {"id": "nivel0_modulo04_formato",     "title": "Formato y presentación"},
            {"id": "nivel0_modulo05_nombrado",    "title": "Nombrado y organización"},
            {"id": "nivel0_modulo06_mentalidad",  "title": "Mentalidad Excel"},
        ],
        "xlsx": ["nivel0_ejemplos.xlsx", "nivel0_practica.xlsx"],
    },
    "nivel1": {
        "level_num": 1,
        "title": "Nivel 1 — Básico",
        "short": "Básico",
        "color": "#1565C0",
        "accent": "#E3F2FD",
        "modules": [
            {"id": "nivel1_modulo01_tipos_datos", "title": "Tipos de datos"},
            {"id": "nivel1_modulo02_formulas",    "title": "Fórmulas y operadores"},
            {"id": "nivel1_modulo03_references",  "title": "Referencias"},
            {"id": "nivel1_modulo04_funciones",   "title": "Funciones esenciales"},
            {"id": "nivel1_modulo05_conditional", "title": "Formato condicional"},
            {"id": "nivel1_modulo06_sort_filter", "title": "Ordenar y filtrar"},
            {"id": "nivel1_modulo07_charts",      "title": "Gráficos básicos"},
        ],
        "xlsx": ["nivel1_ejemplos.xlsx", "nivel1_practica.xlsx"],
    },
    "nivel2": {
        "level_num": 2,
        "title": "Nivel 2 — Intermedio",
        "short": "Intermedio",
        "color": "#2E7D32",
        "accent": "#E8F5E9",
        "modules": [
            {"id": "nivel2_modulo01_absolute_refs",  "title": "Referencias absolutas y mixtas"},
            {"id": "nivel2_modulo02_condicionales",  "title": "Funciones condicionales"},
            {"id": "nivel2_modulo03_sumifs",         "title": "SUMIFS y agregación"},
            {"id": "nivel2_modulo04_texto",          "title": "Funciones de texto"},
            {"id": "nivel2_modulo05_fechas",         "title": "Funciones de fecha"},
            {"id": "nivel2_modulo06_validation",     "title": "Validación de datos"},
            {"id": "nivel2_modulo07_named_ranges",   "title": "Rangos nombrados"},
            {"id": "nivel2_modulo08_pivottables",    "title": "Tablas dinámicas"},
            {"id": "nivel2_modulo09_charts_adv",     "title": "Gráficos avanzados"},
        ],
        "xlsx": ["nivel2_ejemplos.xlsx", "nivel2_practica.xlsx"],
    },
    "nivel3": {
        "level_num": 3,
        "title": "Nivel 3 — Avanzado",
        "short": "Avanzado",
        "color": "#E65100",
        "accent": "#FFF3E0",
        "modules": [
            {"id": "nivel3_modulo01_xlookup",        "title": "XLOOKUP"},
            {"id": "nivel3_modulo02_index_match",    "title": "INDEX / MATCH"},
            {"id": "nivel3_modulo03_dynamic_arrays", "title": "Arrays dinámicos"},
            {"id": "nivel3_modulo04_pivot_adv",      "title": "Tablas dinámicas avanzadas"},
            {"id": "nivel3_modulo05_power_query",    "title": "Power Query"},
            {"id": "nivel3_modulo06_dashboards",     "title": "Dashboards"},
            {"id": "nivel3_modulo07_proteccion",     "title": "Protección y seguridad"},
            {"id": "nivel3_modulo08_colaboracion",   "title": "Colaboración en Excel"},
        ],
        "xlsx": ["nivel3_ejemplos.xlsx", "nivel3_practica.xlsx"],
    },
    "nivel4": {
        "level_num": 4,
        "title": "Nivel 4 — Excel Pro",
        "short": "Excel Pro",
        "color": "#4A148C",
        "accent": "#F3E5F5",
        "modules": [
            {"id": "nivel4_modulo01_macros",          "title": "Macros"},
            {"id": "nivel4_modulo02_vba",             "title": "VBA básico"},
            {"id": "nivel4_modulo03_power_pivot",     "title": "Power Pivot"},
            {"id": "nivel4_modulo04_fuentes_externas","title": "Fuentes de datos externas"},
            {"id": "nivel4_modulo05_pq_avanzado",     "title": "Power Query avanzado"},
            {"id": "nivel4_modulo06_certificacion",   "title": "Certificación"},
        ],
        "xlsx": ["nivel4_ejemplos.xlsx", "nivel4_practica.xlsx"],
    },
}

ALL_MODULE_IDS = {
    m["id"]
    for lv in LEVELS.values()
    for m in lv["modules"]
}

MODULE_LOOKUP = {
    m["id"]: {**m, "level_key": lk, **{k: v for k, v in lv.items() if k != "modules"}}
    for lk, lv in LEVELS.items()
    for m in lv["modules"]
}


# ── Auth decorators ───────────────────────────────────────────────────────────

def require_login(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("curso_user_id"):
            flash("Inicia sesión para continuar.", "warning")
            return redirect(url_for("curso.login"))
        return f(*args, **kwargs)
    return decorated


def require_approved(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("curso_user_id"):
            return redirect(url_for("curso.login"))
        if not session.get("curso_is_admin") and not session.get("curso_is_approved"):
            return redirect(url_for("curso.pending"))
        return f(*args, **kwargs)
    return decorated


def require_admin(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("curso_is_admin"):
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ── Session helpers ───────────────────────────────────────────────────────────

def _save_session(user_id, email, username, is_admin, is_approved, access_token):
    session["curso_user_id"]     = user_id
    session["curso_email"]       = email
    session["curso_username"]    = username
    session["curso_is_admin"]    = is_admin
    session["curso_is_approved"] = is_approved
    session["curso_access_token"]= access_token


def _clear_session():
    for key in list(session.keys()):
        if key.startswith("curso_"):
            session.pop(key)


def _after_auth(user, access_token):
    """Called after any successful auth (email or OAuth). Sets up session."""
    from app.python.supabase_client import get_profile, create_or_update_profile
    user_id = user.id
    email   = user.email
    username = (user.user_metadata or {}).get("username") or \
               (user.user_metadata or {}).get("full_name") or \
               email.split("@")[0]

    profile = get_profile(user_id)

    admin_email = current_app.config.get("ADMIN_EMAIL", "")
    is_admin    = email == admin_email or (profile and profile.get("is_admin", False))
    is_approved = is_admin or (profile and profile.get("is_approved", False))

    if not profile:
        create_or_update_profile(user_id, email, username, is_admin, is_approved)
    elif is_admin and not profile.get("is_admin"):
        from app.python.supabase_client import set_admin, approve_user
        set_admin(user_id, True)
        approve_user(user_id)

    _save_session(user_id, email, username, is_admin, is_approved, access_token)
    return is_approved or is_admin


# ── JSX transformer ───────────────────────────────────────────────────────────

def _transform_jsx(raw: str) -> str:
    """
    Prepare a JSX module file for in-browser rendering via Babel standalone.
    - Strips ES module imports (React hooks come from the global React object)
    - Removes 'export default'
    - Appends the ReactDOM render call
    """
    lines = raw.splitlines()
    out   = []
    react_identifiers = set()

    for line in lines:
        stripped = line.strip()
        # Collect React named imports → expose from global React
        if re.match(r"^import\s*\{", stripped) and ('"react"' in stripped or "'react'" in stripped):
            match = re.search(r"\{([^}]+)\}", stripped)
            if match:
                identifiers = [i.strip() for i in match.group(1).split(",")]
                react_identifiers.update(identifiers)
            continue  # skip the import line
        # Skip other import lines
        if re.match(r"^import\b", stripped):
            continue
        # Remove 'export default'
        line = re.sub(r"^export\s+default\s+", "", line)
        out.append(line)

    result = "\n".join(out)

    # Prepend destructured React globals
    if react_identifiers:
        ids = ", ".join(sorted(react_identifiers))
        result = f"const {{ {ids} }} = React;\n\n" + result

    # Append render
    result += "\n\nReactDOM.createRoot(document.getElementById('react-root')).render(<Module />);\n"
    return result


# ── Public routes ─────────────────────────────────────────────────────────────

@curso_bp.route("/")
def landing():
    if session.get("curso_user_id"):
        return redirect(url_for("curso.dashboard"))
    return render_template("curso/landing.html", levels=LEVELS)


@curso_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("curso_user_id"):
        return redirect(url_for("curso.dashboard"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        try:
            from app.python.supabase_client import sign_in
            resp = sign_in(email, password)
            approved = _after_auth(resp.user, resp.session.access_token)
            if approved:
                return redirect(url_for("curso.dashboard"))
            return redirect(url_for("curso.pending"))
        except Exception as e:
            flash("Credenciales incorrectas. Intenta de nuevo.", "error")

    return render_template("curso/login.html")


@curso_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("curso_user_id"):
        return redirect(url_for("curso.dashboard"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        username = request.form.get("username", "").strip()
        confirm  = request.form.get("confirm", "")

        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("curso/register.html")
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return render_template("curso/register.html")
        try:
            from app.python.supabase_client import sign_up, sign_in
            sign_up(email, password, username)
            # Sign in immediately to get a session
            resp     = sign_in(email, password)
            approved = _after_auth(resp.user, resp.session.access_token)
            if approved:
                return redirect(url_for("curso.dashboard"))
            flash("Cuenta creada. Espera a que el administrador la active.", "success")
            return redirect(url_for("curso.pending"))
        except Exception as e:
            msg = str(e)
            if "already registered" in msg or "already exists" in msg:
                flash("Este correo ya está registrado.", "error")
            else:
                flash(f"Error al crear la cuenta: {msg}", "error")

    return render_template("curso/register.html")


@curso_bp.route("/auth/google")
def auth_google():
    from app.python.supabase_client import sign_in_with_google
    callback = url_for("curso.auth_callback", _external=True)
    google_url = sign_in_with_google(callback)
    return redirect(google_url)


@curso_bp.route("/auth/callback")
def auth_callback():
    """
    Handles both PKCE code exchange and a fallback POST from the JS client.
    Supabase redirects here after Google OAuth.
    """
    code = request.args.get("code")
    if code:
        try:
            from app.python.supabase_client import get_client
            sb   = get_client()
            resp = sb.auth.exchange_code_for_session({"auth_code": code})
            approved = _after_auth(resp.user, resp.session.access_token)
            if approved:
                return redirect(url_for("curso.dashboard"))
            return redirect(url_for("curso.pending"))
        except Exception as e:
            flash(f"Error de autenticación: {e}", "error")
            return redirect(url_for("curso.login"))

    # Implicit flow — token arrives in URL hash, handled by JS
    return render_template("curso/auth_callback.html")


@curso_bp.route("/auth/session", methods=["POST"])
def auth_session():
    """Receives access_token from the browser JS client (implicit OAuth flow)."""
    data         = request.get_json(silent=True) or {}
    access_token = data.get("access_token", "")
    if not access_token:
        return {"ok": False, "error": "no token"}, 400
    from app.python.supabase_client import get_user_from_token
    user = get_user_from_token(access_token)
    if not user:
        return {"ok": False, "error": "invalid token"}, 401
    approved = _after_auth(user, access_token)
    return {"ok": True, "approved": approved}


@curso_bp.route("/logout")
def logout():
    _clear_session()
    return redirect(url_for("curso.landing"))


@curso_bp.route("/pending")
@require_login
def pending():
    if session.get("curso_is_approved") or session.get("curso_is_admin"):
        return redirect(url_for("curso.dashboard"))
    return render_template("curso/pending.html")


# ── Student routes ────────────────────────────────────────────────────────────

@curso_bp.route("/dashboard")
@require_approved
def dashboard():
    from app.python.supabase_client import get_user_permissions, get_user_submissions
    user_id    = session["curso_user_id"]
    enabled    = get_user_permissions(user_id) if not session.get("curso_is_admin") else ALL_MODULE_IDS
    submissions = get_user_submissions(user_id)
    submitted_modules = {s["module_id"] for s in submissions}
    return render_template(
        "curso/dashboard.html",
        levels=LEVELS,
        enabled_modules=enabled,
        submitted_modules=submitted_modules,
        is_admin=session.get("curso_is_admin", False),
    )


@curso_bp.route("/modulo/<module_id>")
@require_approved
def modulo(module_id):
    if module_id not in MODULE_LOOKUP:
        abort(404)

    # Check permission
    is_admin = session.get("curso_is_admin", False)
    if not is_admin:
        from app.python.supabase_client import get_user_permissions
        enabled = get_user_permissions(session["curso_user_id"])
        if module_id not in enabled:
            flash("No tienes acceso a este módulo.", "warning")
            return redirect(url_for("curso.dashboard"))

    # Load and transform JSX
    jsx_path = os.path.join(
        current_app.root_path, "static", "curso", "modulos", f"{module_id}.jsx"
    )
    if not os.path.exists(jsx_path):
        abort(404)
    with open(jsx_path, "r", encoding="utf-8") as f:
        raw_jsx = f.read()

    transformed = _transform_jsx(raw_jsx)
    meta        = MODULE_LOOKUP[module_id]
    level_key   = meta["level_key"]
    level_data  = LEVELS[level_key]

    # Previous / next module navigation
    all_in_level = [m["id"] for m in level_data["modules"]]
    idx          = all_in_level.index(module_id)
    prev_mod     = all_in_level[idx - 1] if idx > 0 else None
    next_mod     = all_in_level[idx + 1] if idx < len(all_in_level) - 1 else None

    from app.python.supabase_client import get_user_submissions
    user_subs = get_user_submissions(session["curso_user_id"])
    already_submitted = any(s["module_id"] == module_id for s in user_subs)

    supabase_anon_key = current_app.config.get("SUPABASE_ANON_KEY", "")
    supabase_url      = current_app.config.get("SUPABASE_URL", "")

    return render_template(
        "curso/modulo.html",
        module_id=module_id,
        meta=meta,
        level_data=level_data,
        jsx_content=transformed,
        prev_mod=prev_mod,
        next_mod=next_mod,
        already_submitted=already_submitted,
        enabled_modules=enabled,
        supabase_anon_key=supabase_anon_key,
        supabase_url=supabase_url,
    )


@curso_bp.route("/descargar/<filename>")
@require_approved
def descargar(filename):
    safe = secure_filename(filename)
    directory = os.path.join(current_app.root_path, "static", "curso", "archivos")
    return send_from_directory(directory, safe, as_attachment=True)


@curso_bp.route("/submit/<module_id>", methods=["POST"])
@require_approved
def submit(module_id):
    if module_id not in MODULE_LOOKUP:
        abort(404)

    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Selecciona un archivo.", "error")
        return redirect(url_for("curso.modulo", module_id=module_id))

    filename = secure_filename(file.filename)
    ext      = os.path.splitext(filename)[1].lower()
    if ext not in (".xlsx", ".xls", ".xlsm"):
        flash("Solo se aceptan archivos Excel (.xlsx, .xls, .xlsm).", "error")
        return redirect(url_for("curso.modulo", module_id=module_id))

    MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    file_bytes = file.read()
    if len(file_bytes) > MAX_BYTES:
        flash("El archivo supera el límite de 10 MB.", "error")
        return redirect(url_for("curso.modulo", module_id=module_id))

    try:
        from app.python.supabase_client import upload_submission_file, create_submission
        user_id   = session["curso_user_id"]
        path      = upload_submission_file(user_id, module_id, filename, file_bytes)
        create_submission(user_id, module_id, path, filename)
        flash("¡Entrega enviada correctamente!", "success")
    except Exception as e:
        flash(f"Error al subir el archivo: {e}", "error")

    return redirect(url_for("curso.modulo", module_id=module_id))


# ── Admin routes ──────────────────────────────────────────────────────────────

@curso_bp.route("/admin")
@require_admin
def admin_index():
    from app.python.supabase_client import get_all_profiles, get_all_submissions
    profiles    = get_all_profiles()
    submissions = get_all_submissions()
    pending     = [p for p in profiles if not p["is_approved"] and not p["is_admin"]]
    return render_template(
        "curso/admin/index.html",
        profiles=profiles,
        submissions=submissions,
        pending=pending,
        levels=LEVELS,
    )


@curso_bp.route("/admin/usuarios")
@require_admin
def admin_usuarios():
    from app.python.supabase_client import get_all_profiles
    profiles = get_all_profiles()
    return render_template("curso/admin/usuarios.html", profiles=profiles, levels=LEVELS)


@curso_bp.route("/admin/usuarios/<user_id>/aprobar", methods=["POST"])
@require_admin
def admin_aprobar(user_id):
    from app.python.supabase_client import approve_user
    approve_user(user_id)
    flash("Usuario aprobado.", "success")
    return redirect(url_for("curso.admin_usuarios"))


@curso_bp.route("/admin/usuarios/<user_id>/revocar", methods=["POST"])
@require_admin
def admin_revocar(user_id):
    from app.python.supabase_client import get_admin_client
    get_admin_client().table("profiles").update({"is_approved": False}).eq("id", user_id).execute()
    flash("Acceso revocado.", "success")
    return redirect(url_for("curso.admin_usuarios"))


@curso_bp.route("/admin/usuarios/<user_id>/modulos", methods=["GET", "POST"])
@require_admin
def admin_modulos_usuario(user_id):
    from app.python.supabase_client import (
        get_profile, get_all_permissions_for_user,
        set_module_permission, bulk_set_level_permissions,
    )

    if request.method == "POST":
        action     = request.form.get("action")  # "toggle", "enable_level", "disable_level"
        admin_id   = session["curso_user_id"]

        if action == "toggle":
            mod_id  = request.form.get("module_id")
            enabled = request.form.get("enabled") == "true"
            set_module_permission(user_id, mod_id, enabled, admin_id)

        elif action in ("enable_level", "disable_level"):
            level_key = request.form.get("level_key")
            enabled   = action == "enable_level"
            mids      = [m["id"] for m in LEVELS[level_key]["modules"]]
            bulk_set_level_permissions(user_id, mids, enabled, admin_id)

        flash("Permisos actualizados.", "success")
        return redirect(url_for("curso.admin_modulos_usuario", user_id=user_id))

    profile     = get_profile(user_id)
    perms       = get_all_permissions_for_user(user_id)
    perm_map    = {p["module_id"]: p["enabled"] for p in perms}
    return render_template(
        "curso/admin/modulos_usuario.html",
        profile=profile,
        levels=LEVELS,
        perm_map=perm_map,
        user_id=user_id,
    )


@curso_bp.route("/admin/entregas")
@require_admin
def admin_entregas():
    from app.python.supabase_client import get_all_submissions, get_submission_download_url
    submissions = get_all_submissions()
    return render_template(
        "curso/admin/entregas.html",
        submissions=submissions,
        get_download_url=get_submission_download_url,
        levels=LEVELS,
        module_lookup=MODULE_LOOKUP,
    )


@curso_bp.route("/admin/entregas/<sub_id>/revisar", methods=["POST"])
@require_admin
def admin_revisar_entrega(sub_id):
    from app.python.supabase_client import update_submission_review
    grade    = request.form.get("grade", "").strip()
    feedback = request.form.get("feedback", "").strip()
    update_submission_review(sub_id, grade, feedback, session["curso_user_id"])
    flash("Revisión guardada.", "success")
    return redirect(url_for("curso.admin_entregas"))
