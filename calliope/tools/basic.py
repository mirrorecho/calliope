# import importlib
import inspect, os
import abjad

def illustrate_me(
            bubble = None,
            filename=None, 
            subfolder="illustrations", 
            score_type=None,
            as_pdf=True, 
            open_pdf=True, 
            as_midi=False):

    from calliope import bubbles
    
    calling_info = inspect.stack()[1]
    calling_module_path = calling_info[1]
    calling_module_name = os.path.split(calling_module_path)[1].split(".")[0]
    calling_module = inspect.getmodule( calling_info[0] )

    if not score_type:
        score_type = bubbles.AutoScore

    # only illustrate if being called from main module (as opposed to import)
    if calling_module.__name__ == "__main__":

        if not bubble:
            bubble = bubbles.ModuleBubble(calling_module)
        elif inspect.isclass(bubble):
            bubble = bubble()
        my_score = score_type( bubble )
        illustration_directory_path = os.path.join(
            os.path.dirname(calling_module_path),
            subfolder,
            )
        if not os.path.exists(illustration_directory_path):
            os.makedirs(illustration_directory_path)

    #     # NOTE... this is odd... within sublimetext using the virtual envionment package on a mac ONLY, 
    #     # lilypond executable is not found properly (something to do with os.environ not finding the right PATH info)
    #     # ... adding this here as a band-aid to solve that
        mac_default_lilypond_path = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
        if os.path.exists("/Applications/LilyPond.app/Contents/Resources/bin/lilypond"):
            from abjad import abjad_configuration
            abjad_configuration["lilypond_path"] = mac_default_lilypond_path

        my_persistance_agent = abjad.persist( my_score.get_lilypond_file() )

        filename = filename or calling_module_name
        
        if as_pdf:
            pdf_filename = "%s.pdf" % filename
            illustration_file_path = os.path.join(
                illustration_directory_path,
                pdf_filename,
                )

            my_persistance_agent.as_pdf(illustration_file_path)
            if open_pdf:
                abjad.systemtools.IOManager.open_file(illustration_file_path)
        if as_midi:
            pdf_filename = "%s.midi" % filename
            midi_file_path = os.path.join(
                illustration_directory_path,
                pdf_filename,
                )
            my_persistance_agent.as_midi(midi_file_path)