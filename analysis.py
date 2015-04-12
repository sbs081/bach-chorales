#!/usr/bin/env python

from __future__ import print_function
import glob
from itertools import combinations
import os
import music21
from music21.figuredBass import checker
from music21.interval import notesToChromatic
from music21.expressions import Fermata


SKIP_CHORALES = ["chor043", "chor133", "chor143", "chor280", "chor283",
                 "chor316", "chor358"]


def _interval(a, b):
    return abs(notesToChromatic(a, b).semitones) % 12


def is_direct_fifth_or_octave(voice1, voice2, k):
    i = _interval(voice1[k], voice2[k])

    if i == 7 or i == 0:
        d1 = notesToChromatic(voice1[k - 1], voice1[k]).direction
        d2 = notesToChromatic(voice2[k - 1], voice2[k]).direction
        return (d1 == d2) and (d1 != 0)


def has_fermata(segment):
    return any(isinstance(expression, Fermata) for expression in segment.expressions)


def is_one_step(s1, s2):
    steps = [0, 1, 2]
    return True if s1 in steps or s2 in steps else False


def voice_combinations(size):
    return combinations(range(size), 2)


def make_lily_score(music_data, score):
    for item in music_data:
        m = item[3]
        outname = item[11] + '.ly'
        stream = score.measures(m - 1, m)
        stream.write('lily', outname)


def analyze_chorale_in_voices(voices, positions, choral_name):
    # pos1 = higher, pos2 = lower

    def notes(k):
        name1 = voice2[k].name.replace("-", "b")
        name2 = voice1[k].name.replace("-", "b")
        return "%s-%s" % (name1, name2)

    name = ["soprano", "alto", "tenor", "bass"]
    pos1, pos2 = positions
    voice1 = voices[pos1]
    voice2 = voices[pos2]
    size = len(voice1)
    result = []

    for x in xrange(1, size):
        if is_direct_fifth_or_octave(voice2, voice1, x):
            segment_human = x + 1  # humans like to read starting from 1
            n1, n2 = voice1[x], voice2[x]
            p1, p2 = voice1[x - 1], voice2[x - 1]
            measure = n1.measureNumber

            fermata = has_fermata(n1) or has_fermata(p1)
            step1 = _interval(p1, n1)
            step2 = _interval(p2, n2)

            aname = os.path.splitext(choral_name)[0]
            figname = '%s/figs/%s-%d' % (os.path.curdir, aname, measure)

            result.append((choral_name, name[pos2], name[pos1],
                           measure, segment_human,
                           step1, step2, is_one_step(step1, step2),
                           notes(x - 1), notes(x), fermata, figname))

    return result


def split_voices(score):
    parts_number = len(score.parts)
    voices = [score.parts[x].flat.notes for x in range(parts_number)]
    sizes = [len(x) for x in voices]

    if len(set(sizes)) != 1:
        raise Exception("Voices don't have the same size:", sizes)
    else:
        return voices


def analyze_chorale(score, name):
    voices = split_voices(score)

    result = []
    for pos in voice_combinations(len(voices)):
        data = analyze_chorale_in_voices(voices, pos, name)
        result.extend(data)
        make_lily_score(data, score)
    return result


def analyze_all_chorales(log=True):
    if log:
        out = open('result.csv', 'w')
        out.write("name,voices,measure,segment,step1,step2,one-voice-step,notes1,notes2,fermata,figname\n")

    for chorale in sorted(glob.glob("kern/*.krn")):
        name = os.path.basename(chorale)
        root_name = os.path.splitext(name)[0]

        score = music21.converter.parse(chorale)
        segments = checker.getVoiceLeadingMoments(score)

        if root_name not in SKIP_CHORALES:
            print("* Chorale: ", root_name)
            result = analyze_chorale(segments, root_name)
            if log:
                for item in result:
                    out.write("%s,%s-%s,%d,%d,%s,%s,%s,%s,%s,%s,%s\n" % item)
                    out.flush()
        else:
            print("- [SKIP] ", root_name)


analyze_all_chorales(log=False)
