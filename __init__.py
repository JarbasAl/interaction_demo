from mycroft.skills import MycroftSkill
from mycroft import intent_file_handler
from mycroft.skills.core import resting_screen_handler
from datetime import datetime


# you should name your skill something more descriptive
# Here its called DemoSkill
# be sure it matches the last line of this file  -> return DemoSkill()
class DemoSkill(MycroftSkill):

    # a new intent will always look like this
    # just copy paste it
    @intent_file_handler("happy.intent")
    def handle_happy_intent(self, message):
        image_file = join(dirname(__file__), "ui", "happy.gif")
        self.gui.show_animated_image(image_file)
        # always have at least 1 speech command
        # otherwise the user does not know if something happened
        self.speak_dialog("happy")

    # the "handle_XXX_intent" should match "XXX.intent"
    # this is just good practice and helps keeping code easy to understand
    @intent_file_handler("sad.intent")
    def handle_sad_intent(self, message):
        image_file = join(dirname(__file__), "ui", "sad.gif")
        self.gui.show_animated_image(image_file)
        self.speak_dialog("sad")

        # Times to ask user for input, -1 for infinite
        # infinite should be avoided!!!
        num_retries = 5
        # you can ask questions to the user
        # inside get_response should be a .dialog file name
        # this example will speak "why.dialog"
        dialog_variables = {"emotion": "sad"}  # optional, same as speak_dialog
        user_response = self.get_response("why", dialog_variables,
                                          num_retries=num_retries)
        if user_response:
            # here you can add extra if... else...

            # save to file using helper function
            self.save_utterance(user_response, "sad")
            # remember, always speak or the user won't know what happened
            self.speak_dialog("saved")
        else:
            # User can not respond and timeout or say "cancel" to stop
            self.speak_dialog("no_answer")

    # NOTE you need to install https://github.com/MycroftAI/skill-mark-2
    @resting_screen_handler("robot_eyes")
    def handle_resting_screen(self, message):
        image_file = join(dirname(__file__), "ui", "neutral.png")
        self.gui.show_animated_image(image_file)

    # this is just an helper function to keep code cleaner
    # intent should only handle voice interaction, other logic should have
    # its own method
    def save_utterance(self, utterance, emotion):
        now = str(datetime.now())  # current date and time

        # open a file for writing, by default skills a folder reserved for
        # their personal data, the "a" below means "append", it will write
        # to the end of the file and create it if it does not exist
        # the file is saved at /home/pi/.mycroft/skills/SKILL_NAME/FILE_NAME
        with self.file_system.open("user_utterances.csv", "a") as f:
            # write "utterance, emotion, time" to file
            f.write(",".join([utterance, emotion, now]) + "\n")
            # the \n means newline, its like pressing enter


def create_skill():
    return DemoSkill()
