import abjad
import calliope

class SmearAfter(calliope.Transform):
    """
    bass class for all transforms
    """
    min_beats = 0
    extend_beats = 0

    fill = False
    max_beats = 0 # only useful if fill=True

    cover_notes = False
    gap_beats = 0 #gap between current note and next note
    sib_relation = 1

    rearticulate = False
    ancestor = None

    def transform(self, selectable, **kwargs):
        ancestor = self.ancestor or selectable
        removed_es = []
        if self.sib_relation == 1:
            my_list = list(selectable.note_events)
        else:
            my_list = reversed(list(selectable.note_events))

        for e in my_list:
            if e not in removed_es:
                my_beats = max([self.min_beats, e.beats+self.extend_beats])
                following_es = []
                ref_e = e
                beats_counter = ref_e.beats
                while ref_e and ref_e.tree_sib(self.sib_relation, ancestor) is not None and (
                    ref_e.tree_sib(self.sib_relation, ancestor).skip_or_rest
                    or (my_beats and self.cover_notes and my_beats > beats_counter)
                    ):
                    
                    following_e = ref_e.tree_sib(self.sib_relation, ancestor)
                    following_es.append(following_e)
                    ref_e = following_e
                    beats_counter += ref_e.beats
                    # print("yo", ref_e.tree_sib(self.sib_relation, ancestor))

                sum_following_es = sum([r.beats for r in following_es])
                sum_beats = e.beats + sum_following_es
                min_gap_beats = min([self.gap_beats, sum_following_es])


                if self.fill:
                    new_beats = e.beats + sum_following_es - min_gap_beats
                elif my_beats:
                    new_beats = min([my_beats, sum_beats-min_gap_beats])
                    new_beats = max([new_beats, e.beats])

                if self.max_beats and new_beats > self.max_beats:
                    new_beats = self.max_beats
                elif new_beats < e.beats:
                    new_beats = e.beats - my_gap   

                beats_diff = sum_beats - new_beats
                beats_counter = e.beats

                if self.rearticulate and new_beats > e.beats:
                    my_e = calliope.Event(beats=new_beats - e.beats, pitch=e.pitch)
                    if self.sib_relation == 1:
                        e.parent.insert(e.my_index+1, my_e)
                    else:
                        e.parent.insert(e.my_index, my_e)
                else:
                    e.beats = new_beats
                    my_e = e

     

                for fe in following_es:
                    beats_counter += fe.beats
                    if beats_diff and beats_counter > new_beats:
                        fe.beats = (0-beats_diff) if fe.skip_or_rest else beats_diff
                        beats_diff = 0
                    else:
                        if fe not in removed_es:
                            fe.parent.remove(fe)
                            removed_es.append(fe)
                if beats_diff:
                    my_e.parent.insert(my_e.my_index+self.sib_relation, 
                        calliope.Event(beats=0-beats_diff)
                        )



class SmearBefore(SmearAfter):
    sib_relation = -1


# if __name__ == '__main__':

#     l = calliope.Line(
#         *[calliope.Cell(
#             rhythm=(-1, 0.5, 1, -0.5, 1, -2, -2),
#             pitches=("R", 4, 5, "R", 0, "R", "R",),
#             ) for i in range(4) ])
#     lb = calliope.LineBlock(
#         l(),
#         l().transformed(calliope.SmearBefore(fill=True, rearticulate=True)),
#         l().transformed(calliope.SmearAfter(min_beats=1.5, cover_notes=True)),
#         )
        
#     calliope.illustrate(lb.to_score())




