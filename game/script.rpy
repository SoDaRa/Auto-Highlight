# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define kota = Character('Kota', callback=name_callback, cb_name='kot', image='ko')
define luke = Character('Luke', callback=name_callback, cb_name='luke', image='luke')

layeredimage ko:
    at sprite_highlight('kot')
    group hair_front auto:
        attribute loose if_any['angry', 'happy', 'laughing', 'surprise']
        attribute tied if_any['angry', 'happy', 'laughing', 'surprise']
    group hair_side auto:
        attribute loose if_any['neutral', 'puzzled', 'sad'] default
        attribute tied if_any['neutral', 'puzzled', 'sad']
    group rightarm auto:
        attribute relaxed default
    group clothes_rightarm:
        attribute mug default if_all['kimono']:
            'ko_clothes_rightarm_mug_kimono'
        attribute raised if_all['kimono']:
            'ko_clothes_rightarm_raised_kimono'
        attribute relaxed if_all['kimono']:
            'ko_clothes_rightarm_relaxed_kimono'
        attribute mug if_all['barman']:
            'ko_clothes_rightarm_mug_barman'
        attribute raised if_all['barman']:
            'ko_clothes_rightarm_raised_barman'
        attribute relaxed if_all['barman']:
            'ko_clothes_rightarm_relaxed_barman'
    always:
        'ko_body'
    group clothes_body auto:
        attribute kimono default
    group leftarm auto:
        attribute relaxed default
    group clothes_leftarm:
        attribute mug default if_all['kimono']:
            'ko_clothes_leftarm_mug_kimono'
        attribute raised if_all['kimono']:
            'ko_clothes_leftarm_raised_kimono'
        attribute relaxed if_all['kimono']:
            'ko_clothes_leftarm_relaxed_kimono'
        attribute mug if_all['barman']:
            'ko_clothes_leftarm_mug_barman'
        attribute raised if_all['barman']:
            'ko_clothes_leftarm_raised_barman'
        attribute relaxed if_all['barman']:
            'ko_clothes_leftarm_relaxed_barman'
    group emote auto:
        attribute neutral default

layeredimage luke:
    at sprite_highlight('luke')
    always:
        'luke_wings_neutral'
    group arm auto:
        attribute hip default
    always:
        'luke_body_neutral'

    group clothes auto:
        attribute tankpants default
    group emote auto:
        attribute neutral default
    attribute bandanna if_any['crying', 'cocky', 'happy', 'wink']:
        'luke_bandanna_front'
    attribute bandanna if_any['annoyed', 'laughing', 'neutral', 'sad', 'surprised']:
        'luke_bandanna_side'
    attribute bandanna if_any['hysterical']:
        'luke_bandanna_hysterical'
    attribute glasses if_any['cocky', 'crying', 'happy', 'wink']:
        'luke_glasses_front'
    attribute glasses if_any['annoyed', 'laughing', 'neutral', 'sad', 'surprised']:
        'luke_glasses_side'

image black = Solid('#000')
image bg room = Solid('#606060')
define audio.laugh = "audio/laughtrack.ogg"

# The game starts here.

label start:

    scene bg room with dissolve

    "Unlike my other code projects, there isn't much I feel the need to say in the demo script to show it off."
    "So I outsourced the writing for this one to a group chat and put in whatever they said."
    show ko sad kimono mug at left
    show luke bandanna at right
    with dissolve
    # These display lines of dialogue.

    kota "Oh god, not tonight. Not tonight of all nights."
    luke cocky "You're not weaseling your way out of this one. It's an All-American fourth of July and we're lighting kerosene."
    show luke neutral
    kota surprise relaxed "But I need the matches in order to cook the dinner for Onsen."
    luke happy "But we could just grill for Onsen. Everything would work out just fine."
    kota angry "Absolutely not. Whatever abomination you cook up might actually just kill him."
    luke hysterical "What do you mean, I'm gonna get some deep-fried avocado burgers for everyone. And then we'll all ride motorcycles into the sunset!"
    kota puzzled "Darn it, Luke from the critically-acclaimed, award-winning visual novel, Minotaur Hotel, now with a free SFW version available for download on {a=https://minoh.itch.io/minotaur-hotel-sfw}itch.io{/a}, Onsen and I are gonna have ramen."
    luke glasses laughing salute "Time to rock-and-rolllllllll!!!"
    kota sad "I will not be doing any \"rolling\". Also, please take those things off."
    luke wink -glasses hip "Hey don't smoke kids."
    kota angry raised "Please add a comma to what you just said..."
    play sound laugh
    pause 0.5
    # This ends the game.
    scene black with Dissolve(3)
    return
