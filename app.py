import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
import os
import time
import joblib
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()
root.title("Revaton - Anomaly Detection")
# bg_img = tk.PhotoImage(file="img/header2.png")
bg_img = Image.open("img/header2.png")


canvas_width = 1920
canvas_height = 1080
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
bg_img = bg_img.resize((canvas_width, canvas_height), Image.ANTIALIAS)
bg_img = ImageTk.PhotoImage(bg_img)
canvas.create_image(canvas_width/2, canvas_height/2, image=bg_img)

knn = joblib.load('knn_model.pkl')


def files(data):
    with open('flags.txt', 'a') as f:
        f.write(str(data['src_ip']))

# def create_frame(data1, data2):
#     frame1 = tk.Frame(root, bg="#ffffff", width=1920, height=1080)
#     frame1.place(relx=0.5, rely=0.5, anchor="center")
#     label = tk.Label(frame1, text="Anomaly Detected", bg="white", fg='black',
#                      font=("Arial", 12))
#     label.place(relx=0.5, rely=0.5, anchor='center')
#     label.pack(side='top')
#     # label = tk.Lyabel(frame1, text=data1, bg="#00FEFB", fg="black", font=("Arial", 12), width=90, height=10)
#     # label.pack(side= tk.RIGHT)
#     tree = ttk.Treeview(frame1, columns=list(data1.columns), show='headings')
#     tree.pack(side='right', fill='both', padx=(10, 10))

#     for col in data1.columns:
#         tree.heading(col, text=col)

#     for idx, row in data1.iterrows():
#         tree.insert('', 'end', values=list(row))

#     # Create a figure and add subplots
#     fig = Figure(figsize=(8, 10))
#     ax1 = fig.add_subplot(222)
#     ax2 = fig.add_subplot(212)
#     fig.set_facecolor('lightgray')
#     ax1.set_facecolor('white')

#     # Add pie chart to the first subplot
#     value_counts = data2['src_ip'].value_counts()
#     percentages = 100 * value_counts / len(data2)
#     ax1.pie(percentages, labels=percentages.index, autopct='%1.1f%%',
#             startangle=90, colors=sns.color_palette('bright'), textprops={'fontsize': 8})
#     ax1.axis('equal')
#     ax1_title = ax1.set_title('Source IP Distribution',
#                               fontsize=12, fontweight='bold')

#     ax1.set_position([0.125, 0.725, 0.775, 0.2])
#     ax1_title.set_position([0.5, 0])
#     ax1.set_aspect('equal')
#     ax1.set_xlim(-0.8, 0.8)
#     ax1.set_ylim(-1.5, 1.5)

#     # Add histogram to the second subplot
#     # sns.lineplot(data=data2, x='timestamp', y='pkt_size_avg',
#     #                color='darkorange', ax=ax2)
#     # ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
#     # ax2.set_title('Packet Size Distribution', fontsize=14, fontweight='bold')
#     # ax2.set_xlabel('Timestamp', fontsize=12, rotation=45)
#     # ax2.set_ylabel('Packet Size (bytes)', fontsize=12,)
#     sns.histplot(data=data2, x='timestamp', y='pkt_size_avg', bins=20,
#                  cmap='coolwarm', edgecolor='black', alpha=0.8, color='darkorange', ax=ax2)
#     ax2.set_title('Packet Size Distribution', fontsize=14, fontweight='bold')
#     ax2.set_xlabel('Timestamp', fontsize=12)
#     ax2.set_ylabel('Packet Size (bytes)', fontsize=12)
#     plt.show()

#     ax2.set_position([0.125, 0.325, 0.775, 0.2])
#     ax2.set_aspect('equal')
#     ax2.set_xlim(-0.1, 0.2)
#     ax2.set_ylim(-0.1, 0.2)

#     # Create a canvas to display the figure
#     canvas = FigureCanvasTkAgg(fig, master=frame1)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.LEFT)

#     button3 = tk.Button(root, text="Flag", bg="red", fg="black", font=(
#     "Jakarta Sans", 12), width=15, height=2, command=files(data1), borderwidth=6)
#     button3.place(relx=0.59, rely=0.55, anchor="center")


