import os
import json
import pandas as pd
from unstructured.partition.pdf import partition_pdf

def extract_images_base64(chunks):
    """
    Extracts images in base64 format from CompositeElement objects in PDF chunks.

    Args:
        chunks (list): List of chunks from the partitioned PDF.

    Returns:
        list: List of base64 encoded image strings.
    """
    images_b64 = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            if hasattr(chunk.metadata, "orig_elements"):
                chunk_els = chunk.metadata.orig_elements
                for el in chunk_els:
                    if "Image" in str(type(el)):
                        if hasattr(el.metadata, "image_base64"):
                            images_b64.append(el.metadata.image_base64)
    return images_b64

def save_tables_to_excel(tables, output_dir):
    """
    Saves extracted tables to an Excel file in the specified output directory.

    Args:
        tables (list): List of table objects.
        output_dir (str): Directory to save the Excel file.

    Returns:
        str: Path to the saved Excel file.
    """
    if not tables:
        return None

    excel_path = os.path.join(output_dir, "tables.xlsx")
    try:
        with pd.ExcelWriter(excel_path) as writer:
            for i, table in enumerate(tables):
                if isinstance(table, dict) and "rows" in table:
                    df = pd.DataFrame(table["rows"])
                    df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
        return excel_path
    except Exception as e:
        raise RuntimeError(f"Error saving tables to Excel: {str(e)}")

def save_chunks_to_json(chunks, output_dir, filename="chunks.json"):
    """
    Saves extracted chunks to a JSON file.

    Args:
        chunks (list): List of extracted text chunks.
        output_dir (str): Directory to save the JSON file.
        filename (str): Name of the JSON file.

    Returns:
        str: Path to the saved JSON file.
    """
    try:
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            json.dump([chunk.to_dict() for chunk in chunks], f)
        return path
    except Exception as e:
        raise RuntimeError(f"Error saving chunks to JSON: {str(e)}")

def save_images_to_json(images_b64, output_dir, filename="images.json"):
    """
    Saves extracted images in base64 format to a JSON file.

    Args:
        images_b64 (list): List of base64 encoded image strings.
        output_dir (str): Directory to save the JSON file.
        filename (str): Name of the JSON file.

    Returns:
        str: Path to the saved JSON file.
    """
    try:
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            json.dump(images_b64, f)
        return path
    except Exception as e:
        raise RuntimeError(f"Error saving images to JSON: {str(e)}")

def process_pdf(file_path, output_dir):
    """
    Processes a PDF file by partitioning it into text, tables, and images.

    Args:
        file_path (str): Path to the PDF file.
        output_dir (str): Directory to save the processed outputs.

    Returns:
        tuple: (texts, tables, images_b64)
            - texts (list): Extracted text chunks.
            - tables (list): Extracted tables.
            - images_b64 (list): Base64 encoded image strings.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        chunks = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
        )

        # Separate text and tables
        tables, texts = [], []
        for chunk in chunks:
            if "Table" in str(type(chunk)):
                tables.append(chunk.to_dict())
            elif "CompositeElement" in str(type(chunk)):
                texts.append(chunk)

        # Extract images
        images_b64 = extract_images_base64(chunks)

        # Save data
        save_tables_to_excel(tables, output_dir)
        save_chunks_to_json(texts, output_dir)
        save_images_to_json(images_b64, output_dir)

        return texts, tables, images_b64

    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")
