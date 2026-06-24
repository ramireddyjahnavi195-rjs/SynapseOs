# ============================================
# SYNAPSEOS - AI SOFTWARE ARCHITECT PLATFORM
# ============================================

import os
import json

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.secret_key = "synapseos_secret_key"
users = {}

@app.route("/")
def home():
    if "user" not in session:
          return redirect(url_for("login"))
    return render_template("index.html")


def create_fallback_blueprint(project_idea, reason_text):
    return {
        "title": f"{project_idea} - Fallback AI Blueprint",

        "problem_statement": reason_text,

        "complexity_analysis": {
            "complexity_level": "Intermediate",
            "estimated_time": "3 to 5 weeks",
            "team_size": "2 to 4 members",
            "risk_level": "Medium",
            "required_skills": [
                "Frontend Development",
                "Backend APIs",
                "Database Design",
                "Authentication",
                "Deployment Basics"
            ],
            "reason": "The project requires multiple modules, backend integration, database management, authentication, and deployment planning."
        },

        "development_estimation": {
            "prototype_timeline": "4 to 6 weeks",
            "mvp_timeline": "3 to 5 months",
            "enterprise_timeline": "12 to 18 months",
            "team_requirement": "4 to 8 developers",
            "budget_estimate": "$10,000 to $100,000",
            "deployment_scale": "Cloud scalable architecture"
        },

        "tech_stack_recommendation": {
            "frontend": "React.js / HTML CSS JavaScript",
            "backend": "Flask / FastAPI",
            "database": "MongoDB / PostgreSQL",
            "ai_ml": "Gemini API / Python ML Models",
            "devops": "Docker, GitHub Actions",
            "cloud": "Render / Railway / AWS",
            "security": "JWT Authentication, Role-Based Access Control",
            "reason": "This stack is suitable for scalable, secure, and AI-powered full-stack applications."
        },
        "development_roadmap": [
  {
    "phase": "",
    "tasks": [],
    "deliverable": ""
  }
],
"devops_recommendation": {
  "docker_strategy": "",
  "ci_cd_pipeline": "",
  "cloud_platform": "",
  "monitoring": "",
  "scalability": "",
  "security": "",
  "production_notes": ""
},
"architecture_diagram": [
  {
    "layer": "",
    "description": ""
  }
],
        "development_roadmap": [
    {
        "phase": "Phase 1: Requirement Analysis",
        "tasks": [
            "Understand project goals",
            "Identify users",
            "Define core modules",
            "Prepare features list"
        ],
        "deliverable": "Requirement specification document"
    },
    {
        "phase": "Phase 2: UI/UX Design",
        "tasks": [
            "Design homepage",
            "Create dashboard UI",
            "Design forms",
            "Make responsive layout"
        ],
        "deliverable": "Frontend UI screens"
    },
    {
        "phase": "Phase 3: Backend Development",
        "tasks": [
            "Build APIs",
            "Connect database",
            "Implement authentication",
            "Add validations"
        ],
        "deliverable": "Working backend system"
    },
    {
        "phase": "Phase 4: AI Integration",
        "tasks": [
            "Integrate Gemini AI",
            "Generate AI responses",
            "Handle AI fallback logic",
            "Optimize prompts"
        ],
        "deliverable": "AI-powered system"
    },
    {
        "phase": "Phase 5: Testing & Deployment",
        "tasks": [
            "Perform testing",
            "Fix bugs",
            "Deploy to cloud",
            "Monitor performance"
        ],
        "deliverable": "Production-ready deployment"
    }
],

        "tech_stack": [
            "Frontend: React.js / HTML CSS JavaScript",
            "Backend: Flask / FastAPI",
            "Database: MongoDB / PostgreSQL",
            "Authentication: JWT Login",
            "Deployment: Docker + Cloud Hosting"
        ],
        "devops_recommendation": {
    "docker_strategy": "Containerize frontend, backend, and database services using Docker.",
    "ci_cd_pipeline": "Use GitHub Actions to automate testing and deployment.",
    "cloud_platform": "Deploy on Render/Railway for prototype and AWS/GCP for production.",
    "monitoring": "Use Prometheus and Grafana for monitoring.",
    "scalability": "Use load balancing, caching, and horizontal scaling.",
    "security": "Use HTTPS, JWT authentication, RBAC, and environment variables.",
    "production_notes": "Maintain separate staging and production environments."
},

        "frontend_modules": [
            "Landing Page",
            "Login and Registration Page",
            "Admin Dashboard",
            "User Dashboard",
            "Reports and Analytics Page"
        ],

        "backend_apis": [
            "POST /register - create new user",
            "POST /login - authenticate user",
            "GET /dashboard - fetch dashboard data",
            "POST /create-record - add new record",
            "GET /reports - fetch reports"
        ],

        "database_tables": [
            "users",
            "roles",
            "records",
            "reports",
            "activity_logs"
        ],

        "architecture": [
            "Frontend sends requests to backend",
            "Backend processes business logic",
            "Database stores users and records",
            "Authentication protects private routes",
            "Cloud deployment supports scalability"
        ],

        "future_upgrades": [
            "AI Chatbot",
            "PDF Reports",
            "Kubernetes Deployment",
            "Role Based Access",
            "Real-time Analytics"
        ]
    }
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        if email in users:
            return "User already exists. Please login."

        users[email] = {
            "username": username,
            "password": generate_password_hash(password)
        }

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users.get(email)

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            return redirect(url_for("home"))

        return "Invalid email or password."

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/copilot")
def copilot():
    return render_template("copilot.html")


