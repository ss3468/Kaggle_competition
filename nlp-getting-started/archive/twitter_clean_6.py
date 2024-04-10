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
    #text = re.sub(r"fromåÊwounds", "from wounds", text)
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
    text = re.sub(r'\bMT(\s)?@\w+:?', '', text)
    text = re.sub(r'\bDT(\s)?@\w+(\:)?', '', text)
    text = re.sub(r'\b[Vv]ia @{1,}\w+\b', '', text)
    text = re.sub(r"@(\d{1,2}:\d{2}(:\d{2})?\s*(?:AM|PM)?)",r"@ \1",text)
    text = re.sub(r"(\.)?@{1,}(\')?\w+(\:)?",'',text)
    text = re.sub(r"\bview and download video\b",' ',text,flags=re.I)
    text = re.sub(r'(\w+)#(\w+)', r'\1 \2', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'\bvia\s*/r/[^\s]+', '', text)
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
emoticons=['((\>)?(?<![a-zA-Z0-9])(:3{1,}))','((\>)?[\:\;]([DdPp]|(\()|(\){1,})))','([\;\:]\-([\;\(OoDd]|(\){1,})))','(\<3)','(\>\_[\<\>])','(\-(\_{1,})\-)','[OT]_[oT]','(\:\'\()','(\=\/)','(\-\.\-)']
def remove_emoticons(text):
    tem=text.split(' ')
    emoticon_pattern = re.compile(r''+'|'.join(emoticons))
    new_list=[re.sub(emoticon_pattern, '', word) for word in tem]
    return ' '.join(new_list)
def clean_slang(text):
    # units of measure
    text = re.sub(r"\b(\d{1,})(\s+)?km\b",r"\1 kilometers",text,flags=re.I)
    text = re.sub(r"\b(\d{1,})inch\b",r"\1 inch",text,flags=re.I)
    text = re.sub(r"\b(\d{1,})(\s+)?yr(s)?\b", r"\1 year\3", text,flags=re.I)
    text = re.sub(r"\b(\d{1,})year(s)?\b", r"\1 year\2", text,flags=re.I)
    text = re.sub(r"\b(\d{1,})k\b", r"\1,000", text,flags=re.I)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)
     #spelling
    text = re.sub(r"\blil\b",' little ',text,flags=re.I)
    text = re.sub(r"\balil\b",' a little ',text,flags=re.I)
    text = re.sub(r"\bbb\b",'baby',text)
    text = re.sub(r"\bgon\b",'gonna',text)
    text = re.sub(r"\bryt\b",'right',text)
    text = re.sub(r"\bbstrd\b",'bastard',text)
    text = re.sub(r"\btakig\b",'taking',text)
    text = re.sub(r"\bfavourite\b",'favorite',text,flags=re.I)
    # date adjustments
    text=re.sub(r'\b69 august 1945\b','08/06/1945 and 08/09/1945',text)
    text=re.sub(r'\b27 Jan 2007he\b','27 Jan 2007 he',text)
    text=re.sub(r"\bAug 3 1915(\w+)\b",r"Aug 3 1915 \1",text)
    text=re.sub(r"\bAug 3-7\b","08/03-08/07",text)
    text=re.sub(r"\bWED.AUG.5TH\b","08/05",text)
    #slang terms, typos, and informal abbreviations
    text = re.sub(r'2k(\d{2})',r'20\1',text,flags=re.I)
    text=re.sub(r"(?<!\S)u(?!\S)","you",text,flags=re.I)
    text = re.sub(r"(\b[bB]4\b)|(\b[bB]e4\b)", "before", text)
    text = re.sub(r"\bb4federal\b", "before federal", text)
    text = re.sub(r"\bs2g\b", "swear to god", text)
    text = re.sub(r"\bS3XLEAK\b", "sex leak", text)
    text = re.sub(r'\bu2\b','you too',text,flags=re.I)
    text = re.sub(r"exp0sed", "exposed", text)
    text = re.sub(r"Ph0tos", "Photos", text)
    text = re.sub(r"\bthx\b", "thanks", text,flags=re.I)
    text = re.sub(r"\bP/U\b", "pick up", text)
    text = re.sub(r'(\bw/o\b)|(\bw/out\b)',"without",text,flags=re.I)
    text = re.sub(r'\bw/e\b',"whatever",text,flags=re.I)
    text = re.sub(r'\bw/(\s+)?((\w+\b)|([.,;!?])|$)',r'with \2',text,flags=re.I)
    text = re.sub(r"\bc/o\b", "care of", text)
    text = re.sub(r"(\bb/c\b)|(bcs)|(\bbc\b)|(\bcuz\b)|(\bbcuz\b)", "because", text)
    text = re.sub(r"\bRT\b", "Retweet", text)
    text = re.sub(r"\bH20\b", "water", text)
    text = re.sub(r"\bppl\b", "people", text,flags=re.I)
    text = re.sub(r"\bFVCK\b", "FUCK", text)
    text=re.sub(r"kidnap\'g","kidnapping",text)
    text=re.sub(r"(\w+)(\s+)?&(\s+)?(\w+)",r"\1 and \4",text,flags=re.I)
    text=re.sub(r"\bgov(')?t\b","government",text,flags=re.I)
    text=re.sub(r"(\bINTL\.)|(\bINTL\b)","International",text,flags=re.I)
    text=re.sub(r"(\$\d{1,})Mln\b",r"\1 million",text,flags=re.I)
    # acronymns
    text = re.sub(r"\bPOTUS\b", "President of the United States", text)
    text=re.sub(r"\blol\b","laugh out loud",text,flags=re.I)
    text=re.sub(r'\bfyi\b','for your information',text,flags=re.I)
    text=re.sub(r'\bbrb\b','Be Right Back',text,flags=re.I)
    text=re.sub(r'\blmao\b','laugh my ass off',text,flags=re.I)
    text=re.sub(r'\bcya\b',"see you",text)
    text=re.sub(r'\bwtf\b','what the fuck',text,flags=re.I)
    text=re.sub(r'\blmfao\b','laugh my fucking ass off',text,flags=re.I)
    text=re.sub(r'\bomg\b','Oh My God',text,flags=re.I)
    text=re.sub(r'\bomfg\b','Oh My Fucking God',text,flags=re.I)
    text=re.sub(r'\bbae\b','before anyone else',text,flags=re.I)
    text=re.sub(r'\bICYMI\b','In case you missed it',text,flags=re.I)
    text=re.sub(r'\bidk\b',"I don't know",text,flags=re.I)
    text=re.sub(r'\bidm\b',"I don't mind",text,flags=re.I)
    text=re.sub(r'\bbtw\b',"by the way",text,flags=re.I)
    text=re.sub(r'\basap\b',"As Soon As Possible",text,flags=re.I)
    text=re.sub(r'\btbh\b',"to be honest",text,flags=re.I)
    text=re.sub(r'\bbbc\b',"British Broadcasting Corporation",text,flags=re.I)
    text=re.sub(r'\b[Ss]mh\b',"Shake my hand",text)
    # location
    text=re.sub(r'\bU\.S(\.)?', 'United States',text,flags=re.I)
    text=re.sub(r'\bUSA\b', 'United States of America',text)
    text=re.sub(r'\bNYC\b', 'New York City',text)
    text = re.sub(r"\bcalif\b", "California", text)
    text=re.sub(r"\bnm\b","New Mexico",text)
    text = re.sub(r"\bokwx\b", "Oklahoma City Weather", text)
    text = re.sub(r"\barwx\b", "Arkansas Weather", text)    
    text = re.sub(r"\bgawx\b", "Georgia Weather", text)  
    text = re.sub(r"\bscwx\b", "South Carolina Weather", text)  
    text = re.sub(r"\bcawx\b", "California Weather", text)
    text = re.sub(r"\btnwx\b", "Tennessee Weather", text)
    text = re.sub(r"\bazwx\b", "Arizona Weather", text)  
    text = re.sub(r"\balwx\b", "Alabama Weather", text)
    #organizations
    text=re.sub(r'\bFB\b', 'Facebook',text)
    text=re.sub(r'\bIG\b', 'Instagram',text)
    return text
