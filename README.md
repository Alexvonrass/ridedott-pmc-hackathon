## This repository contains the PMC hackathon submission from the ridedott team **

## Use case description

We're aiming to solve the use case presented in the operations track of the hackathon
The use case is related to the communication between the patient (or their parents) and the doctor or nurse at the PM

We aim to provide real-time translation between the two parties, and to provide a RAG automatic response to the 
patient's question. The hope is that this response will free up valuable time for the doctor. We use weaviate to take
care of the retrieval part

According to the PMC staff, this use case can be further broken down into two cases:
1. This communication is remote (like a voice message, or a video message)
2. The communication is in person, with both parties present in a room. This needs to support continous
conversation, ie be aware of the previous sentences as the context

## Solution description

1. The folder "cloud functions" has the code for the cloud function that handles the remote case
2. The folder "dashapp" has the MVP for the UI to solve the in-person use case
3. "Notebooks" has the parsing scripts to get the instructions from the PMC that we use to populate the vector database
4. The same folder has the script to populate this database that is then used for RAG

## How to run the code

`poetry install` should set up the environment
`python ridedott_pmc_hackathon/dashapp/app.py` to start up the dash app, which can then be accessed 
at `http://127.0.0.1:8050/`
You can use 'record audio' and 'upload audio' to test the app
You will need to add a folder "sa" and a "sa.json" containing the service account secret to run the code

The cloud function is deployed manually and the code can be seen at 
`https://console.cloud.google.com/functions/details/europe-west1/test-function?env=gen1&authuser=0&project=qwiklabs-gcp-02-08a8c713b151&tab=source`
