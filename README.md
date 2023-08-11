# Story Chat

This project is a unique blend of literature and technology, allowing users to converse with characters from popular stories from Project Gutenberg.

## Features
- Utilizes embeddings of stories to create a dynamic and engaging experience.
- Leverages the OpenAI API along with Langchain to generate realistic dialogues.
- Interactive Streamlit interface for smooth user interaction.

## Installation

### Requirements
- Python 3.6+
- OpenAI API key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/E-Silverstein/Story-Chat.git
2. Install requirements:
   pip install -r requirements.txt
3. Add OpenAI API Key to enviroment or replace key within code
   ```bash
   export OPENAI_API_KEY=<your secret key>
   ```
   or replace
   ```code
   openai_api_key = os.environ['OPENAI_KEY']
   ```
   with
   ```code
   openai_api_key = <your secret key>
4. Run Streamlit server
   ```bash
   streamlit run main.py
