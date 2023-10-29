# import pandas as pd
# import random
# import os
# import time

# # Function to generate random data and save to an Excel sheet
# def generate_and_save_sheet(sheet_name, num_pairs):
#     data = {'DocID': [], 'TermID': []}
#     for i in range(num_pairs):
#         data['DocID'].append(i)
#         data['TermID'].append(random.randint(1, 5000))
#     df = pd.DataFrame(data)
#     df.to_excel(sheet_name, index=False)

# # Function to merge and sort dataframes
# def merge_and_sort_data(dataframes):
#     merged_df = pd.concat(dataframes)
#     merged_df.sort_values(by='TermID', inplace=True)
#     merged_df.reset_index(drop=True, inplace=True)
#     return merged_df

# # Function to process CNF query
# def process_cnf_query(data_df, cnf_query):
#     results = set(data_df['DocID'])
#     for clause in cnf_query:
#         clause_results = set()
#         for term1, term2 in clause:
#             term1_docs = set(data_df[data_df['TermID'] == term1]['DocID'])
#             term2_docs = set(data_df[data_df['TermID'] == term2]['DocID'])
#             term_results = term1_docs.intersection(term2_docs)
#             clause_results = clause_results.union(term_results)
#         results = results.intersection(clause_results)
#     return list(results)

# # Main function
# def main():
#     # Create 10 blocks with 500 pairs each and save to separate sheets
#     num_blocks = 10
#     pairs_per_block = 10000000
#     dataframes = []
#     for i in range(num_blocks):
#         sheet_name = f"Block_{i+1}.xlsx"
#         generate_and_save_sheet(sheet_name, pairs_per_block)
#         dataframes.append(pd.read_excel(sheet_name))

#     # Measure the time taken to load and merge the dataframes
#     start_time = time.time()
#     merged_df = merge_and_sort_data(dataframes)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print("Time taken to merge and sort dataframes:", elapsed_time, "seconds")

#     # Define a CNF query
#     cnf_query = [
#         [(100, 200), (44,30)]  # Clause 2: (Term5 AND Term6) OR (Term7 AND Term8)
#     ]

#     # Measure the time taken to process the CNF query
#     start_time = time.time()
#     matching_docs = process_cnf_query(merged_df, cnf_query)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print("Time taken to process CNF query:", elapsed_time, "seconds")

#     # Output matching DocIDs
#     print("Matching DocIDs:", matching_docs)

# if __name__ == "__main__":
#     main()

import random
import time
import heapq
import pandas as pd

# Define the number of sheets and pairs per sheet
num_sheets = 10
pairs_per_sheet = 1000000

# Define the range for term IDs and doc IDs
term_id_range = range(1, 5001)  # 1 to 5000
doc_id_range = range(1, 10001)  # 1 to 10000

# Define the maximum batch size for CSV files
max_batch_size = 1000000  # Adjust this based on your available memory

# Function to generate random data and save to CSV files
def generate_and_save_csv(sheet_name, num_pairs):
    data = {'DocID': [], 'TermID': []}
    for _ in range(num_pairs):
        data['DocID'].append(random.choice(doc_id_range))
        data['TermID'].append(random.choice(term_id_range))
    df = pd.DataFrame(data)
    
    # Save data in compressed CSV batches
    num_batches = len(df) // max_batch_size + 1
    for i in range(num_batches):
        batch_start = i * max_batch_size
        batch_end = (i + 1) * max_batch_size
        df_batch = df[batch_start:batch_end]
        if not df_batch.empty:
            batch_file_name = f"{sheet_name}_{i + 1}.csv.gz"  # Use gzip compression
            df_batch.to_csv(batch_file_name, index=False, compression='gzip')

# Function to merge and sort dataframes
def merge_and_sort_data(dataframes):
    merged_df = pd.concat(dataframes)
    merged_df.sort_values(by='TermID', inplace=True)
    merged_df.reset_index(drop=True, inplace=True)
    return merged_df

# Function to process CNF query
def process_cnf_query(merged_df, cnf_query):
    # Initialize a set of matching DocIDs with all DocIDs
    matching_doc_ids = set(merged_df['DocID'].unique())
    
    # Process each clause in the CNF query
    for clause in cnf_query:
        clause_matches = set(matching_doc_ids)  # Initialize with all DocIDs
        
        # Process each literal in the clause
        for literal in clause:
            term_id, doc_id = literal
            doc_ids = set(merged_df[(merged_df['TermID'] == term_id) & (merged_df['DocID'] == doc_id)]['DocID'].unique())
            clause_matches.intersection_update(doc_ids)
        
        # Update the set of matching DocIDs
        matching_doc_ids.intersection_update(clause_matches)
    
    return matching_doc_ids


# Generate and save sheets
start_time = time.time()
dataframes = []
for i in range(num_sheets):
    sheet_name = f"Sheet_{i + 1}"
    generate_and_save_csv(sheet_name, pairs_per_sheet)
    sheet_dataframes = []
    for j in range(len(dataframes) + 1):
        batch_file_name = f"{sheet_name}_{j + 1}.csv.gz"
        try:
            sheet_dataframes.append(pd.read_csv(batch_file_name, compression='gzip'))
        except FileNotFoundError:
            continue
    dataframes.append(pd.concat(sheet_dataframes))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to generate and save sheets: {elapsed_time} seconds")

# Merge and sort the dataframes (Simulating BSBI)
start_time = time.time()
merged_df = merge_and_sort_data(dataframes)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to merge and sort dataframes (Simulating BSBI): {elapsed_time} seconds")

# Process a CNF query
cnf_query = [
    [(175, 270), (44, 30)],  # Clause 1: (Term175 AND Term270) OR (Term44 AND Term30)
    [(100, 200), (44, 30)]   # Clause 2: (Term100 AND Term200) OR (Term44 AND Term30)
]

matching_doc_ids = process_cnf_query(merged_df, cnf_query)

# Print the matching DocIDs
print(f"Documents satisfying the query: {matching_doc_ids}")

# Save the merged dataframe as a compressed CSV file
merged_df.to_csv("Merged_Sheet.csv.gz", index=False, compression='gzip')

