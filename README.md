# agents
My Early Agents 
# 🛡️ LLM-Powered Security Design Review Agent

This proof of concept uses multiple large language models (LLMs) to independently conduct a security design review of a provided system specification and architecture. It then ranks and merges their responses into a unified, high-quality threat model and design review.

---

## 🚀 What It Does

- Accepts a software requirements and design specification for a product/feature release
- Assesses if there is sufficient documentation to perform a design review (rejects if necessary)
- Converts diagrams to mermaid format
- Submits the review request to multiple LLMs getting security design reviews as output
- Each ouputted security design review is evaluated and may be rejected with reasons back to the model N times
- All the accepted design reviews are then merged to get a superset of security findings and recommendations with no duplicates. 
- This merging process is also subject to an evaluation-reject-with-reason loop

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

📜 License
MIT — you are free to copy, adapt, and use this code however you'd like.

🙋‍♂️ Author
Created by Andrew Bathgate, as a contribution to the agentic security tooling community. PRs, forks, and feedback welcome.


