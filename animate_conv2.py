import tkinter as tk
import pandas as pd
import sys
import re
import time
import random

class BackchannelChat:
    def __init__(self, root, filename, survey):
            """
            Create the image gallery
            """
            self.root = root
            self.chat_logs = pd.read_csv(filename)
            self.survey = survey
            self.chat_frame = None
            self.chat_canvas = None
            self.chat_messages_frame = None
            self.current_message = 1
            self.typing_box = None
            self.send_btn = None
            self.backchannel_frame = None
            self.backchannel_text=None
            
            self.backchannel_frame = tk.Frame(root, height=200, pady=20)
            self.backchannel_frame.pack(fill=tk.BOTH, expand=False)
            bot_icon = tk.Label(self.backchannel_frame, text="Bot")
            bot_icon.pack(side=tk.LEFT)
            self.backchannel_text = tk.Label(self.backchannel_frame, text="hello I'm  a bot", font="Arial 16 bold")
            self.backchannel_text.pack(side=tk.LEFT)
            
            # Create a Frame to hold the chat logs
            self.chat_frame = tk.Frame(root, width=2000)
            self.chat_frame.pack(fill=tk.X, expand=True)

            # Create a canvas to display the chat logs
            self.chat_canvas = tk.Canvas(self.chat_frame, height=500, width=1500)
            self.chat_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
            # Create a scrollbar for the chat canvas
            scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.chat_canvas.config(yscrollcommand=scrollbar.set)
            
            self.chat_messages_frame = tk.Frame(self.chat_canvas)
            self.chat_canvas.create_window((0, 0), window=self.chat_messages_frame, anchor="nw")
            self.chat_messages_frame.bind("<Configure>", lambda event: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

            self.typing_box = tk.Text(root, bg="white", height=10)
            self.typing_box.pack(fill=tk.X)
            self.send_btn = tk.Button(root, text="Send")
            self.send_btn.pack() 
            
            # Define speaker colors
            speaker1, speaker2 = self.chat_logs['speaker'].unique()
            self.speaker_colors = {speaker1: 'blue', speaker2: 'red'}

            conversationalist1 = self.survey[(self.survey["partner_id"] == speaker1) & (self.survey["user_id"] == speaker2)].iloc[0]["conversationalist"]
            conversationalist2 = self.survey[(self.survey["partner_id"] == speaker2) & (self.survey["user_id"] == speaker1)].iloc[0]["conversationalist"]

            # Add title
            title_label1 = tk.Label(root, text=f"Speaker 1: {conversationalist1}  (rating by Speaker 2) | Backchannels Given: {chat_logs[chat_logs['speaker'] == speaker2]['backchannel_count'].sum()}", font=("Arial", 16, "bold"), fg=self.speaker_colors.get(speaker1, 'black'))
            title_label1.pack()
            title_label2 = tk.Label(root, text=f"Speaker 2: {conversationalist2} (rating by Speaker 1) | Backchannels Given: {chat_logs[chat_logs['speaker'] == speaker1]['backchannel_count'].sum()}", font=("Arial", 16, "bold"), fg=self.speaker_colors.get(speaker2, 'black'))
            title_label2.pack()
            
            self.load_msg(self.chat_logs.iloc[self.current_message])
            root.bind('<Right>', lambda event: self.type_msg(self.chat_logs.iloc[self.current_message]))
            root.bind('<Return>', lambda event: self.send_msg())
    
    def type_msg(self, message):
        self.typing_box.delete('1.0', tk.END)
        for i in range(len(message['utterance'])):
            self.typing_box.insert(tk.END, message['utterance'][i])
            self.typing_box.update()
            if i%20 == 0:
                pause = random.uniform(0, 1)
                if pause > 0.9:
                    pause = 1
            else:
                pause = 0.01
            time.sleep(pause)
        
    def next_msg(self):
        self.current_message +=1
        self.load_msg(self.chat_logs.iloc[self.current_message])
        
    def send_msg(self):
        self.typing_box.delete('1.0', tk.END)
        self.next_msg()
        self.next_msg()
        
    def load_msg(self, log):
        speaker = log['speaker']
        message = log['utterance']
        
        message_frame = tk.Frame(self.chat_messages_frame, padx=5, pady=5, highlightthickness=10, highlightbackground="green")
        speaker_label = tk.Label(message_frame, text=f"Speaker {speaker}", font=("Arial", 12, "bold"), fg=self.speaker_colors.get(speaker, 'black'))
        message_label = tk.Label(message_frame, text=message, font=("Arial", 12), wraplength=int(root.winfo_screenwidth() * 0.3))
        
        if speaker == list(self.speaker_colors.keys())[1]:
            message_frame.pack(fill=tk.X)
            speaker_label.pack(anchor=tk.W)
            message_label.pack(side=tk.LEFT)  
        else:
            message_frame.pack(fill=tk.X)
            speaker_label.pack(anchor=tk.E)
            message_label.pack(side=tk.RIGHT)     
        
        self.chat_canvas.yview_moveto('1.0')
        print(log["backchannel"])
        print(type(log["backchannel"]))
        if (log["backchannel"] != "nan") and (type(log["backchannel"]) == str) and(speaker == list(self.speaker_colors.keys())[1]):
            print()
            for i in range(len(log["backchannel"])):
                self.backchannel_text.config(text=log["backchannel"][:i])
                self.backchannel_frame.update()
                time.sleep(0.1)
    # def load_chat_logs(self):
    #     # Add chat logs to the GUI
    #     for i, log in chat_logs.iterrows():
    #         speaker = log['speaker']
    #         message = log['utterance']
    #         backchannel = log['backchannel']

    #         message_frame = tk.Frame(self.chat_messages_frame, padx=5, pady=5)
    #         message_frame.pack(fill=tk.X)

    #         speaker_label = tk.Label(message_frame, text=f"Speaker {(i%2)+1}", font=("Arial", 12, "bold"), fg=self.speaker_colors.get(speaker, 'black'))
    #         speaker_label.pack(anchor=tk.W)

    #         message_label = tk.Label(message_frame, text=message, font=("Arial", 12), wraplength=int(root.winfo_screenwidth() * 0.3))
    #         message_label.pack(side=tk.LEFT)

    #         backchannel_label = tk.Label(message_frame, text=backchannel, font=("Arial", 12), fg="gray",  wraplength=int(root.winfo_screenwidth() * 0.4))
    #         backchannel_label.pack(side=tk.RIGHT)


# TODO: Change to conversation of interest
filename = sys.argv[1]

match = re.search(r'([a-fA-F\d]{8}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{12})', filename)

if match:
    conv_id = match.group(1)
else:
    conv_id = "754240f9-69ef-481c-8484-3de526bf96a3"
    print("No conversation ID found in filename. Using default conversation ID.")
# Run the GUI
# chat_logs = load_chat_logs(filename)
transcript_df = pd.read_csv("all_transcripts_with_sentiment.csv")
chat_logs = transcript_df[transcript_df["conversation"] == conv_id].copy()
combined_survey = pd.read_csv("survey_full.csv")
survey = combined_survey[combined_survey["conversation"] == conv_id].copy()

root = tk.Tk()
root.title("Backchannel Chat")
root.geometry("1000x800")

# Create the image gallery
chat = BackchannelChat(root, filename, survey)
root.mainloop()
