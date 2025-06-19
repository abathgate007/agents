# DesignReview Agent PoC
# ## Different models review a set of requirements and architecture in a mermaid file and then do all the steps of security review. Then we use LLM to  rank them and then merge them into a more complete and accurate threat model
# 

# %%
# Start with imports 

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display

# %%
# Always remember to do this!
load_dotenv(override=True)

# %%
# Print the key prefixes to help with any debugging

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set (and this is optional)")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")

# %%

#This is the prompt which asks the LLM to do a security design review and provides a set of requirements and an architectural diagram in mermaid format
designreviewrequest = """For the following requirements and architectural diagram, please perform a full security design review which includes the following 7 steps
1. Define scope and system boundaries.
2. Create detailed data flow diagrams.
3. Apply threat frameworks (like STRIDE) to identify threats.
4. Rate and prioritize identified threats.
5. Document-specific security controls and mitigations.
6. Rank the threats based on their severity and likelihood of occurrence.
7. Provide a summary of the security review and recommendations.

Here are the requirements and mermaid architectural diagram:
Software Requirements Specification (SRS) - Juice Shop: Secure E-Commerce Platform
This document outlines the functional and non-functional requirements for the Juice Shop, a secure online retail platform.

1. Introduction

1.1 Purpose: To define the requirements for a robust and secure e-commerce platform that allows customers to purchase products online safely and efficiently.
1.2 Scope: The system will be a web-based application providing a full range of e-commerce functionalities, from user registration and product browsing to secure payment processing and order management.
1.3 Intended Audience: This document is intended for project managers, developers, quality assurance engineers, and stakeholders involved in the development and maintenance of the Juice Shop platform.
2. Overall Description

2.1 Product Perspective: A customer-facing, scalable, and secure e-commerce website with a comprehensive administrative backend.
2.2 Product Features:
Secure user registration and authentication with multi-factor authentication (MFA).
A product catalog with detailed descriptions, images, pricing, and stock levels.
Advanced search and filtering capabilities for products.
A secure shopping cart and checkout process integrating with a trusted payment gateway.
User profile management, including order history, shipping addresses, and payment information.
An administrative dashboard for managing products, inventory, orders, and customer data.
2.3 User Classes and Characteristics:
Customer: A registered or guest user who can browse products, make purchases, and manage their account.
Administrator: An authorized employee who can manage the platform's content and operations.
Customer Service Representative: An authorized employee who can assist customers with orders and account issues.
3. System Features

3.1 Functional Requirements:
User Management:
Users shall be able to register for a new account with a unique email address and a strong password.
The system shall enforce strong password policies (e.g., length, complexity, and expiration).
Users shall be able to log in securely and enable/disable MFA.
Users shall be able to reset their password through a secure, token-based process.
Product Management:
The system shall display products with accurate information, including price, description, and availability.
Administrators shall be able to add, update, and remove products from the catalog.
Order Processing:
The system shall process orders through a secure, PCI-compliant payment gateway.
The system shall encrypt all sensitive customer and payment data.
Customers shall receive email confirmations for orders and shipping updates.
3.2 Non-Functional Requirements:
Security:
All data transmission shall be encrypted using TLS 1.2 or higher.
The system shall be protected against common web vulnerabilities, including the OWASP Top 10 (e.g., SQL Injection, XSS, CSRF).
Regular security audits and penetration testing shall be conducted.
Performance:
The website shall load in under 3 seconds on a standard broadband connection.
The system shall handle at least 1,000 concurrent users without significant performance degradation.
Reliability: The system shall have an uptime of 99.9% or higher.
Usability: The user interface shall be intuitive and easy to navigate for all user types.

and here is the mermaid architectural diagram:

graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile App]
    end
    
    subgraph "Frontend Layer"
        Angular[Angular SPA Frontend]
        Static[Static Assets<br/>CSS, JS, Images]
    end
    
    subgraph "Application Layer"
        Express[Express.js Server]
        Routes[REST API Routes]
        Auth[Authentication Module]
        Middleware[Security Middleware]
        Challenges[Challenge Engine]
    end
    
    subgraph "Business Logic"
        UserMgmt[User Management]
        ProductCatalog[Product Catalog]
        OrderSystem[Order System]
        Feedback[Feedback System]
        FileUpload[File Upload Handler]
        Payment[Payment Processing]
    end
    
    subgraph "Data Layer"
        SQLite[(SQLite Database)]
        FileSystem[File System<br/>Uploaded Files]
        Memory[In-Memory Storage<br/>Sessions, Cache]
    end
    
    subgraph "Security Features (Intentionally Vulnerable)"
        XSS[DOM Manipulation]
        SQLi[Database Queries]
        AuthBypass[Login System]
        CSRF[State Changes]
        Crypto[Password Hashing]
        IDOR[Resource Access]
    end
    
    subgraph "External Dependencies"
        NPM[NPM Packages]
        JWT[JWT Libraries]
        Crypto[Crypto Libraries]
        Sequelize[Sequelize ORM]
    end
    
    %% Client connections
    Browser --> Angular
    Mobile --> Routes
    
    %% Frontend connections
    Angular --> Static
    Angular --> Routes
    
    %% Application layer connections
    Express --> Routes
    Routes --> Auth
    Routes --> Middleware
    Routes --> Challenges
    
    %% Business logic connections
    Routes --> UserMgmt
    Routes --> ProductCatalog
    Routes --> OrderSystem
    Routes --> Feedback
    Routes --> FileUpload
    Routes --> Payment
    
    %% Data layer connections
    UserMgmt --> SQLite
    ProductCatalog --> SQLite
    OrderSystem --> SQLite
    Feedback --> SQLite
    FileUpload --> FileSystem
    Auth --> Memory
    
    %% Security vulnerabilities (dotted lines indicate vulnerable paths)
    Angular -.-> XSS
    Routes -.-> SQLi
    Auth -.-> AuthBypass
    Angular -.-> CSRF
    UserMgmt -.-> Crypto
    Routes -.-> IDOR
    
    %% External dependencies
    Express --> NPM
    Auth --> JWT
    UserMgmt --> Crypto
    SQLite --> Sequelize
    
    %% Styling
    classDef clientLayer fill:#e1f5fe
    classDef frontendLayer fill:#f3e5f5
    classDef appLayer fill:#e8f5e8
    classDef businessLayer fill:#fff3e0
    classDef dataLayer fill:#fce4ec
    classDef securityLayer fill:#ffebee
    classDef externalLayer fill:#f1f8e9
    
    class Browser,Mobile clientLayer
    class Angular,Static frontendLayer
    class Express,Routes,Auth,Middleware,Challenges appLayer
    class UserMgmt,ProductCatalog,OrderSystem,Feedback,FileUpload,Payment businessLayer
    class SQLite,FileSystem,Memory dataLayer
    class XSS,SQLi,AuthBypass,CSRF,Crypto,IDOR securityLayer
    class NPM,JWT,Crypto,Sequelize externalLayer"""



