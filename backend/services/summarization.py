# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Set OpenAI API Keys
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# # Ensure the API Key is available
# if not os.environ["OPENAI_API_KEY"]:
#     raise EnvironmentError("OPENAI_API_KEY is missing. Set it in the .env file.")

# # Text and Table Summarization
# def summarize_text_and_tables(texts, tables):
#     """
#     Summarizes text and tables using OpenAI's ChatGPT model.
#     """
#     prompt_text = """
#     Analyze the given input and provide a concise summary based on the following guidelines:

#     1. **Text**: If the input is text, summarize the main ideas, key points, or arguments. Focus on clarity, and avoid unnecessary details.
#     2. **Table**: If the input is a table, identify its purpose and summarize the key insights, trends, or comparisons it presents. Highlight important rows, columns, or aggregated values if applicable.

#     Respond only with the summary. Avoid prefacing the response with "Here is a summary" or similar phrases.

#     Input: {element}
#     """

#     # Initialize OpenAI's ChatGPT model
#     model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")  # Use "gpt-3.5-turbo" if "gpt-4" is unavailable
#     prompt = ChatPromptTemplate.from_template(prompt_text)

#     # Summarize text inputs
#     summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
#     text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

#     # Summarize table inputs
#     tables_html = [table.metadata.text_as_html for table in tables]
#     table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})

#     return text_summaries, table_summaries

# # Image Summarization
# def summarize_images(images):
#     """
#     Summarizes images using OpenAI's ChatGPT model.
#     """
#     prompt_template = """
#     Analyze the given image and provide a detailed description based on the following guidelines:

#     1. **General Overview**: Start with a brief description of what the image represents (e.g., diagram, graph, table, or flowchart).
#     2. **Components**: Identify and describe the key elements or components visible in the image (e.g., axes, labels, nodes, connections, shapes, etc.).
#     3. **Data Representation**:
#        - If the image is a graph, specify the type of graph (e.g., bar chart, line graph, scatter plot) and describe the data being represented.
#        - Mention the axes, their labels, and the range of values shown.
#        - Identify significant trends, peaks, or patterns visible in the data.
#     4. **Purpose and Interpretation**: Based on the visual content, describe the likely purpose of the image. For example, explain what concept, relationship, or comparison it is illustrating.
#     5. **Special Notes**: Highlight any annotations, colors, or markings that might indicate additional insights or emphasis.

#     The response should be detailed, clear, and concise, ensuring that all relevant visual information is captured effectively. Avoid vague descriptions or generalities, and provide an accurate and structured summary of the image's content.
#     """

#     # Initialize OpenAI's ChatGPT model
#     model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")  # Use "gpt-3.5-turbo" if "gpt-4" is unavailable

#     # Generate summaries for each image
#     summaries = []
#     for image in images:
#         prompt = ChatPromptTemplate.from_messages([
#             (
#                 "user",
#                 [
#                     {"type": "text", "text": prompt_template},
#                     {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}},
#                 ],
#             )
#         ])
#         chain = prompt | model | StrOutputParser()
#         summaries.append(chain.invoke({"input": ""}))

#     return summaries

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
if not os.environ["OPENAI_API_KEY"]:
    raise EnvironmentError("OPENAI_API_KEY is missing. Set it in the .env file.")

# Text and Table Summarization
def summarize_text_and_tables(texts, tables, user_id, file_id):
    """
    Summarizes text and tables using OpenAI's ChatGPT model.
    Includes user_id and file_id in metadata for integration with vector store.
    """
    prompt_text = """
    Analyze the given input and provide a concise summary based on the following guidelines:

    1. **Text**: Summarize the main ideas, key points, or arguments. Focus on clarity, and avoid unnecessary details.
    2. **Table**: Identify its purpose and summarize key insights, trends, or comparisons. Highlight important rows, columns, or aggregated values if applicable.

    Respond only with the summary.

    Input: {element}
    """

    # Initialize OpenAI's ChatGPT model
    model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template(prompt_text)

    try:
        # Summarize text
        summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
        text_summaries = summarize_chain.batch(texts, {"max_concurrency": 3})

        # Summarize tables
        tables_html = [table.metadata.text_as_html for table in tables]
        table_summaries = summarize_chain.batch(tables_html, {"max_concurrency": 3})

        # Append metadata
        text_summaries_with_metadata = [
            {"content": summary, "metadata": {"user_id": user_id, "file_id": file_id}}
            for summary in text_summaries
        ]
        table_summaries_with_metadata = [
            {"content": summary, "metadata": {"user_id": user_id, "file_id": file_id}}
            for summary in table_summaries
        ]

        return text_summaries_with_metadata, table_summaries_with_metadata

    except Exception as e:
        raise RuntimeError(f"Error summarizing text or tables: {str(e)}")

# Image Summarization
def summarize_images(images, user_id, file_id):
    """
    Summarizes images using OpenAI's ChatGPT model.
    Includes user_id and file_id in metadata for integration with vector store.
    """
    prompt_template = """Analyze the given image and provide a detailed description based on the following guidelines:

1. **General Overview**: Start with a brief description of what the image represents (e.g., diagram, graph, table, or flowchart).
2. **Components**: Identify and describe key elements (e.g., axes, labels, nodes, connections, shapes, etc.).
3. **Data Representation**:
   - Specify the type of visualization (e.g., bar chart, line graph).
   - Mention axes, labels, and significant trends.
4. **Purpose and Interpretation**: Describe the likely purpose of the image and its context.
5. **Special Notes**: Highlight annotations or markings that indicate insights.

The response should be detailed, clear, and concise.
"""

    # Initialize OpenAI's ChatGPT model
    model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

    summaries = []
    for image in images:
        try:
            prompt = ChatPromptTemplate.from_messages([
                (
                    "user",
                    [
                        {"type": "text", "text": prompt_template},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}},
                    ],
                )
            ])
            chain = prompt | model | StrOutputParser()
            summary = chain.invoke({"input": ""})
            summaries.append({"content": summary, "metadata": {"user_id": user_id, "file_id": file_id}})
        except Exception as e:
            raise RuntimeError(f"Error summarizing image: {str(e)}")

    return summaries
