import customtkinter as ctk
from ollama import Client
import threading
import queue
import json
import os

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("P.A.I")
        self.geometry("800x600")
        
        # Initialize message history
        self.message_history = []
        self.history_file = "chat_history.json"
        self.load_history()
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create chat display
        self.chat_display = ctk.CTkTextbox(self.main_frame, wrap="word", state="disabled")
        self.chat_display.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
        
        # Create input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Create input field
        self.input_field = ctk.CTkEntry(self.input_frame, placeholder_text="Type your message here...")
        self.input_field.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Create send button
        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0, 0))
        
        # Bind Enter key to send message
        self.input_field.bind("<Return>", lambda event: self.send_message())
        
        # Initialize Ollama client
        self.client = Client()
        
        # Create message queue for thread-safe updates
        self.message_queue = queue.Queue()
        
        # Start message processing
        self.process_messages()
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def add_message(self, message, is_user=True):
        """Add a message to the chat display"""
        self.chat_display.configure(state="normal")
        
        # Add user/bot prefix
        prefix = "You: " if is_user else "Bot: "
        self.chat_display.insert("end", prefix + message + "\n\n")
        
        # Scroll to bottom
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def send_message(self):
        """Send message to LLM and display response"""
        message = self.input_field.get().strip()
        if not message:
            return
            
        # Clear input field
        self.input_field.delete(0, "end")
        
        # Add user message to chat
        self.add_message(message, is_user=True)
        
        # Disable input while processing
        self.input_field.configure(state="disabled")
        self.send_button.configure(state="disabled")
        
        # Start processing in a separate thread
        threading.Thread(target=self.process_llm_response, args=(message,), daemon=True).start()

    def process_llm_response(self, message):
        """Process LLM response in a separate thread"""
        try:
            # Add user message to history
            self.message_history.append({"role": "user", "content": message})
            
            # Get response from LLM with full conversation history
            response = self.client.chat(
                model='llama3',
                messages=self.message_history
            )
            
            # Add assistant response to history
            self.message_history.append({"role": "assistant", "content": response['message']['content']})
            
            self.message_queue.put(response['message']['content'])
        except Exception as e:
            self.message_queue.put(f"Error: {str(e)}")
        finally:
            # Re-enable input
            self.input_field.configure(state="normal")
            self.send_button.configure(state="normal")
            self.input_field.focus()

    def process_messages(self):
        """Process messages from the queue"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.add_message(message, is_user=False)
        except queue.Empty:
            pass
        finally:
            # Schedule next check
            self.after(100, self.process_messages)

    def load_history(self):
        """Load conversation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.message_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            self.message_history = []

    def save_history(self):
        """Save conversation history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.message_history, f)
        except Exception as e:
            print(f"Error saving history: {str(e)}")

    def on_closing(self):
        """Handle window closing"""
        self.save_history()
        self.destroy()

if __name__ == "__main__":
    app = ChatApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop() 