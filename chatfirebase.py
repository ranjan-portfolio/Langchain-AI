from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

load_dotenv()


"""
Steps to replicate this example:
1. Create a Firebase account
2. Create a new Firebase project and FireStore Database
3. Retrieve the Project ID
4. Install the Google Cloud CLI on your computer
    - https://cloud.google.com/sdk/docs/install
    - Authenticate the Google Cloud CLI with your Google account
        - https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
    - Set your default project to the new Firebase project you created
5. pip install langchain-google-firestore
6. Enable the Firestore API in the Google Cloud Console:
    - https://console.cloud.google.com/apis/enableflow?apiid=firestore.googleapis.com&project=test-dbe94
"""


PROJECT_ID="test-dbe94"
SESSION_ID="SESSION_ID"
COLLECTION_NAME="chat_history"

print("The AI chat is getting ready..")
client=firestore.Client(project=PROJECT_ID)
print("starting AI power...")
chat_history=FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,

)
for msg in chat_history.messages:
   if isinstance(msg,HumanMessage) :
    print(f"You: {msg.content}")
   if isinstance(msg,AIMessage):
    print(f"AI: {msg.content}")

model=ChatOpenAI(model="gpt-4o")
while True:
    
    human_message=input("You:")
    if human_message.lower()=="exit" :
        break
    chat_history.add_user_message(human_message)
    ai_message= model.invoke(chat_history.messages)
    chat_history.add_ai_message(ai_message.content)
    print(f"AI:{ai_message.content}")

