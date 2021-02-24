from transformers import pipeline
'''
# Allocate a pipeline for sentiment-analysis
classifier = pipeline('sentiment-analysis')
result = classifier('To Bogeys darkling crypt')
print(result)

index = result[0]
dict = index
score = dict['score']
print(score)
result = dict['label']
print(result)
'''

from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2')
set_seed(42)
b = generator("It isnt said the Caterpillar"
 , max_length=200, num_return_sequences=1)

print(b)