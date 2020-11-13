from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pybtex.database.input import bibtex
from django.conf import settings
import pandas as pd
import string
import os


def collectImages(file_name):
    myDataFrame = pd.read_csv(file_name)
    myDataFrame.drop(myDataFrame.columns[myDataFrame.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    print(myDataFrame.head(5))


def parseToCsv(bib_data):
    bib_data.entries.keys()
    df = pd.DataFrame()
    author_dict = {}
    id_ls = []
    abstract = {}
    booktitle = {}
    title = {}
    year = {}
    volume = {}
    number = {}
    pages = {}
    keywords = {}
    doi = {}
    issn = {}
    author1 = {}
    months = {}

    for id in bib_data.entries:
        id_ls.append(id)
        abstract[id] = bib_data.entries[id].fields['abstract']

        try:
            booktitle[id] = bib_data.entries[id].fields['booktitle']
        except KeyError:
            booktitle[id] = 'none'

        title[id] = bib_data.entries[id].fields['title']

        year[id] = bib_data.entries[id].fields['year']

        try:
            months[id] = bib_data.entries[id].fields['month']
        except KeyError:
            months[id] = 'none'

        try:
            volume[id] = bib_data.entries[id].fields['volume']
        except KeyError:
            volume[id] = 'none'

        try:
            number[id] = bib_data.entries[id].fields['number']
        except KeyError:
            number[id] = 'none'

        try:
            pages[id] = bib_data.entries[id].fields['pages']
        except KeyError:
            pages[id] = 'none'

        try:
            keywords[id] = bib_data.entries[id].fields['keywords']
        except KeyError:
            keywords[id] = 'none'

        try:
            doi[id] = bib_data.entries[id].fields['doi']
        except KeyError:
            doi[id] = 'none'

        try:
            issn[id] = bib_data.entries[id].fields['ISSN']
        except KeyError:
            issn[id] = 'none'

        authors = ""
        translator = str.maketrans('', '', string.punctuation)
        for author in bib_data.entries[id].persons["author"]:
            new_author = str(author.first_names) + " " + str(author.last_names)
            new_author = new_author.translate(translator)
            if len(authors) == 0:
                authors = "" + new_author
            else:
                authors = authors + ", " + new_author
        author_dict[id] = authors

    df['id'] = id_ls
    df['author'] = df['id'].map(author_dict)
    df['abstract'] = df['id'].map(abstract)
    df['booktitle'] = df['id'].map(booktitle)
    df['title'] = df['id'].map(title)
    df['year'] = df['id'].map(year)
    df['volume'] = df['id'].map(volume)
    df['number'] = df['id'].map(number)
    df['pages'] = df['id'].map(pages)
    df['keywords'] = df['id'].map(keywords)
    df['doi'] = df['id'].map(doi)
    df['ISSN'] = df['id'].map(issn)
    df['months'] = df['id'].map(months)
    file_name = os.path.join(settings.MEDIA_ROOT, 'output.csv')
    df.to_csv(file_name)
    collectImages(file_name)


def readUploadedFile(uploaded_file):
    myVar = uploaded_file.read()
    parser = bibtex.Parser()
    bib_data = parser.parse_bytes(myVar)
    parseToCsv(bib_data)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document', False)
        if(uploaded_file != False):
            print(uploaded_file.name)
            print(uploaded_file.size)
            readUploadedFile(uploaded_file)
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def homeView(request):
    return render(request, 'home.html', {})
