from itertools import cycle
import logging
import sys
import io
import argparse


def add_card():
    message = 'The card:'
    print(message)
    logger.info(message)
    while True:
        term = input()
        logger.info(term)
        if term in flashcards.keys():
            message = f'The card "{term}" already exists. Try again:'
            print(message)
            logger.info(message)
        else:
            message = 'The definition of the card:'
            print(message)
            logger.info(message)
            while True:
                definition = input()
                logger.info(definition)
                if definition in flashcards.values():
                    message = f'The definition "{definition}" already exists. Try again:'
                    print(message)
                    logger.info(message)
                else:
                    flashcards[term] = definition
                    break
            message = f'The pair ("{term}":"{definition}") has been added.'
            print(message)
            logger.info(message)
            mistakes[term] = 0
            break


def remove_card():
    message = 'Which card?'
    print(message)
    logger.info(message)
    term = input()
    logger.info(term)
    if term not in flashcards.keys():
        message = f'Can\'t remove "{term}": there is no such card.'
        print(message)
        logger.info(message)
    else:
        del flashcards[term]
        del mistakes[term]
        message = 'The card has been removed'
        print(message)
        logger.info(message)


def import_pack(file_name):
    try:
        amount = 0
        f1 = open(file_name, 'r', encoding='utf-8')
        term, definition, mistake = ('', '', '')
        for i, line in enumerate(f1, start=1):
            if i % 3 == 1:
                term = line.strip()
            elif i % 3 == 2:
                definition = line.strip()
            else:
                mistake = line.strip()
            if term != '' and definition != '' and mistake != '':
                amount += 1
                flashcards[term] = definition
                mistakes[term] = int(mistake)
                term, definition, mistake = ('', '', '')
        f1.close()
        message = f'{amount} cards have been loaded.'
        print(message)
        logger.info(message)
    except:
        message = 'File not found.'
        print(message)


def export_pack(file_name):
    f2 = open(file_name, 'w', encoding='utf-8')
    for key, val in flashcards.items():
        f2.write(key + '\n')
        f2.write(val + '\n')
        f2.write(str(mistakes[key]) + '\n')
    f2.close()
    message = f'{len(flashcards)} cards have been saved.'
    print(message)
    logger.info(message)


def ask_flashcards():
    message = 'How many times to ask?'
    print(message)
    logger.info(message)
    amount = input()
    logger.info(amount)
    terms = cycle(flashcards.keys())
    for i in range(int(amount)):
        current_term = next(terms)
        message = f'Print the definition of "{current_term.strip()}"'
        print(message)
        logger.info(message)
        answer = input()
        logger.info(answer)
        if answer in flashcards.values():
            if answer == flashcards[current_term]:
                message = 'Correct!'
                print(message)
                logger.info(message)
            else:
                message = f'Wrong. The right answer is "{flashcards[current_term].strip()}", but your definition is ' \
                          f'correct for "{list(flashcards.keys())[list(flashcards.values()).index(answer)]}".'
                print(message)
                logger.info(message)
                mistakes[current_term] += 1
        else:
            message = f'Wrong. The right answer is "{flashcards[current_term].strip()}".'
            print(message)
            logger.info(message)
            mistakes[current_term] += 1


def reset_stats():
    for key in mistakes.keys():
        mistakes[key] = 0
    message = 'Card statistics have been reset.'
    print(message)
    logger.info(message)


def hardest_card():
    hardest = []
    for key, val in mistakes.items():
        if val == max(mistakes.values()) and max(mistakes.values()) != 0:
            hardest.append(key)
    if len(hardest) == 1:
        message = f'The hardest card is "{hardest[0]}". You have {max(mistakes.values())} errors answering it.'
        print(message)
        logger.info(message)
    elif len(hardest) > 1:
        message = f"The hardest cards are {', '.join(hardest)}"
        print(message)
        logger.info(message)
    else:
        message = 'There are no cards with errors.'
        print(message)
        logger.info(message)


parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')

flashcards = {}
mistakes = {}
logger = logging.getLogger('basic_logger')
logger.setLevel(logging.DEBUG)
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logger.addHandler(ch)

args = parser.parse_args()
args = [args.import_from, args.export_to]
if args[0] is not None:
    import_pack(args[0])

while True:
    main_message = 'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):'
    print(main_message)
    logger.info(main_message)
    command = input()
    logger.info(command)
    if command == 'add':
        add_card()
    elif command == 'remove':
        remove_card()
    elif command == 'import':
        main_message = 'File name:'
        print(main_message)
        logger.info(main_message)
        filename = input()
        logger.info(filename)
        import_pack(filename)
    elif command == 'export':
        main_message = 'File name:'
        print(main_message)
        logger.info(main_message)
        filename = input()
        logger.info(filename)
        export_pack(filename)
    elif command == 'ask':
        ask_flashcards()
    elif command == 'exit':
        main_message = 'Bye bye!'
        print(main_message)
        logger.info(main_message)
        if args[1] is not None:
            export_pack(args[1])
        sys.exit()
    elif command == 'reset stats':
        reset_stats()
    elif command == 'hardest card':
        hardest_card()
    elif command == 'log':
        main_message = 'File name:'
        print(main_message)
        logger.info(main_message)
        command = input()
        logger.info(command)
        f = open(f'{command}', 'w', encoding='utf-8')
        log_contents = log_capture_string.getvalue()
        f.write(log_contents)
        f.close()
        main_message = 'The log has been saved.'
        print(main_message)
        logger.info(main_message)
    print()
