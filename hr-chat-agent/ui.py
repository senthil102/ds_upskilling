import base64
from html import escape
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent
CSS_FILE = BASE_DIR / "assets" /  "css" / "style.css"
LOGO_FILE = BASE_DIR / "assets" /  "img" / "logo.svg"

COMPANY_NAME = "HR Assist"                      
COMPANY_TAGLINE = "People. Policies. Answers."  


def inject_css():
    """Read style.css and inject it into the page."""
    css = CSS_FILE.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)



def _logo_data_uri() -> str:
    encoded = base64.b64encode(LOGO_FILE.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _brand(size: int, light: bool) -> str:
    """Gradient icon tile (holding the white company logo) + name/tagline."""
    theme = "brand-light" if light else "brand-dark"
    return (
        f'<div class="brand {theme}">'
        f'<div class="brand-tile" style="width:{size}px;height:{size}px">'
        f'<img src="{_logo_data_uri()}" alt="Logo">'
        '</div>'
        '<div class="brand-text">'
        f'<div class="brand-name">{COMPANY_NAME}</div>'
        f'<div class="brand-tag">{COMPANY_TAGLINE}</div>'
        '</div>'
        '</div>'
    )


def login_brand() -> str:
    """Brand block for the login card (+ marker used by login-page CSS)."""
    return '<span class="login-marker"></span>' + _brand(56, light=False)


def sidebar_logo() -> str:
    """Brand block for the dark sidebar."""
    return _brand(44, light=True)


# Components
def initials(name: str) -> str:
    parts = name.split()
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][0].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def profile_card(name, employee_id, department, role) -> str:
    return (
        '<div class="profile-card">'
        '<div class="profile-row">'
        f'<div class="avatar">{escape(initials(name))}</div>'
        '<div>'
        f'<div class="profile-name">{escape(str(name))}</div>'
        f'<div class="profile-meta">{escape(str(employee_id))} · {escape(str(department))}</div>'
        '</div>'
        '</div>'
        f'<span class="role-badge">{escape(str(role))}</span>'
        '</div>'
    )


def chat_topbar() -> str:
    return (
        '<div class="topbar">'
        '<div>'
        '<div class="topbar-title">HR Chat</div>'
        '<div class="topbar-sub">Ask about HR policies, leave and your employee information</div>'
        '</div>'
        '<div class="status-pill"><span class="status-dot"></span>Online</div>'
        '</div>'
    )


def welcome_hero(first_name: str) -> str:
    return (
        '<div class="welcome">'
        '<div class="welcome-icon">'
        f'<img src="{_logo_data_uri()}" alt="Logo">'
        '</div>'
        f'<div class="welcome-title">Hello, {escape(first_name)}</div>'
        '<div class="welcome-sub">How can I help you today?</div>'
        '<div class="welcome-label">Try asking</div>'
        '</div>'
    )


def page_header(title: str, subtitle: str):
    st.markdown(
        f'<div class="page-header"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def stat_card(label: str, value) -> str:
    return (
        f'<div class="stat-card"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div></div>'
    )