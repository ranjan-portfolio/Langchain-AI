from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.agents import initialize_agent, AgentType,Tool
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")

sender_list=["ranjanabha@gmail.com"]

# This function will be used as a tool for sending email

def sendemail(response: str):

    subject="Your daily tech news byte"
    SENDER_EMAIL="ranjanabha@gmail.com"
    receiver="saumyadip.sinha0611@gmail.com"

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver
        msg.attach(MIMEText(response, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver, msg.as_string())

        return f"✅ Email sent successfully to {receiver}"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"


model=ChatOpenAI(model="gpt-4o")

# chain for getting top 10 tech news

tech_news_template ="""
You are a smart tech journalist.
Provide top {news_count} latest technology development of the day
"""

prompt=PromptTemplate(template=tech_news_template,input_variables=["news_count"])

news_chain=prompt|model|StrOutputParser()

# chain for formatting news content into HTML 


send_email_subscriber="""
    Your are my digital asistant.
    Take the following news and prepare an HTML formatted email to be sent to {sender_list}.
    Here are the news:
    {news_content}
"""

email_prompt=PromptTemplate(template=send_email_subscriber,input_variables=["sender_list","news_content"])

email_chain=email_prompt|model|StrOutputParser()

#Run chains

news=news_chain.invoke({
    "news_count":"10"
})

html_news=email_chain.invoke({
    "sender_list":sender_list,
    "news_content":news
})

sendemail_tool=Tool(name="SendEmail",
               func=sendemail,
               description="Sends email using sendemail function")

tools=[sendemail_tool]

agent=initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True

)
response=agent.run(f"Email my tech news letter: {html_news}")

print(response)







