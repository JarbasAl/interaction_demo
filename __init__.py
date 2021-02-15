from mycroft.skills import MycroftSkill
from mycroft import intent_file_handler
from mycroft.skills.core import resting_screen_handler
from datetime import datetime
from os.path import join, dirname


# you should name your skill something more descriptive
# Here its called DemoSkill
# be sure it matches the last line of this file  -> return DemoSkill()
class DemoSkill(MycroftSkill):

    # NOTE you need to install https://github.com/MycroftAI/skill-mark-2
    @resting_screen_handler("robot_eyes")
    def handle_resting_screen(self, message=None):
        image_file = join(dirname(__file__), "ui", "neutral.png")
        self.gui.show_animated_image(image_file)

    # the "handle_XXX_intent" should match "XXX.intent"
    # this is just good practice and helps keeping code easy to understand
    @intent_file_handler("interaction.intent")
    def handle_interaction_intent(self, message):

        # Times to ask user for input, -1 for infinite
        # infinite should be avoided!!!
        num_retries = 3

        # you can ask questions to the user
        # inside get_response should be a .dialog file name
        user_response = self.get_response("interaction_response",
                                          num_retries=num_retries)

        # if user answers
        if user_response:
            emotion = None

            # now let's match a feeling to what user said
            # this will check if any line inside a .voc file is present in
            # the utterance, not an exact match, just needs to be
            # somewhere in the user response
            if self.voc_match(user_response, "happy"):
                emotion = "happy"
            elif self.voc_match(user_response, "sad"):
                emotion = "sad"

            if emotion:
                # NOTE file names should match
                image_file = join(dirname(__file__), "ui", emotion + ".gif")
                self.gui.show_animated_image(image_file)

                # ask the user why he feels that way
                dialog_variables = {"emotion": emotion}
                why_response = self.get_response("why", dialog_variables,
                                                  num_retries=num_retries)

                if not why_response:
                    # user didn't say why he feels {emotion}
                    # but we still want to save the emotion
                    why_response = "<no response>"

                # save to file using helper function
                self.save_utterance(why_response, emotion)

                # remember, always speak or the user won't know what happened
                self.speak_dialog("saved")
            else:
                # unknown emotion
                # remember, always speak or the user won't know what happened
                self.speak_dialog("unknown")

        else:
            # User can not respond and timeout or say "cancel" to stop
            self.speak_dialog("no_answer")

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
