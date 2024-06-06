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
    text = re.sub(r'\bvia \/r\/\w+\b', '', text)
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
def remove_emoticons(text):
    text=re.sub(r'(?<!\S)\:(-)?[DPpOoSs]\b',' ',text)
    text=re.sub(r'(?<!\S)(>)?[:;](\')?(-)?[)(]{1,}\s*(?!\S)',' ',text)
    text=re.sub(r'(?<!\S)\;-\;\s*(?!\S)',' ',text)
    text=re.sub(r'(?<!\S)(>)?:3{1,}\b', ' ', text)
    text=re.sub(r'(?<!\S)=/\s*(?!\S)', ' ', text)
    text=re.sub(r'(?<!\S)\:/(?!\S)', ' ', text)
    text=re.sub(r'(?<!\S)[><-]_{1,}[<>-]\s*(?!\S)', ' ', text)
    text=re.sub(r'\b[OT]_{1,}[oT]\b', ' ', text)
    text=re.sub(r'(?<!\S)=[pP]\b', ' ', text)
    text=re.sub(r'\b[Xx]D\b', ' ', text)
    text=re.sub(r'(?<!\S)[<]3\b', ' ', text)
    # text=re.sub(r'(?<!\d)[:;]\){1,}(?<!\d)', ' ', text)
    return text
def convert_emoticons(text):
    # Standard boundaries
    text=re.sub(r'(?<!\S)[<]3\b', 'Heart', text)
    text=re.sub(r'(?<!\S):(-)?D\b', 'Laughing', text)
    text=re.sub(r'(?<!\S):(-)?[Pp]\b', 'cheeky', text)
    text=re.sub(r'(?<!\S)=[pP]\b', 'cheeky', text)
    text=re.sub(r'(?<!\S):[Ss]\b', 'Skeptical', text)
    text=re.sub(r'\b[Xx]D\b', 'Laughing', text)
    text=re.sub(r'(?<!\S)[>]:3{1,}\b', 'playfulness', text)
    text=re.sub(r'(?<!\S):(-)?[oO]\b', 'Surprise', text)
    text=re.sub(r'\bO_o\b', 'Surprised', text)
    text=re.sub(r'\bT_T\b', 'Annoyed', text)
    text=re.sub(r'(?<!\S):(-)?3\b', 'mischievous', text)
    # non Standard
    text=re.sub(r'(?<!\S):(-)?[)]\s*(?!\S)', 'Smiley', text)
    text=re.sub(r'(?<!\S);(-)?[)]\s*(?!\S)', 'Wink', text)
    text=re.sub(r'(?<!\S):(-)?[)]{2}\s*(?!\S)', 'Very Happy', text)
    text=re.sub(r'(?<!\S);-;\s*(?!\S)', 'Sad', text)
    text=re.sub(r'(?<!\S)\:(-)?/(?!\S)', 'Skeptical', text)
    text=re.sub(r'(?<!\S)=/\s*(?!\S)', 'Skeptical', text)
    text=re.sub(r'((?<!\S)<_<\s*(?!\S))|((?<!\S)>_>\s*(?!\S))', 'Devious', text)
    text=re.sub(r'(?<!\S)(>_<)\s*(?!\S)', 'Annoyed', text)
    text=re.sub(r'(?<!\S)>:[(]\s*(?!\S)', 'Angry', text)
    text=re.sub(r'(?<!\S):(-)?[(]\s*(?!\S)', 'Frown', text)
    text=re.sub(r'(?<!\S):\'(-)?[(]\s*(?!\S)', 'Crying', text)
    return text
