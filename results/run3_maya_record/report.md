# Run 3 · Maya pilot (voice v0.1) · stage 1: Orpheus recording + Gate 1

Voice: **tara** · lines: 300 · takes: 2 (+3 retry for lines with none passing)
Recording: 26.9 min for 53.3 min of audio (1.98× real time)
Lines with a kept take: **266/300** · kept audio: 19.9 min

## Per row

| row | kept | takes made | rejected | reject rate | pace kept (words/s, mean · max) | emotion model agrees (kept) |
|---|---|---|---|---|---|---|
| normal | 62/75 | 201 | 101 | 50% | 2.49 · 3.18 | 0/62 |
| bright | 69/75 | 174 | 53 | 30% | 2.27 · 3.16 | 0/69 |
| low | 68/75 | 171 | 50 | 29% | 2.28 · 3.08 | 2/68 |
| tense | 67/75 | 186 | 71 | 38% | 2.32 · 3.13 | 67/67 |

Reasons for rejection: words 193, rushed 82, dragging 15, voice drift 10

Speaker similarity (passing takes): mean 0.952, sd 0.029, min 0.757; drift-rejected: 10
Emotion recogniser (superb wav2vec2 ER, 4 classes neu/hap/sad/ang): measured only in this run; it picks between passing takes.

Option B v1 (pause marks follow the acting): 36/266 kept lines changed; 230 unchanged.

## Lines with no kept take

- m3n01 (normal): I work at the café in the evenings, so I study in the mornings.
- m3n07 (normal): The café was quiet this afternoon, so I watched the people outside.
- m3n21 (normal): Here's one way to say it: "Usually I get up at six, but today I slept late."
- m3n24 (normal): Sam's mum is home with the baby now, and everyone's helping.
- m3n29 (normal): I took a photo of the sea this evening, and the colours were beautiful.
- m3n32 (normal): Meanwhile, Priya was on the phone with her mum, so I cooked dinner.
- m3n34 (normal): The train leaves at seven thirty, and the ticket is four hundred and fifty rupees.
- m3n39 (normal): Really?
- m3n41 (normal): My shift starts at five, so I usually eat something light before work.
- m3n51 (normal): Hmm… so what did your mum say about that?
- m3n57 (normal): Let's practise this one together. I'll say it, and you repeat it.
- m3n60 (normal): Think about it for a moment, and then tell me what you'd do.
- m3n72 (normal): In the end, we found the café, but it was already closed.
- m3b20 (bright): And then, suddenly, the whole café started singing for her birthday!
- m3b21 (bright): Thirty-three days of saving, and I've got three thousand rupees!
- m3b24 (bright): Really?!
- m3b30 (bright): Thenuka's getting so big! Sam showed me a photo!
- m3b52 (bright): The café gave everyone free cake today, because it's the owner's birthday!
- m3b74 (bright): Twenty-two thousand rupees! That's exactly what I needed for the trip!
- m3l03 (low): I just want to sit next to her and hold her hand.
- m3l19 (low): It's Sunday again…
- m3l24 (low): I can't go home this week. The café needs me… and I hate it.
- m3l34 (low): Even the sea looks grey to me today…
- m3l35 (low): I just want to hear her say my name again.
- m3l58 (low): The café was so busy, and I didn't even have time for water.
- m3l74 (low): Three weeks… thirty-three days… I'm counting every day.
- m3t15 (tense): Really.
- m3t17 (tense): I'm not going to say sorry for something I didn't do.
- m3t24 (tense): He owes the café two thousand rupees, and he's never coming back.
- m3t43 (tense): Somebody parked in front of our gate, so we couldn't get out.
- m3t45 (tense): My neighbour plays loud music every night until two.
- m3t46 (tense): I waited forty minutes for the bus, and then two came together.
- m3t50 (tense): Someone took my umbrella from the café. My new one.
- m3t56 (tense): Hmm. I don't believe that for a second.

## Option B changes (kept lines)

