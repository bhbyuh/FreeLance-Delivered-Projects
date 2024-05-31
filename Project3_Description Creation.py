from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import  RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from pydantic import BaseModel

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
        template =''' Give as possible as statements similar to that context add entities like location,animal,vehicle or bodypart ,must replace entities person,location,object. Generate each sentence of max ten words {statement} 
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
with open("descriptions_excluding_person.txt", "r") as file:
    lines = file.readlines()

# Store the lines in a list, removing any leading or trailing whitespace
data_list = [line.strip() for line in lines]
print(len(data_list))
new_data=list()
i=0
for query in data_list:
    llm = get_llm(model_name="phi3")
    answer = semantic_search_rag(query, llm)
    new_data.append(answer)
    print(i+1,'done')
    i+=1
    print(answer)

write_list_to_file(new_data, "Retreive_data.txt")