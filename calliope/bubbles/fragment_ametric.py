import calliope

# TO DO... THIS IS NOT PROPERLY IMPLEMENTED... NEED TO REVISIT
class Ametric(calliope.Fragment):
    show_x_meter = False
    show_time_span = False
    start_text = None # e.g. "Freely"
    time_span_text = None # e.g. "10'' ca"
    duration = (2,1)
    start_bar_line = "!"
    end_bar_line = None
    accidental_style = None

    def blow_bubble(self, bubble_name):
        """
        overriding blow_bubble to add free stuff to each sub-bubble
        """
        music = super().blow_bubble(bubble_name)
        
        # this will auto-increase the length of the music (in skips) to the length of the Ametric duration
        add_skips_duration = Duration(self.duration) - inspect_(music).get_duration()
        if add_skips_duration > 0:
            skips = scoretools.make_skips( Duration(1, add_skips_duration.denominator), ((add_skips_duration.numerator,add_skips_duration.denominator),) )
            music.append(skips)

        leaves = select(music).by_leaf()
        if self.show_x_meter:
            x_meter_command = indicatortools.LilyPondCommand( ("timeX"), "before" )
            attach(x_meter_command, music)
        else:
            # HIDE THE TIME SIGNATURE:
            hide_time_command = indicatortools.LilyPondCommand("""once \override Staff.TimeSignature #'stencil = ##f """, "before")
            attach(hide_time_command, music)
        if self.duration:
            time_command =  indicatortools.LilyPondCommand("time " + str(self.duration[0]) + "/" + str(self.duration[1]), "before")
            attach(time_command, music)
        if self.start_bar_line:
            bar_command =  indicatortools.LilyPondCommand('bar "' + self.start_bar_line + '"', 'before')
            attach(bar_command, music)
        else:
            # MAYBE TO DO... auto calculate bar-length based on longest bubble
            pass
        if self.start_text or self.time_span_text:
            # TO DO... this could conflict with tempo mark / text
            # ALSO MAYBE TO DO... better time_span_text using a measure-length spanner
            my_text = ", ".join([t for t in [self.start_text, " " + self.time_span_text] if t])
            tempo_text = indicatortools.Tempo(textual_indication=my_text)
            attach(tempo_text, music)
        if self.accidental_style:
            accidental_style_command = indicatortools.LilyPondCommand("accidentalStyle " + self.accidental_style, "before")
            attach(accidental_style_command, music)
        return music

class AmetricStart(Ametric):
    start_bar_line = "||"
    show_x_meter = True
    start_text = "Freely"
    accidental_style = "neo-modern-cautionary"