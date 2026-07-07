# Resume Customizer AI

A personal resume customization tool that takes a job description and uses a 3-agent Claude AI pipeline to tailor your resume, then exports it as both PDF and Word files. Access is gated behind Google login, since the app is private to a single user.

## How It Works

1. **Job Analyzer** (Claude Haiku 4.5) - Extracts the job title, required skills, responsibilities, and keywords from the job description.
2. **Resume Writer** (Claude Sonnet 4.6) - Rewrites and tailors the selected resume to match the job analysis.
3. **Quality Checker** (Claude Haiku 4.5) - Scores the customized resume (1-10) and provides feedback; the writer loops up to 2 times until the score is >= 7.

## Project Structure

```text
├── app.py                # Streamlit UI
├── agents/
│   ├── job_analyzer.py   # Agent 1 - extracts job requirements
│   ├── resume_writer.py  # Agent 2 - customizes the resume
│   └── quality_checker.py# Agent 3 - scores and gives feedback
├── document_generator/
│   ├── pdf_generator.py  # Generates PDF using ReportLab
│   └── word_generator.py # Generates Word using python-docx
├── utils/
│   └── cleaner.py        # Strips banned/AI-cliché words
├── mock_agents.py        # Mock agents for layout testing (no API calls)
└── requirements.txt
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/iamginjala/resume-customizer-ai.git
cd resume-customizer-ai
```

### 2. Create and activate virtual environment (uv)

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

### 5. Set up Google login

The app uses Streamlit's built-in [`st.login`](https://docs.streamlit.io/develop/api-reference/user/st.login) authentication, backed by Authlib and Google as the OpenID Connect provider.

1. In the [Google Cloud Console](https://console.cloud.google.com/apis/credentials), create an **OAuth 2.0 Client ID** (Web application type).
2. Add `http://localhost:8501/oauth2callback` under **Authorized redirect URIs** (for local dev).
3. Create `.streamlit/secrets.toml` in the project root (this file is gitignored — never commit it):

   ```toml
   [auth]
   redirect_uri = "http://localhost:8501/oauth2callback"
   cookie_secret = "a-random-long-string"
   client_id = "your-client-id.apps.googleusercontent.com"
   client_secret = "your-client-secret"
   server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
   ```

   Generate `cookie_secret` with something like `python -c "import secrets; print(secrets.token_hex(32))"`.

### 6. Run the app

```bash
streamlit run app.py
```

## Usage

1. Log in with your Google account
2. Select a resume from the dropdown
3. Paste the job description
4. Click **Generate Resume**
5. Download the PDF or Word file



## Tech Stack

- [Streamlit](https://streamlit.io) - UI and hosting
- [Anthropic Claude](https://anthropic.com) - AI agents
- [Authlib](https://authlib.org) - OAuth/OpenID Connect for Google login
- [ReportLab](https://www.reportlab.com) - PDF generation
- [python-docx](https://python-docx.readthedocs.io) - Word generation
- [uv](https://github.com/astral-sh/uv) - Package management

## Deployment

Deployed on [Streamlit Cloud](https://streamlit.io/cloud). In the app's **Secrets** settings, set:

- `ANTHROPIC_API_KEY` (not in a `.env` file)
- The full `[auth]` block from step 5 above, with `redirect_uri` updated to your deployed app's URL (e.g. `https://your-app.streamlit.app/oauth2callback`), and that same redirect URI added as an **Authorized redirect URI** on the Google OAuth client.