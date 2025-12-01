# Description 
shows a preview of the output content
# Default behavior
it shows five line of the file after creating output
```
>>> lrcstack sheet ".\lyrics.lrc" -a "translation.txt"
Sheet created: .\lyrics.csv

[00:10.92] | 嗚呼、陶酔の極み、悦に浸り右左         | Ah—intoxicated to the core, lost in delight, swaying left and right|
[00:13.66] | 虚構で埋まるキャパシティ              | A mind filled to capacity with fiction|
[00:15.07] | QWERTYだけが武器らしい←リアリティ、笑  | The only weapon left — a QWERTY keyboard. How real, huh? lol|
[00:17.15] | んで何、お前だけが正しい？            | And what, you think you're the only one who's right?
[00:19.36] | 虚しいね、不完全を肯定できないエゴの塊  | How empty. Just a lump of ego unable to embrace imperfection
...
```

```
>>> lrcstack stack ".\lyrics.csv" -s
Stacked to: .\lyrics_stacked.lrc

[00:10.92]嗚呼、陶酔の極み、悦に浸り右左
[00:10.92]Ah—intoxicated to the core, lost in delight, swaying left and right
[00:13.66]虚構で埋まるキャパシティ
[00:13.66]A mind filled to capacity with fiction
[00:15.07]QWERTYだけが武器らしい←リアリティ、笑
[00:15.07]The only weapon left — a QWERTY keyboard. How real, huh? lol
[00:17.15]んで何、お前だけが正しい？
[00:17.15]And what, you think you're the only one who's right?
[00:19.36]虚しいね、不完全を肯定できないエゴの塊
[00:19.36]How empty. Just a lump of ego unable to embrace imperfection
...
```

# Using `--preview` or `-p`
before creating the file, shows a preview to confirm.

```
>>> lrcstack sheet ".\lyrics.lrc" -a "translation.txt" -p
Preview:

[00:10.92] | 嗚呼、陶酔の極み、悦に浸り右左         | Ah—intoxicated to the core, lost in delight, swaying left and right|
[00:13.66] | 虚構で埋まるキャパシティ              | A mind filled to capacity with fiction|
[00:15.07] | QWERTYだけが武器らしい←リアリティ、笑  | The only weapon left — a QWERTY keyboard. How real, huh? lol|
[00:17.15] | んで何、お前だけが正しい？            | And what, you think you're the only one who's right?
[00:19.36] | 虚しいね、不完全を肯定できないエゴの塊  | How empty. Just a lump of ego unable to embrace imperfection
...

Do you want to wirte it to .\lyrics.csv? (Y/n)
```
### conflict
currently `--parenthesis` is using `-p` which needs to be changed before this feature is implemented. Thinking of `--enclose` and `-e`
# Using `--verbosity` or `-v`
Shows a full preview

