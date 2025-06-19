# agents
My Early Agents 
# 🛡️ LLM-Powered Security Design Review Agent

This proof of concept uses multiple large language models (LLMs) to independently conduct a security design review of a provided system specification and architecture. It then ranks and merges their responses into a unified, high-quality threat model and design review.

---

## 🚀 What It Does

- Accepts a software requirements specification (SRS) and architecture diagram (in Mermaid format).
- Submits the review request to multiple LLMs (OpenAI, Anthropic Claude, Gemini, DeepSeek, Groq, Ollama).
- Collects and displays each model's security design review.
- Judges and ranks the LLMs based on the completeness and accuracy of their reviews.
- Merges the best parts of each response into a single synthesized report.

---

## 📌 Review Steps Followed by the Agent

Each model is asked to perform a full security design review including:

1. Define scope and system boundaries  
2. Create detailed data flow diagrams  
3. Apply STRIDE or similar frameworks  
4. Rate and prioritize threats  
5. Document mitigations  
6. Rank risks  
7. Provide a final summary and recommendations  

---

## 📁 Project Structure

- `design_review_agent_poc.py`: The interactive Jupyter notebook powering the whole process
- `.env`: API keys for OpenAI, Claude, Gemini, etc. (excluded from repo)
- `README.md`: This file

---

## 🛠️ Setup

1. Clone this repository
2. Create a `.env` file and include your API keys:

```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-claude-key
GOOGLE_API_KEY=your-gemini-key
DEEPSEEK_API_KEY=your-deepseek-key
GROQ_API_KEY=your-groq-key
Install dependencies:


🧠 Example Inputs
The included prompt contains requirements and a full architectural diagram for the OWASP Juice Shop — a purposely vulnerable e-commerce platform used for security testing.

📊 Outputs
Individual LLM security reviews (rendered via Markdown)

Ranked JSON output showing which LLM performed best

Final merged security review, synthesized into clear sections

✅ Status
PoC complete and functional

Easily extensible: swap models, prompt templates, or target architectures

📜 License
MIT — you are free to copy, adapt, and use this code however you'd like.

🙋‍♂️ Author
Created by Andrew Bathgate, as a contribution to the agentic security tooling community. PRs, forks, and feedback welcome.

yaml
Copy
Edit
