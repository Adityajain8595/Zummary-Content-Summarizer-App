from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from gtts import gTTS
import base64
import re

#Defining max tokens
MAX_TOKENS = 6000

def chunk_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    return split_docs

def summarize_chain(docs, llm):
    total_text = " ".join(doc.page_content for doc in docs)
    total_tokens = len(total_text) // 4       # Taking rough estimate: 1 token ≈ 4 characters for English

    # Use 'stuff' for summarization if under token limit else switch to 'map-reduce'
    if total_tokens < MAX_TOKENS:
        # Prompt setup
        template = ('''Please provide a concise and detailed summary of the following content.
                    Understand the type and message of the text provided.
                    Add suitable bold big title followed by an introduction from newline.  
                    Keep section-wise brief pointers (mentioning topics or highlights).
                    End with a fitting conclusion.
                    Text: {text}''')

        prompt = PromptTemplate(input_variables=['text'], template=template)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="text"
        )
        output = chain.run(docs)
        return str(output)
    else:
        chunked_docs = chunk_documents(docs)

        initial_template = ("You are an assistant for text summarization tasks. "
                    "Write a concise and short summary of the provided text. \n"
                    "{text}"
                )

        map_prompt = PromptTemplate(input_variables=['text'], template=initial_template)
        map_chain = LLMChain(llm=llm, prompt=map_prompt)

        final_template = '''Provide the final summary of the entire text with these important points.
                        Add a suitable title. Start the precise summary with an introduction, state key notes in pointers and 
                        end with conclusion.
                        The provided text: {text}
                    '''
        combine_prompt = PromptTemplate(input_variables=['text'], template=final_template)
        combine_chain = LLMChain(llm=llm, prompt=combine_prompt)
        
        chain = MapReduceDocumentsChain(
            llm_chain=map_chain,
            reduce_documents_chain=StuffDocumentsChain(
                llm_chain=combine_chain,
                document_variable_name="text"
            ),
            document_variable_name="text"
        )
        output = chain.run(chunked_docs)
        return str(output)
    
def generate_audio(summary_text, lang="en"):

    #Formatting text for better audio
    text = re.sub(r'[#*_>`\-]', '', summary_text)       # Simplifying formatting of markdown text
    text = re.sub(r'(?<=[^\.\!\?])\n', '. ', text)      # Add periods if line ends without one
    text = re.sub(r'\n+', ' ', text)                    # Flatten newlines
    text = re.sub(r'\s{2,}', ' ', text)                 # Remove extra spaces

    
    tts = gTTS(text, lang=lang)
    tts.save("summary_audio.mp3")
    with open("summary_audio.mp3", "rb") as f:
        audio_bytes = f.read()

    b64 = base64.b64encode(audio_bytes).decode()
    return audio_bytes, b64
    



    