openai = OpenAI()
competitors = []
answers = []

# We make the first call to the first model
model_name = "gpt-4o-mini"

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

# Anthropic has a slightly different API, and Max Tokens is required

model_name = "claude-3-7-sonnet-latest"

claude = Anthropic()
response = claude.messages.create(model=model_name, messages=messages, max_tokens=1000)
answer = response.content[0].text

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.0-flash"

response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
model_name = "deepseek-chat"

response = deepseek.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
model_name = "llama-3.3-70b-versatile"

response = groq.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)


!ollama pull llama3.2

ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
model_name = "llama3.2"

response = ollama.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)


# It's nice to know how to use "zip"
for competitor, answer in zip(competitors, answers):
    print(f"Competitor: {competitor}\n\n{answer}")


# Let's bring this together - note the use of "enumerate"

together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"


#Now we are going to ask the model to rank the design reviews
judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{designreviewrequest}

Your job is to evaluate each response for completeness and accuracy, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""

judge_messages = [{"role": "user", "content": judge}]

# Judgement time!

openai = OpenAI()
response = openai.chat.completions.create(
    model="o3-mini",
    messages=judge_messages,
)
results = response.choices[0].message.content
print(results)


# OK let's turn this into results!

results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")

#Now we have all the design reviews, let's see if LLMs can merge them into a single design review that is more complete and accurate than the individual reviews.
mergePrompt = f"""Here are design reviews from {len(competitors)} LLms. Here are the responses from each one:

{together} Your task is to synthesize these reviews into a single, comprehensive design review and threat model that:

1. **Includes all identified threats**, consolidating any duplicates with unified wording.
2. **Preserves the strongest insights** from each review, especially nuanced or unique observations.
3. **Highlights conflicting or divergent findings**, if any, and explains which interpretation seems more likely and why.
4. **Organizes the final output** in a clear format, with these sections:
   - Scope and System Boundaries
   - Data Flow Overview
   - Identified Threats (categorized using STRIDE or equivalent)
   - Risk Ratings and Prioritization
   - Suggested Mitigations
   - Final Comments and Open Questions

Be concise but thorough. Treat this as a final report for a real-world security audit.
"""


openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": mergePrompt}],
)
results = response.choices[0].message.content
print(results)

