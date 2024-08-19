from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
# from process_raw_file import extract_audio_with_ffmpeg, transcribe_audio, process_video
load_dotenv()
from langchain.schema import Document
# openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_subjective(processed_transcript):
  """function to generate subjective from transcription"""

  examples = [
    {
      "input": "Patient – Good Morning, doctor. May I come in? Doctor – Good Morning. How are you? You do look quite pale this morning. Patient – Yes, doctor. I’ve not been feeling well for the past few days. I’ve been having a stomach ache for a few days and feeling a bit dizzy since yesterday. Doctor – Okay, let me check. (applies pressure on the stomach and checks for pain) Does it hurt here? Patient – Yes, doctor, the pain there is the sharpest. Doctor – Well, you are suffering from a stomach infection, that’s the reason you are having a stomach ache and also getting dizzy. Did you change your diet recently or have something unhealthy? Patient – Actually, I went to a fair last week and ate food from the stalls there. Doctor – Okay, so you are probably suffering from food poisoning. Since the food stalls in fairs are quite unhygienic, there’s a high chance those uncovered food might have caused food poisoning. Patient – I think I will never eat from any unhygienic place in the future. Doctor – That’s good. I’m prescribing some medicines, have them for one week and come back for a checkup next week. And please try to avoid spicy and fried foods for now. Patient – Okay, doctor, thank you. Doctor – Welcome.",
      "output": "The patient reports feeling unwell for the past few days, presenting with a stomach ache that started several days ago and dizziness that began yesterday. The pain is described as sharp, particularly when pressure is applied to the stomach. The patient admits to having consumed food from stalls at a fair last week, which may have been unhygienic. The patient acknowledges a likely association between the consumption of this food and the onset of symptoms. The patient is concerned about avoiding similar situations in the future and agrees to follow the prescribed medication and dietary advice."
    },
    {
      "input": "Patient – Good afternoon, Doctor. Doctor – Good afternoon, Mr. Bose. How are you? Patient – I’m doing good, doctor, but my daughter isn’t doing well. Everywhere, people are getting affected with COVID and I am really worried about her. Doctor – Please have a seat and tell me what happened. Patient – Last week, my daughter came back from Pune as her college was closed on account of COVID. From the second day, she has had high fever and has been coughing badly. I think that she has contracted the virus on her way home. Doctor – Okay, I understand your concern. Having a fever and cough doesn’t necessarily mean that someone has contracted the virus. These are symptoms of common cold too. The change in the temperature of the atmosphere could have triggered these symptoms. Still, to put your worries to rest, I am prescribing some medicines and an RT PCR test. Do the test by tomorrow, and if the test results are positive, make sure she is isolated. On the other hand, if the result is negative, just give her the medicine and ask her to drink a lot of water. Also, bring her in so I could examine her. Patient – Okay, doctor. I will bring her in the evening. Thank you. Doctor – You are welcome.",
      "output": "The patient's father reports that his daughter has been experiencing a high fever and severe cough since returning from Pune last week, where her college was closed due to COVID-19 concerns. The father is highly anxious about the possibility of his daughter contracting COVID-19 during her journey back home. He expresses significant worry, noting the widespread impact of the virus and the recent onset of symptoms. He is seeking guidance on the next steps, including diagnostic testing and further examination. The father is cooperative and plans to bring his daughter in for examination later in the day."
    }
  ]
  
  prompt_template = (
    "Generate a subjective in a SOAP note for this conversation between a patient and their physician. "
    "{context}\n\n"
    "Examples:\n"
  )
  # Append examples to the prompt
  for example in examples:
      prompt_template += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
  
  # Define the final prompt template
  prompt = ChatPromptTemplate.from_messages([
      ("system", prompt_template + "{context}")
  ])

  llm = ChatOpenAI(model="gpt-4o")
  # Instantiate chain
  chain = create_stuff_documents_chain(llm, prompt)
  transcript_doc = Document(page_content=processed_transcript, metadata={})
  # Invoke chain
  result = chain.invoke({"context": processed_transcript})
  # print(result)
  return result

