# User imports
import json, ast
import random
import pprint
import smtplib

scores = [
    [0,0], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8], [0,9],
    [1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], [1,8], [1,9],
    [2,0], [2,1], [2,2], [2,3], [2,4], [2,5], [2,6], [2,7], [2,8], [2,9],
    [3,0], [3,1], [3,2], [3,3], [3,4], [3,5], [3,6], [3,7], [3,8], [3,9],
    [4,0], [4,1], [4,2], [4,3], [4,4], [4,5], [4,6], [4,7], [4,8], [4,9],
    [5,0], [5,1], [5,2], [5,3], [5,4], [5,5], [5,6], [5,7], [5,8], [5,9],
    [6,0], [6,1], [6,2], [6,3], [6,4], [6,5], [6,6], [6,7], [6,8], [6,9],
    [7,0], [7,1], [7,2], [7,3], [7,4], [7,5], [7,6], [7,7], [7,8], [7,9],
    [8,0], [8,1], [8,2], [8,3], [8,4], [8,5], [8,6], [8,7], [8,8], [8,9],
    [9,0], [9,1], [9,2], [9,3], [9,4], [9,5], [9,6], [9,7], [9,8], [9,9],
]


class Numbers:
    def __init__(self):
        self.players = {}
        self.password = "ltcn vesh bjwk ffch"
        self.email = "tylerstruntz@gmail.com"
        self.price = 2
    # End __init__

    def get_players(self):
        with open('players.json') as f:
            self.players = json.load(f)

        self.players = ast.literal_eval(json.dumps(self.players))

        for player in self.players:
            print('added player: [{}]'.format(player['Name']))
    # End get_players

    def get_players_picks(self):
        for players in self.players:
            self.pick_numbers(players, players['Numbers'])
    # End get_players_picks

    def pick_numbers(self, player, numbers):
        print('Picking numbers for {}'.format(player['Name']))
        i = 0
        while i != numbers:
            score_picked = random.choice(scores)
            player['Picks'].append(score_picked)
            scores.remove(score_picked)
            i += 1
    # End pick_numbers
    
    def greeting(self, name, numbers):
        msg = "Hello {}, you picked {} numbers. ".format(name, numbers)
        return msg
    # End greeting

    def closing(self, numbers):
        msg = "Please venmo @Tyler-Struntz ${}".format(numbers * self.price)
        return msg
    # End closing

    def create_message_numbers(self, picks):
        msg = "{}".format(picks)
        # print(msg)
        return msg
    # End create_message
        

    def sms_string(self, provider, cell):
        if provider == 'sprint' or provider == 'Sprint':
            to_mail = '{}@messaging.sprintpcs.com'.format(cell)
        return to_mail
    # End sms_string

    def send_email(self, password):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.email, self.password)

            for players in self.players:
                
                greeting_msg = self.greeting(players['Name'], players['Numbers'])
                numbers_msg = self.create_message_numbers(players['Picks'])
                closing_msg = self.closing(players['Numbers'])

                greeting_sms = ("From: %s\r\n" % self.email
                        + "To: %s\r\n" % players['Email']
                        + "Subject: %s\r\n" % "Vikings vs Bengals Week 1"
                        + "\r\n"
                        + greeting_msg)

                numbers_sms = ("From: %s\r\n" % self.email
                                + "To: %s\r\n" % players['Email']
                                + numbers_msg)

                closing_sms = ("From: %s\r\n" % self.email
                                + "To: %s\r\n" % players['Email']
                                + closing_msg)

                link_sms = ("From: %s\r\n" % self.email
                            + "To: %s\r\n" % players['Email']
                            + "https://venmo.com/code?user_id=2246084780883968494&created=1630698961.777948&printed=1")

                if players['Preference'] == 'Text':
                    to_mail = self.sms_string(players['Provider'], players['Cell'])
                else: 
                    to_mail = players['Email']
                
                server.sendmail(self.email, to_mail, greeting_sms)
                server.sendmail(self.email, to_mail, numbers_sms)
                server.sendmail(self.email, to_mail, closing_sms)
                server.sendmail(self.email, to_mail, link_sms)

            # End for 
            server.close()
        except Exception as e:
            print('something went wrong. . . {}'.format(e))
        # End try-except
    # End send_message

    def run(self):
        self.get_players()
        self.get_players_picks()
        self.send_email(self.password)
    # End run

if __name__ == "__main__":
    num = Numbers()
    num.run()    
    
