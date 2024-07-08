import glob
import os
import asyncio
from config import open_api_key

os.environ['OPENAI_API_KEY'] = open_api_key

from llama_index.core import SimpleDirectoryReader
from llama_index.core.response_synthesizers import TreeSummarize

from TextSummarize import TextSummary

async def read_files():
    reader = SimpleDirectoryReader(input_files=[file for file in glob.glob("data/*.txt")])
    docs = reader.load_data()
    #print(docs)
    summaries = []
    for i in docs:
        text = i.text
        txts = TextSummary()
        await asyncio.gather(txts.generate_response_from_text(text))
        #await asyncio.gather(summarize(query="Can you provide summary of available books?", text=text))


async def summarize(query, text):
    summarizer = TreeSummarize(verbose=True)
    response = await summarizer.aget_response(query, [text])
    return response


print(asyncio.run(read_files()))