- m3n44: empty,→empty… (1.50s)
- m3l04: everyone…→everyone, (0.00s)
- m3l06: Sam…→Sam, (0.00s)
- m3l08: no…→no, (0.00s)
- m3l10: quiet…→quiet, (0.00s)
- m3l12: sentence…→sentence, (0.00s)
- m3l16: month…→month, (0.00s)
- m3l20: Okay…→Okay, (0.00s)
- m3l22: lot…→lot, (0.00s)
- m3l26: customers…→customers, (0.00s)
- m3l27: cry…→cry, (0.00s)
- m3l28: died…→died, (0.00s)
- m3l30: Jaffna…→Jaffna, (0.00s)
- m3l31: stand…→stand, (0.00s)
- m3l32: home…→home, (0.00s)
- m3l36: Oh…→Oh, (0.00s)
- m3l39: understand…→understand, (0.00s)
- m3l40: Hmm…→Hmm, (0.00s)
- m3l42: Oh…→Oh, (0.00s)
- m3l43: know…→know, (0.00s)
- m3l45: alright…→alright, (0.00s)
- m3l47: Slowly…→Slowly, (0.00s)
- m3l48: Hmm…→Hmm, (0.00s)
- m3l51: tonight…→tonight, (0.00s)
- m3l55: late…→late, (0.00s)
- m3l56: year…→year, (0.00s)
- m3l59: cold…→cold, (0.00s)
- m3l60: bus…→bus, (0.00s)
- m3l62: mistake…→mistake, (0.00s)
- m3l64: me…→me, (0.00s)
- m3l65: days…→days, (0.00s)
- m3l66: tonight…→tonight, (0.00s)
- m3l67: mistake…→mistake, (0.00s)
- m3l68: final…→final, (0.00s)
- m3l72: there…→there, (0.00s)
- m3l73: alone…→alone, (0.00s)

## Emotion model disagreements (kept lines)

