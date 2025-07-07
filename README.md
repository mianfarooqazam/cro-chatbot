
## Setup Instructions

### Prerequisites
- Python 3.8
- pip (Python package manager)

### Installation

1. **Install python 3.8** ( Works well with Rasa )
   ```bash
   brew install pyenv
   pyenv install 3.8.18
   ```
   
2. **Create a Virtual Environment with Python 3.8**
   ```bash
   python3.8 -m venv venv
   ```
3. **Activate the Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```   
   
5. **Start the action server** (Terminal 1)
   ```bash
   rasa run actions
   ```

6. **Start the Rasa server** (Terminal 2)
   ```bash
   rasa shell
   ```

## API Integration

### REST API Endpoint
```
POST http://localhost:5005/webhooks/rest/webhook
```

