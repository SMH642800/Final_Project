import googletrans
from pprint import pprint


translator = googletrans.Translator()

def translate_text(text,dest='en'):
    result = translator.translate(text, dest).text
    return result

result1 = translate_text( text = "水之呼吸", dest = 'en' )
result2 = translate_text( "水之呼吸" , dest = 'ja' )
result3 = translate_text( "水之呼吸" , 'ko')
print(result1)
print(result2)
print(result3)