```
>>> lrcstack stack ".\lyrics.csv" -s -p -v
Preview:

[00:10.92]嗚呼、陶酔の極み、悦に浸り右左
[00:10.92]Ah—intoxicated to the core, lost in delight, swaying left and right
[00:13.66]虚構で埋まるキャパシティ
[00:13.66]A mind filled to capacity with fiction
[00:15.07]QWERTYだけが武器らしい←リアリティ、笑
[00:15.07]The only weapon left — a QWERTY keyboard. How real, huh? lol
[00:17.15]んで何、お前だけが正しい？
[00:17.15]And what, you think you're the only one who's right?
[00:19.36]虚しいね、不完全を肯定できないエゴの塊
[00:19.36]How empty. Just a lump of ego unable to embrace imperfection
[00:21.80]「コレ、ソレが絶対正解です！」
[00:21.80]"This, that — is the absolute answer!"
[00:23.27]とかなんとか宣っては毎日
[00:23.27]So you preach every day
[00:24.63]Hyperなフロントを切り売り
[00:24.63]Selling off your hyper front
[00:25.81]責任は一切合切放置
[00:25.81]Leaving all responsibility behind
[00:27.47]表層だけ一人前に掬ってる
[00:27.47]Skimming just the surface like a pro
[00:28.95]データコレクターの道理
[00:28.95]The logic of a data collector—
[00:30.32]とうに、轢き回すだけ回され
[00:30.32]Already dragged, spun, and chewed up
[00:31.50]荒れた00世代の矜持
[00:31.50]That's the pride of our worn-out Gen 00
[00:33.65]心中を綴るには困る
[00:33.65]It's hard to pour my heart out
[00:35.02]どうにも狭すぎる余白
[00:35.02]The margin's too narrow to contain it
[00:36.47]杞憂では済まなそうな
[00:36.47]Can't be shrugged off as "just anxiety."
[00:37.71]ブルータリティな社会を咀嚼
[00:37.71]This brutal society
[00:39.16]靭性ないメンタリティで
[00:39.16]With a fragile mentality
[00:40.59]人生の色をブルーに焦がす
[00:40.59]I burn my life's colors into blue
[00:42.10]現在地も不明なまま
[00:42.10]Still unsure where I am
[00:43.17]偶然できた道を進む
[00:43.17]I walk down a road born by coincidence
[00:44.30]Fallible
[00:44.30]Fallible
[00:47.23]Fallible
[00:47.23]Fallible
[00:50.01]Fallible
[00:50.01]Fallible
[00:52.71]Fallible
[00:52.71]Fallible
[00:54.38]In life's gamble, we are fallible
[00:54.38]In life's gamble, we are fallible
[00:58.40]Fallible
[00:58.40]Fallible
[01:01.25]Fallible
[01:01.25]Fallible
[01:04.25]Fallible
[01:04.25]Fallible
[01:05.56]In life's gamble, we are fallible
[01:05.56]In life's gamble, we are fallible
[01:07.25]何かに宿る正しさなんて
[01:07.25]The "truth" that dwells in something
[01:08.89]本当は無いんだって
[01:08.89]There is no such thing
[01:09.92]在るものじゃなく祈るものなんだって
[01:09.92]It's not something that exists—it's something we pray for
[01:11.33]今だって、「正しくあれ」と祈っているから
[01:11.33]Even now, I'm still praying, "Let me be right."
[01:13.63]0からやっていくから
[01:13.63]Starting again from zero
[01:15.18]全部抱えていくから
[01:15.18]Carrying everything on my back
[01:16.53]その上を怖がらず行くから
[01:16.53]Still, I'll walk forward—unafraid
[01:18.90]常に見直していく自分のやり方
[01:18.90]Constantly re-examining the way I live
[01:20.92]Ey 反対側に居る奴も受け入れるこの在り方
[01:20.92]Ey, even those on the opposite side—I'll try to accept them too
[01:23.83]嗚呼、喧騒の最中にあるこの心臓
[01:23.83]Ah, in the middle of all this chaos, I draw willpower from this heart
[01:25.99]から汲んでいく意志
[01:25.99]Living with contradictions—
[01:27.07]矛盾と共存していく00世代の矜持
[01:27.07]That's the pride of our Gen 00
[01:29.52]
[01:52.15]心中を綴るには困る
[01:52.15]It's hard to pour my heart out
[01:53.79]どうにも狭すぎる余白
[01:53.79]The margin's too narrow to contain it
[01:55.03]杞憂では済まなそうな
[01:55.03]Can't be shrugged off as "just anxiety."
[01:56.28]ブルータリティな社会を咀嚼
[01:56.28]This brutal society
[01:57.76]靭性ないメンタリティで
[01:57.76]With a fragile mentality
[01:59.05]人生の色をブルーに焦がす
[01:59.05]I burn my life's colors into blue
[02:00.73]現在地も不明なまま
[02:00.73]Still unsure where I am
[02:01.85]偶然できた道を進む
[02:01.85]I walk down a road born by coincidence
[02:03.24]探している、この心臓の向く方向を
[02:03.24]Searching—for where this heart points
[02:07.90]ただただ願っている、いつか肯定できるように
[02:07.90]Simply wishing—that someday I can accept it all
[02:14.26]ハロー、知らず失った灯よ
[02:14.26]Hello, the light I lost without knowing
[02:17.77]忘れてしまった視界よ
[02:17.77]Hello, the vision I've long forgotten
[02:20.51]何も分からなくなった今も
[02:20.51]Even now, lost in confusion
[02:23.08]祈りだけは変わらず響いている
[02:23.08]Only my prayer still rings true
[02:46.56]In life's gamble, we are fallible
[02:46.56]In life's gamble, we are fallible
[02:50.81]Fallible
[02:50.81]Fallible
[02:53.54]Fallible
[02:53.54]Fallible
[02:56.41]Fallible
[02:56.41]Fallible
[02:57.97]In life's gamble, we are fallible
[02:57.97]In life's gamble, we are fallible
[02:59.59]

Do you want to write it to .\lyrics_stacked.lrc? (Y/n)
```