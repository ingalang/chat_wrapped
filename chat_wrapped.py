import os
from bs4 import BeautifulSoup
import codecs
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re
from wordcloud import WordCloud
import seaborn as sns
import argparse
from datetime import date as the_date

class ChatMessage(object):
    def __init__(self, sender, text, reactions, date, time):
        self.sender = sender
        self.text = text
        self.reactions = reactions
        self.date = date
        self.time = time

def plot_avg_msg_length_per_person(chat_messages_dict, save=True):
    names = []
    lengths = []
    for name in chat_messages_dict.keys():
        avg_msg_length = sum(len(msg.text.split()) for msg in chat_messages_dict[name]) / len(chat_messages_dict[name])
        names.append(name)
        lengths.append(avg_msg_length)

    names = np.array(names)
    lengths = np.array(lengths)
    inds = lengths.argsort()
    names = np.flip(names[inds])
    lengths = np.flip(lengths[inds])

    plt.bar(names, lengths, color='green')
    plt.title(f'Average length of messages (number of words) per person')
    if save:
        plt.savefig(f'avg_msg_length.png')
    plt.show()


def plot_relative_num_of_str_per_person(chat_messages_dict, search_string, save=True):
    num_str_per_person = {}
    for key in chat_messages_dict.keys():
        all_text = " ".join(msg.text.lower() for msg in chat_messages_dict[key])
        string_count = all_text.count(search_string)
        num_str_per_person[key] = string_count/len(all_text.split())
    data = np.array([count for count in num_str_per_person.values()])
    labels = np.array([name for name in num_str_per_person.keys()])
    inds = data.argsort()
    data = np.flip(data[inds])
    labels = np.flip(labels[inds])

    # create par plot
    plt.bar(labels, data)
    #plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title(f'Antall \'{search_string}\' fordelt på antall ord per person')
    if save:
        plt.savefig(f'num_str_{search_string}.png')
    plt.show()

def get_chat_messages(html_text, target_year):
    current_year = int(str(the_date.today()).split('-')[0])
    chat_messages = []
    years_after_target_year = [year for year in range(target_year, current_year)]

    soup = BeautifulSoup(html_text, 'html.parser')
    reaction_reg = re.compile(r'([\W]+)([a-zA-Z0-9_øåæ ]*)')

    unique_years = []

    for statement in soup.find_all(class_="pam _3-95 _2pi0 _2lej uiBoxWhite noborder"):

        # Extracting the name
        name = statement.find(class_="_3-96 _2pio _2lek _2lel")
        if isinstance(name, type(None)):
            continue
        name = name.text

        # Extracting the reaction
        reactions = []
        reaction = statement.find(class_="_tqp")
        if not isinstance(reaction, type(None)):
            reaction = reaction.text
            matches = re.finditer(reaction_reg, reaction)
            for m in matches:
                reactions.append((m.group(1), m.group(2)))

        # Extracting the message
        message = statement.find(class_="_3-96 _2let")
        if isinstance(message, type(None)):
            continue
        if reaction is None:
            message = message.text
        else:
            message = re.sub(reaction, '', message.text)

        # Extracting the date
        date = statement.find(class_="_3-94 _2lem")
        if isinstance(date, type(None)):
            continue
        date = date.text
        date, time = date.split(', ')

        msg_year = int(date[-4:])
        if msg_year not in unique_years:
            unique_years.append(msg_year)

        if msg_year == target_year:
            chat_msg = ChatMessage(sender=name, text=message, reactions=reactions, date=date, time=time)
            chat_messages.append(chat_msg)
        elif msg_year in years_after_target_year:
            continue
        else:
            return chat_messages, unique_years
    return chat_messages, unique_years

def plot_share_of_messages(chat_messages_dict, style='pie'):

    data = [len(messages) for messages in chat_messages_dict.values()]
    labels = [key for key in chat_messages_dict.keys()]

    colors = sns.color_palette('bright')[0:5]

    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title('Share of messages from each person')
    plt.savefig('share_of_messages.png')
    plt.show()

def plot_reactions(name, sent_counts, received_counts, save=False):
    barWidth = 0.40
    fig = plt.subplots(figsize=(12, 8))

    # set height of bar
    all_emojis = np.unique(list(sent_counts.keys()) + list(received_counts.keys()))
    print(f'Emojis for {name}:')
    print(' '.join(all_emojis))
    sent = [sent_counts[emoji] if emoji in sent_counts else 0 for emoji in all_emojis]
    received = [received_counts[emoji] if emoji in received_counts else 0 for emoji in all_emojis]

    # Set position of bar on X axis
    br1 = np.arange(len(all_emojis))
    br2 = [x + barWidth for x in br1]

    # Make the plot
    plt.bar(br1, sent, color='pink', width=barWidth,
            edgecolor='black', label='sendt')
    plt.bar(br2, received, color='lightblue', width=barWidth,
            edgecolor='black', label='mottatt')

    # Adding Xticks
    plt.xticks([r + barWidth/2 for r in range(len(all_emojis))],
               all_emojis)
    plt.title(f'Reactions: {name}')

    plt.legend()
    if save:
        plt.savefig(f'{name.split()[0].lower()}_reactions.png')
    plt.show()

