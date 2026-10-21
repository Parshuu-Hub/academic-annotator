import pypdf
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    full_text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {str(e)}")

    return full_text

def annotate_paper(text):
        repo_pattern = r"(github\.com|gitlab\.com|bitbucket\.org)/[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+"

        has_code_repo = bool(re.search(repo_pattern, text, re.IGNORECASE))
        data_keywords = r"(data availability|dataset available|supplementary material|reproducibility|zenodo|figshare)"
        has_data_statement = bool(re.search(data_keywords, text, re.IGNORECASE))
        ethics_keywords = r"(ethical approval|ethics committee|institutional review board|irb approval)"
        has_ethics_clearance = bool(re.search(ethics_keywords, text, re.IGNORECASE))
        rigour_score = sum([has_code_repo, has_data_statement, has_ethics_clearance])

        annotations = {
            "Has_Public_Code": has_code_repo,
            "Has_Data_Statement": has_data_statement,
            "Has_Ethics_Clearance": has_ethics_clearance,
            "Rigour_Score": rigour_score
        }
        return annotations

def process_papers_to_dataset(pdf_paths_list):
    dataset_records = []

    for path in pdf_paths_list:
        print(f"Processing and annotating: {path}...")
        try:
            raw_text = extract_text_from_pdf(path)
            annotation_labels = annotate_paper(raw_text)
            record = {
                "File_Name": path.split("/")[-1],
                **annotation_labels
            }
            dataset_records.append(record)
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
    
    df = pd.DataFrame(dataset_records)

    df.to_csv("annotated_research_dataset.csv", index=False)
    print("Dataset successfully generated and saved as 'annotated_research_dataset.csv'!")
    return df


if __name__ == "__main__":
    test_files = ["sample_papers/sample.pdf"] 
    process_papers_to_dataset(test_files)
