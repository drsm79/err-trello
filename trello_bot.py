import logging
import config
from errbot import BotPlugin, botcmd
from trello import Cards, Boards


class TrelloBot(BotPlugin):
    def connect_trello(self):
        cards = Cards(
            config.__dict__.get("TRELLO_APP_KEY"),
            token=config.__dict__.get("TRELLO_TOKEN")
        )
        boards = Boards(
            config.__dict__.get("TRELLO_APP_KEY"),
            token=config.__dict__.get("TRELLO_TOKEN")
        )
        return cards, boards

    def get_configuration_template(self):
        """
        Configure the trello api
        """
        return {
            "TRELLO_APP_KEY": "qwertyuiop0987654321",
            "TRELLO_TOKEN": "abcdefghijklmnop",
            "TRELLO_BOARD": "517628yiuhj"
        }

    @botcmd()
    def trello_new(self, mess, args):
        """
        Create a new trello card
        """
        cards, boards = self.connect_trello()
        first_list = boards.get_list(config.__dict__.get('TRELLO_BOARD'))[0]
        logging.info(args)
        new_card = cards.new(args, first_list['id'])
        return "created card: %s" % new_card['shortUrl']

    @botcmd(split_args_with=' ')
    def trello(self, mess, args):
        """
        Add a link to a trello card
        """
        cards, _ = self.connect_trello()
        card = args[0]
        text = ' '.join(args[1:])
        logging.info(card)
        logging.info(text)
        cards.new_action_comment(card, text)
        return "updated card"
