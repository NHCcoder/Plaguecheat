# <img src="./assets/dark.ico#gh-dark-mode-only" alt="Dark Mode Logo" width="30" height="30"> <img src="./assets/favicon.ico#gh-light-mode-only" alt="Light Mode Logo" width="30" height="30"> mpathy.ai POC




An initial POC of open-source LLMs using Ollama for local use and live sentiment analysis in chats.

<div align="center">
<img src="./assets/demo.gif" alt="icon"/>
</div>

# Setup

You'll need [Ollama](https://ollama.com/) installed and running. This POC is using `llama3` by default but can easily be switched out for other models found [here](https://ollama.com/library).

Once installed, you can download a model and run it in the background using this command in your terminal:

```bash
ollama run llama3
```

To try out other models, first download the desired model using the `ollama pull` command and then change the model name in `state.py`.

### 🧬 1. Clone the Repo

```bash
git clone https://github.com/stealth-ai-startup/llm-chat-sentiment-poc.git
```

### 📦 2. Install libraries

Install `pip` dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 3. Run the application

Initialize and run the app (You'll only need to initialize the first time):

```bash
reflex init
reflex run
```

The web app will compile and then start running at `http://localhost:3000`