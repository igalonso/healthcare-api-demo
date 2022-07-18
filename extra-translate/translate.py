import os


def quickstart(project_id: str, location: str, processor_id: str, file_path: str):

    from google.cloud import documentai_v1 as documentai

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)
    document = result.document

    document_pages = document.pages

    # For a full list of Document object attributes, please reference this page: https://googleapis.dev/python/documentai/latest/_modules/google/cloud/documentai_v1beta3/types/document.html#Document

    # Read the text recognition output from the processor
    print("The document contains the following paragraphs:")
    texto = ""
    for page in document_pages:
        paragraphs = page.paragraphs
        for paragraph in paragraphs:
            print(paragraph)
            paragraph_text = get_text(paragraph.layout, document)
            print(f"Paragraph text: {paragraph_text}")
            texto = texto + "" + paragraph_text
    return texto

def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../key.json"

aux_text = quickstart("healthcare-api-demo-352513","eu","ba3a253639cb48c2","URG.pdf")

print(aux_text)

translate_text("en",aux_text)



# with open('texto.txt') as f:
#     lines = f.readlines()
# count = 0
# text = ""
# for line in lines:
#     count += 1
#     text = text+" "+ line  

# f = open("output.txt", "a")
# f.write(translate_text("en",str(text)))
# f.close()
