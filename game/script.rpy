# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define kota = Character('Kota', callback=name_callback, cb_name='kot', image='ko')
define luke = Character('Luke', callback=name_callback, cb_name='luke', image='luke')
define both = Character('Both', callback=name_callback, cb_name=['luke', 'kot'])

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

# This is example of a character who I want to have two different focuses. One normal and one to represent them at a distance.
# So we need to break the sprite_highlight out of the main layeredimage, and define a general layeredimage for both to use.
# I usually name them with a '1' so the usual one still available. And if they had a seperate pose that required a different
# layeredimage, I can define a 'luke2', 'luke3', etc.
layeredimage luke1:
    always:
        'luke1_wings_neutral'
    group arm auto:
        attribute hip default
    always:
        'luke1_body_neutral'

    group clothes auto:
        attribute tankpants default
    group emote auto:
        attribute neutral default
    attribute bandanna if_any['crying', 'cocky', 'happy', 'wink']:
        'luke1_bandanna_front'
    attribute bandanna if_any['annoyed', 'laughing', 'neutral', 'sad', 'surprised']:
        'luke1_bandanna_side'
    attribute bandanna if_any['hysterical']:
        'luke1_bandanna_hysterical'
    attribute glasses if_any['cocky', 'crying', 'happy', 'wink']:
        'luke1_glasses_front'
    attribute glasses if_any['annoyed', 'laughing', 'neutral', 'sad', 'surprised']:
        'luke1_glasses_side'
# This crop is used for the "phone" version of the sprite and references the PhoneFocus.
transform sprite_phone_tf_luke(child):
    contains:
        'phone_backing' 
    contains:
        AlphaMask(Transform(child, crop=(100, 0, 400, 601)), 'phone_mask')
    contains:
        'phone_border' 
    xysize(400, 601)
    yalign 0.3
    function PhoneFocus('luke')
# Here we define both of the sprites to be used.
image luke       = LayeredImageProxy('luke1', transform=sprite_highlight('luke'))
image luke phone = LayeredImageProxy('luke1', sprite_phone_tf_luke)

image black = Solid('#000')
image bg room = Solid('#606060')
define audio.laugh = "audio/laughtrack.ogg"

# The game starts here.

label start:

    scene bg room with dissolve

    "Unlike my other code projects, there isn't much I feel the need to say in the demo script to show it off."
    "So I outsourced the writing for this one to a group chat and put in whatever they said."
    show ko happy kimono mug at left
    show luke bandanna at right
    with dissolve
    # These display lines of dialogue.
    both "Hey! Tonight I'm gonna have a feast!"
    kota sad "Oh god, not you too... Not tonight of all nights."
    luke cocky "You're not weaseling your way out of this one. It's an All-American fourth of July and we're lighting kerosene."
    show luke neutral
    kota surprise relaxed "But I need the matches in order to cook the dinner for Onsen."
    luke happy "But we could just grill for Onsen. Everything would work out just fine."
    kota angry "Absolutely not. Whatever abomination you cook up might actually just kill him."
    luke hysterical "What do you mean, I'm gonna get some deep-fried avocado burgers for everyone. And then we'll all ride motorcycles into the sunset!"
    kota puzzled "Darn it, Luke from the critically-acclaimed, award-winning visual novel, Minotaur Hotel, now with a free SFW version available for download on {a=https://minoh.itch.io/minotaur-hotel-sfw}itch.io{/a}, Onsen and I are gonna have ramen."
    luke glasses laughing salute "Time to rock-and-rolllllllll!!!"
    kota sad "I will not be doing any \"rolling\". Also, please take those things off."
    show luke:
        ease 1.5 xcenter 1.5
    luke wink -glasses hip "Can't hear ya I'm already heading out."
    hide luke
    show luke phone bandanna cocky:
        xcenter .75 yalign .3
    kota angry raised "Hey! You should have added a comma to what you just said!"
    luke "Can't hear you over the parrrrttyyyyy!!!"
    kota sad "Will you ever stop showing off?"
    play sound laugh
    pause 0.5
    # This ends the game.
    scene black with Dissolve(3)
    return
