from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from sync.state import playback_state
from video.logging import log_video_selection
from video.validator import normalize_bilibili_url

from app.auth import is_authenticated, login_with_password, require_auth

bp = Blueprint("app", __name__)


@bp.route("/", methods=["GET"])
@require_auth
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        payload = request.get_json() or request.form
        password = payload.get("password") if payload else None
        if password and login_with_password(password):
            return jsonify({"ok": True}) if request.is_json else redirect(url_for("app.index"))
        return (jsonify({"ok": False, "error": "Invalid password"}), 401)
    if is_authenticated():
        return redirect(url_for("app.index"))
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    session.clear()
    return jsonify({"ok": True})


@bp.route("/video", methods=["POST"])
@require_auth
def set_video():
    payload = request.get_json() or {}
    url = payload.get("url")
    valid, embed_url, error = normalize_bilibili_url(url)
    if not valid or not embed_url:
        return jsonify({"ok": False, "error": error}), 400
    playback_state.set_video(embed_url)
    log_video_selection(request.remote_addr or "unknown", embed_url)
    return jsonify({"ok": True, "embed_url": embed_url})
