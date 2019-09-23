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
    # select_property = "bubbles" # TO DO: causes oddo recursion when setting properties on startup... WHY?
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

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = abjad.LilyPondFile.new(music, includes=self.stylesheets, 
            )
        self.info("got abjad representation of lilypond file... now rendering with lilypond")
        return lilypond_file

    def illustrate_me(self, 
            as_pdf = True, 
            open_pdf = True, 
            as_midi = False,
            **kwargs
        ):

        # NOTE... this is odd... with sublimetext using the virtual envionment package on a mac ONLY, 
        # lilypond executable is not found properly (something to do with os.environ not finding the right PATH info)
        # ... adding this here as a bandaid:
        mac_default_lilypond_path = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
        if os.path.exists(mac_default_lilypond_path):
            from abjad import abjad_configuration
            abjad_configuration["lilypond_path"] = mac_default_lilypond_path

        ly_file = self.get_lilypond_file()
        my_persistance_agent = abjad.persist( ly_file )

        path = self.get_output_path(**kwargs)
        # print("%s.ly" % path)

        if as_pdf:
            pdf_filename = "%s.pdf" % path
            my_persistance_agent.as_pdf(pdf_filename)
            if open_pdf:
                abjad.IOManager.open_file(pdf_filename)
        if as_midi:
            midi_filename = "%s.midi" % path
            my_persistance_agent.as_midi(midi_filename)


