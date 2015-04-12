#!/usr/bin/env python

import glob
import os
import music21
from music21.figuredBass import checker


for item in glob.glob('371chorales/*.krn'):
    aname = os.path.basename(item)
    name = os.path.splitext(aname)[0]

    print "* converting", name

    score = music21.converter.parse(item)
    moments = checker.getVoiceLeadingMoments(score)
    moments.write('musicxml', os.path.join('xml', name + '.xml'))
