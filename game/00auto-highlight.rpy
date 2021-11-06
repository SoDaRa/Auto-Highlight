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
#   As such, this file is named 00auto-highlight.rpy to help with that.
# - Be sure that all images that you want to share the same sprite highlight name
#   are using the same image tag.

""" Variables """
# - sprite_focus - (Dictionary) It is used to help inform who should be animated
#                  and occasionaly holds timing data
# - Has entries added to it in the SpriteFocus __call__ function.
# - I chose to use a define because it's status should not affect the story and
#   it can be cleared safely when the player closes the game. Then, when someone boots
#   up again, it will only have entries added to it as needed.
# - If you wish for it's status to be kept between play sessions, then change the 'define' to 'default'
define sprite_focus = {}

# - speaking_char - (Varient) Is manipulated by the character callback to help us know
#                   who the current speaking character is.
# - Keeps track of which character is currently speaking. Is updated in name_callback
#   and checked in SpriteFocus __call__ to determine if sprite's character is speaking
#   or not.
default speaking_char = None

""" Transforms """
# - This is the actual transform that will help apply the changes to your sprites.
# - SpriteFocus is used as a callable class here. The function statement doesn't
#   pass additional parameters to our function, so I use a callable class here to
#   give the function statement something it can call like a function, while still
#   providing a way to pass through the transform parameter.
transform sprite_highlight(sprite_name):
    function SpriteFocus(sprite_name)
    # I don't recommend adding ATL down here since the above statement won't return None.
init -10 python:
    import math

    # name: Name of the character talking at present. Usually a string.
    #       Used by SpriteFocus's __call__ function to determine which sprites to put in talking and non-talking states
    def name_callback(event, interact=True, name=None, **kwargs):
        global speaking_char
        if event == "begin":
            speaking_char = name

    # Used to help make sprite_tf more reusable while still using the function statement in the ATL
    class SpriteFocus(object):
        # char_name - Used to check who we are manipulating. This is used as a
        #             key into sprite_focus and should be equal to it's equivalent string
        #             that is written to speaking_char in the character callback.
        def __init__(self, char_name):
            self.char_name = char_name

        ## Main function ##
        # trans - Renpy transform object that we'll manipulate
        # start_time - (float) Starting time of the current transform
        # anim_time  - (float) Animation time of the current transform. May be >= st.
        def __call__(self, trans, start_time, anim_time):
            # The ease function we use to make the animation move a bit more naturally.
            def get_ease(t):
                return .5 - math.cos(math.pi * t) / 2.0
            #### Setup ####
            global sprite_focus, speaking_char # Get the global variables we defined earlier
            char_name = self.char_name # Just to save having self.char_name everywhere
            # Add an entry for our char_name if it's not in the dictionary yet
            if char_name not in sprite_focus:
                sprite_focus[char_name] = False
            anim_length = 0.2       # How long (in seconds) the animation will last
            bright_change = 0.08    # How much the brightness changes
            sat_change = 0.2        # How much the saturation changes
            zoom_change = 0.0025    # How much the zoom changes
            # - y_change is mostly here because the Minotaur Hotel sprites were made to be kept level with
            #   the bottom of the screen. The zoom change causes them to rise slightly
            #   above it. So I apply a small yoffset to keep them in place.
            # - If you have full sprites, this can be omitted.
            #   If you do, remember to remove the cooresponding lines in the Transform Manipulation near the bottom
            y_change = 1            # How much y_offset to apply.

            # is_talking - (Boolean) Determines if we're the talking char or not.
            #              True means we are talking. False means we aren't.
            is_talking = speaking_char == char_name
            # - If you would like to add support for multiple characters to be highlighted
            #   then you may want to pass a list of names to speaking_char. And then have something like:
            # if isinstance(speaking_char, list):
            #     is_talking = char_name in speaking_char
            # - Or if you want some special name like "all" to mean every sprite should be focused:
            # if speaking_char == 'all':
            #     is_talking = True

            #### Check & Update Status ####
            # - If our key in the sprite_focus dictionary is a number AND anim_time is less than that number
            #   then we want to update our talking status in sprite_focus to be a boolean.
            # - This is to prevent any issues that arrise from anim_time being less than a value we put into sprite_focus.
            # - IMPORTANT: Anytime our value in sprite_focus is set to a boolean will
            #   represent us being either talking (boolean True) or not talking (boolean False).
            #   It being set to a number will represent animating from one to another.
            if isinstance(sprite_focus[char_name], (int, float)) and anim_time < sprite_focus[char_name]:
                sprite_focus[char_name] = is_talking
            # If our value in the sprite_focus is not equivalent to our talking status AND is a boolean
            if sprite_focus[char_name] != is_talking and isinstance(sprite_focus[char_name], bool):
                # Since our talking status has flipped, log the time so we can use it as a timer in the next section
                sprite_focus[char_name] = anim_time
                # Unless we're in rollback or are skipping. In which case, we'll want to just snap to the new status
                if renpy.is_skipping() or renpy.in_rollback():
                    sprite_focus[char_name] = is_talking

            #### Determine Time and Position in Animation ####
            # - Figure out the current time of the animation
            # - This will still work, even if our entry in sprite_focus is currently a boolean.
            #   However, it will never be used in such a scenario due to the next if statement.
            # - Also where that anim_time value we stored in sprite_focus is used
            curr_time = max(anim_time - sprite_focus[char_name],0) # Prevent going below zero
            # - The following variable is the actual value we'll use to animate on.
            # - By default, it's set to 1.0. Which cooresponds to the animation being completed.
            #   It should always remain within the range 0 to 1.
            curr_ease = 1.0
            # If curr_time is still less than the animation length AND we aren't a boolean in sprite_focus
            if curr_time < anim_length and not isinstance(sprite_focus[char_name], bool):
                curr_ease = get_ease(curr_time/anim_length) # Get our actual animation position
            else:
                sprite_focus[char_name] = is_talking # If done with time, register talking status

            #### Transform Manipulation ####
            # - This bit is what actually applies the changes to the sprite we're manipulating
            # - If you want a different effect for the talking and non-talking versions, you'll mostly
            #   be doing stuff in here. The actual values you want will depend on the properties you want
            #   to change. But will boil down to having the curr_ease * some_amount_of_change.
            # - Both transformations should also smoothly flow into each other.
            #   For example, if the talking non-talking version has the sprite moved down 10 pixels,
            #   the talking version should start from 10 pixels down and rise up.
            if is_talking: # Apply the talking transformation
                trans.matrixcolor = SaturationMatrix((1.0-sat_change) + curr_ease * sat_change) * BrightnessMatrix(-bright_change + curr_ease * bright_change)
                trans.zoom = min(curr_ease * zoom_change + (1.0-zoom_change), 1.0)
                trans.yoffset = y_change - curr_ease * y_change # Delete here if you removed y_change earlier
            else:           # Apply the not-talking transformation
                trans.matrixcolor = SaturationMatrix(1.0 - curr_ease * sat_change) * BrightnessMatrix(curr_ease * -bright_change)
                trans.zoom = max(1.0 - curr_ease * zoom_change, (1.0-zoom_change))
                trans.yoffset = y_change * curr_ease            # Delete here if you removed y_change earlier
            # Finally, we don't really want to ever stop running this.
            # So we just ask to be continuously redrawn ASAP forever.
            # Returning > 0 will cause it to redraw slower. And returning None will cause it to stop running
            return 0