def create_frame(data1, data2):

    frame1 = tk.Frame(root, bg="#ffffff", width=1600, height=800)
    frame1.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(frame1, text="Anomaly Detected", bg="white", fg='black',
                     font=("Arial", 20, 'bold'))
    label.pack(side='top', pady=20)

    # Create a scatterplot of flow_iat_std vs. flow_iat_min
    flow_iat_std = data2['flow_iat_std']
    flow_iat_min = data2['flow_iat_min']

    # Create a grid of subplots with 2 rows and 1 column
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

    # Create the scatter plot in the top subplot
    ax1.scatter(flow_iat_std, flow_iat_min)
    ax1.set_xlabel('flow_iat_std', fontsize=12)
    ax1.set_ylabel('flow_iat_min', fontsize=12)
    ax1.set_title('Scatterplot of flow_iat_std vs. flow_iat_min', fontsize=10)
    ax1.tick_params(labelsize=12)

    # Create the line graph in the bottom subplot
    flow_byts_s = data2['flow_byts_s']
    totlen_fwd_pkts = data2['totlen_fwd_pkts']
    ax2.plot(flow_byts_s, label='Flow Bytes/s')
    ax2.plot(totlen_fwd_pkts, label='Total Length of Fwd Packets')
    ax2.set_xlabel('Timestamp', fontsize=12)
    ax2.set_ylabel('Flow Bytes/s', fontsize=12)
    ax2.set_title(
        'Line Graph of Flow Bytes/s and Total Length of Fwd Packets', fontsize=10)
    # ax2.legend(fontsize=12)
    ax2.tick_params(labelsize=12)

    # Adjust spacing between subplots and save the figure
    plt.tight_layout()

    fig.subplots_adjust(left=0.5, right=0.9)

    # Create a canvas to display the graphs
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, padx=50)

    # Create a table with the first 5 rows of data1
    tree = ttk.Treeview(frame1, columns=list(data1.columns), show='headings')
    tree.pack(side='right', fill='both', padx=(10, 10))

    for col in data1.columns:
        tree.heading(col, text=col)

    for idx, row in data1.iterrows():
        tree.insert('', 'end', values=list(row))

    # Create a button to flag the file

    button3 = tk.Button(frame1, text="Flag", bg="red", fg="white", font=(
        "Arial", 14, 'bold'), width=10, height=2, command=files(data1))
    button3.pack(side='bottom', pady=20)


def infer():
    num_rows_processed = 0
    result = pd.DataFrame(columns=['prediction'])
    while True:
        # Load the CSV file using pandas
        df = pd.read_csv('flows.csv')

        # Extract the new rows that have been added since the last prediction
        df_new = df.iloc[num_rows_processed:]

        df_new_copy = df_new.copy()

        if len(df_new) > 0:
            # Extract the required 7 features
            features = [
                "bwd_pkt_len_std",
                "flow_byts_s",
                "totlen_fwd_pkts",
                "fwd_pkt_len_std",
                "flow_iat_std",
                "flow_iat_min",
                "fwd_iat_tot"
            ]
            X_new = df_new[features].values
            y_pred = knn.predict(X_new)
            result = result.append(pd.DataFrame(
                y_pred, columns=['prediction']))
            rows_with_pred = result.loc[result['prediction'] == 1].index
            columns_to_extract = ['timestamp', 'src_ip',
                                  'dst_ip', 'src_port', 'dst_port', 'protocol']
            fin_data = df_new.loc[rows_with_pred, columns_to_extract]
            num_rows_processed += len(df_new)
            return fin_data, df_new_copy
        time.sleep(300)


def get_data():
    # subprocess.Popen(["x-terminal-emulator", "-e",
    #                  "sudo cicflowmeter -i wlp4s0 -c flows.csv; exec bash"])
    label_alert = tk.Label(root, text="Alert", bg="#00FEFB", fg="black")
    label_alert.pack(pady=20)
    # time.sleep(300)
    fin_data, df_new_copy = infer()
    create_frame(fin_data, df_new_copy)


def acl():
    subprocess.Popen(["x-terminal-emulator", "-e", "./acl.sh"])


# button
button1 = tk.Button(root, text="Start Tracking", bg="#00FEFB", fg="black", font=(
    "Jakarta Sans", 12), width=15, height=2, command=get_data, borderwidth=6)

button2 = tk.Button(root, text="Access Control", bg="#00FEFB", fg="black", font=(
    "Jakarta Sans", 12), width=15, height=2, command=acl, borderwidth=6)

button1.place(relx=0.43, rely=0.55, anchor="center")

button2.place(relx=0.59, rely=0.55, anchor="center")


root.mainloop()