def make_wordcloud(name, chat_messages, stop_words, save=True):
    full_text = ' '.join([msg.text.lower() for msg in chat_messages])

    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords=stop_words).generate(full_text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(name)
    if save:
        plt.savefig(f'{name.split()[0].lower()}_wordcloud.png')
    plt.show()

def print_general_stats(chat_messages, year):
    headline_str = f' Chat message stats, {year} '
    print(headline_str.center(60, "#"))

    num_messages = len(chat_messages)
    unique_dates = len(np.unique([msg.date for msg in chat_messages]))
    num_words = len([word for msg in chat_messages for word in msg.text.split()])
    num_reactions = len([reaction for msg in chat_messages for reaction in msg.reactions])

    print(f'Total number of messages: {num_messages}')
    print(f'Total number of active days: {unique_dates}')
    print(f'Total number of words: {num_words}')
    print(f'Total number of reactions: {num_reactions}')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', type=str, required=True)
    parser.add_argument('--year', type=int, required=False, default=2020)
    parser.add_argument('--remove_names', type=str, required=False, nargs='+',
                        help='List of names (or other words, if desired) to remove, if any. '
                             'Names should be separated by spaces, like: Luke Ryan Angela')
    parser.add_argument('--plot_rel_num_str', type=str, required=False, nargs='+',
                        help='List of strings, where each string passed '
                             '(space-separated) will result in a plot showing the '
                             'relative frequency of said string (string count / total word count) '
                             'in all chat messages per person')
    parser.add_argument('--plot_reactions', type=bool, required=False, default=True,
                        help='bool. Whether to plot the reactions that were sent and received by each person.')
    parser.add_argument('--plot_share_of_messages', type=bool, required=False, default=True,
                        help='bool. Whether to plot the share of messages sent by each person.')
    parser.add_argument('--make_wordcloud', type=bool, required=False, default=True,
                        help='bool. Whether to make a wordcloud based on messages from each person. '
                             'Any names or words passed to the remove_names argument will be removed from the wordcloud.')


    args = parser.parse_args()

    in_dir, year, stop_names, plot_rel_num_str, reactions, share_of_messages, wordcloud = \
        args.in_dir, args.year, args.remove_names, args.plot_rel_num_str, \
        args.plot_reactions, args.plot_share_of_messages, args.make_wordcloud

    # Separate the words passed as the plot_rel_num_str argument
    #plot_rel_num_str = [word.strip() for word in plot_rel_num_str.lower().split(',')]
    plot_rel_num_str = [word.lower() for word in plot_rel_num_str]

    # Get the number of HTML files to process
    num_filenames = len([filename for filename in os.listdir(in_dir) if filename.endswith('.html')])

    all_messages = []

    # Go through each of the HTML files in our directory and store them in a list of ChatMessage objects
    for i in range(1, num_filenames):
        filename = f'message_{i}.html'
        filepath = os.path.join(in_dir, filename)
        with codecs.open(filepath, 'r', encoding='utf-8') as html_file:
            chat_html = html_file.read()
        messages, unique_years = get_chat_messages(chat_html, year)
        if messages:
            all_messages.extend(messages)
        elif all(y >= year for y in unique_years):
            continue
        else:
            break

    # Get the names of the individual participants in the chat
    names = np.unique([msg.sender for msg in all_messages])
    print(f'Chat participants: {names}')

    # Get the full text, which is made by concatenating text from all chat messages
    full_text = ' '.join([msg.text.lower() for msg in all_messages])

    # Get all stop words based on user input as well as most common words in full text
    word_counts = Counter(full_text.split())
    if stop_names:
        #additional_stop_words = [name.strip() for name in stop_names.lower().split(',')]
        additional_stop_words = [name.lower() for name in stop_names]
    else:
        additional_stop_words = []

    # Remove top 100 stop words plus additional (user-defined) stop words
    stop_words = set([k for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)][:100] + additional_stop_words)

    chat_messages_dict = {}
    for name in names:
            messages_sent = [msg for msg in all_messages if msg.sender == name]
            reactions_given = [reaction[0] for msg in all_messages if msg.reactions for reaction in msg.reactions if reaction[1] == name]
            reactions_received = [reaction[0] for msg in messages_sent if msg.reactions for reaction in msg.reactions]

            reactions_given_count = Counter(reactions_given)
            reactions_received_count = Counter(reactions_received)

            chat_messages_dict[name] = messages_sent
            if reactions:
                plot_reactions(name, reactions_given_count, reactions_received_count, save=True)
            if wordcloud:
                make_wordcloud(name, messages_sent, stop_words, save=True)


    print_general_stats(chat_messages=all_messages, year=year)
    if share_of_messages:
        plot_share_of_messages(chat_messages_dict)
    if plot_rel_num_str:
        for word in plot_rel_num_str:
            plot_relative_num_of_str_per_person(chat_messages_dict, word, save=True)

    plot_avg_msg_length_per_person(chat_messages_dict, save=True)



if __name__ == '__main__':
    main()