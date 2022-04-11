import boto3
import csv
import io
import json
import logging
import re

###########
# LOGGING #
###########

logger = logging.getLogger()
logger.setLevel(logging.INFO)

###########
# CONFIGS #
###########

#############
# FUNCTIONS #
#############

# Translation Function
def translate_text(body, dest_language):
    
    #init translate service
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
      
    response = translate.translate_text(
        Text=body,
        SourceLanguageCode='auto',
        TargetLanguageCode=get_lang_code(dest_language)
    )
    
    logger.info(response)
    
    return response['TranslatedText']
    

# Convert human readable language to lang_code
def get_lang_code(dest_language):
    if dest_language == "Afrikaans":
        lang_code = "af"
    elif dest_language =="Albanian":
    	lang_code = "sq"
    elif dest_language =="Amharic":
    	lang_code = "am"
    elif dest_language =="Arabic":
    	lang_code = "ar"
    elif dest_language =="Armenian":
    	lang_code = "hy"
    elif dest_language =="Azerbaijani":
    	lang_code = "az"
    elif dest_language =="Bengali":
    	lang_code = "bn"
    elif dest_language =="Bosnian":
    	lang_code = "bs"
    elif dest_language =="Bulgarian":
    	lang_code = "bg"
    elif dest_language =="Catalan":
    	lang_code = "ca"
    elif dest_language =="Chinese (Simplified)":
    	lang_code = "zh"
    elif dest_language =="Chinese (Traditional)":
    	lang_code = "zh-TW"
    elif dest_language =="Croatian":
    	lang_code = "hr"
    elif dest_language =="Czech":
    	lang_code = "cs"
    elif dest_language =="Danish":
    	lang_code = "da"
    elif dest_language =="Dari":
    	lang_code = "fa-AF"
    elif dest_language =="Dutch":
    	lang_code = "nl"
    elif dest_language =="English":
    	lang_code = "en"
    elif dest_language =="Estonian":
    	lang_code = "et"
    elif dest_language =="Farsi (Persian)":
    	lang_code = "fa"
    elif dest_language =="Filipino Tagalog":
    	lang_code = "tl"
    elif dest_language =="Finnish":
    	lang_code = "fi"
    elif dest_language =="French":
    	lang_code = "fr"
    elif dest_language =="French (Canada)":
    	lang_code = "fr-CA"
    elif dest_language =="Georgian":
    	lang_code = "ka"
    elif dest_language =="German":
    	lang_code = "de"
    elif dest_language =="Greek":
    	lang_code = "el"
    elif dest_language =="Gujarati":
    	lang_code = "gu"
    elif dest_language =="Haitian Creole":
    	lang_code = "ht"
    elif dest_language =="Hausa":
    	lang_code = "ha"
    elif dest_language =="Hebrew":
    	lang_code = "he"
    elif dest_language =="Hindi":
    	lang_code = "hi"
    elif dest_language =="Hungarian":
    	lang_code = "hu"
    elif dest_language =="Icelandic":
    	lang_code = "is"
    elif dest_language =="Indonesian":
    	lang_code = "id"
    elif dest_language =="Italian":
    	lang_code = "it"
    elif dest_language =="Japanese":
    	lang_code = "ja"
    elif dest_language =="Kannada":
    	lang_code = "kn"
    elif dest_language =="Kazakh":
    	lang_code = "kk"
    elif dest_language =="Korean":
    	lang_code = "ko"
    elif dest_language =="Latvian":
    	lang_code = "lv"
    elif dest_language =="Lithuanian":
    	lang_code = "lt"
    elif dest_language =="Macedonian":
    	lang_code = "mk"
    elif dest_language =="Malay":
    	lang_code = "ms"
    elif dest_language =="Malayalam":
    	lang_code = "ml"
    elif dest_language =="Maltese":
    	lang_code = "mt"
    elif dest_language =="Mongolian":
    	lang_code = "mn"
    elif dest_language =="Norwegian":
    	lang_code = "no"
    elif dest_language =="Persian":
    	lang_code = "fa"
    elif dest_language =="Pashto":
    	lang_code = "ps"
    elif dest_language =="Polish":
    	lang_code = "pl"
    elif dest_language =="Portuguese":
    	lang_code = "pt"
    elif dest_language =="Romanian":
    	lang_code = "ro"
    elif dest_language =="Russian":
    	lang_code = "ru"
    elif dest_language =="Serbian":
    	lang_code = "sr"
    elif dest_language =="Sinhala":
    	lang_code = "si"
    elif dest_language =="Slovak":
    	lang_code = "sk"
    elif dest_language =="Slovenian":
    	lang_code = "sl"
    elif dest_language =="Somali":
    	lang_code = "so"
    elif dest_language =="Spanish":
    	lang_code = "es"
    elif dest_language =="Spanish (Mexico)":
    	lang_code = "es-MX"
    elif dest_language =="Swahili":
    	lang_code = "sw"
    elif dest_language =="Swedish":
    	lang_code = "sv"
    elif dest_language =="Tagalog":
    	lang_code = "tl"
    elif dest_language =="Tamil":
    	lang_code = "ta"
    elif dest_language =="Telugu":
    	lang_code = "te"
    elif dest_language =="Thai":
    	lang_code = "th"
    elif dest_language =="Turkish":
    	lang_code = "tr"
    elif dest_language =="Ukrainian":
    	lang_code = "uk"
    elif dest_language =="Urdu":
    	lang_code = "ur"
    elif dest_language =="Uzbek":
    	lang_code = "uz"
    elif dest_language =="Vietnamese":
    	lang_code = "vi"
    elif dest_language =="Welsh":
    	lang_code = "cy"
    else:
        lang_code = "en"
        logger.info("Destination language not available so default language was selected: {}".format(lang_code))
       
    return lang_code
            
# Read in Tableau payload and convert it into a CSV
def tableau_data_transformation(event_data):
    try:
        csvio = io.StringIO()
        writer = csv.writer(csvio)
        writer.writerows(zip(*event_data.values()))
        body = csvio.getvalue()
        logger.info("Transformed Body: {}".format(body))
        return body
    except Exception as e:
        logger.error(e, exc_info=True)

# Prepare translation results for Tableau
def serialize_translator_response(translate_response):
    try:
        list_results = re.split(r'\n|,', translate_response)

        if '' in list_results:
            list_results.remove('')
        
        return_value = json.dumps(list_results)
        logger.info(return_value)
        serialized_value = json.loads(return_value)
        logger.info(serialized_value)
        return serialized_value
    except Exception as e:
        logger.error(e, exc_info=True)

# Main function
def lambda_handler(event, context):
    logger.info("Event: {0}".format(event))

    if event['script'] == 'return int(1)':
        return 1
    else: 
        dest_language = event['script'] # Target Language Indentifier
        logger.info("dest_language: {0}".format(dest_language))
        event_data = event['data']
        logger.info("Event data: {0}".format(event_data))
    
        try:
            body = tableau_data_transformation(event_data)
            translate_response = translate_text (body, dest_language)
            translate_response_serialized = serialize_translator_response(translate_response)
            return translate_response_serialized

        except Exception as e:
            logger.error(e, exc_info=True)  