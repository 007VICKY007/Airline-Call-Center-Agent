import json
import re
import os
from typing import Dict, Any, List, Union
import together
from dotenv import load_dotenv
from data import FLIGHT_DATABASE, SAMPLE_TRANSCRIPTS

load_dotenv("api_keys.env")

together_api_key = os.getenv('TOGETHER_API_KEY')
if together_api_key:
    together.api_key = together_api_key

def is_together_available() -> bool:
    return bool(together_api_key)

def invoke_together_model(prompt: str, model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1") -> Dict:
    if not together_api_key:
        raise EnvironmentError("Together AI API key not configured")
    
    response = together.Complete.create(
        prompt=prompt,
        model=model,
        max_tokens=500,
        temperature=0.1,
        top_p=0.9
    )
    
    return response

def get_flight_info(flight_number: str) -> Dict[str, Any]:
    flight_number = flight_number.upper()
    
    if flight_number in FLIGHT_DATABASE:
        return FLIGHT_DATABASE[flight_number]
    return {}

def info_agent_request(flight_number: str) -> str:
    try:
        result = get_flight_info(flight_number)
        
        if not result:
            return json.dumps({"error": f"Flight {flight_number} not found in database."})
        
        return json.dumps(result)
            
    except Exception as e:
        return json.dumps({"error": f"Error processing request: {str(e)}"})

def extract_flight_number(query: str) -> str:
    patterns = [
        r'flight\s+([A-Za-z]{1,3}\d{1,4})',
        r'([A-Za-z]{1,3}\d{1,4})\s+flight',
        r'flight\s+number\s+([A-Za-z]{1,3}\d{1,4})',
        r'([A-Za-z]{1,3}\d{1,4})'
    ]
    
    for pattern in patterns:
        matches = re.search(pattern, query, re.IGNORECASE)
        if matches:
            return matches.group(1)
    
    if is_together_available():
        try:
            prompt = f"""
            Extract the flight number from the following user query. 
            Respond with ONLY the flight number, or 'NONE' if no flight number is found.
            
            User query: {query}
            
            Flight number:
            """
            
            response = invoke_together_model(prompt)
            extracted = response['output']['choices'][0]['text'].strip()
            
            if re.match(r'^[A-Za-z]{1,3}\d{1,4}$', extracted):
                return extracted
            elif extracted != "NONE":
                for pattern in patterns:
                    matches = re.search(pattern, extracted, re.IGNORECASE)
                    if matches:
                        return matches.group(1)
        except Exception as e:
            print(f"Error using Together AI for extraction: {str(e)}")
            pass
    
    return ""

def qa_agent_respond(user_query: str) -> str:
    try:
        flight_number = extract_flight_number(user_query)
        
        if not flight_number:
            return json.dumps({
                "answer": "I couldn't identify a flight number in your query. Please specify a flight number like 'AI123'."
            })
        
        flight_data = get_flight_info(flight_number)
        
        if not flight_data:
            return json.dumps({
                "answer": f"Flight {flight_number} not found in database."
            })
        
        if is_together_available():
            try:
                prompt = f"""
                Generate a concise answer to the user's query about a flight based on the flight data provided.
                The response should be factual and address the specific question asked.
                
                User query: {user_query}
                
                Flight data: {json.dumps(flight_data)}
                
                Answer:
                """
                
                response = invoke_together_model(prompt)
                answer = response['output']['choices'][0]['text'].strip()
                
                if answer and len(answer) <= 200:
                    return json.dumps({
                        "answer": answer
                    })
            except Exception as e:
                print(f"Error using Together AI for response generation: {str(e)}")
        
        if re.search(r'depart|departure|leave|time', user_query, re.IGNORECASE):
            answer = f"Flight {flight_data['flight_number']} departs at {flight_data['departure_time']} to {flight_data['destination']}. Current status: {flight_data['status']}."
        elif re.search(r'destination|arrive|goes to|going to', user_query, re.IGNORECASE):
            answer = f"Flight {flight_data['flight_number']} is headed to {flight_data['destination']}. It departs at {flight_data['departure_time']}. Current status: {flight_data['status']}."
        elif re.search(r'status|delayed|on time|cancelled', user_query, re.IGNORECASE):
            answer = f"Flight {flight_data['flight_number']} status: {flight_data['status']}. It's scheduled to depart at {flight_data['departure_time']} to {flight_data['destination']}."
        elif re.search(r'terminal|gate', user_query, re.IGNORECASE):
            answer = f"Flight {flight_data['flight_number']} departs from Terminal {flight_data['terminal']}, Gate {flight_data['gate']}. Current status: {flight_data['status']}."
        else:
            answer = f"Flight {flight_data['flight_number']} to {flight_data['destination']} departs at {flight_data['departure_time']} from Terminal {flight_data['terminal']}, Gate {flight_data['gate']}. Current status: {flight_data['status']}."
        
        return json.dumps({
            "answer": answer
        })
            
    except Exception as e:
        return json.dumps({"answer": f"Error processing request: {str(e)}"})

def categorize_call(transcript: str) -> str:
    try:
        categories = {
            "Flight Booking": ["book", "reserve", "purchase", "buy", "schedule"],
            "Flight Cancellation": ["cancel", "refund", "money back"],
            "Flight Rescheduling": ["reschedule", "change", "move", "different date"],
            "Baggage Issue": ["baggage", "luggage", "bag", "suitcase", "missing", "lost"],
            "Complaint": ["complaint", "unhappy", "disappointed", "poor", "terrible", "bad experience", "upset"],
            "Seat Change": ["seat", "change seat", "different seat", "window", "aisle"],
            "General Inquiry": ["status", "check", "information", "time", "when"]
        }
        
        if is_together_available():
            try:
                prompt = f"""
                You are an AI assistant that categorizes airline call center conversations. 
                Categories include: Flight Booking, Flight Cancellation, Flight Rescheduling, 
                Refund Request, Baggage Issue, Complaint, and General Inquiry.
                
                Please categorize the following call transcript and extract key information 
                like flight numbers, dates, and specific issues. Provide the output in JSON 
                format with 'category' and 'details' fields.
                
                Transcript: {transcript}
                
                Output:
                """
                
                response = invoke_together_model(prompt)
                categorization = response['output']['choices'][0]['text'].strip()
                
                try:
                    json.loads(categorization)
                    return categorization
                except json.JSONDecodeError:
                    pass
            except Exception as e:
                print(f"Error using Together AI for categorization: {str(e)}")
        
        transcript_lower = transcript.lower()
        determined_category = "General Inquiry"
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in transcript_lower:
                    determined_category = category
                    break
        
        flight_numbers = []
        pattern = r'([A-Za-z]{1,3}\d{1,4})'
        matches = re.findall(pattern, transcript)
        if matches:
            flight_numbers = [match for match in matches if match.upper().startswith('AI')]
        
        resolved = "thank you" in transcript_lower and "have a" in transcript_lower
        resolution_status = "Resolved" if resolved else "Pending"
        
        customer_name = "Unknown"
        name_patterns = [
            r'name is ([A-Za-z\s]+),',
            r'name is ([A-Za-z\s]+)\.', 
            r'I\'m ([A-Za-z\s]+),',
            r'this is ([A-Za-z\s]+),'
        ]
        
        for pattern in name_patterns:
            name_match = re.search(pattern, transcript)
            if name_match:
                customer_name = name_match.group(1).strip()
                break
        
        details = {
            "flight_numbers": flight_numbers,
            "customer_name": customer_name,
            "resolution_status": resolution_status,
            "call_summary": f"{determined_category} related to flight(s): {', '.join(flight_numbers) if flight_numbers else 'None specified'}"
        }
        
        return json.dumps({
            "category": determined_category,
            "details": details
        })
    
    except Exception as e:
        return json.dumps({"error": f"Error categorizing call: {str(e)}"})

def compute_call_center_kpis(transcripts: List[str]) -> str:
    if not transcripts:
        return json.dumps({"error": "No transcripts provided"})
    
    try:
        categories = {}
        resolution_count = 0
        flight_mentions = {}
        customer_sentiments = []
        
        for transcript in transcripts:
            categorization = json.loads(categorize_call(transcript))
            category = categorization.get("category", "Unknown")
            details = categorization.get("details", {})
            
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
            
            if details.get("resolution_status") == "Resolved":
                resolution_count += 1
            
            for flight in details.get("flight_numbers", []):
                if flight in flight_mentions:
                    flight_mentions[flight] += 1
                else:
                    flight_mentions[flight] = 1
            
            sentiment_score = 0
            positive_words = ["thank", "good", "great", "excellent", "helpful", "appreciate", "happy", "satisfied"]
            negative_words = ["unhappy", "disappointed", "poor", "terrible", "bad", "issue", "problem", "complaint", "delay", "upset", "missed"]
            
            transcript_lower = transcript.lower()
            for word in positive_words:
                if word in transcript_lower:
                    sentiment_score += 1
            for word in negative_words:
                if word in transcript_lower:
                    sentiment_score -= 1
                    
            customer_sentiments.append(sentiment_score)
        
        avg_response_time = 25
        
        avg_sentiment = sum(customer_sentiments) / len(customer_sentiments) if customer_sentiments else 0
        
        resolution_rate = (resolution_count / len(transcripts)) * 100 if transcripts else 0
        
        most_common_category = max(categories.items(), key=lambda x: x[1])[0] if categories else "None"
        
        most_mentioned_flights = sorted(flight_mentions.items(), key=lambda x: x[1], reverse=True)[:3] if flight_mentions else []
        
        kpi_result = {
            "total_calls": len(transcripts),
            "call_categories": categories,
            "resolution_rate": resolution_rate,
            "average_response_time": avg_response_time,
            "average_sentiment": avg_sentiment,
            "most_common_issue": most_common_category,
            "most_mentioned_flights": dict(most_mentioned_flights),
            "category_distribution": {category: (count / len(transcripts)) * 100 for category, count in categories.items()}
        }
        
        return json.dumps(kpi_result)
        
    except Exception as e:
        return json.dumps({"error": f"Error computing KPIs: {str(e)}"})