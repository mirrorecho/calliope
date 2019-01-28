Bubble

    container_type = abjad.Container
    lilypond_type== None
    is_simultaneous=True
    music_contents = None
    stylesheets = () # TO DO, best place for this?

    child_types = (Bubble,)

Score(calliope.Bubble)

    container_type=abjad.Score
    is_simultaneous = None
    # TO DO: REMOVE?
    # hide_empty = False 
    # title = ""

    child_types=(calliope.Staff, calliope.StaffGroup)

StaffGroup(calliope.Bubble)

    container_type = abjad.StaffGroup
    is_simultaneous = True
    instrument = None # NEW: unique to StaffGroup
    
    select_property = "staff_groups"
    StaffGroup.child_types = (Staff, StaffGroup)

Staff(calliope.Bubble)

    container_type = abjad.Staff
    is_simultaneous = False
    instrument = None
    clef = None

    select_property = "staves"

( {Voice} ) ( <<VoiceBlock>> )  ... to do figure this out

Machine # (anthing that applies to all machines)

    can_have_children = True # TO DO: move to Tree?
    must_have_children = True # TO DO: used? move to Tree?
    transforms = () # can be set to any iterable
    factory = None
    is_simultaneous = False
    bar_line = None # TO DO: keep?
    respell = None # set to "sharps" or "flats"  to force respelling

Fragment # (anthing that applies to machines that contain other machines)

    metrical_durations = None
    use_child_metrical_durations = False
    meter = None
    time_signature = None
    pickup = None # must be able to be represented as a single note with no dots

FragmentBlock


FragmentRow
    

Section

Phrase -> PhraseBlock

Cell -> CellBlock

Event -> EventBlock

LogicalTie -> Chord




{Section} <<SectionBlock>>
( {Line} ) <<LineBlock>>
( {Cell} )(...) <<CellBlock>>
Event
LogicalTie
(Leaf) (psuedo) <<Chord>>(psuedo)

Score
 - is_simultaneous=True
