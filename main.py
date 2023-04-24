import openai
import re
import chardet

openai.api_key = "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"
engine = "text-davinci-002" #языкаовая модель
pattern = r'(?<=")[^"]*?(?=")|(?<=§)[^§H]*?(?=§)' #регулярка для поиска слов, котоыре надо переводить

def translator(line):
    translation = openai.Completion.create(
        engine=engine,
        prompt=f"Translate '{line}' into Russian:",
        max_tokens=1000,
        temperature=0.1 #вариативность ответов. от 0 до 1. 1 - развернутые и неожиданные ответы. Дает не верный перевед при увелечении значения
    ).choices[0].text.strip()
    return translation

# определяем кодировку входного файла "eng.txt"
with open("eng.txt", "rb") as f:
    result = chardet.detect(f.read()) #определяется кодировка. При записи в rus.txt появляись знаки вопроса
    encoding = result['encoding']

# открываем файл в нужной кодировке
with open("eng.txt", "r", encoding=encoding) as file:
    lines = file.readlines()

    # записываем перевод в "rus.txt" в нужной кодировке
    with open("rus.txt", "w", encoding="utf-8") as out_file:
        for i in range(len(lines)):
            matches = re.findall(pattern, lines[i])
            for match in matches:
                translated = translator(match)
                lines[i] = lines[i].replace(match, translated)
            out_file.write(lines[i])
            print(lines[i])