- m3n02 want neu got ang (0.094): The bus was full again today, so I walked from Wellawatte.
- m3n03 want neu got ang (0.018): Priya made dosa this morning, and the whole flat smelled amazing.
- m3n04 want neu got ang (0.004): It's been raining all week, and my shoes are still wet.
- m3n05 want neu got ang (0.006): Do you usually study at home, or do you go to the library?
- m3n06 want neu got ang (0.002): I call my family every Sunday, but this week Appa was busy.
- m3n08 want neu got ang (0.104): My cousin Priya and I share a small flat, and it's always a bit messy.
- m3n09 want neu got ang (0.039): Where do you usually go on weekends?
- m3n10 want neu got ang (0.003): When I think about it, Colombo is busy, but it's never boring.
- m3n11 want neu got ang (0.033): I usually walk along Galle Face after work, because the air is so cool.
- m3n12 want neu got ang (0.0): Hmm, interesting. And then what did you say?
- m3n13 want neu got ang (0.051): Wait, really? You went to Kandy on your own?
- m3n14 want neu got ang (0.003): Fair enough. I think I'd do the same.
- m3n15 want neu got ang (0.0): Go on. I'm listening.
- m3n16 want neu got ang (0.0): Listen first, and then say it back to me.
- m3n17 want neu got ang (0.004): That was clear. Now try it with "because".
- m3n18 want neu got ang (0.0): Take your time. There's no rush.
- m3n19 want neu got ang (0.023): Oh, you went to the shop yesterday? Nice. "Went", not "go".
- m3n20 want neu got ang (0.003): Can you say that again, a little slower?
- m3n22 want neu got ang (0.008): Let's try a longer answer this time. Use "and" or "but".
- m3n25 want neu got ang (0.0): Excuse me, could you please tell me where the bus stop is?
- m3n26 want neu got ang (0.003): Would you mind moving your bag, please? I'd like to sit down.
- m3n27 want neu got ang (0.005): I'm sorry, but I think you're next in the queue, not me.
- m3n28 want neu got ang (0.027): Honestly? I like Batman more, because he's just a normal person.
- m3n30 want neu got ang (0.001): Have you ever been to India? I'd love to see Madurai one day.
- m3n31 want neu got ang (0.297): First I made the tea, then I cleaned the tables, and after that I finally sat down.
- m3n33 want neu got ang (0.013): There are three things on the list: rice, vegetables, and the thick yellow dal.
- m3n35 want neu got ang (0.002): I washed the cups, dried them, and then I watched the waves.
- m3n36 want neu got ang (0.029): Thenuka, Kavi and Nimal: three brothers in one small house.
- m3n37 want neu got ang (0.005): So that's it, then.
- m3n38 want neu got ang (0.0): It's Sunday again.
- m3n40 want neu got ang (0.0): Okay, tell me everything.
- m3n42 want neu got ang (0.269): Priya and I take turns cooking, but she always forgets to buy onions.
- m3n43 want neu got ang (0.009): The road near our flat is so noisy in the mornings, especially on Mondays.
- m3n44 want neu got ang (0.0): I like the bus when it's empty, because I can look at the sea.
- m3n45 want neu got ang (0.011): We have a small balcony, and I keep two plants there.
- m3n46 want neu got ang (0.0): Do you prefer tea or coffee in the morning?
- m3n47 want neu got ang (0.0): Our teacher gave us a lot of homework, so I'll be up late tonight.
- m3n48 want neu got ang (0.01): I bought a new umbrella last week, and I've already lost it.
- m3n49 want neu got ang (0.003): Is your college far from your house, or can you walk there?
- m3n50 want neu got ang (0.092): The shop near the station sells the best mangoes, but it closes early.
- m3n52 want neu got ang (0.0): Oh, okay. So you didn't go in the end?
- m3n53 want neu got ang (0.0): That sounds nice. How long did it take to get there?
- m3n55 want neu got ang (0.017): Right, I understand. And how do you feel about it now?
- m3n56 want neu got ang (0.04): Good. Now tell me about your morning, using "first" and "then".
- m3n58 want neu got ang (0.0): Try to answer with two sentences this time.
- m3n59 want neu got ang (0.002): Oh, you have two brothers? Nice. "Brothers", with an "s" at the end.
- m3n61 want neu got ang (0.001): Here's a question for you: what's the best thing about your town?
- m3n62 want neu got ang (0.073): Sam says the baby sleeps all day and cries all night.
- m3n64 want neu got ang (0.001): I'm saving a little every week for the trip, so I don't eat out much.
- m3n65 want neu got ang (0.005): Could you send me the notes from today's class, please?
- m3n66 want neu got ang (0.001): I don't agree, but I understand why you think that.
- m3n67 want neu got ang (0.0): Let's wait for the others, and then we can decide together.
- m3n68 want neu got ang (0.003): I like old Tamil songs, especially when it's raining outside.
- m3n69 want neu got ang (0.007): Sam thinks every film needs a big fight at the end, but I don't.
- m3n70 want neu got ang (0.007): I usually take photos of people's hands when they're cooking.
- m3n71 want neu got ang (0.007): Yesterday I missed the bus, so I took a tuk-tuk, but then we got stuck in traffic.
- m3n73 want neu got ang (0.004): She thinks the third Thursday is free, but I'm not sure.
- m3n75 want neu got ang (0.007): The vegetables were fresh, the fish was fried, and the rice was perfect.
- m3b01 want hap got ang (0.006): I got it! I'm shift leader now, and I start on Monday!
- m3b02 want hap got ang (0.008): Paati's home! She called me, and she sounds so strong again!
- m3b03 want hap got ang (0.025): She's cooking crab curry again, so I know she's really better!
- m3b04 want hap got ang (0.081): Chennai, Madurai, and maybe the beach too! I can't wait!
- m3b05 want hap got ang (0.073): Ella with the whole class? Okay, that's a brilliant idea!
- m3b06 want hap got ang (0.094): He smiled at Sam? Thenuka's first smile? That's so sweet!
- m3b07 want hap got ang (0.037): Wait, really? That's amazing news!
- m3b08 want hap got ang (0.187): Oh, congratulations! You must be so happy!
- m3b09 want hap got ang (0.006): You finally did it! I knew you could!
- m3b10 want hap got ang (0.004): I can't believe it! You actually called him?
- m3b11 want hap got ang (0.027): Yes! That's exactly right, and you used "but" perfectly!
- m3b12 want hap got ang (0.009): Much better! I understood every word that time.
- m3b13 want hap got ang (0.04): Wow, that was a long answer! Well done!
- m3b14 want hap got ang (0.303): The sunset was so pretty tonight! The whole sky was orange!
- m3b15 want hap got ang (0.008): I saved enough for the train ticket! Only the hotel left now!
- m3b16 want hap got ang (0.093): Look at this photo! The light on the water is perfect!
- m3b17 want hap got ang (0.013): Sri Lanka won by two wickets? Sam must be going crazy!
- m3b18 want hap got ang (0.004): Okay, Marvel wasn't bad. Don't tell Sam I said that!
- m3b19 want hap got ang (0.011): Thank you so much! That's really kind of you!
- m3b22 want hap got ang (0.0): I can't believe she said that!
- m3b23 want hap got ang (0.001): It's Sunday again!
- m3b25 want hap got ang (0.027): Okay, tell me EVERYTHING!
- m3b26 want hap got ang (0.001): They said yes! I can take the whole of next month off for India!
- m3b27 want hap got ang (0.005): Paati walked to the gate by herself today! Arun sent me a video!
- m3b28 want hap got ang (0.017): My first week as shift leader, and nothing went wrong!
- m3b29 want hap got ang (0.003): I booked the train to Madurai! It's really happening!
- m3b31 want hap got ang (0.0): Sam passed his driving test! He called me the moment he got out!
- m3b32 want hap got ang (0.0): We're going to Ella! The whole class said yes!
- m3b33 want hap got ang (0.052): Paati made crab curry for the whole street, and everyone loved it!
- m3b34 want hap got ang (0.001): My manager said I'm the best shift leader they've had!
- m3b35 want hap got ang (0.0): Paati's coming to Colombo! She said yes!
- m3b36 want hap got ang (0.046): Oh, that's lovely! Tell me more!
- m3b37 want hap got ang (0.007): No way, you met him? What was he like?
- m3b38 want hap got ang (0.001): Wow, you remembered! Thank you!
- m3b39 want hap got ang (0.004): That's so good to hear! I'm really happy for you!
- m3b40 want hap got ang (0.044): Oh, I love that idea!
- m3b41 want hap got ang (0.215): Seriously? That's the best news this week!
- m3b42 want hap got ang (0.005): Oh, how wonderful! When did you find out?
- m3b43 want hap got ang (0.0): Ha! That's so you!
- m3b44 want hap got ang (0.014): You're joking! Both of you?
- m3b45 want hap got ang (0.0): That was brilliant! You didn't stop once!
- m3b46 want hap got ang (0.038): Yes! You used "then" and "after that" — perfect!
- m3b47 want hap got ang (0.226): Great question! Okay, let me think…
- m3b48 want hap got ang (0.011): Oh, nice! That's a much better word!
- m3b49 want hap got ang (0.004): Good job! You're getting faster every day!
- m3b50 want hap got ang (0.058): Perfect! I understood every single word!
- m3b51 want hap got ang (0.0): Yes, that's it! Say it like that every time!
- m3b53 want hap got ang (0.004): Priya cleaned the whole flat! I don't even know what happened!
- m3b55 want hap got ang (0.005): I found my umbrella! It was in my bag the whole time!
- m3b56 want hap got ang (0.003): Amma's sending a box of sweets from Jaffna!
- m3b58 want hap got ang (0.007): Arun got the top mark in his class! My little brother!
- m3b59 want hap got ang (0.002): Guess what? Priya's getting a dog!
- m3b60 want hap got ang (0.152): The new bakery opened near the station, and the bread is amazing!
- m3b61 want hap got ang (0.06): Finally, a day off! No work, no class, nothing!
- m3b62 want hap got ang (0.003): I took the best photo of my life today! A fisherman and his boat at sunset!
- m3b63 want hap got ang (0.003): There's a new Batman film coming out! I'm going on the first day!
- m3b64 want hap got ang (0.052): I finally made Paati's crab curry, and it actually tasted like hers!
- m3b65 want hap got ang (0.005): Sam's team won the match, and he took the last wicket!
- m3b66 want hap got ang (0.009): Look, the hotel in Chennai has a pool!
- m3b67 want hap got ang (0.029): Okay, I'll say it: that film was actually really good!
- m3b68 want hap got ang (0.007): I can see the temple from the train window! It's beautiful!
- m3b69 want hap got ang (0.004): Yes, of course! I'd love to help!
- m3b70 want hap got ang (0.007): Thank you! You really didn't have to do that!
- m3b71 want hap got ang (0.033): Then, just as we reached the top, the clouds opened, and we saw everything!
- m3b72 want hap got ang (0.046): So first I was late, but then the manager said, "Don't worry, you're the best!"
- m3b73 want hap got ang (0.01): And after all that, the bus came early for once!
- m3b75 want hap got ang (0.009): Three trains, two buses, and finally, there it was — the sea!
- m3l01 want sad got ang (0.001): Paati's in hospital again, and I'm so far away…
- m3l02 want sad got ang (0.002): Amma says she's okay, but I can hear it in her voice…
- m3l04 want sad got ang (0.005): He shouted at me in front of everyone… and I didn't say anything.
- m3l05 want sad got ang (0.05): I went to the back room and cried. I felt so small.
- m3l06 want sad got ang (0.058): Oh, Sam… I'm so sorry about Bruno. He was family.
- m3l07 want sad got ang (0.003): I keep thinking about her cooking in that small kitchen…
- m3l08 want sad got ang (0.0): Oh no… that must be really hard.
- m3l09 want sad got ang (0.0): I'm sorry. Do you want to talk about it?
- m3l10 want sad got ang (0.001): Some nights the flat feels very quiet… and I miss Jaffna.
- m3l11 want sad got ang (0.041): I'm tired today. I worked late, and I didn't sleep well.
- m3l13 want sad got ang (0.179): Don't worry about mistakes. Everyone makes them.
- m3l14 want sad got ang (0.001): I'm really sorry. I didn't mean to hurt you.
- m3l15 want sad got ang (0.002): After that, I walked home in the rain, and I didn't even notice I was wet.
- m3l16 want sad got ang (0.01): It was the third time this month… and nobody thanked me.
- m3l17 want sad got ang (0.0): So that's it, then…
- m3l18 want sad got ang (0.0): I can't believe she said that…
- m3l20 want sad got ang (0.0): Okay… tell me everything.
- m3l21 want sad got ang (0.005): They took her to the hospital at night, and nobody called me until morning…
- m3l22 want sad got ang (0.0): Appa says she's sleeping a lot… and she's not eating much.
- m3l23 want sad got ang (0.005): I looked at the bus times to Jaffna three times today.
- m3l25 want sad got ang (0.0): Every time my phone rings, I'm scared it's bad news.
- m3l26 want sad got ang (0.0): I keep saying sorry to customers… even when it's not my fault.
- m3l27 want sad got ang (0.005): I didn't want anyone to see me cry… but they all did.
- m3l28 want sad got ang (0.066): Sam's been so quiet since Bruno died… I don't know what to say to him.
- m3l29 want sad got ang (0.003): I miss Paati's voice. She used to sing in the kitchen.
- m3l30 want sad got ang (0.0): Maybe I should have stayed in Jaffna… near my family.
- m3l31 want sad got ang (0.023): When I left Jaffna, Paati held my hand at the bus stand… and didn't let go.
- m3l32 want sad got ang (0.006): Arun asked when I'm coming home… and I didn't have an answer.
- m3l33 want sad got ang (0.001): I wonder if she still remembers my voice on the phone…
- m3l36 want sad got ang (0.002): Oh… I didn't know that. I'm so sorry.
- m3l37 want sad got ang (0.001): That sounds really lonely…
- m3l38 want sad got ang (0.001): Oh no. Are you okay?
- m3l39 want sad got ang (0.0): I understand… it's not easy.
- m3l40 want sad got ang (0.02): Hmm… that's sad. I'm sorry it happened.
- m3l41 want sad got ang (0.0): Take all the time you need. I'm here.
- m3l42 want sad got ang (0.0): Oh… that must have hurt.
- m3l43 want sad got ang (0.003): I know… some days are just like that.
- m3l44 want sad got ang (0.0): It's okay if you don't know the word. Just say what you can.
- m3l45 want sad got ang (0.001): That's alright… we can come back to this one later.
- m3l46 want sad got ang (0.005): Don't be sad about it. It was a really difficult question.
- m3l47 want sad got ang (0.0): Slowly… one word at a time.
- m3l48 want sad got ang (0.001): Hmm… no, not quite. But that's okay, let's look at it together.
- m3l49 want sad got ang (0.005): It's been raining for three days, and I haven't seen the sun once.
- m3l50 want sad got ang (0.0): Priya's gone home for the weekend, so the flat's empty.
- m3l51 want sad got ang (0.022): I'm too tired to cook tonight… I'll just have some bread.
- m3l52 want sad got ang (0.01): I didn't do well in the test. I studied, but I forgot everything.
- m3l53 want sad got ang (0.024): Sometimes I eat lunch alone in the park, and I watch the families.
- m3l54 want sad got ang (0.002): My feet hurt so much after work tonight…
- m3l56 want sad got ang (0.001): Nobody remembered my birthday this year… except Priya.
- m3l57 want sad got ang (0.0): I don't feel like talking today… sorry.
- m3l59 want sad got ang (0.017): I think I'm getting a cold… my head's so heavy.
- m3l60 want sad got ang (0.001): I lost my purse on the bus… with all my savings inside.
- m3l61 want sad got ang (0.368): I'm sorry. I should have told you earlier.
- m3l62 want sad got ang (0.01): I know I made a mistake… and I feel terrible about it.
- m3l63 want sad got ang (0.032): Maybe you're right. I don't really know anymore.
- m3l64 want sad got ang (0.0): Please don't be angry with me… I'm trying my best.
- m3l65 want sad got ang (0.037): I haven't listened to music for days… it just doesn't feel the same.
- m3l66 want sad got ang (0.004): I watched an old film tonight… the one Paati liked.
- m3l67 want sad got ang (0.001): I deleted all the photos by mistake… a whole year of photos.
- m3l68 want sad got ang (0.001): Sam's team lost the final… he didn't say a word all evening.
- m3l69 want sad got ang (0.033): I tried to cook her curry tonight, but it didn't taste the same…
- m3l70 want sad got ang (0.024): First the bus didn't come, then it started raining, and then my phone died.
- m3l71 want sad got ang (0.028): I waited for an hour, but in the end, nobody came.
- m3l72 want sad got ang (0.036): After the call, I just sat there… for a long time.
- m3l73 want sad got ang (0.094): So in the end, I walked home alone… and it was dark.
- m3n23 want neu got ang (0.022): I start as shift leader on Monday, so I need to learn the schedule.
- m3n54 want neu got ang (0.001): Wait, so who was driving?
- m3n63 want neu got ang (0.002): Being shift leader means I have to count the money at the end of the day.
- m3n74 want neu got ang (0.04): My phone number ends in two, nine, seven, zero.
- m3b54 want hap got ang (0.029): The rain stopped, and there's a rainbow over the sea!
- m3b57 want hap got ang (0.002): It's a long weekend, so I'm going to sleep for two days!
- m3l75 want sad got ang (0.001): The thick, grey clouds stayed there the whole weekend.

