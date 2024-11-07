For this project, we're tackling the problem of part-of-speech (POS) tagging, which involves assigning the correct grammatical category (e.g., noun, verb, adjective) to each word in a sentence. This task is essential in natural language processing (NLP) because understanding the grammatical structure of text is a foundational step for more complex language models. POS tagging enables systems to analyze and process text in a way that resembles human comprehension, facilitating downstream applications like machine translation, sentiment analysis, and information retrieval.
In this project, we use a Hidden Markov Model (HMM) to perform POS tagging. HMMs are popular for sequential data processing tasks like POS tagging, where the sequence of words is analyzed to predict a sequence of tags. Here, each word is an observation, and each POS tag is a hidden state. The model uses transition probabilities (the likelihood of a tag following another tag) and emission probabilities (the likelihood of a word given a tag) to compute the most probable sequence of tags for a sentence.
The project includes implementing the Viterbi algorithm, which efficiently computes the most probable tag sequence by using dynamic programming. By training the HMM on a corpus of tagged sentences, we can generalize it to predict tags for new sentences, with the goal of achieving high accuracy in automated text analysis. This model’s effectiveness hinges on its ability to generalize from the training data to accurately handle a diverse range of words and sentence structures in unseen text.


The approach for building a POS tagger using a Hidden Markov Model (HMM) involves two main phases: training and testing. The goal is to train the model on a set of tagged sentences to learn the statistical patterns of transitions between tags and associations between words and tags, and then use this model to predict tags for unseen text. Here’s a breakdown of the approach:
Training Phase:
Data Parsing: The training data is parsed to extract word-tag pairs, creating a list of all unique tags and words in the dataset.
Transition Probability Calculation: Transition probabilities represent the likelihood of moving from one POS tag to another. We calculate these probabilities based on the frequency of tag sequences in the training data, applying smoothing to handle cases of unseen tag sequences.
Emission Probability Calculation: Emission probabilities represent the likelihood of a word being assigned a specific POS tag. These probabilities are computed based on the occurrence of each word-tag pair in the dataset.
Model Storage: Both transition and emission probabilities are stored as dictionaries, allowing fast look-up during the testing phase. The final trained model is saved in a file for later use.



![WhatsApp Image 2024-11-07 at 11 13 36 AM](https://github.com/user-attachments/assets/a9450263-1909-4b30-8b04-919998955c0a)

![WhatsApp Image 2024-11-07 at 11 14 33 AM](https://github.com/user-attachments/assets/c02ffc94-b628-46b2-b693-e31563085021)


![WhatsApp Image 2024-11-07 at 11 17 19 AM](https://github.com/user-attachments/assets/d3c42e56-b1d5-4e39-9042-026c006d5ccc)

Testing Phase:
Viterbi Algorithm: The Viterbi algorithm is used to find the most probable sequence of tags for a given sentence. Starting from the first word, the algorithm uses the transition and emission probabilities to iteratively compute the likelihood of each tag sequence and selects the most probable path.
Smoothing for Unknown Words: If a word in the test sentence is not found in the training data, smoothing techniques are applied to estimate a probability for this word based on the observed tag distribution in the training set.
Evaluation: The model’s accuracy is evaluated by comparing the predicted tags to the true tags in a labeled test dataset.


Pre-processing steps:
The preprocessing stage involves reading and preparing the training data to calculate transition and emission probabilities for each tag in the training dataset.
Code for Preprocessing (train.py):
Parsing Training Data: The parse_traindata() function reads training data, separating words and tags, and prepares a list of word-tag pairs.
Data Extraction: The transition_count() and emission_count() functions calculate counts for tag transitions and tag emissions.

Model preparation - training:
This section covers creating the HMM model by calculating transition and emission probabilities from the training data. The model calculates the likelihood of tag sequences and word emissions based on training data counts.
Code for Transition and Emission Probability Calculations:
Transition Probability Calculation: transition_probability() calculates the probability of moving from one tag to another.
Emission Probability Calculation: emission_probability() calculates the probability of a word given a tag.


Model Training Log - Including Training Data Log and Graph
For model training logging:
Training Data Log: This will log transition and emission probabilities to hmmmodel.txt.
Graphical Representation: Python's matplotlib could be used to visualize model performance during training. For now, let’s log the transition and emission data.


Model Validation
Model validation involves using the Viterbi algorithm to predict POS tags on a test dataset and compare predictions with ground-truth labels.
Code for Model Validation (test.py):
Viterbi Algorithm: Used for sequence prediction based on trained transition and emission probabilities.
Accuracy Calculation: Compares predicted tags to expected tags and calculates the accuracy


