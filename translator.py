import sys
import requests
from bs4 import BeautifulSoup

arg = sys.argv
if len(arg) != 4:
    print("The script should be called with three arguments, the first the language from which you want to translate,"
          " the second the language to translate and the last, te word you want to translate")
else:
    languages = {'Arabic': '1.', 'German': '2.', 'English': '3.', 'Spanish': '4.', 'French': '5.', 'Hebrew': '6.',
                 'Japanese': '7.', 'Dutch': '8.', 'Polish': '9.', 'Portuguese': '10.', 'Romanian': '11.',
                 'Russian': '12.', 'Turkish': '13.'}

    from_language = arg[1].lower()
    to_language = arg[2].lower()
    word = str(arg[3]).title()

    def page_request(destiny):
        r = requests.get('https://context.reverso.net/translation/{}-{}/{}'.format(from_language, destiny, word),
                         headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.content, 'html.parser')

        words = soup.find_all('a', {'class': 'translation'})
        phrases = soup.find_all('span', {'class': 'text'})
        words_list_f = [i.text.strip('\n ') for i in words]
        phrases_list_f = []
        counter = 0
        for i in phrases:
            if word in i.text:
                phrases_list_f.append(i.text.strip('\n'))
                phrases_list_f.append(phrases[counter + 1].text.strip('\n'))
            counter += 1
        return words_list_f, phrases_list_f


    def trans_t(destiny):
        print('\n{} translations:'.format(destiny).title())
        for t in page_request(destiny)[0][1:5]:
            print(t)

    def trans_c(destiny):
        print('\n{} examples:'.format(destiny).title())
        counter = 0
        for c in page_request(destiny)[1]:
            print(c + ':' if counter % 2 == 0 else c + '\n')
            counter += 1
            if counter >= 10:
                break


    def examples(destiny):
        trans_t(destiny)
        trans_c(destiny)


    try:
        r = requests.get('https://context.reverso.net/translation/{}-{}/{}'.format(from_language, to_language, word),
                         headers={'User-Agent': 'Mozilla/5.0'})
        languages[to_language.title()]
        if len(page_request(to_language)[0]) == 1:
            1 / 0

    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    except KeyError:
        print("Sorry, the program doesn't support {}".format(to_language))
        print('Sorry, unable to find {}'.format(word))
    except ZeroDivisionError:
        print('Sorry, unable to find {}'.format(word))
    else:
        if arg[2] not in ('all', 'All'):
            examples(to_language)
        else:
            for k in languages.keys():
                if k.lower() == from_language:
                    continue
                else:
                    examples(k.lower())
