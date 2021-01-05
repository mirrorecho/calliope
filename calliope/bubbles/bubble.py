import os
import abjad
import calliope

# TO DO: consider... should this be a mixin????
class Bubble(calliope.Tree):
    """
    A factory for an abjad container.
    """
    container_type=abjad.Container
    lilypond_type=None
    stylesheets = () # TO DO, best place for this?
    is_simultaneous=True
    music_contents = None
    factory = None # a factory for this factory! :-)

    def __init__(self, *args, **kwargs):

        if isinstance(self, calliope.Factory):
            self.factory = self

        super().__init__(*args, **kwargs)


    def set_children_from_class(self, *args, **kwargs):
        """ overrides Tree's set_children_from_class in order call fabricate on factory instance """
        if self.factory is not None:
            if self.factory.masks == False:
                super().set_children_from_class(*args, **kwargs)
            self.factory.fabricate(self, *args, **kwargs) # TO DO... remove args/kwargs here?
        else:
            super().set_children_from_class(*args, **kwargs)

    # select_property = "bubbles" # TO DO: causes odd recursion when setting properties on startup... WHY?
    # NOTE: should never set "name" attribute at the class level... because it's an attribute (with setter logic) on the uqbar UniqueTreeContainer

    def music_container(self, *args, **kwargs):
        if self.is_simultaneous is not None:
            kwargs["is_simultaneous"] = self.is_simultaneous
        if self.lilypond_type:
            kwargs["lilypond_type"] = self.lilypond_type
        if self.name:
            kwargs["name"] = self.name
        return self.container_type(*args, **kwargs)

    def music(self, **kwargs):
        my_container = self.music_container(**kwargs)
        my_container.extend(
            self.music_contents if self.music_contents 
            else [ self.child_music( b ) for b in self ] 
            )
        return my_container

    def process_music(self, music, **kwargs):
        pass

    def blow(self, **kwargs):
        my_music = self.music(**kwargs)
        self.process_music(my_music, **kwargs)
        return my_music

    # TO DO - KISS?
    def child_music(self, child_bubble):
        # can be overridden to add custom stuff for each child of a particular bubble
        return child_bubble.blow()

    def ly(self):
        return format(self.blow())

    def get_lilypond_file(
        self, 
        as_midi=False,
        composer="Randall West",
        title=None,
        part_name=None,
        piece_name=None,
        transpose_me = False,
        **kwargs,
        ):
        music = self.blow()

        # TO DO... NOT THE BEST PLACE FOR TRANSPOSITIONS
        if transpose_me:
            staves = getattr(self, "staves", None)
            if staves:
                abjad_staves = abjad.select(music).components(abjad.Staff)
                for staff, abjad_staff in zip(staves, abjad_staves):
                    if staff.instrument:
                        staff.instrument.transpose_from_sounding_pitch(abjad_staff)
                        staff.info("transposing to: " + str(staff.instrument.middle_c_sounding_pitch))
                    else:
                        staff.warn("CANNOT TRANSPOSE... staff has no instrument")

        if as_midi:
            tempo = getattr(self, "midi_tempo", 60)
            midi_command = abjad.LilyPondLiteral("""
                \\midi {
                    \\context {
                        \\Score
                        midiChannelMapping = #'instrument
                    }
                    \\tempo 4 = %s
                }
                \\layout { }                 
                """
                 % tempo, "after")
            abjad.attach(midi_command, music)

        lilypond_file = abjad.LilyPondFile.new(
            music, 
            includes=self.stylesheets, 
            )
        # self.info("got abjad instance of LilyPondFile... now rendering with lilypond")
        
        lilypond_file.header_block.composer = abjad.Markup(composer)
        if title is not None:
            lilypond_file.header_block.title = abjad.Markup(title)
        if part_name is not None:
            lilypond_file.header_block.instrument = abjad.Markup(part_name)
        if piece_name is not None:
            lilypond_file.header_block.piece = abjad.Markup(piece_name)

        return lilypond_file

    def illustrate_me(self, 
            as_pdf = True, 
            open_pdf = True, 
            as_midi = False,
            open_midi = False,
            **kwargs
        ):
        self.info("ready to illustrate")

        # BELOW IS NO LONGER NEEDED WITH ABJAD CONFIG FILE
        # NOTE... this is odd... with sublimetext using the virtual envionment package on a mac ONLY, 
        # lilypond executable is not found properly (something to do with os.environ not finding the right PATH info)
        # ... adding this here as a bandaid:
        # mac_default_lilypond_path = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
        # if os.path.exists(mac_default_lilypond_path):
        #     from abjad import abjad_configuration
        #     abjad_configuration["lilypond_path"] = mac_default_lilypond_path

        ly_file = self.get_lilypond_file(as_midi=as_midi, **kwargs)
        my_persistance_agent = abjad.persist( ly_file )

        path = self.get_output_path(**kwargs)
        # print("%s.ly" % path)

        if as_pdf:
            pdf_filename = "%s.pdf" % path
            my_pdf = my_persistance_agent.as_pdf(pdf_filename)
            print(my_pdf)
            if open_pdf:
                abjad.IOManager.open_file(pdf_filename)
        if as_midi:
            midi_filename = "%s.midi" % path
            # my_persistance_agent.as_midi(midi_filename)
            if open_midi:
                abjad.IOManager.open_file(midi_filename)

