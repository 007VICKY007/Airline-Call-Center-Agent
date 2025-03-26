FLIGHT_DATABASE = {
    "AI123": {
        "flight_number": "AI123",
        "departure_time": "08:00 AM",
        "destination": "Delhi",
        "status": "Delayed",
        "terminal": "T2",
        "gate": "G14",
        "arrival_time": "10:30 AM"
    },
    "AI456": {
        "flight_number": "AI456",
        "departure_time": "10:30 AM",
        "destination": "Mumbai",
        "status": "On Time",
        "terminal": "T1",
        "gate": "G22",
        "arrival_time": "12:15 PM"
    },
    "AI789": {
        "flight_number": "AI789",
        "departure_time": "02:15 PM",
        "destination": "Bangalore",
        "status": "Boarding",
        "terminal": "T3",
        "gate": "G5",
        "arrival_time": "04:00 PM"
    },
    "AI234": {
        "flight_number": "AI234",
        "departure_time": "06:45 PM",
        "destination": "Chennai",
        "status": "Cancelled",
        "terminal": "T2",
        "gate": "G19",
        "arrival_time": "08:30 PM"
    },
    "AI567": {
        "flight_number": "AI567",
        "departure_time": "11:15 AM",
        "destination": "Kolkata",
        "status": "On Time",
        "terminal": "T1",
        "gate": "G7",
        "arrival_time": "01:30 PM"
    },
    "AI890": {
        "flight_number": "AI890",
        "departure_time": "04:30 PM",
        "destination": "Hyderabad",
        "status": "Scheduled",
        "terminal": "T3",
        "gate": "G12",
        "arrival_time": "06:15 PM"
    },
    "AI432": {
        "flight_number": "AI432",
        "departure_time": "07:15 AM",
        "destination": "Goa",
        "status": "On Time",
        "terminal": "T1",
        "gate": "G10",
        "arrival_time": "09:00 AM"
    },
    "AI765": {
        "flight_number": "AI765",
        "departure_time": "02:30 PM",
        "destination": "Jaipur",
        "status": "Delayed",
        "terminal": "T3",
        "gate": "G18",
        "arrival_time": "04:15 PM"
    },
    "AI321": {
        "flight_number": "AI321",
        "departure_time": "09:45 AM",
        "destination": "Ahmedabad",
        "status": "On Time",
        "terminal": "T2",
        "gate": "G5",
        "arrival_time": "11:30 AM"
    },
    "AI654": {
        "flight_number": "AI654",
        "departure_time": "05:30 PM",
        "destination": "Pune",
        "status": "Boarding",
        "terminal": "T1",
        "gate": "G20",
        "arrival_time": "07:00 PM"
    }
}

SAMPLE_TRANSCRIPTS = [
    """
    Agent: Hello, thank you for calling Air Express. How may I assist you today?
    Customer: Hi, I need to check the status of my flight AI123 to Delhi.
    Agent: I'd be happy to help you with that. May I have your booking reference?
    Customer: It's ABC123.
    Agent: Thank you. I can see that flight AI123 to Delhi is currently delayed by 30 minutes. It's now scheduled to depart at 8:30 AM.
    Customer: Oh, that's not too bad. Will this affect my connecting flight?
    Agent: Let me check that for you. I see you have a connection in Delhi to Mumbai. The good news is that you'll still have sufficient time to make your connection.
    Customer: That's a relief. Thank you for checking.
    Agent: Is there anything else I can help you with today?
    Customer: No, that's all. Thank you.
    Agent: Thank you for calling Air Express. Have a great day!
    """,
    
    """
    Agent: Good morning, thank you for calling Air Express. How can I help you today?
    Customer: I missed my flight AI456 this morning and need to rebook.
    Agent: I'm sorry to hear that. Let me check availability for you. May I have your booking reference?
    Customer: XYZ789.
    Agent: Thank you. I see several options I can rebook you on. The next available flight is at 2:15 PM today.
    Customer: That works for me. Can I get the same seat?
    Agent: Let me check. Yes, I can assign you a similar seat. Would you like me to proceed with the rebooking?
    Customer: Yes, please.
    Agent: All set. I've rebooked you on flight AI789 departing at 2:15 PM. Your boarding pass has been sent to your email.
    Customer: Great, thank you for your help.
    Agent: You're welcome. Have a safe journey.
    """
]
