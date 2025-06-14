# Desktop LLM Chat Application

A modern desktop chat application built with customtkinter that allows you to interact with an LLM (Language Learning Model) through a clean and intuitive interface.

## Features

- Modern, dark-themed UI using customtkinter
- Real-time chat interface
- Asynchronous message processing
- Support for Enter key to send messages
- Error handling and user feedback
- Thread-safe message updates

## Requirements

- Python 3.7 or higher
- customtkinter
- ollama

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure you have Ollama running locally with the llama3 model installed.

2. Run the application:
```bash
python chat_app.py
```

3. Type your message in the input field and press Enter or click the Send button to chat with the LLM.

## Notes

- The application uses the llama3 model by default. Make sure you have it installed in your Ollama instance.
- The interface will be disabled while waiting for a response to prevent multiple simultaneous requests.
- Error messages will be displayed in the chat if there are any issues with the LLM communication. 