def generate_objective(processed_transcript):
  """function to generate objective from transcription"""

  examples = [
    {
      "input": "Patient – Good Morning, doctor. May I come in? Doctor – Good Morning. How are you? You do look quite pale this morning. Patient – Yes, doctor. I’ve not been feeling well for the past few days. I’ve been having a stomach ache for a few days and feeling a bit dizzy since yesterday. Doctor – Okay, let me check. (applies pressure on the stomach and checks for pain) Does it hurt here? Patient – Yes, doctor, the pain there is the sharpest. Doctor – Well, you are suffering from a stomach infection, that’s the reason you are having a stomach ache and also getting dizzy. Did you change your diet recently or have something unhealthy? Patient – Actually, I went to a fair last week and ate food from the stalls there. Doctor – Okay, so you are probably suffering from food poisoning. Since the food stalls in fairs are quite unhygienic, there’s a high chance those uncovered food might have caused food poisoning. Patient – I think I will never eat from any unhygienic place in the future. Doctor – That’s good. I’m prescribing some medicines, have them for one week and come back for a checkup next week. And please try to avoid spicy and fried foods for now. Patient – Okay, doctor, thank you. Doctor – Welcome.",
      "output": "The patient appears pale and reports experiencing a stomach ache for the past few days and dizziness since the previous day. Physical examination reveals sharp pain upon palpation of the abdomen, particularly in the area where pressure is applied. The physician suspects a stomach infection, likely related to recent dietary changes or consumption of food from unhygienic sources. The patient's vital signs were not explicitly mentioned but should be monitored, given the reported symptoms. The physician prescribes a course of medication and advises dietary restrictions to manage the infection."
      },
    {
      "input": "Patient – Good afternoon, Doctor. Doctor – Good afternoon, Mr. Bose. How are you? Patient – I’m doing good, doctor, but my daughter isn’t doing well. Everywhere, people are getting affected with COVID and I am really worried about her. Doctor – Please have a seat and tell me what happened. Patient – Last week, my daughter came back from Pune as her college was closed on account of COVID. From the second day, she has had high fever and has been coughing badly. I think that she has contracted the virus on her way home. Doctor – Okay, I understand your concern. Having a fever and cough doesn’t necessarily mean that someone has contracted the virus. These are symptoms of common cold too. The change in the temperature of the atmosphere could have triggered these symptoms. Still, to put your worries to rest, I am prescribing some medicines and an RT PCR test. Do the test by tomorrow, and if the test results are positive, make sure she is isolated. On the other hand, if the result is negative, just give her the medicine and ask her to drink a lot of water. Also, bring her in so I could examine her. Patient – Okay, doctor. I will bring her in the evening. Thank you. Doctor – You are welcome.",
      "output": "The patient’s father reports that his daughter has developed a high fever and severe cough shortly after returning from Pune, where she was exposed to potential COVID-19 infection. The patient has not been examined yet, but the physician acknowledges the symptoms could be consistent with COVID-19 or a common cold. An RT-PCR test has been prescribed to confirm or rule out the presence of the virus. The patient has been advised to stay hydrated and isolate if the test results are positive. The physician plans to examine the patient later in the day if the symptoms persist."
    }
  ]
  
  prompt_template = (
    "Generate a objective in a SOAP note for this conversation between a patient and their physician. "
    "{context}\n\n"
    "Examples:\n"
  )
  # Append examples to the prompt
  for example in examples:
      prompt_template += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
  
  # Define the final prompt template
  prompt = ChatPromptTemplate.from_messages([
      ("system", prompt_template + "{context}")
  ])
  
  llm = ChatOpenAI(model="gpt-4o")
  # Instantiate chain
  chain = create_stuff_documents_chain(llm, prompt)

  # Invoke chain
  result = chain.invoke({"context": processed_transcript})
  # print(result)
  return result

