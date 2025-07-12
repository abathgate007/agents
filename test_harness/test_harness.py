# test_harness.py
# Author: Andrew Bathgate | Date: 2025-07-05

import asyncio
from config import load_config
from design import Design
from llm_model import LLMModel
from security_design_reviewer import SecurityDesignReviewer


async def main():
    # Step 1: Load API keys from .env
    config = load_config()

    # Step 2: Create a rudimentary design input
    requirements = """
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

"""

    mermaid_architecture = """
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
    class NPM,JWT,Crypto,Sequelize externalLayer"""

    design = Design()
    design.add_text(requirements)
    design.add_mermaid(mermaid_architecture)

    # Step 3: Instantiate LLM models (OpenAI only for now)
    models = [
        LLMModel(model_name="gpt-4o", api_key=config.openai_api_key, model_type="openai"),
        LLMModel(model_name="deepseek-chat", api_key=config.deepseek_api_key, base_url="https://api.deepseek.com/v1", model_type="openai"),
        LLMModel(model_name="claude-3-7-sonnet-latest", api_key=config.anthropic_api_key, model_type="anthropic"),
        LLMModel(model_name="gemini-2.0-flash", api_key=config.google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model_type="google"),
        LLMModel(model_name="llama-3.3-70b-versatile", api_key=config.groq_api_key, base_url="https://api.groq.com/openai/v1", model_type="openai")
    ]

    # Step 4: Run the Security Design Review
    reviewer = SecurityDesignReviewer(models=models)
    result = await reviewer.review(design)

    # Step 5: Print results
    print("\n=== Security Design Review Output ===\n")
    print(result.as_markdown())
    print("\n--- Summary ---")
    print(result.summary())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