def clean_slang(text):
    #abbreviations
    text=re.sub(r'\blol\b','laugh out loud',text,flags=re.I)
    text=re.sub(r'\bfyi\b','for your information',text,flags=re.I)
    text=re.sub(r'\blmao\b','laugh my ass off',text,flags=re.I)
    text=re.sub(r'\blmfao\b','laugh my fucking ass off',text,flags=re.I)
    text=re.sub(r'\bsmh\b','shake my hand',text,flags=re.I)
    text=re.sub(r'\bcya\b','see you',text,flags=re.I)
    text=re.sub(r'\bomg\b','oh my god',text,flags=re.I)
    text=re.sub(r'\bwtf\b','what the fuck',text,flags=re.I)
    text=re.sub(r'\btbh\b','to be honest',text,flags=re.I)
    text=re.sub(r'\bbrb\b','be right back',text,flags=re.I)
    text=re.sub(r'\bftw\b','for the win',text,flags=re.I)
    text=re.sub(r'\bidc\b','I don\'t care',text,flags=re.I)
    #slang terms
    text=re.sub(r'\b3p - 3\\:30a\b','3p - 3:30a',text)
    text=re.sub(r'\b2k(\d{2})\b',r'20\1',text,flags=re.I)
    text=re.sub(r'\b(\d{1,})\,(000)\b',r'\1\2',text,flags=re.I)
    text=re.sub(r'\bw/e\b','whatever',text,flags=re.I)
    text=re.sub(r'\bP/U\b','pick up',text,flags=re.I)
    text=re.sub(r'(\bb4\b)|(\bbe4\b)','before',text,flags=re.I)
    text=re.sub(r'\bthx\b','thank you',text,flags=re.I)
    text=re.sub(r'\btlk\b','talk',text,flags=re.I)
    text=re.sub(r'\bbb\b','baby',text,flags=re.I)
    text=re.sub(r'\bwidout\b','without',text,flags=re.I)
    text=re.sub(r'\s*&\s*',' and ',text)
    text=re.sub(r'(\bw/o\b)|(\bw/out\b)','without',text)
    text=re.sub(r'\bw/(?!\S)', 'with', text)
    text=re.sub(r'\bw/(\w+)',r'with \1', text)
    #misspellings
    text=re.sub(r'\bamageddon\b','armageddon',text,flags=re.I)
    text=re.sub(r'\brecentlu\b','recently',text,flags=re.I)
    text=re.sub(r'\bexp0sed\b','exposed',text,flags=re.I)
    text=re.sub(r'\bph0tos\b','photos',text,flags=re.I)
    text=re.sub(r'\btrfc\b','traffic',text,flags=re.I)
    text=re.sub(r'\blonge rGreen\b','longer Green',text)
    return text
def expand_contractions(text):
    expanded_text = contractions.fix(text)
    expanded_text=re.sub(r"(\b\w+)'s\b",r"\1",expanded_text)
    return expanded_text
def remove_punctuation(text):
    return re.sub(r'(?<!\w)[^\w\s]|[^\w\s](?!\w)', '', text)
def clean_text(text):
    text=clean_html_text(text)
    text=remove_partial_tag(text)
    text=clean_encoding_error(text)
    text=remove_urls(text)
    text=new_line(text)
    text=clean_twitter_text(text)
    text=fix_repeating_characters(text)
    text=convert_emoticons(text)
    # text=remove_emoticons(text)
    text=clean_slang(text)
    text=expand_contractions(text)
    text=remove_punctuation(text)
    return text
def manual_impute_label(df,text_col):
    df.loc[(df[text_col] == 'To fight bioterrorism sir.')&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "Mmmmmm I'm burning.... I'm burning buildings I'm building.... Oooooohhhh oooh ooh...")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "that horrible sinking feeling when you\x89Ûªve been at home on your phone for a while and you realise its been on 3G this whole time")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "In #islam saving a person is equal in reward to saving all humans! Islam is the opposite of terrorism!")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "I Pledge Allegiance To The P.O.P.E. And The Burning Buildings of Epic City. ??????")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "wowo--=== 12000 Nigerian refugees repatriated from Cameroon")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "Hellfire! We donÛªt even want to think about it or mention it so letÛªs not do anything that leads to it #islam!")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "like for the music video I want some real action shit like burning buildings and police chases not some weak ben winston shit")&df['new_target'].isna(), 'new_target'] = 0
    df.loc[(df['text'] == "RT NotExplained: The only known image of infamous hijacker D.B. Cooper. http://t.co/JlzK2HdeTG")&df['new_target'].isna(), 'new_target'] = 1
    df.loc[(df['text'] == "Caution: breathing may be hazardous to your health.")&df['new_target'].isna(), 'new_target'] = 1
    return df
def text_mislabels(df,text_col,target_col):
    df_mislabeled = df.groupby([text_col],as_index=False)[target_col].mean()
    df_mislabeled.to_csv('df_mislabeled.csv',index=False)
    new_df=df_mislabeled.reset_index()#df_mislabeled[df_mislabeled[target_col]!=0.5]
    new_df['new_target']=np.where(new_df[target_col] > 0.5, 1, np.where(new_df[target_col] < 0.5, 0, np.nan))#np.where(new_df[target_col]>0.5,1,0)
    # corrected_labels = df.groupby(text_col)[target_col].agg(lambda x: x.mode()[0] if len(x.mode()) == 1 else None).reset_index()
    # tweets_df_corrected_labels = pd.merge(df, corrected_labels, on=text_col, how='left', suffixes=('_original', '_corrected'))
    # new_df=tweets_df_corrected_labels.drop_duplicates(text_col, keep='first')
    #new_df=fill_missing(new_df,text_col,target_col) # this function will make sure the values that are missing get filled out
    #new_df=fill_missing(new_df,text_col,target_col)
    new_df=manual_impute_label(new_df,'text')
    new_df.drop(labels=['index',target_col],axis=1,inplace=True)
    return df.merge(new_df,on=text_col)