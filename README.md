
# ✈ AI-Powered Airline Call Center Optimization System

A comprehensive system for optimizing airline call center operations using AI technologies. This application demonstrates a multi-agent architecture that handles flight information retrieval, customer query processing, call categorization, and performance analytics.

## ✨ Features

- *🔍 Flight Information Agent*: Retrieve detailed information about flights including departure/arrival times, status, terminal, and gate information.
- *💬 QA Response Agent*: Answer natural language queries about flights with context-aware responses.
- *📊 Call Categorization*: Automatically categorize call transcripts into relevant categories (booking, cancellation, baggage issues, etc.).
- *📈 KPI Analysis*: Generate comprehensive analytics from call transcripts including resolution rates, sentiment analysis, and category distribution.

## 🏗 System Architecture

The system is organized into three main modules:

1. *📁 data.py*: Contains the flight database and sample call transcripts.
2. *🤖 agents.py*: Implements the core agent functionality and business logic.
3. *🖥 app.py*: Provides a user-friendly Gradio interface for interacting with the system.

## 📥 Installation

### Prerequisites

- 🐍 Python 3.8 or higher
- 📦 pip package manager

### Setup

1. Clone this repository:
   
   https://github.com/007VICKY007/Airline-Call-Center-Agent.git
   cd Airline-Call-Center-Agent
   

2. Create a virtual environment (recommended):
   
   python -m venv venv
   

3. Activate the virtual environment:
   - On Windows:
     
     venv\Scripts\activate
     
   - On macOS/Linux:
     
     source venv/bin/activate
     

4. Install the required dependencies:
   
   pip install gradio together python-dotenv
   

5. Create a .env file in the project root and add your Together AI API key (optional):
   
   TOGETHER_API_KEY=your_api_key_here
   

## 🚀 Running the Code

1. Run the application:
   
   python app.py
   

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://127.0.0.1:7860).

3. Navigate through the tabs to use different features:
   - *✈ Flight Information Agent*: Enter a flight number (e.g., AI123) to get flight details.
   - *❓ Flight Query Agent*: Ask natural language questions about flights.
   - *🔍 Call Categorization*: Analyze call transcripts to determine the nature of customer inquiries.
   - *📊 KPI Analysis*: Generate call center performance metrics from transcript data.

## 🤖 Multi-Agent Function Calling Approach

The system implements a multi-agent architecture where specialized agents perform different tasks:

1. *Info Agent*: Retrieves raw flight data from the database and formats it as JSON.
   python
   # Example function call
   flight_info = info_agent_request("AI123")
   

2. *QA Agent*: Processes natural language queries by:
   - Extracting flight numbers using regex patterns or AI
   - Retrieving flight data through the Info Agent
   - Generating natural language responses based on query intent
   python
   # Example function call
   response = qa_agent_respond("What time does flight AI123 depart?")
   

3. *Categorization Agent*: Analyzes call transcripts to:
   - Identify the primary reason for the call
   - Extract key information (flight numbers, customer names, etc.)
   - Determine resolution status
   python
   # Example function call
   categorization = categorize_call(transcript)
   

4. *KPI Agent*: Aggregates information from multiple call transcripts to:
   - Calculate performance metrics (resolution rate, response time)
   - Identify trends and common issues
   - Perform basic sentiment analysis
   python
   # Example function call
   kpi_data = compute_call_center_kpis(transcripts)
   

These agents can operate independently or collaborate through function calls. For example, the QA Agent calls the Info Agent to retrieve flight data before generating its response.

The system also demonstrates AI function augmentation by optionally using Together AI for enhanced capabilities. When available, the AI can:
- Extract flight numbers from complex queries
- Generate more natural and contextually appropriate responses
- Improve categorization accuracy
- Provide better sentiment analysis

If Together AI is not available, the system gracefully falls back to pattern-based processing.

## 📋 Sample Data

The system comes pre-loaded with:
- 🛫 10 sample flights with varying statuses and details
- 🗣 6 sample call transcripts covering different scenarios (general inquiries, rebooking, baggage issues, seat changes, etc.)

## 📤 Output Format

All outputs are provided in JSON format for easy integration with other systems and APIs.

## ⚙ Customization

- *✈ Adding Flights*: Update the FLIGHT_DATABASE dictionary in data.py.
- *🗣 Adding Call Transcripts*: Add new transcripts to the SAMPLE_TRANSCRIPTS list in data.py.
- *🧠 Modifying AI Models*: Change the model parameters in the invoke_together_model function in agents.py.

## 📄 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- 🎨 Built with [Gradio](https://www.gradio.app/) for the user interface
- 🤖 Powered by [Together AI](https://www.together.ai/) for enhanced NLP capabilities
