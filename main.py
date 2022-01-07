from GitHubMetrisc import commit_freq
from GitHubMetrisc import issues_activity
import re
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'ACCESS_TOKEN'

# All available metrics
metrics_list = [commit_freq, issues_activity]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Open source project analyzer bot!\n"
                        "Send me the link to a github repo and I'll tell you some information about it.")


@dp.message_handler()
async def echo(message: types.Message):
    url = message.text
    matched = re.match('((https://)|(http:/\/))?github\.com\/([A-Za-z0-9\S]+)'
                       '\/([A-Za-z0-9\S]+)', url)
    if matched:
        username = matched.group(4)
        repo = matched.group(5)
        answer = '\n\n'.join([m.get_info(username, repo) for m in metrics_list])
    else:
        answer = 'Sorry, it seems like your url is not valid\n' \
                 ' The valid url should look like that: https://github.com/username/reponame'

    await message.answer(answer)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)