def replace_and_format_dates(input_text, date_patterns, output_date_format):
    original_format=[]
    formatted_dates = []

    # Iterate through each date pattern in the list
    for pattern in date_patterns:
        # Use regular expression to find date patterns
        date_matches = re.findall(pattern, input_text)
        
        # Parse dates in the found patterns and format them
        original_format.extend([date for date in date_matches])
        formatted_dates.extend([parser.parse(date, fuzzy=True).strftime(output_date_format) for date in date_matches])
    # Replace original date formats with formatted dates in the input text
    for original_date, formatted_date in zip(original_format, formatted_dates):
        input_text = input_text.replace(original_date, formatted_date)

    return input_text
def convert_dates(input_text):
    date_patterns_mdy = [
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+of\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+\d{4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\-\d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\.\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}\b'
    ]
    date_patterns_md = [
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\b',
        r'\b(?:JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s+\d{1,2}(?:st|nd|rd|th)?\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th)?\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sept|oct|nov|dec)\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\.\s+\d{1,2}(?:st|nd|rd|th)?\b'
    ]
    date_patterns_my = [
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+\d{4}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
    ]
    output_text=replace_and_format_dates(input_text, date_patterns_mdy,'%m/%d/%Y')
    output_text=replace_and_format_dates(output_text, date_patterns_md,'%m/%d')
    output_text=replace_and_format_dates(output_text, date_patterns_my,'%m/%Y')
    return output_text
def expand_contractions(text):
    expanded_text = contractions.fix(text)# expands all contractions except posessive nouns
    return expanded_text
def remove_irr_char_func(text):
    return re.sub(r'[^a-zA-Z]', ' ', text)
def remove_extra_whitespaces_func(text):
    return re.sub(r'^\s*|\s\s*', ' ', text).strip()
def clean_text(text):
    text=clean_html_text(text)
    text=remove_partial_tag(text)
    text=clean_encoding_error(text)
    text=remove_urls(text)
    text=new_line(text)
    text=clean_twitter_text(text)
    text=fix_repeating_characters(text)
    text=remove_emoticons(text)
    text=clean_slang(text)
    text=convert_dates(text)
    #text=expand_contractions(text)
    #text=remove_irr_char_func(text)
    text=remove_extra_whitespaces_func(text)
    return text