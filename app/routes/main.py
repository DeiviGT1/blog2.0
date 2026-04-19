# app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/ping')
def ping():
    """Keep-alive endpoint — Vercel cron hits this every 5 min to prevent cold starts."""
    return jsonify({"status": "ok"}), 200

@main_bp.route('/')
def index():
    # Supabase OAuth may redirect here with ?code=... instead of /curso/auth/callback
    code = request.args.get("code")
    if code:
        code_verifier = session.pop("curso_pkce_verifier", None)
        if not code_verifier:
            flash("Error de autenticación. Intenta de nuevo.", "error")
            return redirect(url_for("curso.login"))
        try:
            from app.python.supabase_client import get_client
            sb   = get_client()
            resp = sb.auth.exchange_code_for_session({
                "auth_code": code,
                "code_verifier": code_verifier,
            })
            # Import _after_auth from curso routes
            from app.routes.curso_routes import _after_auth
            _after_auth(resp.user, resp.session.access_token)
            return redirect(url_for("curso.dashboard"))
        except Exception as e:
            flash(f"Error de autenticación: {e}", "error")
            return redirect(url_for("curso.login"))
    return render_template('main/index.html')

@main_bp.route('/hf')
def hf():
    return render_template('main/hf.html')