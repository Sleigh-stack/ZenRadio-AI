
import customtkinter as ctk
import requests, random, vlc

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

player=None
stations=[]
history=[]
idx=-1
instance=vlc.Instance("--no-video","--quiet")

app=ctk.CTk()
app.title("ZenRadio")
app.geometry("1200x720")

title=ctk.CTkLabel(app,text="ZenRadio",font=("Segoe UI",32,"bold"))
title.pack(pady=15)

top=ctk.CTkFrame(app,corner_radius=30)
top.pack(fill="x",padx=30,pady=10)

entry=ctk.CTkEntry(top,width=450,height=42,
placeholder_text="Search radio stations...",
corner_radius=25)
entry.pack(side="left",padx=15,pady=15)

now=ctk.StringVar(value="No station playing")

def play_station(st):
    global player,history,idx
    url=st.get("url_resolved")
    if not url: return
    if player:
        player.stop()
    player=instance.media_player_new()
    media=instance.media_new(url)
    player.set_media(media)
    player.audio_set_volume(vol.get())
    player.play()
    now.set(st.get("name","Unknown"))
    history.append(st)
    idx=len(history)-1

def search():
    global stations
    q=entry.get()
    try:
        r=requests.get(
        "https://de1.api.radio-browser.info/json/stations/search",
        params={"name":q,"limit":50,"hidebroken":"true"},
        timeout=10)
        stations=r.json()
        if stations:
            play_station(stations[0])
    except:
        now.set("Search failed")

ctk.CTkButton(top,text="Search",command=search,
corner_radius=25).pack(side="left",padx=10)

card=ctk.CTkFrame(app,width=300,height=300,corner_radius=30)
card.pack(pady=15)

album=ctk.CTkLabel(card,text="♪",font=("Segoe UI",90))
album.place(relx=.5,rely=.5,anchor="center")

ctk.CTkLabel(app,textvariable=now,
font=("Segoe UI",22,"bold")).pack()

eq=ctk.CTkFrame(app,fg_color="transparent")
eq.pack()

bars=[]
for i in range(32):
    b=ctk.CTkProgressBar(eq,width=10,height=90)
    b.pack(side="left",padx=2)
    bars.append(b)

def animate():
    for b in bars:
        b.set(random.random())
    app.after(100,animate)

animate()

controls=ctk.CTkFrame(app,corner_radius=30)
controls.pack(pady=20)

def prev():
    global idx
    if idx>0:
        idx-=1
        play_station(history[idx])

def nxt():
    if stations:
        play_station(random.choice(stations))

ctk.CTkButton(controls,text="⏮",width=60,height=60,corner_radius=30,command=prev).pack(side="left",padx=15)
ctk.CTkButton(controls,text="⏭",width=60,height=60,corner_radius=30,command=nxt).pack(side="left",padx=15)

def volume(v):
    if player:
        player.audio_set_volume(int(float(v)))

vol=ctk.CTkSlider(app,from_=0,to=100,command=volume,width=300)
vol.set(70)
vol.pack()

app.mainloop()
