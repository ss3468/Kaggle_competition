from bs4 import BeautifulSoup
import html
import re
import contractions
from dateutil import parser
import pandas as pd
import numpy as np
def clean_html_text(text):
    decoded_text = html.unescape(text)
    cleaned_text = BeautifulSoup(decoded_text, 'html.parser').get_text(strip=True)
    return cleaned_text
def remove_partial_tag(text):
    pattern = re.compile(r'<\w+\b[^>]*href\s*=\s*[^>]*\.\.\.')
    fixed_html = re.sub(pattern, '', text)
    return fixed_html
def clean_encoding_error(text):
    text = re.sub(r"China\x89Ûªs", "China's", text)
    text = re.sub(r"let\x89Ûªs", "let's", text)
    text = re.sub(r"JapÌ_n", "Japan", text)    
    text = re.sub(r"Ì©", "e", text)
    text = re.sub(r"SuruÌ¤", "Suruc", text)
    text = re.sub(r"å£3million", "3 million", text)
    text = re.sub(r"don\x89Ûªt", "do not", text)
    text = re.sub(r"I\x89Ûªm", "I am", text)
    text = re.sub(r"you\x89Ûªve", "you have", text)
    text = re.sub(r"it\x89Ûªs", "it is", text)
    text = re.sub(r"doesn\x89Ûªt", "does not", text)
    text = re.sub(r"It\x89Ûªs", "It is", text)
    text = re.sub(r"Here\x89Ûªs", "Here is", text)
    text = re.sub(r"I\x89Ûªve", "I have", text)
    text = re.sub(r"can\x89Ûªt", "cannot", text)
    text = re.sub(r"wouldn\x89Ûªt", "would not", text)
    text = re.sub(r"That\x89Ûªs", "That is", text)
    text = re.sub(r"You\x89Ûªre", "You are", text)
    text = re.sub(r"Don\x89Ûªt", "Do not", text)
    text = re.sub(r"Can\x89Ûªt", "Cannot", text)
    text = re.sub(r"you\x89Ûªll", "you will", text)
    text = re.sub(r"I\x89Ûªd", "I would", text)
    text = re.sub(r"\bdonå«t\b", "do not", text)
    text = re.sub(r"\bmÌ¼sica\b", "music", text)
    text= re.sub(r"(\bvÌ_a\b)|(\bvi\x89Û\b)","via",text)
    text=re.sub(r"\bvÌ_deo\b","video",text)
    text=re.sub(r"\bAustralia\x89Ûªs\b","Australia's",text)
    text=re.sub(r"\b(\w+)(åê){1,}(\w+)(åê){1,}(\w+)\b",r"\1 \3 \5",text,flags=re.I)
    text=re.sub(r"\b(\w+)(åê){1,}(\w+)\b",r"\1 \3",text,flags=re.I)
    text=re.sub(r"\b(\w+)(åê){1,}(\#)(\w+)\b",r"\1 \3\4",text,flags=re.I)
    text=re.sub(r"\b(\w+)(åê){1,}(\()\b",r"\1 \3",text,flags=re.I)
    text=re.sub(r'[^\x00-\x7F]+', '', text)
    return text
def remove_urls(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')  # Regex pattern for matching URLs

    # Replace URLs with an empty string
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = re.sub(r"pic.twitter.com\S+",'', cleaned_text)
    return cleaned_text
def new_line(text):
    text = re.sub(r'\t', ' ', text) # remove tabs
    text = re.sub(r'\n', ' ', text) # remove line jump
    return text
def clean_twitter_text(text):
    text = re.sub(r'(\bRT(\s)?@\w+(\:)?)|(\bRT\s\'@\w+(\:)?)', '', text)
    text = re.sub(r"\bRT\b", "Retweet", text)
    text = re.sub(r'\bMT(\s)?@\w+:?', '', text)
    text = re.sub(r'\bDT(\s)?@\w+(\:)?', '', text)
    text = re.sub(r'\b[Vv]ia @{1,}\w+\b', '', text)
    text = re.sub(r"@(\d{1,2}:\d{2}(:\d{2})?\s*(?:AM|PM)?)",r"@ \1",text)
    text = re.sub(r"(\.)?@{1,}(\')?\w+(\:)?",'',text)
    text = re.sub(r"\bview and download video\b",' ',text,flags=re.I)
    text = re.sub(r'(\w+)#(\w+)', r'\1 \2', text)
    text = re.sub(r'#{1,}(\w+)', r'\1', text)
    text= re.sub(r'-\sFull(?:\sread(\s)?_|\sread\sby_|\sre_|\s*rea(>)?_)\b',' ',text)
    return text
def fix_repeating_characters(text):
    repeating_pattern = r'([^\d])\1{2,}'
    # Use re.sub to replace repeated characters with only two occurrences
    fixed_text = re.sub(repeating_pattern, r'\1\1', text,flags=re.I)
    tem=pd.read_csv('data_syntax\\repeating_character.csv')
    for index, row in tem.iterrows():
        if(row['flag']=='Y'):
            logic_text=r'\b'+row['regex_logic']+r'\b'
            fixed_text=re.sub(logic_text,row['word'],fixed_text,flags=re.I)
        else:
            logic_text=r'\b'+row['regex_logic']+r'\b'
            fixed_text=re.sub(logic_text,row['word'],fixed_text)
    return fixed_text
def clean_text(text):
    text=clean_html_text(text)
    text=remove_partial_tag(text)
    text=clean_encoding_error(text)
    text=remove_urls(text)
    text=new_line(text)
    text=clean_twitter_text(text)
    text=fix_repeating_characters(text)
    return text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def fill_missing(df,text_col,target_col):
    for index, row in df.iterrows():
        if pd.isnull(row['new_target']):
            if row[target_col] == 0.5:
                # Grouping based on 'target_p'
                grouped = df.groupby(target_col)[text_col].apply(list)
                # Create TF-IDF vectorizer
                tfidf_vectorizer = TfidfVectorizer()
                # Fit and transform text data
                tfidf_matrix = tfidf_vectorizer.fit_transform(grouped[0] + grouped[1] + [row[text_col]])
                # Calculate similarity with both groups
                sim_group0 = max(cosine_similarity(tfidf_matrix[:len(grouped[0])], tfidf_matrix[-1]))
                sim_group1 = max(cosine_similarity(tfidf_matrix[len(grouped[0]):-1], tfidf_matrix[-1]))
                print(sim_group0, sim_group1)
                print(row[text_col])
                # Fill with the target group with higher similarity
                df.at[index, 'new_target'] = 0 if sim_group0 > sim_group1 else 1
    return df
def text_deduplication(df,text_col,target_col):
    df_mislabeled = df.groupby([text_col],as_index=False)[target_col].mean()
    new_df=df_mislabeled#df_mislabeled[df_mislabeled[target_col]!=0.5]
    new_df['new_target']=np.where(new_df[target_col] > 0.5, 1, np.where(new_df[target_col] < 0.5, 0, np.nan))#np.where(new_df[target_col]>0.5,1,0)
    # corrected_labels = df.groupby(text_col)[target_col].agg(lambda x: x.mode()[0] if len(x.mode()) == 1 else None).reset_index()
    # tweets_df_corrected_labels = pd.merge(df, corrected_labels, on=text_col, how='left', suffixes=('_original', '_corrected'))
    # new_df=tweets_df_corrected_labels.drop_duplicates(text_col, keep='first')
    new_df=fill_missing(new_df,text_col,target_col) # this function will make sure the values that are missing get filled out
    return new_df