@app.route("/agents")
def agents():
    return render_template("agents.html")


@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))

def generate_blueprint_with_gemini(project_idea):
    prompt = f"""
You are SynapseOS, an expert AI software architect.

Create a professional software engineering blueprint for this project idea:
"{project_idea}"

Return ONLY valid JSON.

Use this exact structure:

{{
  "title": "",
  "problem_statement": "",
  "complexity_analysis": {{
    "complexity_level": "",
    "estimated_time": "",
    "team_size": "",
    "risk_level": "",
    "required_skills": [],
    "reason": ""
  }},
  "development_estimation": {{
    "prototype_timeline": "",
    "mvp_timeline": "",
    "enterprise_timeline": "",
    "team_requirement": "",
    "budget_estimate": "",
    "deployment_scale": ""
  }},
  "tech_stack_recommendation": {{
    "frontend": "",
    "backend": "",
    "database": "",
    "ai_ml": "",
    "devops": "",
    "cloud": "",
    "security": "",
    "reason": ""
  }},
  "tech_stack": [],
  "frontend_modules": [],
  "backend_apis": [],
  "database_tables": [],
  "architecture": [],
  "future_upgrades": []
}}

Rules:
- Do not use markdown.
- Do not use code fences.
- Do not write explanation outside JSON.
- Every list must contain at least 5 useful items.
- Make the blueprint specific to the project idea.
- Include realistic REST APIs.
- Include useful database table names.
- Include AI, security, DevOps, and scalability suggestions where useful.
- Include complexity_analysis with realistic complexity level, time estimate, team size, risk level, required skills, and reason.
- Include development_estimation for prototype, MVP, and enterprise versions.
- Include tech_stack_recommendation with frontend, backend, database, AI/ML, DevOps, cloud, security, and reason.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    ai_text = response.text.strip()
    ai_text = ai_text.replace("```json", "").replace("```", "").strip()

    start_index = ai_text.find("{")
    end_index = ai_text.rfind("}") + 1

    if start_index != -1 and end_index != -1:
        ai_text = ai_text[start_index:end_index]

    try:
        blueprint = json.loads(ai_text)

    except Exception as error:
        print("JSON Parsing Error:", error)
        print("Gemini Raw Response:", ai_text)

        blueprint = create_fallback_blueprint(
            project_idea,
            "SynapseOS generated a fallback blueprint because Gemini response formatting failed."
        )

    required_fields = [
        "title",
        "problem_statement",
        "complexity_analysis",
        "development_estimation",
        "tech_stack_recommendation",
        "development_roadmap",
        "devops_recommendation",
        "architecture_diagram",
        "tech_stack",
        "frontend_modules",
        "backend_apis",
        "database_tables",
        "architecture",
        "future_upgrades"
    ]

    for field in required_fields:
        if field not in blueprint:
            if field in ["title", "problem_statement"]:
                blueprint[field] = "Not provided"
            elif field in ["complexity_analysis", "development_estimation", "tech_stack_recommendation"]:
                blueprint[field] = {}
            else:
                blueprint[field] = []

    if not isinstance(blueprint.get("complexity_analysis"), dict):
        blueprint["complexity_analysis"] = {}

    blueprint["complexity_analysis"].setdefault("complexity_level", "Intermediate")
    blueprint["complexity_analysis"].setdefault("estimated_time", "3 to 5 weeks")
    blueprint["complexity_analysis"].setdefault("team_size", "2 to 4 members")
    blueprint["complexity_analysis"].setdefault("risk_level", "Medium")
    blueprint["complexity_analysis"].setdefault("required_skills", [
        "Frontend Development",
        "Backend APIs",
        "Database Design",
        "Authentication",
        "Deployment Basics"
    ])
    blueprint["complexity_analysis"].setdefault(
        "reason",
        "The project requires multiple modules, backend integration, database management, and deployment planning."
    )

    if not isinstance(blueprint.get("development_estimation"), dict):
        blueprint["development_estimation"] = {}

    blueprint["development_estimation"].setdefault("prototype_timeline", "4 to 6 weeks")
    blueprint["development_estimation"].setdefault("mvp_timeline", "3 to 5 months")
    blueprint["development_estimation"].setdefault("enterprise_timeline", "12 to 18 months")
    blueprint["development_estimation"].setdefault("team_requirement", "4 to 8 developers")
    blueprint["development_estimation"].setdefault("budget_estimate", "$10,000 to $100,000")
    blueprint["development_estimation"].setdefault("deployment_scale", "Cloud scalable architecture")

    if not isinstance(blueprint.get("tech_stack_recommendation"), dict):
        blueprint["tech_stack_recommendation"] = {}

    blueprint["tech_stack_recommendation"].setdefault("frontend", "React.js / HTML CSS JavaScript")
    blueprint["tech_stack_recommendation"].setdefault("backend", "Flask / FastAPI")
    blueprint["tech_stack_recommendation"].setdefault("database", "MongoDB / PostgreSQL")
    blueprint["tech_stack_recommendation"].setdefault("ai_ml", "Gemini API / Python ML Models")
    blueprint["tech_stack_recommendation"].setdefault("devops", "Docker, GitHub Actions")
    blueprint["tech_stack_recommendation"].setdefault("cloud", "Render / Railway / AWS")
    blueprint["tech_stack_recommendation"].setdefault("security", "JWT Authentication, Role-Based Access Control")
    blueprint["tech_stack_recommendation"].setdefault(
        "reason",
        "This stack is suitable for building scalable, secure, and AI-powered full-stack applications."
    )
    if not isinstance(blueprint.get("development_roadmap"), list):
      blueprint["development_roadmap"] = [
        {
            "phase": "Phase 1: Requirement Analysis",
            "tasks": [
                "Understand project goals",
                "Identify users",
                "Define modules",
                "Prepare project plan"
            ],
            "deliverable": "Requirement document"
        }
    ]
    if not isinstance(blueprint.get("devops_recommendation"), dict):
       blueprint["devops_recommendation"] = {}

    blueprint["devops_recommendation"].setdefault(
        "docker_strategy",
        "Containerize frontend, backend, and database services using Docker."
    )

    blueprint["devops_recommendation"].setdefault(
        "ci_cd_pipeline",
        "Use GitHub Actions to automate testing and deployment."
    )

    blueprint["devops_recommendation"].setdefault(
        "cloud_platform",
        "Deploy on Render/Railway for prototype and AWS/GCP for production."
    )

    blueprint["devops_recommendation"].setdefault(
       "monitoring",
       "Use Prometheus and Grafana for monitoring."
   )

    blueprint["devops_recommendation"].setdefault(
        "scalability",
        "Use load balancing, caching, and horizontal scaling."
   )

    blueprint["devops_recommendation"].setdefault(
       "security",
       "Use HTTPS, JWT authentication, RBAC, and environment variables."
    )

    blueprint["devops_recommendation"].setdefault(
       "production_notes",
       "Maintain separate staging and production environments."
   )
    if not isinstance(blueprint.get("architecture_diagram"), list):
       blueprint["architecture_diagram"] = [
        {
            "layer": "Frontend Layer",
            "description": "User interface built with responsive web technologies."
        },
        {
            "layer": "Backend API Layer",
            "description": "Handles business logic, authentication, and API requests."
        },
        {
            "layer": "Database Layer",
            "description": "Stores users, records, reports, and activity logs."
        },
        {
            "layer": "AI Intelligence Layer",
            "description": "Processes intelligent recommendations and AI-generated insights."
        },
        {
            "layer": "Cloud Deployment Layer",
            "description": "Hosts application services using scalable cloud infrastructure."
        },
        {
            "layer": "Security Layer",
            "description": "Protects the system using JWT, HTTPS, RBAC, and environment variables."
        }
    ]
    list_fields = [
        "tech_stack",
        "frontend_modules",
        "backend_apis",
        "database_tables",
        "architecture",
        "development_roadmap",
        "devops_recommendation",
        "architecture_diagram",
        "future_upgrades"
    ]

    for field in list_fields:
        if not isinstance(blueprint[field], list):
            blueprint[field] = [str(blueprint[field])]

    return blueprint


@app.route("/generate-blueprint", methods=["POST"])
def generate_blueprint():
    data = request.get_json()
    project_idea = data.get("projectIdea", "")

    if not project_idea.strip():
        return jsonify({
            "success": False,
            "message": "Please enter a project idea."
        })

    try:
        blueprint = generate_blueprint_with_gemini(project_idea)

        return jsonify({
            "success": True,
            "blueprint": blueprint
        })

    except Exception as error:
        print("Gemini Backend Error:", error)

        fallback_blueprint = create_fallback_blueprint(
            project_idea,
            "SynapseOS generated this fallback blueprint because Gemini AI is temporarily unavailable or quota is exceeded."
        )

        return jsonify({
            "success": True,
            "blueprint": fallback_blueprint
        })
@app.route("/ask-assistant", methods=["POST"])
def ask_assistant():

    data = request.get_json()

    user_question = data.get("question", "")
    project_context = data.get("projectContext", "")

    if not user_question.strip():
        return jsonify({
            "success": False,
            "message": "Please enter a question for SynapseOS Assistant."
        })

    try:

        prompt = f"""
You are SynapseOS AI Copilot, an intelligent software engineering assistant.

Project Context:
{project_context}

Actual User Question:
{user_question}

Instructions:
- Give concise and accurate answers.
- Keep response under 200 words.
- Be practical and project-specific.
- Use modern industry practices.
- Avoid unnecessary long explanations.
- Focus on software engineering, AI systems, APIs, databases, deployment, scalability, and DevOps.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return jsonify({
            "success": True,
            "answer": response.text
        })

    except Exception as error:

        print("Assistant Error:", error)

        return jsonify({
            "success": True,
            "answer": "Gemini is temporarily unavailable. Please try again later."
        })

if __name__ == "__main__":
    app.run(debug=True)