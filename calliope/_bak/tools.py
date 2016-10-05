from abjad import *

import copy



def attach_commands(commands, music_object):
    for c in commands:
        attach(c, music_object)


# adds the box marks (sans the single line staff before/after)
def make_box_marks(music_start_item, music_end_item):
    box_start_commands = [
        indicatortools.LilyPondCommand("once \\override BreathingSign #'break-align-symbol = #'custos", 'before'),
        indicatortools.LilyPondCommand("""once \\override Staff.TimeSignature.space-alist =
            #'((first-note . (fixed-space . 2.0))
               (right-edge . (extra-space . 0))
               ;; space after time signature ..
               (custos . (extra-space . 0)))""", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'text = \\markup { \\filled-box #'(0 . 0.4) #'(-1.4 . 1.4) #0 }", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'break-visibility = #end-of-line-invisible", 'before'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'Y-offset = ##f", 'before'),
        indicatortools.LilyPondCommand("once \\override Staff.BarLine #'space-alist = #'((breathing-sign fixed-space 0))", 'before'),
        indicatortools.LilyPondCommand("breathe", 'before'),
        ]
    box_stop_commands = [
        indicatortools.LilyPondCommand("once \\override BreathingSign #'text = \markup { \\filled-box #'(0 . 0.4) #'(-1.4 . 1.4) #0 }", 'after'),
        indicatortools.LilyPondCommand("once \\override BreathingSign #'Y-offset = ##f", 'after'),
        indicatortools.LilyPondCommand("breathe", 'after'),
    ]
    attach_commands(box_start_commands, music_start_item)
    attach_commands(box_stop_commands, music_end_item)

def hidden_leaf(length=(1,4), pitch=None):
    if pitch == None:
        leaf = scoretools.Rest(length)
    else:
        leaf = scoretools.Note(pitch, length)
    hide_notes = indicatortools.LilyPondCommand("hideNotes", 'before')
    unhide_notes = indicatortools.LilyPondCommand("unHideNotes", 'after')
    attach(hide_notes, leaf)
    attach(unhide_notes, leaf)
    return leaf

def continue_arrow():
    arrow_commands = [
            indicatortools.LilyPondCommand("once \override Rest  #'stencil = #ly:text-interface::print", "before"),
            indicatortools.LilyPondCommand("once \override Rest.staff-position = #-2.2", "before"),
            indicatortools.LilyPondCommand("once \override Rest #'text = \\markup { \\fontsize #6 { \\general-align #Y #DOWN { \\arrow-head #X #RIGHT ##t } } }" , "before"),
            ]
    rest_arrow = scoretools.Rest((1,16))
    attach_commands(arrow_commands, rest_arrow)
    return rest_arrow


def staff_line_commands(lines=(-4, -2, 0, 2, 4), command_position="after"):
    commands = []
    commands.append(indicatortools.LilyPondCommand("stopStaff", command_position))
    commands.append(indicatortools.LilyPondCommand(
                "override Staff.StaffSymbol #'line-positions = #'(" + " ".join([str(i) for i in lines]) + ")", 
                command_position))
    commands.append(indicatortools.LilyPondCommand("startStaff", command_position))
    return commands


def line_staff_skip(position="grace", continue_staff=False):

    #skip = scoretools.Skip(skip_length)
    
    before_staff_line_skip = hidden_leaf((1,32))
    before_staff_normal_skip = hidden_leaf((1,16))

    attach_commands(staff_line_commands((-0.4, -0.3, -.2, -.1, 0, .1, .2, .3, .4)), before_staff_line_skip)
    attach_commands(staff_line_commands(()), before_staff_normal_skip)

    skip_container = scoretools.GraceContainer(kind=position)
    skip_container.append(before_staff_line_skip)    
    if not continue_staff:
        skip_container.append(before_staff_normal_skip)
    return skip_container

def line_staff_continue(continue_lengths, is_percussion=False):
    # (we're assuming that the staff has already been converted to a line)
    line_container = Container()
    for d in continue_lengths:

        # append a hidden leaf for the first half of the continue line for this duration
        half_continue = (d[0], d[1]*2)
        line_container.append(hidden_leaf(half_continue))

        # now make a hidden leaf for the second half, but attach an arrow to the beginning of it
        # also the 2nd hidden leaf is a NOTE (not a rest)... that way lines will never be hidden
        half_continue_leaf2 = hidden_leaf(half_continue, 0)
        arrow_container = scoretools.GraceContainer()
        arrow_container.append(continue_arrow())
        attach(arrow_container, half_continue_leaf2)
        # now append the leaf for the second half (with the arrow)
        line_container.append(half_continue_leaf2)

    # now return the staff to normal
    if is_percussion:
        attach_commands(staff_line_commands((0,)), line_container[-1] )
    else:
        attach_commands(staff_line_commands(()), line_container[-1] )
    
    return line_container



# can live with this for now... but would be nicer to avoid having to use skips
def box_music(music, instruction=None, continue_lengths=None, is_percussion=False):
    music = get_music_container(music)
    music_selection = music.select_leaves()
    if len(music_selection) > 0:

        if not is_percussion:
            attach(line_staff_skip(), music_selection[0])

        if instruction is not None:
            instruction_markup = markuptools.Markup('\italic { "' + instruction + '" }', direction=Up)
            attach(instruction_markup, music_selection[0])

        continue_line_staff = False if continue_lengths is None else True

        attach(line_staff_skip(position="after", continue_staff=continue_line_staff), music_selection[-1])

        if continue_line_staff:
            music.extend(line_staff_continue(continue_lengths, is_percussion=is_percussion))

        return music
    else:
        print("Error... tried to create a box around empty music")




