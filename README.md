# Auto-Highlight
 Demo project for the Auto Highlight module for Ren'py.

## Main File
If you're looking to add the effect to your game, then simply download the file [game/00auto-highlight.rpy](game/00auto-highlight.rpy) and add it to your project's game folder.

## Setup
After adding the file to your project, there's two things you'll have to do to get it setup.
1. You'll need to setup your character definitions to support it. Namely, including `name_callback` in the callback parameter and adding `cb_name` as a parameter. For example: `define eil = Character("Eileen", callback = name_callback, cb_name = "eileen")`
  - Remember that Ren'py supports say_with_arguments. So you can assign one for a particular line by doing: `eil "I think someone else should be focused" (cb_name = "pileen")`
  - Finally, if you wish for the special narrator to make all sprites unfocused or something similar, you can copy this. `define narrator = Character(callback = name_callback, cb_name = None)`
2. You'll need to apply the sprite_highlight transform to all images you want this applied to. For people using layeredimages, this is very easy. As an example: 
```
layeredimage eileen:
    at sprite_highlight('eileen')
    ...
 ```
  - However, if you're using individual sprites, you'll have to be sure this is applied to every one. 
  ```
image eileen happy = At('eileen_happy', sprite_highlight('eileen'))
image eileen sad = At('eileen_sad', sprite_highlight('eileen')) 
```
  - Or, if you'd prefer an ATL example
```
image eileen happy:
    'eileen_happy'
    function SpriteFocus('eileen')
```
With all of that done, you should be all setup to make use of it.
  

## Credits
- Demo script written in a voice all with members in the [FVN Discord](https://discord.gg/GFjSPkh)
- Kota and Luke sprites are used with permission from [Minotaur Hotel](https://minoh.itch.io/minotaur-hotel-sfw). These are not covered by the MIT License. All rights to these sprites belong to the owners. 
