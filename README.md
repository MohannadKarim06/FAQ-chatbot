## 🤖 FAQ Chatbot  
**Flagship NLP & MLOps Project (10/10)**  
> A multilingual, document-based FAQ chatbot powered by semantic search and a transformer-based language model. Upload your own FAQ file and chat with it in real time.

---

### 🚀 Live Demo  
- **Frontend (React):** [https://end-to-end-faq-chatbot.vercel.app/](#)  

---

### 🧠 Key Features

- Upload your own **FAQ CSV** file (question/answer pairs)
- Uses **semantic search + summarization** to extract relevant content
- Prompts a **transformer LLM (Mistral)** with the result to answer
- Multilingual support (Arabic ↔ English translation)
- Confidence scoring & fallback answers
- React + Chakra UI frontend for live chat experience
- Logging, environment configs, and clean API architecture

---

### ⚙️ Tech Stack

| Component    | Technology                              |
|--------------|------------------------------------------|
| NLP          | Sentence Transformers, Sumy, Mistral (HF) |
| Backend      | FastAPI, Pydantic, FAISS                 |
| Frontend     | React, Chakra UI, Vite                   |
| Translation  | Deep Translator                          |
| Deployment   | Render + Docker                          |
| Logging      | Python `logging`                         |

---

### 🧪 How It Works

1. **Upload** your FAQ CSV (columns: `question`, `answer`)
2. The app:
   - Cleans and summarizes answers
   - Embeds them using `all-MiniLM-L6-v2`
   - Stores them in a FAISS index
3. **Ask a question** in the chat box
4. The system:
   - Finds the most semantically similar FAQ
   - Sends it (and your question) to the LLM via Together API
   - Translates (if needed) and displays the answer

---

### 🌍 Multilingual Support

- Detects Arabic or English inputs
- Translates both directions for full understanding
- Can be extended to more languages

---

### 💡 Use Cases

- Customer support automation  
- Internal document Q&A  
- Legal/HR/IT support bots  
- FAQ search assistants for SaaS

---

### 🐳 Deployment with Docker + fly.io

#### Backend
- Push to GitHub
- Use the included `Dockerfile` and `fly.toml`
- Add API env vars in Render dashboard


### ✍️ Author  
**Mohannad Karim**  
_NLP & Machine Learning Engineer | MLOps_  
[Portfolio](https://www.upwork.com/freelancers/~01683e506def8e06a2?mp_source=share) 

---
