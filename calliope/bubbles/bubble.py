import os, inspect
import abjad
import calliope

class Bubble(calliope.Tree):
    """
    A factory for an abjad container.
    """
    container_type=abjad.Container
    context_name=None
    respell=None # TO DO, best place for this?
    stylesheets = () # TO DO, best place for this?
    is_simultaneous=True
    music_contents = None
    child_types = ()
    parent_type = None
    # NOTE: should never set "name" attribute at the class level... because it's an attribute (with setter logic) on the abjad TreeContainer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.parent_type:
            self.parent_type = Bubble
        if not self.child_types:
            self.child_types = (Bubble,)

    # # TO DO: is this the best place for mapping???
    # def map_to(self, *args, **kwargs):
    #     # TO DO... IMPLEMENT MORE FULLY
    #     bubble_type = args[0]
    #     if type(args[1]) is calliope.Mapping:
    #         my_mapping = args[1]
    #     return bubble_type( *my_mapping.map_root.map_bubble(self, as_copy=True) )

    # def map_filter(self, *args, **kwargs):
    #     if args[0] is Mapping:
    #         my_mapping = args[0]

    # TO DO... this implementation of add/mul creates odd nested containers... rethink
    # Could also conflict with abjad tree structures
    def __add__(self, other):
        return self.parent_type(self(), other)

    def __mul__(self, num):
        return self.parent_type( **[self() for i in range(num)] )

    def get_module_info(self):
        """Returns a tuple with the path and name for the module in which this bubble class is defined"""
        module_file = inspect.getmodule(self).__file__
        return os.path.dirname(module_file), os.path.split(module_file)[1].split(".")[0]

    def get_output_path(self, 
            directory=None, 
            sub_directory="illustrations", 
            filename=None, 
            filename_suffix="",
            **kwargs
            ):

        if not directory or not filename:
            module_directory, module_name = self.get_module_info()
        
        directory = directory or module_directory
        full_directory = os.path.join(directory, sub_directory)
        if not os.path.exists(full_directory):
            os.makedirs(full_directory)

        if not filename:
            filename = module_name
            if self.name:
                filename = "_".join([filename, str.lower(self.name)])

        if filename_suffix:
            filename = "_".join([filename, filename_suffix])

        return os.path.join(full_directory, filename)


    def illustrate_me(self, 
            score_type = None,
            as_pdf = True, 
            open_pdf = True, 
            as_midi = False,
            **kwargs
        ):
        # NOTE... this is odd... within sublimetext using the virtual envionment package on a mac ONLY, 
        # lilypond executable is not found properly (something to do with os.environ not finding the right PATH info)
        # ... adding this here as a band-aid:
        mac_default_lilypond_path = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
        if os.path.exists(mac_default_lilypond_path):
            from abjad import abjad_configuration
            abjad_configuration["lilypond_path"] = mac_default_lilypond_path
        
        bubble_to_illustrate = self if not score_type else score_type(self)
        # print(bubble_to_illustrate.ly())

        my_persistance_agent = abjad.persist( bubble_to_illustrate.get_lilypond_file() )
        path = self.get_output_path(**kwargs)
        
        if as_pdf:
            pdf_filename = "%s.pdf" % path
            my_persistance_agent.as_pdf(pdf_filename)
            if open_pdf:
                abjad.systemtools.IOManager.open_file(pdf_filename)
        if as_midi:
            midi_filename = "%s.midi" % path
            my_persistance_agent.as_midi(midi_filename)

    def music_container(self, **kwargs):
        if self.is_simultaneous is not None:
            kwargs["is_simultaneous"] = self.is_simultaneous
        if self.context_name is not None:
            kwargs["context_name"] = self.context_name
        return self.container_type(name=self.name, **kwargs)

    def ly(self):
        return format(self.blow())

    def get_lilypond_file(self):
        music = self.blow()
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(music, includes=self.stylesheets, 
            )
        self.info("got abjad representation of lilypond file... now rendering with lilypond")
        return lilypond_file

    def child_music(self, child_bubble):
        # can be overridden to add custom stuff for each child of a particular bubble
        return child_bubble.blow()

    def process_music(self, music, **kwargs):
        pass

    def music(self, **kwargs):
        my_container = self.music_container(**kwargs)
        my_container.extend(
            self.music_contents if self.music_contents 
            else [ self.child_music( b ) for b in self ] 
            )
        return my_container

    def blow(self, **kwargs):
        my_music = self.music(**kwargs)
        self.process_music(my_music, **kwargs)
        return my_music

