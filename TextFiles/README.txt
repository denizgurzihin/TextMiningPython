Simple Text Mining Application using Python
Input: a set of documents
Your program will read a set of documents (Word or pdf or text files) from a folder
Output: several documents (text files)
Your program will output following files:
1- tf_list.csv: Most frequent 50 words in the input set of documents, sorted descending by their term frequency (tf) coupled with their tf values (comma seperated file, example: document;7)
2- tf_wordCloud.pdf: Word cloud of the these words
3- tfidf_list.csv: Most frequent 50 words in the input set of documents, sorted descending by their term frequency*inverse document frequency (tf-idf) coupled with their tf-idf values (comma seperated file, example: document;2.8)
4- tfidf_wordCloud.pdf: Word cloud of the these words
Description:
- Use your existing GitHub repositories but open a new folder called “project2” and put your python code into this directory.
- You can use any Python libraries to ease your job
- Transforming all text to lowercase may help in your calculations
- You need to filter very common words which are called stopwords before your calculations. You can use stopword list file for this purpose. However, please extend your stopword list with the common words in scientific publications such as abstract, introduction, conclusions, related work, author, university, etc, https://en.wikipedia.org/wiki/Stop_words
- Info for tf-idf calculations: https://en.wikipedia.org/wiki/Tf–idf
- You need to download the publications of a particular faculty member in our department. You will use the set of publication documents of this faculty member as your input. You can use faculty members home page or Google scholar profile. You must download as many publications of the faculty as possible. Use Google or Google scholar to search for publication names and to access pdf’s. You can download and prepare your input files manually if you like. If you automatize this process you will get +15 Extra Credit.
- No analysis or design documents are required fort his Project
- Your projects will be evaluated based on the correctness and the quality of the outputs as well as the object oriented design. Please note that we can use a different input (for example a folder of publication pdf’s) to evaluate your project

Deadline: December 26th, 2018 23:59. Please make sure that all the material is in your GitHub repo by that time.