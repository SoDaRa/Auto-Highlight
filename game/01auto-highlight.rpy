"""
 Auto Highlight Ren'Py Module
 2021 Daniel Westfall <SoDaRa2595@gmail.com>

 http://twitter.com/sodara9
 I'd appreciate being given credit if you do end up using it! :D Would really
 make my day to know I helped some people out!
 http://opensource.org/licenses/mit-license.php
 Github: https://github.com/SoDaRa/Auto-Highlight
 itch.io: https://wattson.itch.io/renpy-auto-highlight
"""
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

""" Setup (IMPORTANT) """
## To get this working you'll need to do two additional things along with having this file in your project.

# - First, you'll need to setup your character definitions to support it.
#   Example:
# define eil = Character("Eileen", callback = name_callback, cb_name = "eileen")
# - cb_name provides the 'name' parameter to the function 'name_callback'
# - Remember that Ren'py supports say_with_arguments.
#   So you can assign one for a particular line by doing:
# eil "I think someone else should be focused" (cb_name = "pileen")
# - Finally, if you wish for the special narrator to make all sprites unfocused or something similar,
#   you can copy this.
# define narrator = Character(callback = name_callback, cb_name = None)

# - Second, you'll need to apply the sprite_highlight transform to all images you want this
#   applied to. For people using layeredimages, this is very easy. As an example:
# layeredimage eileen:
#     at sprite_highlight('eileen')
#     ...
# - However, if you're using individual sprites, you'll have to be sure this is applied to every one.
# image eileen happy = At('eileen_happy', sprite_highlight('eileen'))
# image eileen sad = At('eileen_sad', sprite_highlight('eileen'))
#   Or, if you'd prefer an ATL example
# image eileen happy:
#     'eileen_happy'
#     function SpriteFocus('eileen')

""" General Note """
# - This file has to be compiled before any scripts that define images that use this.
#   As such, this file is named 01auto-highlight.rpy to help with that.
# - Be sure that all images that you want to share the same sprite highlight name
#   are using the same image tag.
# - IMPORTANT: If two images are on screen use the same highlight name, animations will tend to end early
#              as they both try to update the status, making it go very fast or end instantly.
#              If you need more than one using the same reference, I suggest setting up a second SpriteFocus that
#              uses the dict_ref to refer to another focus dictionary.
# - If you want to have multiple characters focused, have a speaker that has cb_name with a list like:
# define both = Character('Both', callback=name_callback, cb_name=['luke', 'kot'])


""" Variables """
# - sprite_focus - (Dictionary) It is used to help inform who should be animated
#                  and occasionaly holds timing data
# - Has entries added to it in the SpriteFocus focus_check function.
# - I chose to use a define because it's status should not affect the story and
#   it can be cleared safely when the player closes the game. Then, when someone boots
#   up again, it will only have entries added to it as needed.
# - If you wish for it's status to be kept between play sessions, then change the 'define' to 'default'
# NEW: I've added a sub-dictionary for if people want multiple images on screen that you want to reference the same char name.
define sprite_focus = {0:{}}

# - speaking_char - (Varient) Is manipulated by the character callback to help us know
#                   who the current speaking character is.
# - Keeps track of which character is currently speaking. Is updated in name_callback
#   and checked in SpriteFocus focus_check to determine if sprite's character is speaking
#   or not.
default speaking_char = None

""" Transforms """
# - This is the actual transform that will help apply the changes to your sprites.
# - SpriteFocus is used as a callable class here. The function statement doesn't
#   pass additional parameters to our function, so I use a callable class here to
#   give the function statement something it can call like a function, while still
#   providing a way to pass through the transform parameter.
# - You may need to define more of these if you want different ways to focus.
transform sprite_highlight(sprite_name):
    function SpriteFocus(sprite_name)
    # I don't recommend adding ATL down here since the above statement won't return None.
