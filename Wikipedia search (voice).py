#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 08:27:22 2021

@author: walter malta
@author: david rocha

Language: Portuguese BR
"""

import speech_recognition as sr
import pyttsx3
import wikipedia
import sys


def write_speak(engine,frase):
    print(frase)
    engine = pyttsx3.init()
    engine.say(frase)
    engine.runAndWait()    

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_ibm(audio,
                                                             username='apikey', 
                                                             password='', # INSERT IBM KEY
                                                             language='pt-BR')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def listen(recognizer, microphone, frase):
    for j in range(5):
        guess = recognize_speech_from_mic(recognizer, microphone)
        #print(guess)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        write_speak(engine,frase)

    # if there was an error, stop the game
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        response = "Desculpe, houve um erro"
        write_speak(engine,response)
        return response
    return guess["transcription"].strip()

if __name__ == "__main__":

    wikipedia.set_lang("pt")
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    #word = random.choice(WORDS)
    '''
    time.sleep(3)
    '''
    engine = pyttsx3.init()
    print('')
    print('#########################################################')
    print('')
    frase = 'Este é um sistema de pesquisa de verbetes na Wikipedia.\nEspere 2s e fale ao microfone o termo que deseja buscar.'
    write_speak(engine,frase)
    while True:

        search = listen(recognizer, microphone, "Não entendi, poderia repetir?")
        if search == 'Desculpe, houve um erro':
            frase = "A aplicação foi finalizada"
            print('')
            print('##################################################')
            print('')
            write_speak(engine,frase)
            sys.exit(0)
        
        print('')
        print('###################################################')
        print('')        
        frase = "Você disse: {}. Este termo está correto?".format(search)
        write_speak(engine,frase)
        print('')
        print('##################################################')
        print('')
        print('-> diga "sim" para prosseguir')
        print('')
        print('-> "não" para repetir o termo de busca')
        print('')
        print('-> e "sair" para finalizar')
        print('')
        print('##################################################')
        
        while True:
            print('')
            confirm = listen(recognizer, microphone, "Não entendi, poderia repetir?")
            if confirm not in ['sim', 'não', 'sair']:
                continue
            else:
                break
        print(confirm)
        if confirm == 'sair':
            frase = "A aplicação foi finalizada"
            print('')
            print('##################################################')
            print('')
            write_speak(engine,frase)
            sys.exit(0)
        elif confirm == 'não':
            print('')
            print('##################################################')
            print('')
            frase = 'Espere 2s e repita ao microfone o termo que deseja buscar'
            write_speak(engine, frase)
            continue
        elif confirm == 'sim':
            try:
                entry = (wikipedia.summary(search)[0:1000])
                last_period = entry.rfind('.')
                entry = entry[0:last_period + 1]
                write_speak(engine, entry)                
                print('')
                print('##################################################')
                print('')
                frase = "Deseja continuar pesquisando?"                
                write_speak(engine,frase)
                print('')
                print('##################################################')
                print('')
                print('-> Diga "sim" para prosseguir')
                print('')
                print('-> e "não" para sair')
                print('')
                print('##################################################')
                while True:
                    print('')
                    cont = listen(recognizer, microphone, "Não entendi, poderia repetir?")
                    if cont not in ['sim', 'não']:
                        continue
                    else:
                        break
        
                print(cont)
                if cont == 'não':
                    print('')
                    print('##################################################')
                    print('')
                    frase = "A aplicação foi finalizada"
                    write_speak(engine,frase)
                    sys.exit(0)
                if cont == 'sim':
                    print('')
                    print('##################################################')
                    print('')
                    frase = 'Espere 2s e fale ao microfone o termo que deseja buscar'
                    write_speak(engine,frase)
                    continue
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as error:
                print('##################################################')
                print('')
                frase = "Erro de ambiguidade ou termo não encontrado"
                write_speak(engine,frase)
                print('')
                print(error)
                print('')
                print('##################################################')
                print('')
                frase = "Deseja continuar pesquisando?"                
                write_speak(engine,frase)
                print('')
                print('##################################################')
                print('')
                print('-> Diga "sim" para prosseguir')
                print('')
                print('-> e "não" para sair')
                print('')
                print('##################################################')
                while True:
                    print('')
                    cont = listen(recognizer, microphone, "Não entendi, poderia repetir?")
                    if cont not in ['sim', 'não']:
                        continue
                    else:
                        break
        
                print(cont)
                if cont == 'não':
                    print('')
                    print('##################################################')
                    print('')
                    frase = "A aplicação foi finalizada"
                    write_speak(engine,frase)
                    sys.exit(0)
                if cont == 'sim':
                    print('')
                    print('##################################################')
                    print('')
                    frase = 'Espere 2s e fale ao microfone o termo que deseja buscar'
                    write_speak(engine,frase)
                    continue

    frase = "A aplicação foi finalizada"
    write_speak(engine,frase)
        
