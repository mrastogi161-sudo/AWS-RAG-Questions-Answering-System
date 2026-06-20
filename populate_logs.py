import requests
import time
import random

BASE_URL = "http://localhost:8000"

answerable_questions = [
    "What is the effective date of this AWS Customer Agreement?",
    "Which AWS Contracting Party applies to customers located in India?",
    "What is the minimum notice period AWS must provide before discontinuing a material functionality of a Service?",
    " What percentage interest does AWS charge on late payments?",
    "How long does AWS allow you to retrieve Your Content after termination?",
    "If I'm a customer in Mexico, which AWS Contracting Party is my agreement with, and from what date does this apply?",
    "Under what circumstances can AWS terminate this Agreement immediately without providing a cure period?",
    "What are the four things AWS may do when faced with an intellectual property infringement claim under Section 7.2(a)?",
    "How does the dispute resolution mechanism differ if your AWS Contracting Party is AWS India vs. Amazon Web Services, Inc.?",
    "What is the aggregate liability cap under this Agreement, and what exceptions exist to this cap?",
    "What obligations do I have regarding taxes if I'm an Indian customer with an AWS India contracting party, and how does withholding tax treatment differ?",
    "What is AWS's liability limit?",
    "How are disputes resolved?",
    "What are the service levels?",
    "Who are the AWS Contracting Parties?",
    "What happens when AWS discontinues a service?",
    "What is the indemnification policy?",
    "How is intellectual property handled?",
    "What are the confidentiality obligations?",
    "How do I access the services?",
    "What are the third-party content terms?",
    "What is the effective date of the agreement?",
    "What are the definitions in Section 12?",
    "How is billing handled?",
    "What are the taxes mentioned?",
    "How does AWS handle your content?"
]

unanswerable_questions = [
    "What is the price of EC2 instances?",
    "Who is the CEO of Amazon?",
    "What is AWS's market share?",
    "How do I deploy a Lambda function?",
    "What is the weather today?",
    "Who won the latest World Cup?",
    "What is the capital of France?",
    "How do I cook pasta?",
    "What movies are playing?",
    "What is 2+2?"
]

all_queries = answerable_questions + unanswerable_questions
random.shuffle(all_queries)

print(f"Starting to log {len(all_queries)} queries...")

for i, query in enumerate(all_queries, 1):
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={"query": query, "top_k": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            status = "✅ Found" if data['found_answer'] else "❌ Not Found"
            print(f"{i:3d}. {status} - {query[:50]}... ({data['response_time_ms']}ms)")
        else:
            print(f"{i:3d}. ❌ Error: {response.text}")
        
        time.sleep(0.5)  
        
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: FastAPI server not running on {BASE_URL}")
        break

print("\n✅ Logging complete!")