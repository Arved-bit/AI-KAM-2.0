# AI Key Account Copilot

A premium, executive-first Streamlit prototype that helps Key Account Managers prepare an opportunity-led customer meeting briefing.

Sprint 1 intentionally uses curated placeholder data. Authentication, CRM, databases, and external research integrations are outside the MVP scope.

## Run locally

Prerequisite: Python 3.12.

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

This repository is ready to deploy without code changes.

1. Push this project to a GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app** and choose the repository and branch.
3. Set **Main file path** to `app.py`.
4. Open **Advanced settings** and select **Python 3.12**.
5. Select **Deploy**.

Community Cloud selects Python versions in its deployment UI, not from repository files. `runtime.txt` is therefore intentionally omitted. For an existing deployment, delete and redeploy the app after selecting Python 3.12: Community Cloud does not allow a deployed app's Python version to be changed in place.

`requirements.txt` pins Streamlit 1.61.1 and Pillow 12.3.0, both compatible with Python 3.12. It also enforces wheel-only installs, so Community Cloud will not build Pillow from source.

## Project structure

```text
app.py                     # Streamlit entry point and screen routing
components/                # Reusable landing, loading, briefing, and styling UI
services/                  # Data and business-logic layer
.streamlit/config.toml     # Streamlit Cloud-compatible application configuration
requirements.txt           # Python dependencies
```