RESULT: PASS

## Log
```
[  1.8 min] models loaded
[  2.8 min] round 1: batch 1/25 in 57 s
[  3.7 min] round 1: batch 2/25 in 55 s
[  4.7 min] round 1: batch 3/25 in 62 s
[  5.3 min] round 1: batch 4/25 in 38 s
[  6.4 min] round 1: batch 5/25 in 65 s
[  7.3 min] round 1: batch 6/25 in 55 s
[  8.3 min] round 1: batch 7/25 in 56 s
[  9.0 min] round 1: batch 8/25 in 42 s
[  9.7 min] round 1: batch 9/25 in 42 s
[ 10.3 min] round 1: batch 10/25 in 35 s
[ 11.3 min] round 1: batch 11/25 in 60 s
[ 12.1 min] round 1: batch 12/25 in 48 s
[ 13.1 min] round 1: batch 13/25 in 61 s
[ 14.0 min] round 1: batch 14/25 in 54 s
[ 14.7 min] round 1: batch 15/25 in 42 s
[ 15.5 min] round 1: batch 16/25 in 49 s
[ 16.6 min] round 1: batch 17/25 in 68 s
[ 17.6 min] round 1: batch 18/25 in 56 s
[ 18.7 min] round 1: batch 19/25 in 71 s
[ 19.6 min] round 1: batch 20/25 in 53 s
[ 20.6 min] round 1: batch 21/25 in 59 s
[ 21.3 min] round 1: batch 22/25 in 41 s
[ 22.0 min] round 1: batch 23/25 in 46 s
[ 23.0 min] round 1: batch 24/25 in 58 s
[ 24.0 min] round 1: batch 25/25 in 61 s
[ 57.4 min] round 1: 256/300 lines have a passing take; retrying 44 with 3 more takes
[ 58.6 min] retry: batch 1/4 in 73 s
[ 59.7 min] retry: batch 2/4 in 67 s
[ 61.0 min] retry: batch 3/4 in 75 s
[ 62.1 min] retry: batch 4/4 in 67 s
```
