from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import DocumentForm
from .utils import find_common_words
from docx import Document # type: ignore
from PyPDF2 import PdfReader # type: ignore


def extract_text_from_file(file):
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise ValueError("Type de fichier non supporté")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def index(request):
    form = DocumentForm()
    context = {'form': form}
    return render(request, 'AlgoApp/index.html', context)

def compare_documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc1 = request.FILES['document1']
            doc2 = request.FILES['document2']
            try:
                text1 = extract_text_from_file(doc1)
                text2 = extract_text_from_file(doc2)
            except ValueError as e:
                context = {'form': form, 'error': str(e)}
                return render(request, 'AlgoApp/index.html', context)
            
            common_words, common_words_with_case, similarity_percentage, similarity_percentage_with_case = find_common_words(text1, text2)
            context = {
                'form': form,
                'similarity_percentage': similarity_percentage,
                'common_words_with_case':common_words_with_case,
                'common_words':common_words,
                'similarity_percentage_with_case':similarity_percentage_with_case,
                'doc1': text1,
                'doc2': text2
            }
            return render(request, 'AlgoApp/result.html', context)
        else:
            form = DocumentForm()
            context = {'form': form}
            return render(request, 'AlgoApp/index.html', context)
