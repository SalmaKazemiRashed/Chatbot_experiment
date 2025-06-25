from langchain import PromptTemplate, LLMChain
from langchain_community.llms import HuggingFacePipeline
#from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from .config import Config

pipe = pipeline("text2text-generation", model=Config.HUGGINGFACE_MODEL)

llm = HuggingFacePipeline(pipeline=pipe)

template = """protein knowledge assistant.
Relevant protein knowledge:
{context}

User question:
{question}

Answer:"""

prompt = PromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

def generate_response(question, context):
    return chain.run(question=question, context=context)
