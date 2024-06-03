# 2024-1 SNU GSDS BKMS1 FINAL PROJECT

## Abstract
Paper-hub 
with Python, Flask, HTML, JS, Postgresql, TimescaleDB

<div align="center">
<img src=examples/dashboard.png width="640" height="400"/> <br> <br>
<div align="center">bkms1 - **Sangwon Lee**</div>
</div>

## Instruction
<!-- prettier-ignore -->
PaperHub project is a paper-sharing site using vector db. Using the Hugging Face's open-source embedding model, keywords are removed from the user's paper, embedded as a vector to be used for search, and stored in the DB. Using similarity search, it is possible not only to recommend the latest paper according to the user's interests, but also to process all natural language questions of the user.

## Powered by HuggingFace Open embedding Model
>> https://huggingface.co/blog/mteb 
>>  * In use : Sentence-Transformers - https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2
>>  * We tried : openai - https://openai.com/index/new-embedding-models-and-api-updates/   
>> &emsp;&emsp;&emsp;&emsp; : nvidia - https://huggingface.co/nvidia/NV-Embed-v1  "ranks No.1 now!"

## Natural language Question
<div align="center">
<img src='examples/find paper with nl question.png' width="640" height="400"/> <br> <br>
</div>
<div align="center">
<img src='examples/nlq result.png' width="640" height="400"/> <br> <br>
</div>
