# Getting Started with Lattice

Welcome to Lattice. Whether you are an experienced software engineer or someone brand new to the world of Artificial Intelligence, this guide is designed to help you set up, run, and understand your first autonomous AI agent. 

To help visualize your journey, here is a high-fidelity preview of the terminal dashboard you will be launching by the end of this guide:

![Lattice Terminal Console Mockup](images/lattice_terminal_mockup.png)

---

## What is Lattice?

Think of Lattice as a highly focused, digital research assistant. 

When you ask a human researcher a complex question, they do not just guess the answer. Instead, they write down a plan, search for information online, read articles, write summaries, and double-check their findings. 

Lattice does the exact same thing using a structured cycle:
1. **Think**: Analyze the current task and decide what information is missing.
2. **Act**: Call a tool (like a web search or web reader) to fetch data.
3. **Observe**: Read the tool's results, write notes on a digital scratchpad, and decide what to do next.

Let's get this assistant set up on your machine.

---

## Step 1: Create a Safe Space (Virtual Environment)

When installing new software, it is best practice to keep it isolated from the rest of your computer. In Python, we do this by creating a virtual environment (a private workspace folder just for this project).

Open your computer's terminal, navigate to the folder where you moved this project, and run these commands:

```bash
# Navigate into the project folder
cd lattice-agent

# Create a new virtual environment folder named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

*Note: Once activated, you will see `(venv)` prepended to your command prompt. This means any libraries we install now will be safely contained inside this folder.*

---

## Step 2: Install the Libraries

Lattice relies on a few key, production-grade packages (like the official Google Gemini SDK and OpenAI SDK) to communicate with AI models. Install them easily using pip:

```bash
# Upgrade pip to the latest version for safety
pip install --upgrade pip

# Install the dependencies listed in requirements.txt
pip install -r requirements.txt
```

---

## Step 3: Configure Your Keys

Lattice needs to know how to connect to your preferred AI model provider. We use a hidden file called a `.env` file to store these connection keys securely.

1. Create a copy of our template file:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file in your editor. You will see several options.
3. If you want to use Google's state-of-the-art Gemini model (highly recommended and set as default), simply get an API key from Google AI Studio, paste it next to `GEMINI_API_KEY`, and save the file:

```env
# Choose the AI provider you want to use
LLM_PROVIDER=gemini

# Paste your API key here
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Maximum research steps the agent can take per question
MAX_STEPS=10
```

---

## Step 4: Start the Interactive Console

Now for the exciting part. Let's boot up the agent and talk to it in real-time.

Run the launch script:
```bash
python main.py
```

You will see an elegant ASCII welcome banner, followed by a prompt asking for your research question:
```text
Lattice > 
```

### Try this Beginner-Friendly Test Case:
To see how smart your new assistant is, type this query and hit enter:
> "Search for the current price of Google stock, then search for it again."

Watch the console output. Lattice will:
1. Decompose the request.
2. Call the `web_search` tool to fetch the price.
3. Observe the result.
4. When it goes to call the search tool the second time, our built-in Jaccard loop guard will recognize that the agent is trying to repeat itself. It will block the repeat action, save your API costs, and output a warning directing the agent to pivot and summarize its findings instead.

---

## Step 5: Verify Everything is Working

To make absolutely sure your copy of Lattice is set up correctly, we have included automated test files. These are tiny scripts that verify our loop-prevention formulas and tokenization boundaries are working.

Run this simple command in your terminal to execute the tests:

```bash
python -m unittest discover -s tests
```

You should see a clean response confirming that all test blocks completed successfully:
```text
Ran 6 tests in 0.000s

OK
```
Congratulations. You are now officially running a production-grade, loop-protected autonomous research agent on your local machine.
