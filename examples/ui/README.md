# **User Interfaces of Browser-Use**

| **File Name**          | **User Interface** | **Description**                           | **Example Usage**                         |
|------------------------|-------------------|-------------------------------------------|-------------------------------------------|
| `command_line.py`      | **Terminal**      | Parses arguments for command-line execution. | `python command_line.py`                  |
| `gradio_demo.py`       | **Gradio**        | Provides a dark, chat-style browser-agent UI. | `uv run --extra ui python examples/ui/gradio_demo.py` |
| `streamlit_demo.py`    | **Streamlit**     | Runs a Streamlit-based web interface.    | `python -m streamlit run streamlit_demo.py` |

The Gradio demo follows the compact, RTL chat layout used by the Browser Use workspace and defaults to Ollama, which runs locally without API charges. Install Chromium once with `uv run browser-use install`, install Ollama, start its service if it is not already running (`ollama serve`), and download the default model with `ollama pull llama3.1:8b`. For a smaller local model, select `llama3.2:3b` and run `ollama pull llama3.2:3b`. Vision is enabled only for models that support image input; text-only models use the browser DOM. The app defaults to headless browser mode for servers; uncheck it to show the browser window on a desktop. To connect the app to an existing remote browser instead of launching Chromium locally, set `BROWSER_USE_CDP_URL` to its CDP URL. Gemini and Groq are also available through their limited free tiers; they require provider API keys, which can be entered in the collapsed settings panel or supplied through `GOOGLE_API_KEY`/`GEMINI_API_KEY` and `GROQ_API_KEY`. Uploaded files are passed to the agent as available file paths.
