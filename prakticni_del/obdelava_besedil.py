from sklearn.feature_extraction.text import CountVectorizer
import glob
import pandas as pd
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag


# tokenization and lemmatization (ločita besede )
lemmatizer= WordNetLemmatizer()


# pokupčkamo besede s podobnim korenom, pomenom skupaj
# run, runs, running -> run
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('RB'):
        return wordnet.ADV
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    else:
        return wordnet.NOUN
    
def tokenize_lematize(tekst):
    tokens = word_tokenize(tekst.lower())  # vse besede pišemo z malo začetnico
    tagged = pos_tag(tokens)
    return [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        for word, tag in tagged
        if word.isalpha()    # znebimo se ločil, st,...
    ]
    


# TfidVectorizer odstrani 'stopwords' in ustvari nenegativno matriko

filepaths = glob.glob(r'C:\Users\mokro\Desktop\diploma\dipl_data\knjige_opisi\*.txt')
# min_df=2, max_df=0.9 odstranita redke in pogoste besede, to uniči celoten rezultat
vectorizer= CountVectorizer(stop_words='english', input = 'filename', encoding='latin-1', min_df=2, max_df=0.9)


wordMatrix = vectorizer.fit_transform(filepaths) 
#print(wordMatrix)

# malo lepše, prikaz
#dense_matrix = wordMatrix.toarray()
#print(dense_matrix)

#feature_names = vectorizer.get_feature_names_out()
#df = pd.DataFrame(dense_matrix, columns=feature_names)
#print(df.head())