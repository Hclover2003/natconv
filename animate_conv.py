import tkinter as tk
import pandas as pd

def load_chat_logs(filename):
    chat_logs = pd.read_csv(filename)
    return chat_logs

def create_chat_gui(chat_logs, survey):
    root = tk.Tk()
    root.title("Chat Logs")
    
   # Get the screen width
    screen_width = root.winfo_screenwidth()

    # Set the window size to the full width of the screen
    root.geometry(f"{screen_width-20}x600")
    
    # Define speaker colors
    speaker1, speaker2 = chat_logs['speaker'].unique()
    speaker_colors = {speaker1: 'blue', speaker2: 'red'}

    # Create a Frame to hold the chat logs
    chat_frame = tk.Frame(root)
    chat_frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas to display the chat logs
    chat_canvas = tk.Canvas(chat_frame)
    chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the chat canvas
    scrollbar = tk.Scrollbar(chat_frame, command=chat_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_canvas.config(yscrollcommand=scrollbar.set)

    # Create a frame to hold the chat messages
    chat_messages_frame = tk.Frame(chat_canvas)
    chat_canvas.create_window((0, 0), window=chat_messages_frame, anchor=tk.NW)

    conversationalist1 = survey[survey["partner_id"] == speaker1].iloc[0]["conversationalist"]
    conversationalist2 = survey[survey["partner_id"] == speaker2].iloc[0]["conversationalist"]

    # Add title
    title_label1 = tk.Label(root, text=f"Speaker 1: {conversationalist1}  (rating by Speaker 2) | Backchannels Given: {chat_logs[chat_logs['speaker'] == speaker1]['backchannel_count'].sum()}", font=("Arial", 16, "bold"), fg=speaker_colors.get(speaker1, 'black'))
    title_label1.pack()
    title_label2 = tk.Label(root, text=f"Speaker 2: {conversationalist2} (rating by Speaker 1) | Backchannels Given: {chat_logs[chat_logs['speaker'] == speaker2]['backchannel_count'].sum()}", font=("Arial", 16, "bold"), fg=speaker_colors.get(speaker2, 'black'))
    title_label2.pack()



    # Add chat logs to the GUI
    for i, log in chat_logs.iterrows():
        speaker = log['speaker']
        message = log['utterance']
        backchannel = log['backchannel']

        message_frame = tk.Frame(chat_messages_frame, padx=5, pady=5)
        message_frame.pack(fill=tk.X)

        speaker_label = tk.Label(message_frame, text=f"Speaker {(i%2)+1}", font=("Arial", 12, "bold"), fg=speaker_colors.get(speaker, 'black'))
        speaker_label.pack(anchor=tk.W)

        message_label = tk.Label(message_frame, text=message, font=("Arial", 12), wraplength=int(root.winfo_screenwidth() / 2))
        message_label.pack(side=tk.LEFT)

        backchannel_label = tk.Label(message_frame, text=backchannel, font=("Arial", 12), fg="gray")
        backchannel_label.pack(side=tk.RIGHT)

    # Configure canvas scrolling
    chat_messages_frame.bind("<Configure>", lambda event: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
    chat_canvas.bind("<Configure>", lambda event: chat_canvas.itemconfigure(chat_messages_frame, width=event.width))

    # Run the GUI main loop
    root.mainloop()


# TODO: Change to conversation of interest
conv_id = "07b732f9-a9e0-43e9-85a4-263a6d78af0d" # Change this to the conversation ID you want to visualize
filename = f"low_conv/{conv_id}_transcript_backbiter.csv" # Change folder to "high_conv" for highly ranked conversations

# Run the GUI
chat_logs = load_chat_logs(filename)
combined_survey = pd.read_csv("survey_full.csv")
survey = combined_survey[combined_survey["conversation"] == conv_id].copy()
create_chat_gui(chat_logs, survey)
