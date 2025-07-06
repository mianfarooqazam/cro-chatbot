
## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation


1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


2. **Start the action server** (Terminal 1)
   ```bash
   rasa run actions
   ```

3. **Start the Rasa server** (Terminal 2)
   ```bash
   rasa shell
   ```

## API Integration

### REST API Endpoint
```
POST http://localhost:5005/webhooks/rest/webhook
```

