import pandas as pd
from datasets import load_dataset

# Load your dataset from the Hugging Face hub or local file
# For example, using a dataset from the Hugging Face hub
dataset = load_dataset("squad")

# Convert the dataset to a pandas DataFrame
df = dataset['train'].to_pandas()

# Assuming the dataset has columns 'id', 'question', and 'answers' (with 'answers' being a dictionary)
# We need to format 'answers' to extract the 'text' part
df['Answer'] = df['answers'].apply(lambda x: x['text'][0] if len(x['text']) > 0 else "")

# Select and rename the necessary columns
formatted_df = df[['id', 'question', 'Answer']]
formatted_df.columns = ['Id', 'Question', 'Answer']

# Save the DataFrame to an Excel file
output_file_path = "/home/user/code/test/data/formatted_dataset.xlsx"
formatted_df.to_excel(output_file_path, index=False)

print(f"Dataset has been saved to {output_file_path}")