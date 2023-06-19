- `low_conv`: selection of 20 conversations that were ranked in lower quantile
- `high_conv`: selection of 20 conversations that were ranked in upper quantile
- `full_survey.csv`: combined results from surveys for all conversations
- `animate_conv.py`: simple GUI to visualize chat logs for qualitative review
  - To use, change conversation id to conversation id of conversation you want to visualize
  - Then, run `python3 animate_conv.py` or `python animate_conv.py`
  - Will get something like this: 
  - <img width="1285" alt="Screen Shot 2023-06-19 at 12 38 11 AM" src="https://github.com/Hclover2003/natconv/assets/46469244/a877de59-cd62-4be6-b11a-cd40e43c112d">
  - On right is backchannels given, on left is message. On bottom is summary: the conversationalist rating given to the two speakers (conversationalist = what you would rank the person you talked to out of top 100 people. 0 is lowest, 100 is highest), and the backchannel given for each.