init -10 python:
    import math

    # Easing functions you can use
    def get_ease(t):
        return .5 - math.cos(math.pi * t) / 2.0
    def get_ease_back(t):
        c1 = 1.70158
        c2 = c1 * 1.525
        return (math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2 if t < 0.5 else (math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    # name: Name of the character talking at present. Usually a string.
    #       Used by focus_check function to determine which sprites to put in talking and non-talking states
    def name_callback(event, interact=True, name=None, **kwargs):
        global speaking_char
        if event == "begin":
            speaking_char = name

    # Abstracts the core functionality of checking the status and getting the current ease value for the animation
    def focus_check(char_name, anim_length, anim_time, ease_func=get_ease, dict_ref=0):
        global speaking_char, sprite_focus
        # Picks the focus dictionary to use. Usually don't need to worry about it.
        if dict_ref not in sprite_focus: 
            sprite_focus[dict_ref] = {}
        focus_dict = sprite_focus[dict_ref]
        # Adds character to the focus dictionary if it doesn't currently exist.
        if char_name not in focus_dict:
            focus_dict[char_name] = False
        status = False
        if speaking_char is not None:
            status = char_name in speaking_char
        # - Or if you want some special name like "all" to mean every sprite should be focused:
        # if speaking_char == 'all':
        #     status = True

        #### Check & Update Status ####
        # - If our key in the sprite_focus dictionary is a number AND anim_time is less than that number
        #   then we want to update our talking status in sprite_focus to be a boolean.
        # - This is to prevent any issues that arrise from anim_time being less than a value we put into sprite_focus.
        # - IMPORTANT: Anytime our value in sprite_focus is set to a boolean, it will
        #   represent us being either talking (boolean True) or not talking (boolean False).
        #   It being set to a number will represent animating from one to another.
        if isinstance(focus_dict[char_name], (int, float)) and anim_time < focus_dict[char_name]:
            focus_dict[char_name] = status
        # If our value in the sprite_focus is not equivalent to our talking status AND is a boolean
        if focus_dict[char_name] != status and isinstance(focus_dict[char_name], bool):
            # Since our talking status has flipped, log the time so we can use it as a timer in the next section
            focus_dict[char_name] = anim_time
            # Unless we're in rollback or are skipping. In which case, we'll want to just snap to the new status
            if renpy.is_skipping() or renpy.in_rollback():
                focus_dict[char_name] = status

        #### Determine Time and Position in Animation ####
        # - Figure out the current time of the animation
        # - This will still work, even if our entry in sprite_focus is currently a boolean.
        #   However, it will never be used in such a scenario due to the next if statement.
        # - Also where that anim_time value we stored in sprite_focus is used
        curr_time = max(anim_time - focus_dict[char_name],0) # Prevent going below zero
        # - The following variable is the actual value we'll use to animate on.
        # - By default, it's set to 1.0. Which cooresponds to the animation being completed.
        #   It should always remain within the range 0 to 1.
        curr_ease = 1.0
        # If curr_time is still less than the animation length AND we aren't a boolean in sprite_focus
        if curr_time < anim_length and not isinstance(focus_dict[char_name], bool):
            t = curr_time / anim_length
            curr_ease = ease_func(t)
            
        else:
            focus_dict[char_name] = status # If done with time, register talking status
        return status, curr_ease

    # Used to help make sprite_tf more reusable while still using the function statement in the ATL
    class SpriteFocus(object):
        def __init__(self, sprite_name):
            self.sprite_name = sprite_name

        def __call__(self, trans, st, at):
            #### Setup ####
            anim_length = .2       # How long in seconds the animation will last
            bright_change = 0.08   # How much the brightness changes
            sat_change = 0.2       # How much the saturation changes
            zoom_change = 0.0025   # How much the zoom changes
            # Our sprites don't have legs, so the zoom will slightly lift them off the bottom of the screen when they are scaled down.
            # To accomodate, we apply a yoffset to give a small push down to keep them aligned to the bottom of the screen.
            y_amount = 1           
            
            status, curr_ease = focus_check(self.sprite_name, anim_length, at)
            if status: # Apply the talking transformation
                trans.matrixcolor = SaturationMatrix((1.0-sat_change) + curr_ease * sat_change) * BrightnessMatrix(-bright_change + curr_ease * bright_change)
                trans.zoom = min(curr_ease * zoom_change + (1.0-zoom_change), 1.0)
                trans.yoffset = y_amount + (-y_amount * curr_ease)
            else:      # Apply the not-talking transformation
                trans.matrixcolor = SaturationMatrix(1.0 - curr_ease * sat_change) * BrightnessMatrix(curr_ease * -bright_change)
                trans.zoom = max(1.0 - curr_ease * zoom_change, (1.0-zoom_change))
                trans.yoffset = y_amount * curr_ease
            return 0
    # This is used to give an alternate focus transform with different properties
    # while using the same sprite_name.
    class PhoneFocus(object):
        def __init__(self, sprite_name):
            self.sprite_name = sprite_name

        def __call__(self, trans, st, at):
            anim_length = .7
            y_amount = -1080
            bright_change = 0.21
            # Notice that we provide get_ease_back here as an alternate warper for the transformation
            status, curr_ease = focus_check(self.sprite_name, anim_length, at, get_ease_back) 
            if status: # Brighten and zoom in
                trans.yoffset = y_amount + -1 * y_amount * curr_ease
                trans.matrixcolor = BrightnessMatrix(-bright_change + curr_ease * bright_change)
            else:      # Darken and zoom out
                trans.matrixcolor = BrightnessMatrix(curr_ease * -bright_change)
                trans.yoffset = y_amount * curr_ease
            return 0
    # This example isn't used in the main script but you could have the background or other sprite gain focus
    # while using the same sprite_name.
    class BGFocus(object):
        def __init__(self, sprite_name):
            self.sprite_name = sprite_name

        def __call__(self, trans, st, at):
            #### Setup ####
            anim_length = .2       # How long in seconds the animation will last
            bright_change = 0.08   # How much the brightness changes
            sat_change = 0.2       # How much the saturation changes
            # Notice that we provide dict_ref here so we can reuse a sprite_name without having colliding statuses
            status, curr_ease = focus_check(self.sprite_name, anim_length, at, dict_ref=1)
            if status: # Apply the talking transformation
                trans.matrixcolor = SaturationMatrix((0.2-sat_change) + curr_ease * sat_change) * BrightnessMatrix(-bright_change + curr_ease * bright_change)
            else:      # Apply the not-talking transformation
                trans.matrixcolor = SaturationMatrix(0.2 - curr_ease * sat_change) * BrightnessMatrix(curr_ease * -bright_change)
            return 0
