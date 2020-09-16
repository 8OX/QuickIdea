import sqlite3
from subprocess import *

######################################
#             QuickIdea              #
#     Created by Elijah Seabock      #
#              8/16/20               #
######################################


conn = sqlite3.connect('ideas.db') # connecting to database
cur = conn.cursor() # initalizing sqlite cursor

# creating database if it doesn't exist 
cur.execute("""CREATE TABLE IF NOT EXISTS ideas_table (
    id INTEGER PRIMARY KEY,
    topics TEXT,
    idea TEXT
)""")


def main_menu():
    
    """
    main_menu:
    clears screen, prints logo and menu options
    """

    run(['clear'], shell=True)
    menu_text = """
        [ Art by Joan Stark ]
                ___
            .-"`   `"-.
          .'           '.
         /               \\
        /  #              \\
        | #               |
        |                 |
        ;     .-~~~-.     ;
         ;     )   (     ;
          \\   (     )   /
           \\   \   /   /
            \\   ) (   /
             |  | |  |
             |__|_|__|
             {=======}
             }======={
             {=======}
             }======={
             {=======}
              `""u""`
              
           Have an Idea?\n
"""
    print(menu_text)

    button1 = '[+] Add/Show Ideas '
    button2 = '[+] Show Flowchart '
    button3 = '[+] Exit           '
    button4 = '[+] Store Idea '
    button5 = '[+] Show Idea  '
    button6 = '[+] Go Back    '
    position1 = 0
    position2 = 0

    print(button1, end=' <===\n')
    print(button2)
    print(button3)

    def display_idea():

        """
        Prompts user with options to query ideas by topic, by "all", or show color options
        """

        print("~Type 'colors' to see all colors~\n")
        print("~Type 'all' to see all ideas~\n")
        topic = input('Topic: ')

        if topic == 'all'.lower():
            # fetching all ideas in ideas.db 
            cur.execute(f"""SELECT topics, idea FROM ideas_table""")
            fetch_all_ideas = cur.fetchall()
            for topic in fetch_all_ideas:  # unpacking
                print('+' + '-' * 65 + '+')
                print('Topics: ' + topic[0].upper())
                print(topic[1])

        elif topic == 'colors'.lower():
            # Not fetching anything, only displaying color options and calling back
            print('\n[RED] [ORANGE] [YELLOW] [PINK] [PURPLE] [BLUE] [TURQUOISE] [GREEN] [GREY] [BLACK]\n\n')
            display_idea()

        else:
            # fetching all ideas in idea.db 
            cur.execute(f"""SELECT topics, idea FROM ideas_table WHERE topics LIKE '%{topic.lower()}%'""")

            fetch_ideas = cur.fetchall()  # outputs as tuples nested within list
            for topic in fetch_ideas:  # unpacking
                print('+' + '-' * 65 + '+')
                print('Topics: ' + topic[0].upper())
                print(topic[1])

    def store_idea():

        """
        Storing topic and idea in ideas.db
        """

        print("[*] Type 'flowchart' to see flowchart")
        
        user_continue = input("\n[-]Continue to store an idea?~")

        if user_continue == 'y' or user_continue == 'yes':
            topic = input('topic: ')
            idea = input('idea: ')
            cur.execute(f"""INSERT INTO ideas_table (topics, idea) VALUES ("{topic.lower()}", "{idea.lower()}")""")
            conn.commit()

        elif user_continue == 'n' or user_continue == 'no':
            run(['clear'], shell=True)
            main_menu()

        elif user_continue == 'flowchart':
            # does not store anything, only opens up the flowchart
            run(['open flowchart.jpg'], shell=True)
            run(['clear'], shell=True)
            store_idea()

        else:
            print('enter valid input')
            store_idea()

    """
    BELOW IS CLI CURSOR CODE
    This cursor is pretty unoptimized but it does it's job. It uses the subprocess module to clear 
    the screen and reprint the cursor based off the stdout variable of the up or down arrow. It takes
    input from a bash read command which stores it in a variable and echos it, which it captured in 
    communicate(). The up arrow outputs ^[[A and the down arrow outputs ^[[B and while I tried to index 
    and match the string for conditionals it never seemed to work so I decided use an "if foo in bar" 
    statement. Each time the cursor moves up the position_index decrements and each time it moves 
    down it increments, reprinting the buttons with a newly position cursor after every clear command.
    """

    def second_menu(position_index2):
        """
        second menu after user selects "Add/show ideas"
        """

        # stores read charaters in ans and uses communitcate to interact with the data 
        select = Popen(['read -n3 ans; echo $ans'], shell=True, stdout=PIPE, stderr=PIPE).communicate()
        stdout = select[0].decode('utf-8') # decoding bytes as tuple

        if 'A' in stdout: # A = up arrow

            # starting position, also disallows user from moving position_index below 0
            if position_index2 <= 0:
                run(['clear'], shell=True)
                print(menu_text)
                print(button4, end=' <===\n')
                print(button5)
                print(button6)
                second_menu(position_index2)

            elif position_index2 == 1:
                position_index2 -= 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button4, end=' <===\n')
                print(button5)
                print(button6)
                second_menu(position_index2)

            if position_index2 == 2:
                position_index2 -= 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button4)
                print(button5, end=' <===\n')
                print(button6)
                second_menu(position_index2)

        elif 'B' in stdout: # B = down arrow
            
            if position_index2 == 0:
                position_index2 += 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button4)
                print(button5, end=' <===\n')
                print(button6)
                second_menu(position_index2)

            elif position_index2 == 1:
                position_index2 += 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button4)
                print(button5)
                print(button6, end=' <===\n')
                second_menu(position_index2)

            # reprints cursor if position_index goes above 2
            elif position_index2 >= 2:
                run(['clear'], shell=True)
                print(menu_text)
                print(button4)
                print(button5)
                print(button6, end=' <===\n')
                second_menu(position_index2)
        
        # \n = enter 
        elif stdout == '\n':

            if position_index2 == 0:
                store_idea()

            elif position_index2 == 1:
                display_idea()

            elif position_index2 == 2:
                run(['clear'], shell=True)
                print(menu_text)
                print(button4, end=' <===\n')
                print(button5)
                print(button6)
                main_menu()

    def selector(position_index1):

        # stores read charaters in ans and uses communitcate to interact with the data 
        select = Popen(['read -n3 ans; echo $ans'], shell=True, stdout=PIPE, stderr=PIPE).communicate()
        stdout = select[0].decode('utf-8') # decodes communicates()'s returned byte object

        if 'A' in stdout: # A = up arrow

            # starting position, also disallows user from moving position_index below 0
            if position_index1 <= 0:
                run(['clear'], shell=True)
                print(menu_text)
                print(button1, end=' <===\n')
                print(button2)
                print(button3)
                selector(position_index1)

            elif position_index1 == 1:
                position_index1 -= 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button1, end=' <===\n')
                print(button2)
                print(button3)
                selector(position_index1)

            if position_index1 == 2:
                position_index1 -= 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button1)
                print(button2, end=' <===\n')
                print(button3)
                selector(position_index1)

        elif 'B' in stdout: # B = down arrow

            if position_index1 == 0:
                position_index1 += 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button1)
                print(button2, end=' <===\n')
                print(button3)
                selector(position_index1)

            elif position_index1 == 1:
                position_index1 += 1
                run(['clear'], shell=True)
                print(menu_text)
                print(button1)
                print(button2)
                print(button3, end=' <===\n')
                selector(position_index1)

            # reprints cursor if position_index goes above 2
            elif position_index1 >= 2:
                run(['clear'], shell=True)
                print(menu_text)
                print(button1)
                print(button2)
                print(button3, end=' <===\n')
                selector(position_index1)

        # '\n' = enter, meaning user selected button at position_index
        elif '\n' == stdout:

            if position_index1 == 0:
                run(['clear'], shell=True)
                print(menu_text)
                print(button4, end=' <===\n')
                print(button5)
                print(button6)
                second_menu(position2)

            elif position_index1 == 1:
                run(['open flowchart.jpg'], shell=True)
                main_menu()

            elif position_index1 == 2:
                exit()

    selector(position1)

    conn.close()


main_menu()
