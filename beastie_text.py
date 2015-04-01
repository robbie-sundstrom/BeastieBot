from gtts import gTTS 

lyrics = """Well Now dont you tell me to smile 
You stick around Ill make it worth your while
Got numbers beyond what you can dial
Maybe its because I'm so versatile
Style profile I said
It always brings me back when I hear Ooh Child
From the Hudson River out to the Nile
I run the marathon til the very last mile
If you battle me I will revile
People always say my style is wild
Youve got gall youve got guile
To step to me Im a rapophile
If you want to battle your in denial
Coming from Uranus to check my style
Go ahead put my rhymes on trial
Cast you off into exile"""

tts = gTTS(text=lyrics)
tts.save('intergalactic.mp3')