def generate_assessment(processed_transcript):
  """function to generate assessment from transcription"""

  examples = [
    {
      "input": "Patient – Good Morning, doctor. May I come in? Doctor – Good Morning. How are you? You do look quite pale this morning. Patient – Yes, doctor. I’ve not been feeling well for the past few days. I’ve been having a stomach ache for a few days and feeling a bit dizzy since yesterday. Doctor – Okay, let me check. (applies pressure on the stomach and checks for pain) Does it hurt here? Patient – Yes, doctor, the pain there is the sharpest. Doctor – Well, you are suffering from a stomach infection, that’s the reason you are having a stomach ache and also getting dizzy. Did you change your diet recently or have something unhealthy? Patient – Actually, I went to a fair last week and ate food from the stalls there. Doctor – Okay, so you are probably suffering from food poisoning. Since the food stalls in fairs are quite unhygienic, there’s a high chance those uncovered food might have caused food poisoning. Patient – I think I will never eat from any unhygienic place in the future. Doctor – That’s good. I’m prescribing some medicines, have them for one week and come back for a checkup next week. And please try to avoid spicy and fried foods for now. Patient – Okay, doctor, thank you. Doctor – Welcome.",
      "output":"The patient is presenting with symptoms consistent with a gastrointestinal infection, likely secondary to food poisoning. The history of recent consumption of food from unhygienic sources (food stalls at a fair) aligns with the onset of symptoms, including sharp abdominal pain and dizziness. The patient's pale appearance further suggests a possible systemic response to the infection. The differential diagnosis includes a stomach infection, most likely due to bacterial contamination. The patient has been advised to take prescribed medications and follow dietary restrictions to manage the infection. Follow-up is recommended in one week to reassess symptoms and response to treatment."
    },
    {
      "input": "Patient – Good afternoon, Doctor. Doctor – Good afternoon, Mr. Bose. How are you? Patient – I’m doing good, doctor, but my daughter isn’t doing well. Everywhere, people are getting affected with COVID and I am really worried about her. Doctor – Please have a seat and tell me what happened. Patient – Last week, my daughter came back from Pune as her college was closed on account of COVID. From the second day, she has had high fever and has been coughing badly. I think that she has contracted the virus on her way home. Doctor – Okay, I understand your concern. Having a fever and cough doesn’t necessarily mean that someone has contracted the virus. These are symptoms of common cold too. The change in the temperature of the atmosphere could have triggered these symptoms. Still, to put your worries to rest, I am prescribing some medicines and an RT PCR test. Do the test by tomorrow, and if the test results are positive, make sure she is isolated. On the other hand, if the result is negative, just give her the medicine and ask her to drink a lot of water. Also, bring her in so I could examine her. Patient – Okay, doctor. I will bring her in the evening. Thank you. Doctor – You are welcome.",
      "output":"The patient’s daughter presents with symptoms of fever and a severe cough, raising concerns about a possible COVID-19 infection. Given the timing of symptom onset following her return from Pune, where COVID exposure could have occurred, an RT-PCR test has been recommended to confirm or rule out the diagnosis. However, differential diagnoses include common cold or viral upper respiratory infection, which could also be consistent with the symptoms described. The patient has been advised to initiate symptomatic treatment and proceed with the COVID testing. Isolation protocols will be followed if the test is positive. A follow-up examination is planned to further assess her condition."
    }
  ]
  
  prompt_template = (
    "Generate an assessment in a SOAP note for this conversation between a patient and their physician. "
    "{context}\n\n"
    "Examples:\n"
  )
  # Append examples to the prompt
  for example in examples:
      prompt_template += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
  
  # Define the final prompt template
  prompt = ChatPromptTemplate.from_messages([
      ("system", prompt_template + "{context}")
  ])
  
  llm = ChatOpenAI(model="gpt-4o")
  # Instantiate chain
  chain = create_stuff_documents_chain(llm, prompt)

  # Invoke chain
  result = chain.invoke({"context": processed_transcript})
  # print(result)
  return result

def generate_plan(processed_transcript):
  """function to generate plan from transcription"""

  examples = [
    {
      "input": "Patient – Good Morning, doctor. May I come in? Doctor – Good Morning. How are you? You do look quite pale this morning. Patient – Yes, doctor. I’ve not been feeling well for the past few days. I’ve been having a stomach ache for a few days and feeling a bit dizzy since yesterday. Doctor – Okay, let me check. (applies pressure on the stomach and checks for pain) Does it hurt here? Patient – Yes, doctor, the pain there is the sharpest. Doctor – Well, you are suffering from a stomach infection, that’s the reason you are having a stomach ache and also getting dizzy. Did you change your diet recently or have something unhealthy? Patient – Actually, I went to a fair last week and ate food from the stalls there. Doctor – Okay, so you are probably suffering from food poisoning. Since the food stalls in fairs are quite unhygienic, there’s a high chance those uncovered food might have caused food poisoning. Patient – I think I will never eat from any unhygienic place in the future. Doctor – That’s good. I’m prescribing some medicines, have them for one week and come back for a checkup next week. And please try to avoid spicy and fried foods for now. Patient – Okay, doctor, thank you. Doctor – Welcome.",
      "output": "1. Prescribe a course of antibiotics and antiemetics for one week to treat the suspected food poisoning and stomach infection. \n\n 2. Advise the patient to avoid spicy and fried foods during the treatment period to prevent further irritation of the stomach. \n\n 3. Schedule a follow-up appointment in one week to reassess the patient's symptoms and recovery progress. \n\n 4. Instruct the patient to maintain hydration and monitor for any worsening of symptoms, with instructions to seek medical attention if necessary. \n\n5. Educate the patient on the risks of consuming food from unhygienic sources and reinforce the importance of food safety in preventing future infections."
    },
    {
      "input": "Patient – Good afternoon, Doctor. Doctor – Good afternoon, Mr. Bose. How are you? Patient – I’m doing good, doctor, but my daughter isn’t doing well. Everywhere, people are getting affected with COVID and I am really worried about her. Doctor – Please have a seat and tell me what happened. Patient – Last week, my daughter came back from Pune as her college was closed on account of COVID. From the second day, she has had high fever and has been coughing badly. I think that she has contracted the virus on her way home. Doctor – Okay, I understand your concern. Having a fever and cough doesn’t necessarily mean that someone has contracted the virus. These are symptoms of common cold too. The change in the temperature of the atmosphere could have triggered these symptoms. Still, to put your worries to rest, I am prescribing some medicines and an RT PCR test. Do the test by tomorrow, and if the test results are positive, make sure she is isolated. On the other hand, if the result is negative, just give her the medicine and ask her to drink a lot of water. Also, bring her in so I could examine her. Patient – Okay, doctor. I will bring her in the evening. Thank you. Doctor – You are welcome.",
      "output": "1. Prescribe symptomatic treatment including antipyretics and cough suppressants to manage the fever and cough.\n\n 2. Order an RT-PCR test to confirm or rule out COVID-19 infection; instruct the patient to complete the test by the next day. \n\n 3. If the RT-PCR test results are positive, instruct the patient to isolate and follow standard COVID-19 protocols to prevent transmission. \n\n 4. If the test results are negative, advise the patient to continue symptomatic treatment and ensure adequate hydration. \n\n 5. Schedule a follow-up visit for further examination and monitoring of the patient's condition. \n\n 5. Provide reassurance to the patient and their family, emphasizing the importance of timely testing and isolation if required."
    }
  ]
  
  prompt_template = (
    "Generate a plan in a SOAP note for this conversation between a patient and their physician. "
    "{context}\n\n"
    "Examples:\n"
  )
  # Append examples to the prompt
  for example in examples:
      prompt_template += f"Input: {example['input']}\nOutput: {example['output']}\n\n"
  
  # Define the final prompt template
  prompt = ChatPromptTemplate.from_messages([
      ("system", prompt_template + "{context}")
  ])
  
  llm = ChatOpenAI(model="gpt-4o")
  # Instantiate chain
  chain = create_stuff_documents_chain(llm, prompt)

  # Invoke chain
  result = chain.invoke({"context": processed_transcript})
  # print(result)
  return result
