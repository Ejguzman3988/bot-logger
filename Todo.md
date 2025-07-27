# LIST OF TODOS

---

- [ ] Execution

---

- [ ] Build the actual script to start the process

---

- [~] BOT CREATION

---

- [x] Create the bot image
- [~] Use rich pixels to build a bot
- [ ] Animate the bot
- [ ] Tie the bot animation to command
- [ ] Scaffold the rest of the animations
- [ ] Create animations
- [x] See if anyone has done anything similar
- [x] Figure out if this is even possible
- [x] Check what type of restrictions animations in terminal have.

---

- [ ] Brand Building

---

- [ ] Better name
- [ ] Build script for YT Video
- [ ] Update README
- [ ] Content plan?

---

## IDEA - What do I want to accomplish?

I recently created a Pokemon shiny hunting bot that I had running on twitch for the past two days while I slept. This gave me the idea to create a robot persona that will hang out with chat. Twitch stream features the game and a log explaining what is happening. Since the bot is meant to be on while I sleep I want to keep the chat company. One way is by creating bot persona that seems life like. Think of this as a log bot companion.

Terminal Gui - Bot Companion

## Why use it?

1. Keep you company.
2. Help stylize your terminal
3. Why not right?

## Features

- Bot: Randomly Generated bot avatar
- Configurable Actions
- Widgets
  - Pomodoro timer
  - Weather  
  - Log monitor
- Random Knowledge Nuggets

## MVP

**V0.1:** Create a bot avatar using rich text. Be able to interact with the bot by inserting terminal commands.

Functionality:

- Opens bot avatar into terminal window
  - `$ bot-logger`
- Can interact by sending commands
  - `$ bot-logger send <action>`
    - Adds action to the queue and triggers an animation
    - `<actions>` list for stream
      - DONATION
      - BITS
      - SUBSCRIPTIONS
      - GIFTED SUBS
      - RAID
      - HOST

**V0.1:** Creation of an animated bot and terminal window

### Must Have Features

Animated bot that lives in the terminal.

### Nice to Have

Widgets actions - tell time

Functionality:

- Tmux integration
- `<actions>` list for loggers
  - TRACE
  - DEBUG
  - INFO
  - WARN
  - ERROR
  - FATAL

### Research

Terminal Graphic GUI
Generation algorithm for pixel art
