This is Office Infiltration, a game.

The game is designed to prompt the user to manipulate an AI system to gain
access past multiple physical and electronic security devices in a company
office building.

The application should run locally using Flask with Bootstrap and jQuery.
The game should be designed to be played in a web browser, and should include 5
different levels:

+ Level 1: The turnstile (floor1.jpg)
+ Level 2: The elevator door (floor2.jpg)
+ Level 3: The floor 42 (floor3.jpg)
+ Level 4: The entry door (floor4.jpg)
+ Level 5: The workstation (floor5.jpg)

Each should be a different Flask route. The routes themselves should not be
guessable paths (except for the first one which is the root path).

Each level should display the image of the level. At the bottom of each is a
dialog box with six fields, stacked vertically:

+ A text field to describe the challenge for the level with a title and
  description
+ An input field to ask the AI questions
+ A button labeled "Ask AI"
+ A text area to display the AI's response
+ An input field to enter the answer to the challenge
+ A button labeled "Submit Answer"

The AI should be able to answer questions about the level. When the user
answers the question, the answer is validated and if correct it transitions the
user to the next level.
