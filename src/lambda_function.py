from main import HousingBot


def lambda_handler(event, context):
    bot = HousingBot(responses=[], categories=[
        ("city", "NNP"), ("budget", "CD")])  # NNP: Proper noun, singular; CD: Cardinal number
    return bot.respond(event['message'])
