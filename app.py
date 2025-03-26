import os
import json
import gradio as gr
from dotenv import load_dotenv
from data import SAMPLE_TRANSCRIPTS
from agents import (
    is_together_available, 
    info_agent_request, 
    qa_agent_respond, 
    categorize_call, 
    compute_call_center_kpis
)

load_dotenv()

custom_css = """
.json-container {
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 10px;
    margin-top: 10px;
    overflow: auto;
    max-height: 400px;
}
.success-message {
    color: #4CAF50;
    font-weight: bold;
}
.error-message {
    color: #F44336;
    font-weight: bold;
}
.header {
    text-align: center;
    margin-bottom: 20px;
}
"""

def format_json_for_display(json_str):
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        return f"Error parsing JSON: {json_str}"

# Info Agent tab
def info_agent_ui(flight_number):
    if not flight_number:
        return "Please enter a flight number."
    
    response = info_agent_request(flight_number)
    return format_json_for_display(response)

# QA Agent tab
def qa_agent_ui(user_query):
    if not user_query:
        return "Please enter a question about a flight."
    
    together_status = "Using Together AI for enhanced responses." if is_together_available() else "Together AI not available. Using pattern-based responses."
    
    response = qa_agent_respond(user_query)
    formatted_response = format_json_for_display(response)
    
    return f"{together_status}\n\n{formatted_response}"

# Call Categorization tab 
def categorize_sample_transcript(transcript_index):
    if transcript_index is None or transcript_index < 0:
        return "Please select a sample transcript."
    
    transcript = SAMPLE_TRANSCRIPTS[transcript_index]
    
    together_status = "Using Together AI for enhanced categorization." if is_together_available() else "Together AI not available. Using pattern-based categorization."
    
    response = categorize_call(transcript)
    formatted_response = format_json_for_display(response)
    
    return f"{together_status}\n\n{formatted_response}"

# Call Categorization tab 
def categorize_custom_transcript(custom_transcript):
    if not custom_transcript:
        return "Please enter a transcript to categorize."
    
    together_status = "Using Together AI for enhanced categorization." if is_together_available() else "Together AI not available. Using pattern-based categorization."
    
    response = categorize_call(custom_transcript)
    formatted_response = format_json_for_display(response)
    
    return f"{together_status}\n\n{formatted_response}"

# KPI Analysis tab
def kpi_analysis_ui():
    together_status = "Using Together AI for enhanced KPI analysis." if is_together_available() else "Together AI not available. Using pattern-based analysis."
    
    response = compute_call_center_kpis(SAMPLE_TRANSCRIPTS)
    formatted_response = format_json_for_display(response)
    
    return f"{together_status}\n\n{formatted_response}"

def display_transcript(transcript_index):
    if transcript_index is None or transcript_index < 0:
        return ""
    return SAMPLE_TRANSCRIPTS[transcript_index]

def create_app():
    with gr.Blocks(css=custom_css) as app:
        gr.Markdown(
            """
            # ✈ AI-Powered Airline Call Center System
            
            This system demonstrates an AI-powered call center for airline services.
            Select a tab below to interact with different agent functionalities.
            
            All outputs are provided in JSON format for easy integration with other systems.
            """
        )
        
        if is_together_available():
            gr.Markdown(
                """
                <div class="success-message">✅ Together AI API configured successfully</div>
                """
            )
        else:
            gr.Markdown(
                """
                <div class="error-message">⚠ Together AI API not configured. Add TOGETHER_API_KEY to .env file for enhanced AI capabilities.</div>
                """
            )
        
        with gr.Tabs():
            with gr.TabItem("Flight Information Agent"):
                gr.Markdown("Get information about a specific flight by entering its number.")
                
                with gr.Row():
                    flight_input = gr.Textbox(label="Flight Number (e.g., AI123)", placeholder="Enter flight number")
                    info_button = gr.Button("Get Flight Information", variant="primary")
                
                info_output = gr.Textbox(
                    label="Flight Information (JSON)", 
                    placeholder="Flight information will appear here...",
                    lines=10
                )
                
                info_button.click(
                    fn=info_agent_ui,
                    inputs=[flight_input],
                    outputs=info_output
                )
            
            with gr.TabItem("Flight Query Agent"):
                gr.Markdown("Ask questions about flights, such as departure times, destinations, or status updates.")
                
                with gr.Row():
                    query_input = gr.Textbox(
                        label="Your Question", 
                        placeholder="e.g., 'What is the status of flight AI123?'"
                    )
                    qa_button = gr.Button("Submit Question", variant="primary")
                
                qa_output = gr.Textbox(
                    label="Response (JSON)", 
                    placeholder="Response will appear here...",
                    lines=10
                )
                
                qa_button.click(
                    fn=qa_agent_ui,
                    inputs=[query_input],
                    outputs=qa_output
                )
            
            with gr.TabItem("Call Categorization"):
                gr.Markdown("Analyze and categorize customer service call transcripts.")
                
                with gr.Tabs():
                    with gr.TabItem("Sample Transcripts"):
                        sample_selector = gr.Dropdown(
                            label="Select a sample transcript", 
                            choices=[f"Sample Transcript {i+1}" for i in range(len(SAMPLE_TRANSCRIPTS))],
                            type="index"
                        )
                        
                        sample_display = gr.Textbox(
                            label="Transcript Preview", 
                            lines=10,
                            interactive=False
                        )
                        
                        sample_button = gr.Button("Categorize Selected Transcript", variant="primary")
                        
                        sample_output = gr.Textbox(
                            label="Categorization Results (JSON)", 
                            placeholder="Categorization results will appear here...",
                            lines=15
                        )
                    
                    with gr.TabItem("Custom Transcript"):
                        custom_input = gr.Textbox(
                            label="Enter call transcript", 
                            placeholder="Agent: Hello, thank you for calling Air Express. How may I assist you today?\nCustomer: ",
                            lines=10
                        )
                        
                        custom_button = gr.Button("Categorize Custom Transcript", variant="primary")
                        
                        custom_output = gr.Textbox(
                            label="Categorization Results (JSON)", 
                            placeholder="Categorization results will appear here...",
                            lines=15
                        )
                
                sample_selector.change(
                    fn=display_transcript,
                    inputs=[sample_selector],
                    outputs=sample_display
                )
                
                sample_button.click(
                    fn=categorize_sample_transcript,
                    inputs=[sample_selector],
                    outputs=sample_output
                )
                
                custom_button.click(
                    fn=categorize_custom_transcript,
                    inputs=[custom_input],
                    outputs=custom_output
                )
            
            with gr.TabItem("KPI Analysis"):
                gr.Markdown("Compute and visualize key performance indicators from call transcripts.")
                
                gr.Markdown(f"Using {len(SAMPLE_TRANSCRIPTS)} sample transcripts for KPI analysis.")
                
                kpi_button = gr.Button("Compute KPIs", variant="primary")
                
                kpi_output = gr.Textbox(
                    label="KPI Analysis Results (JSON)", 
                    placeholder="KPI analysis results will appear here...",
                    lines=20
                )
                
                kpi_button.click(
                    fn=kpi_analysis_ui,
                    inputs=[],
                    outputs=kpi_output
                )
        
        gr.Markdown(
            """
            ---
            AI-Powered Airline Call Center Optimization System | Gradio Demo with Together AI Integration
            """
        )
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch()