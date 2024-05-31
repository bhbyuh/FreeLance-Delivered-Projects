from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from pydantic import BaseModel
import re

def get_llm(model_name):
    try:
        llm = Ollama(model=model_name)
        return llm

    except Exception as e:
        print(f"Error: {e}")    

'''Functio to store output in text file'''
def write_list_to_file(data_list, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n\n')

def semantic_search_rag(query, llm_chain_model):
    try:
        template =''' Apply NER on given statement and just tell only these entities location,animal,vehicle,bodypart,person,object,activity 
                      show output in form 
                      location: write entity only if presenent , if not present just write none
                      animal: write entity only if presenent , if not present just write none
                      vehicle: write entity only if presenent , if not present just write none
                      activity: write entity only if presenent , if not present just write none
                      person: write entity only if presenent , if not present just write none
                      object: write entity only if presenent , if if not present just write none
                      bodypart: write entity only if presenent , if not present just write none
                      statement is {statement} 
        '''
    
        prompt = ChatPromptTemplate.from_template(template)
        setup_and_retrieval = RunnableParallel(
            {"statement": RunnablePassthrough()}
        )
        output_parser= StrOutputParser()
        # chain = setup_and_retrieval | prompt | model | output_parser
        context=  setup_and_retrieval.invoke(query)
        prompt_answer= prompt.invoke({'statement': query})
        model_answer= llm_chain_model.invoke(prompt_answer)
        response= output_parser.invoke(model_answer)
        return response

    except Exception as e:
        raise Exception(f'Error: {e}')   
    

# Read the text data from the file
with open("Retreive_data1.txt", "r", encoding='utf-8') as file:
    lines = file.readlines()

# Store the lines in a list, removing any leading or trailing whitespace
data_list = [line.strip() for line in lines]

# # Define the regex pattern
# pattern = r'\d{1,2}\.'

# # Remove numbers along with the period from each sentence
# data_list = [re.sub(pattern, '', sentence).strip() for sentence in data_list]

# Print the list to verify the data
data_list.pop()
output_data=list()
i=0
for query in data_list:
    llm = get_llm(model_name="phi3")
    answer = semantic_search_rag(query, llm)
    output_data.append(query+'\n'+answer)
    print(i+1,'/',len(data_list),"done")
    print(answer)
    i+=1
write_list_to_file(output_data, "client_NER.txt")