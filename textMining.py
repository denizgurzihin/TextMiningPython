import os
from os import path
import re
import mammoth
import PyPDF2
import string
from nltk.corpus import stopwords
import math
import csv

from wordcloud import WordCloud
import matplotlib.pyplot as plt


# read files from path and clean them
def read_and_clean_file(file_name, destination_path, stop_words):
    text = []

    if file_name.endswith(".txt"):
        with open(path.join(destination_path, file_name), 'r') as text_file:
            # iterate through raw list and use regex to clean non-alphanumeric symbols
            raw_line = text_file.readline()
            while raw_line:
                clean_line = re.sub("[^a-zA-Z_şŞğĞüÜİöÖçÇı]", " ", raw_line).split()
                text += clean_line
                raw_line = text_file.readline()

    elif file_name.endswith(".docx"):
        with open(path.join(destination_path, file_name), 'rb') as docx_file:
            # use mammoth package to convert docx to text
            raw_content = [mammoth.extract_raw_text(docx_file).value]
            # use regex to to clean non-alphanumeric symbols
            clean_content = re.sub("[^a-zA-Z_şŞğĞüÜİöÖçÇı]", " ", raw_content[0]).split()
            text += clean_content

    elif file_name.endswith(".pdf"):
        with open(path.join(destination_path, file_name), 'rb') as pdf_file:
            # use PyPDF2 package to convert pdf to text
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            # iterate through pages and use regex to clean non-alphanumeric symbols
            for page in range(0, pdf_reader.numPages):
                raw_content = [pdf_reader.getPage(page).extractText()]
                clean_content = re.sub("[^a-zA-Z_şŞğĞüÜİöÖçÇı]", " ", raw_content[0]).split()
                text += clean_content

    # convert letters to lower forms
    text = [letter.lower() for letter in text]
    # generate stop words list
    stop_words_list = set(stopwords.words('english'))
    for stop_word in stop_words:
        stop_words_list.add(stop_word)
    # clean stop words and punctuations
    keywords = [word for word in text if word not in stop_words_list and word not in string.punctuation]

    return keywords

# tf - idf calculation functions (from TextBlob package)
def tf(word, blob):
    return blob.count(word) / len(blob)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)


def idf(word, bloblist):
    return math.log(len(bloblist) / (n_containing(word, bloblist)))


def tfidf(word, blob, bloblist):
    return tf(word, blob)*idf(word, bloblist)


# printing word cloud to pdf file
def generate_wordcloud(word_list):
    # Create a list of word
    text = ("")
    cnt = 0
    while cnt < len(word_list):
        temp = word_list[cnt].split(";")
        text = text + temp[0]+" "
        cnt += 1

    # Create the wordcloud object
    wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)

    # retrieve the name of word_list from global dictionary
    for (key, value) in globals().items():
        if type(value) == list and value == word_list:
            file_name = key

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.savefig(file_name + '.pdf')


# printing output to excel file
def generate_csv_file(word_list):
    # retrieve the name of word_list from global dictionary
    for (key, value) in globals().items():
        if type(value) == list and value == word_list:
            file_name = key

    with open(file_name + '.csv', mode='w') as fileobj:
        temp_writer = csv.writer(fileobj, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        temp_writer.writerow(" ")
        counter = 0
        while counter < len(word_list):
            temp_writer.writerow([word_list[counter]])
            counter += 1


############
### MAIN ###
############
additional_stop_words = ["university", "author", "work", "related", "conclusions", "introduction", "abstract"]
current_directory = path.dirname(__file__)
target_dir = os.path.join(current_directory, "textFiles")

merged_documents = []
keywords_with_info = {}
all_documents = []
for file in os.listdir(target_dir):
    key_list = read_and_clean_file(file, target_dir, additional_stop_words)
    # build dictinary like {(word1,count1):document1, (word2,count2):document2 ...}
    keywords_with_info.update({(key_list.count(word), word): file for word in key_list})
    all_documents.append(key_list)

# sort dictionary and get first 50 item
sorted_keywords_with_info = sorted(keywords_with_info, reverse=True)
top_fifty = {sorted_keywords_with_info.__getitem__(i) for i in range(0, 50)}

# convert dictionary to regular list for sorted output
tf_list = []
tfidf_list = []
for (count, word) in top_fifty:
    document = keywords_with_info.get((count, word))
    new_keywords = read_and_clean_file(document, target_dir, additional_stop_words)
    tf_list += ["%s;%f" % (word, tf(word, new_keywords))]
    tfidf_list += ["%s;%f" % (word, tfidf(word, new_keywords, all_documents))]
# sort lists based on their frequency. in order to retrieve frequencies use regex as key
tf_list.sort(key=lambda e: re.sub('[^0-9.]', "", e), reverse=True)
tfidf_list.sort(key=lambda e: re.sub('[^0-9.]', "", e), reverse=True)

# generate csv and word cloud files
generate_csv_file(tf_list)
generate_csv_file(tfidf_list)
generate_wordcloud(tf_list)
generate_wordcloud(tfidf_list)

