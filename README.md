pytchat
=======

pytchat is a python library for fetching youtube live chat.

## Description
pytchat is a python library for fetching youtube live chat
without using youtube api, Selenium or BeautifulSoup.

Other features:
+ Customizable chat data processors including yt api compatible one.
+ Available on asyncio context. 
+ Quick fetching of initial chat data by generating continuation params
instead of web scraping.

For more detailed information, see [wiki](https://github.com/taizan-hokuto/pytchat/wiki).

## Install
```python
pip install pytchat
```
## Demo
![demo](https://taizan-hokuto.github.io/statics/demo.gif "demo")

## Examples
### on-demand mode
```python
from pytchat import LiveChat

chat = LiveChat("G1w62uEMZ74")
while chat.is_alive():
    data = chat.get()
    for c in data.items:
        print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
        data.tick()
```

### callback mode
```python
from pytchat import LiveChat
import time

def main()
    chat = LiveChat("G1w62uEMZ74", callback = func)
    #other background operation.
   
#callback function is automatically called periodically.
def func(data):
    for c in data.items:
        print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
        data.tick()
```

### asyncio context:
```python
from pytchat import LiveChatAsync
import asyncio

async def main():
    chat = LiveChatAsync("G1w62uEMZ74", callback = func)
    #other background operation.

#callback function is automatically called periodically.
async def func(data):
    for c in data.items:
        print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
        await data.tick_async()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


### youtube api compatible processor:
```python
from pytchat import LiveChat, CompatibleProcessor

chat = LiveChat("G1w62uEMZ74", 
     processor = CompatibleProcessor() )

while chat.is_alive():
    data = chat.get()
    polling = data["pollingIntervalMillis"]/1000
    for c in data["items"]:
        if c.get("snippet"):
            print(f"[{c['authorDetails']['displayName']}]"
                    f"-{c['snippet']['displayMessage']}")
            time.sleep(polling/len(data["items"]))

```
### replay:
```python
from pytchat import ReplayChatAsync
import asyncio

async def main():
    chat = ReplayChatAsync("G1w62uEMZ74", seektime = 1000, callback = func)
        #other background operation here.

#callback function is automatically called periodically.
async def func(data):
    for count in range(0,len(data.items)):
        c= data.items[count]
        if count!=len(data.items):
            tick=data.items[count+1].timestamp -data.items[count].timestamp
        else:
            tick=0
        print(f"<{c.elapsedTime}> [{c.author.name}]-{c.message} {c.amountString}")
        await asyncio.sleep(tick/1000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Structure of Default Processor
Each item can be got with items() function.
<table>
  <tr>
    <th>name</th>
    <th>type</th>
    <th>remarks</th>
  </tr>
  <tr>
    <td>type</td>
    <td>str</td>
    <td>"superChat","textMessage","superSticker","newSponsor"</td>
  </tr>
  <tr>
    <td>id</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>message</td>
    <td>str</td>
    <td>emojis are represented by ":(shortcut text):"</td>
  </tr>
  <tr>
    <td>messageEx</td>
    <td>str</td>
    <td>list of message texts and emoji URLs.</td>
  </tr>
  <tr>
    <td>timestamp</td>
    <td>int</td>
    <td>unixtime milliseconds</td>
  </tr>
  <tr>
    <td>datetime</td>
    <td>str</td>
    <td>ex. "2019-10-10 12:34:56"</td>
  </tr>
    <td>elapsedTime</td>
    <td>str</td>
    <td>elapsed time. (ex. "1:02:27") *Replay Only.</td>
  </tr>
  <tr>
    <td>amountValue</td>
    <td>float</td>
    <td>ex. 1,234.0</td>
  </tr>
  <tr>
    <td>amountString</td>
    <td>str</td>
    <td>ex. "$ 1,234"</td>
  </tr>
  <tr>
    <td>currency</td>
    <td>str</td>
    <td><a href="https://en.wikipedia.org/wiki/ISO_4217">ISO 4217 currency codes</a> (ex. "USD")</td>
  </tr>
  <tr>
    <td>bgColor</td>
    <td>int</td>
    <td>RGB Int</td>
  </tr>
  <tr>
    <td>author</td>
    <td>object</td>
    <td>see below</td>
  </tr>
</table>

Structure of author object.
<table>
  <tr>
    <th>name</th>
    <th>type</th>
    <th>remarks</th>
  </tr>
  <tr>
    <td>name</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>channelId</td>
    <td>str</td>
    <td>*chatter's channel ID. NOT broadcasting video's channel ID.</td>
  </tr>
  <tr>
    <td>channelUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>imageUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>badgeUrl</td>
    <td>str</td>
    <td></td>
  </tr>
  <tr>
    <td>isVerified</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatOwner</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatSponsor</td>
    <td>bool</td>
    <td></td>
  </tr>
  <tr>
    <td>isChatModerator</td>
    <td>bool</td>
    <td></td>
  </tr>
</table>

## Licence

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

## Author

[taizan-hokuto](https://github.com/taizan-hokuto)

[twitter:@taizan205](https://twitter.com/taizan205)