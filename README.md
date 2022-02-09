# chat_wrapped
Create summaries, stats, and visualizations of your Facebook Messenger chats! This program allows you to make the plots, wordclouds, and descriptive statistics you need in order to make your "Groupchat Wrapped 2021"

To run the program, you need to first download your data from Facebook, including chat messages. You only need to keep the folder containing the HTML files of text from the chats (i.e., not the media folders). 

The program accepts the following arguments: \
--in_dir :: (required) specify the path of the folder that contains your HTML files with messenger chats \ 
--year :: (optional) specify which year you want a summary of (default is 2021) \ 
--remove_names :: (optional) specify any names or words you want removed from the statistics, for example proper names if you want to anonymize wordclouds. \
    Example: --remove_names Luke Anakin Obi-Wan\
--plot_rel_num_str :: (optional) list of strings for which you want to plot the relative frequency (string count / total word count) of said string for each person in the chat.\
--plot_reactions :: (optional) boolean - whether to create a plot of reactions sent and received by each person. Default is True.\
Example reaction plot: \
![inga_reactions](https://user-images.githubusercontent.com/56589996/153199740-ef9b99f7-68be-4972-a728-9d27924ea427.png)
The fonts in matplotlib do not support emoji encodings, but the program will print emojis that can easily be added to the plots.

--plot_share_of_messages :: (optional) boolean - whether to create a plot showing the share of messages sent by each person. Default is True.\
Example plot: \
![share_of_messages](https://user-images.githubusercontent.com/56589996/153200666-e317ed85-9ffc-4cc5-8430-0c578520847a.png)


--make_wordcloud :: (optional) boolean - whether to create a wordcloud based on chat messages from each person in the chat. Default is True. \
Example wordcloud: \
![inga_wordcloud](https://user-images.githubusercontent.com/56589996/153200838-4274c281-3c87-4bd7-924a-47667fb59800.png)


\ \

All plots will be saved automatically
