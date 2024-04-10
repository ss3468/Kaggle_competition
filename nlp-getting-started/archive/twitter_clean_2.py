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
    text = re.sub(r"fromåÊwounds", "from wounds", text)
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
    text = re.sub(r"donå«t", "do not", text)
    text = re.sub(r"mÌ¼sica", "music", text)
    text= re.sub(r"(vÌ_a)|(vi\x89Û)","via",text)
    text= re.sub(r"bioter\x89Û","bioterrorism",text)
    text=re.sub(r'[^\x00-\x7F]+', '', text)
    return text
def remove_urls(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')  # Regex pattern for matching URLs

    # Replace URLs with an empty string
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = re.sub(r"pic.twitter.com\S+",'', cleaned_text)
    return cleaned_text
def clean_twitter_text(text):
    text = re.sub(r'\bRT\s?@\w+:?', '', text)
    text = re.sub(r'\bRT(\:)?\s\w+:?', '', text)
    text = re.sub(r'\bRT(\:)?\s@\w+:?', '', text)
    text = re.sub(r'\bMT\s?@\w+:?', '', text)
    text = re.sub(r'\b[Vv]ia @{1,}\w+\b', '', text)
    text= re.sub(r'#(\w+)',r'\1',text)
    text=re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b","",text)
    text = re.sub(r'(\.)?@{1,}(?!\d{1,2}:\d{2}\b)\w+(:)?', '', text)
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
    # fixed_text=re.sub(r'\bab{1,}andoned\b','abandoned',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\ba{1,}ll\b','all',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\ba{1,}n{1,}\b','an',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\ba{1,}n{1,}d{1,}\b','and',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\ba{1,}r{1,}g{1,}h{1,}\b','argh',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bawesome{1,}\b','awesome',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bb{1,}a{1,}c{1,}k{1,}\b','back',fixed_text)
    # fixed_text=re.sub(r'\bca{1,}ll\b','call',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bd{1,}a{1,}m{1,}n{1,}\b','damn',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bgo{1,}\b','go',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bgo{1,}a{1,}l\b','goal',fixed_text)
    # fixed_text=re.sub(r'\bple{1,}ase\b','please',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\blo{1,}l\b','lol',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bmad{1,}\b','mad',fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\bno{1,}\b','no',fixed_text,flags=re.I)
    # fixed_text = re.sub(r"\bokay{1,}\b", "okay", fixed_text)
    # fixed_text = re.sub(r"\bom{1,}g{1,}\b", "okay", fixed_text,flags=re.I)
    # fixed_text=re.sub(r'\by{1,}o{1,}u{1,}\b','you',fixed_text)
    # fixed_text = re.sub(r"\bre{1,}a{1,}d\b", "read", fixed_text,flags=re.I)
    # fixed_text = re.sub(r"\bremedy{1,}\b", "remedy", fixed_text)
    # fixed_text = re.sub(r"\bso{1,}\b", "so", fixed_text,flags=re.I)
    # fixed_text = re.sub(r"\byea{1,}h{1,}\b", "yeah", fixed_text,flags=re.I)
    # fixed_text = re.sub(r"\bye{1,}s{1,}\b", "yes", fixed_text,flags=re.I)
    return fixed_text
emoticons=['((\>)?(?<![a-zA-Z0-9])(:3{1,}))','((\>)?[\:\;]([DdPp]|(\()|(\){1,})))','([\;\:]\-([\;\(OoDd]|(\){1,})))','(\<3)','(\>\_[\<\>])','(\-(\_{1,})\-)','[OT]_[oT]','(\:\'\()','(\=\/)','(\-\.\-)']
def remove_emoticons(text):
    tem=text.split(' ')
    emoticon_pattern = re.compile(r''+'|'.join(emoticons))
    new_list=[re.sub(emoticon_pattern, '', word) for word in tem]
    return ' '.join(new_list)
def clean_slang(text):
    #slang terms, typos, and informal abbreviations
    text = re.sub(r'2k(\d{2})',r'20\1',text,flags=re.I)
    text = re.sub(r'(\bb4\b)|(\bbe4\b)','before',text,flags=re.I)
    text = re.sub(r"(\bb/c\b)|(\bbc\b)|(\bcuz\b)|(\bbcuz\b)", "because", text)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)
    text = re.sub(r'(\bw/o\b)|(\bw/out\b)',"without",text,flags=re.I)
    text = re.sub(r'\bw/e\b',"whatever",text,flags=re.I)
    text = re.sub(r'\bw/(\s+)?((\w+\b)|([.,;!?])|$)',r'with \2',text,flags=re.I)
    text = re.sub(r"\bP/U\b", "pick up", text)
    text = re.sub(r'(\bwedn\b)|(\bwedneday\b)|(\bwednes\b)','wednesday',text,flags=re.I)
    text = re.sub(r'\bu2\b','you too',text,flags=re.I)
    text=re.sub(r"\b(?<!p/)u\b","you",text)#text = re.sub(r'\bu\b','you',text,flags=re.I)
    text = re.sub(r'\bda\b','the',text)
    text = re.sub(r'\bfavourite\b','favorite',text,flags=re.I)
    text = re.sub(r'\bcolour\b','color',text,flags=re.I)
    text = re.sub(r'(\bdemonitisation\b)|(\bdemonitization\b)|(\bdemonetisation\b)','demonetization',text,flags=re.I)
    text = re.sub(r"recentlu", "recently", text)
    text = re.sub(r"Ph0tos", "Photos", text)
    text = re.sub(r"amirite", "am I right", text)
    text = re.sub(r"exp0sed", "exposed", text)
    text = re.sub(r"Trfc", "Traffic", text)
    text = re.sub(r"(\d)(\s+)?yr", r"\1 year", text)
    text = re.sub(r"(\d)years", r"\1 years", text)
    text = re.sub(r'\bcya\b',"see you",text)
    text = re.sub(r"\bnvr\b", "never", text)
    text=re.sub(r'\bnarcissit\b','narcissist',text,flags=re.I)
    text=re.sub(r'\bcolour\b','color',text,flags=re.I)
    text=re.sub(r'\b69 august 1945\b','08/06/1945 and 08/09/1945',text)
    text=re.sub(r'\b27 Jan 2007he\b','27 Jan 2007 he',text)
    text=re.sub(r'\baccepte\b','accepted',text)
    text=re.sub(r'\bddnt\b','didn\'t',text)
    text=re.sub(r'\bknowlddge\b','knowledge',text)
    text = re.sub(r"\bs2g\b", "swear to god", text)
    text = re.sub(r"\bS3XLEAK\b", "sex leak", text)
    text = re.sub(r"\bSumthng\b", "something", text)
    text = re.sub(r"\b2day\b", "today", text)
    text=re.sub(r'\brembr\b','remember',text)
    text = re.sub(r"\bKowing\b", "Knowing", text)
    text = re.sub(r"\bc/o\b", "care of", text)
    text = re.sub(r"\bprobaly\b", "probably", text)
    text = re.sub(r"\bwhatevs\b", "whatever", text)
    text = re.sub(r"\breferencereference\b", "reference", text)
    text = re.sub(r"(\bcolomr\b)|(\bcolour\b)", "color", text)
    text = re.sub(r"\bwrld\b", "world", text)   
    text = re.sub(r"\bshld\b", "should", text)
    text = re.sub(r"\bbelo-ooow\b", "below", text)  
    text = re.sub(r"\bwho-ooo-ole\b", "whole", text)
    text = re.sub(r"\bLAIGHIGN\b", "laughing", text)
    text = re.sub(r"\bppl\b","people",text,flags=re.I)
    text = re.sub(r"\bbtwn\b","between",text,flags=re.I)
    text=re.sub(r"(\bmofo\b)|(\bmf\b)|(\bmfs\b)","mother fucker",text,flags=re.I)
    text = re.sub(r"\bSNCTIONS\b", "sanctions", text)
    text=re.sub(r"\bWED.AUG.5TH\b","08/05",text)
    text = re.sub(r"\bHLPS\b", "helps", text)
    text = re.sub(r"\bidkidk\b", "idk idk", text)
    text=re.sub(r"\bkno\b","know",text)
    text=re.sub(r"\btren\b","trend",text)
    text = re.sub(r"\bviaYouTube\b", "via YouTube", text)
    text = re.sub(r"\bbleased\b", "blessed", text)
    text = re.sub(r"\b(\d{1,})km\b",r"\1 kilometers",text,flags=re.I)
    text = re.sub(r"\b(\d{1,})inch\b",r"\1 inch",text)
    text = re.sub(r"\b(\d{1,2})min(s)?\b",r"\1 minutes",text)
    text=re.sub(r"\n"," ",text)
    #acronymns
    text=re.sub(r'\bU\.S(\.)?', 'United States',text,flags=re.I)
    text=re.sub(r'\blol\b','laugh out loud',text,flags=re.I)
    text=re.sub(r'\bomg\b','Oh My God',text,flags=re.I)
    text=re.sub(r'\bbae\b','before anyone else',text,flags=re.I)
    text=re.sub(r'\bfyi\b','for your information',text,flags=re.I)
    text=re.sub(r'\bbrb\b','Be Right Back',text,flags=re.I)
    text=re.sub(r'\blmao\b','laugh my ass off',text,flags=re.I)
    text=re.sub(r'\bcya\b',"see you",text)
    text=re.sub(r'\bwtf\b','what the fuck',text,flags=re.I)
    text=re.sub(r'\blmfao\b','laugh my fucking ass off',text,flags=re.I)
    text = re.sub(r"\bidk\b", "i don\'t know", text)
    #hashtags
    text = re.sub(r"\bpdx911\b", "Portland Police", text)
    text = re.sub(r"amageddon", "armageddon", text)
    text = re.sub(r"\bthankU\b", "thank you", text)
    text = re.sub(r"\btil_now\b", "until now", text)
    text = re.sub(r"\byycstorm\b", "Calgary Storm", text)
    text = re.sub(r"\boffers2go\b", "offers to go", text)
    text = re.sub(r"\bHiroshima70\b", "Hiroshima", text)
    text = re.sub(r"\bnewnewnew\b", "new new new", text)
    text = re.sub(r"\byycweather\b", "Calgary Weather", text)
    text = re.sub(r"\bcalgarysun\b", "Calgary Sun", text)
    text = re.sub(r"\bFIFA16\b", "Fifa 2016", text)
    text=re.sub(r"\bAppreciativeInquiry\b","Appreciative Inquiry",text)
    # abbreviations
    text = re.sub(r"\bFire Co\.", "Fire Company", text)
    text = re.sub(r"\bHolt and Co\.", "Holt and Company", text)
    text = re.sub(r"\broofing co\.", "roofing company", text)
    text = re.sub(r"\bCosta Co\.", "Costa County", text)
    text = re.sub(r"\bYork Co\.", "York County", text)
    text = re.sub(r"\bFairfax Co\.", "Fairfax County", text)
    text = re.sub(r"\bfwy\b", "Freeway", text,flags=re.I)
    text = re.sub(r"\bhwy\b", "Highway", text,flags=re.I)
    
    #location
    text = re.sub(r"\bnyc\b", "New York City", text)
    text = re.sub(r"\bcalif\b", "California", text)
    text=re.sub(r"\bnm\b","New Mexico",text)
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
    expanded_text = contractions.fix(text)
    return expanded_text
def remove_irr_char_func(text):
    text= re.sub('\w*\d\w*', '', text)
    return re.sub(r'[^a-zA-Z]', ' ', text)
def clean_text(text):
    text=clean_html_text(text)
    text=remove_partial_tag(text)
    text=clean_encoding_error(text)
    text=remove_urls(text)
    text=clean_twitter_text(text)
    text=fix_repeating_characters(text)
    text=remove_emoticons(text)
    text=clean_slang(text)
    text=convert_dates(text)
    text=expand_contractions(text)
    text=remove_irr_char_func(text)
    return text