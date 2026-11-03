"""Tunzle melody library: public-domain melodies written as note strings.

Format: "NOTE/beats NOTE/beats ..."  e.g. "E5/1 D#5/.5 R/1"  (R = rest, beats default 1)
"beat" = seconds per beat. "cat" = calendar category. "level" = default difficulty.
"check": True marks melodies worth a quick listen before they are posted.
Add your own entries in the same format; keep them public domain (composer died 70+ years ago / pre-1929).
"""

M = {
# ---------------- classical ----------------
"fur_elise": dict(name="FÜR ELISE", sub="Beethoven (1810)", cat="classical", level="Medium", beat=.19,
    notes="E5 D#5 E5 D#5 E5 B4 D5 C5 A4/2 R C4 E4 A4 B4/2 R E4 G#4 B4 C5/2 R E4 E5 D#5 E5 D#5 E5 B4 D5 C5 A4/2 R C4 E4 A4 B4/2"),
"ode_to_joy": dict(name="ODE TO JOY", sub="Beethoven – 9th Symphony (1824)", cat="classical", level="Easy", beat=.3,
    notes="E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4/1.5 D4/.5 D4/2 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4/1.5 C4/.5 C4/2"),
"beethoven5": dict(name="SYMPHONY NO. 5", sub="Beethoven (1808)", cat="classical", level="Easy", beat=.25,
    notes="R/.5 G4/.5 G4/.5 G4/.5 D#4/4 R/1 F4/.5 F4/.5 F4/.5 D4/4 R/2 G4/.5 G4/.5 G4/.5 D#4/4 R/1 F4/.5 F4/.5 F4/.5 D4/4"),
"nachtmusik": dict(name="EINE KLEINE NACHTMUSIK", sub="Mozart (1787)", cat="classical", level="Medium", beat=.16,
    notes="G4/2 R D4 G4/2 R D4 G4 D4 G4 B4 D5/4 R/2 C5/2 R A4 C5/2 R A4 C5 A4 F#4 A4 D4/4"),
"turkish_march": dict(name="TURKISH MARCH", sub="Mozart – Rondo alla Turca (1784)", cat="classical", level="Medium", beat=.13,
    notes="B4 A4 G#4 A4 C5/2 R/2 D5 C5 B4 C5 E5/2 R/2 F5 E5 D#5 E5 B5 A5 G#5 A5 B5 A5 G#5 A5 C6/4"),
"canon": dict(name="CANON IN D", sub="Pachelbel (c. 1680)", cat="classical", level="Medium", beat=.32,
    notes="F#5/2 E5/2 D5/2 C#5/2 B4/2 A4/2 B4/2 C#5/2 D5/2 C#5/2 B4/2 A4/2 G4/2 F#4/2 G4/2 E4/2"),
"brahms_lullaby": dict(name="BRAHMS' LULLABY", sub="Brahms (1868)", cat="classical", level="Easy", beat=.35, check=True,
    notes="E4/.5 E4/.5 G4/2 E4/.5 E4/.5 G4/2 E4/.5 G4/.5 C5 B4/1.5 A4/.5 A4 G4 D4/.5 E4/.5 F4 D4 D4/.5 E4/.5 F4/2"),
"morning_mood": dict(name="MORNING MOOD", sub="Grieg – Peer Gynt (1875)", cat="classical", level="Medium", beat=.25, check=True,
    notes="G5 E5 D5 C5 D5 E5 G5 E5 D5 C5 D5/.5 E5/.5 D5/.5 E5/.5 G5 E5 G5 A5 E5 A5 G5 E5 D5 C5/3"),
"blue_danube": dict(name="THE BLUE DANUBE", sub="Johann Strauss II (1866)", cat="classical", level="Medium", beat=.22,
    notes="C4 C4 E4 G4 G4/2 R G5 G5/2 E5 E5/2 R C4 C4 E4 G4 G4/2 R G5 G5/2 F5 F5/2"),
"hallelujah": dict(name="HALLELUJAH CHORUS", sub="Handel – Messiah (1741)", cat="opera", level="Easy", beat=.33,
    notes="D5 A4/.75 B4/.25 A4 R D5 A4/.75 B4/.25 A4 R A4/.5 B4/.5 A4/.5 B4/.5 A4 A4/.5 B4/.5 A4 D5/2"),
# ---------------- movie & cartoon ----------------
"william_tell": dict(name="WILLIAM TELL OVERTURE", sub="Rossini (1829) – the 'Lone Ranger' gallop", cat="movie", level="Easy", beat=.14,
    notes="G4/.5 G4/.5 G4 G4/.5 G4/.5 G4 G4/.5 G4/.5 C5 D5 E5/2 G4/.5 G4/.5 G4 G4/.5 G4/.5 G4 G4/.5 G4/.5 E5 D5 C5/2 "
          "G4/.5 G4/.5 G4 G4/.5 G4/.5 G4 G4/.5 G4/.5 C5 D5 E5/2"),
"can_can": dict(name="CAN-CAN", sub="Offenbach (1858) – Infernal Galop", cat="movie", level="Easy", beat=.14,
    notes="C4/2 D4 F4 E4 D4 G4/2 G4/2 G4 A4 E4 F4 D4/2 D4/2 D4 F4 E4 D4 C4 C5 B4 A4 G4 F4 E4 D4 "
          "C4/2 D4 F4 E4 D4 G4/2 G4/2 G4 A4 E4 F4 D4/2 D4/2 D4 F4 E4 D4 C4 G4 D4 E4 C4/4"),
"zarathustra": dict(name="ALSO SPRACH ZARATHUSTRA", sub="Richard Strauss (1896) – the '2001' theme", cat="movie", level="Medium", beat=.27,
    notes="C3/5 G3/5 C4/4 E4/1.2 D#4/6 R C2/.8 G1/.8 C2/.8 G1/.8 C2/.8 G1/.8 C2/.8 G1/.8 C2"),
"funeral_march": dict(name="FUNERAL MARCH", sub="Chopin (1839)", cat="movie", level="Medium", beat=.27,
    notes="A#3/2 A#3/1.5 A#3/.5 A#3/2 C#4/1.5 C4/.5 C4/1.5 A#3/.5 A#3/1.5 A3/.5 A#3/2 R "
          "A#3/2 A#3/1.5 A#3/.5 A#3/2 C#4/1.5 C4/.5 C4/1.5 A#3/.5 A#3/1.5 A3/.5 A#3/4"),
"mountain_king": dict(name="IN THE HALL OF THE MOUNTAIN KING", sub="Grieg (1875)", cat="movie", level="Hard", beat=.17,
    notes="B3/.5 C#4/.5 D4/.5 E4/.5 F#4/.5 D4/.5 F#4 F4/.5 C#4/.5 F4 E4/.5 C4/.5 E4 "
          "B3/.5 C#4/.5 D4/.5 E4/.5 F#4/.5 D4/.5 F#4/.5 B4/.5 A4/.5 F#4/.5 D4/.5 F#4/.5 A4/2 "
          "B3/.5 C#4/.5 D4/.5 E4/.5 F#4/.5 D4/.5 F#4 F4/.5 C#4/.5 F4 E4/.5 C4/.5 E4"),
"valkyries": dict(name="RIDE OF THE VALKYRIES", sub="Wagner (1856)", cat="movie", level="Hard", beat=.36, only_hard=True,
    notes="F#3/.5 B3/.5 D4/3 R/2.5 F#3/.5 B3/.5 D4/3 R/2.5 F#3/.5 B3/.5 D4/3"),
"entertainer": dict(name="THE ENTERTAINER", sub="Scott Joplin (1902)", cat="movie", level="Easy", beat=.22,
    notes="D5/.5 D#5/.5 E5/.5 C6 E5/.5 C6 E5/.5 C6/3 C6/.5 D6/.5 D#6/.5 E6/.5 C6/.5 D6/.5 E6 B5/.5 D6 C6/3 "
          "D5/.5 D#5/.5 E5/.5 C6 E5/.5 C6 E5/.5 C6/3"),
# ---------------- opera & ballet ----------------
"habanera": dict(name="HABANERA", sub="Bizet – Carmen (1875)", cat="opera", level="Medium", beat=.3, check=True,
    notes="D5/1.5 C#5/.5 C5 C5 B4/1.5 A#4/.5 A4 A4 G#4/1.5 G4/.5 F#4 F4/.5 E4/.5 F4 E4/2"),
"toreador": dict(name="TOREADOR SONG", sub="Bizet – Carmen (1875)", cat="opera", level="Medium", beat=.35, check=True,
    notes="C5 D5/.75 C5/.25 A4 A4 A4/.75 G4/.25 A4/.75 A#4/.25 A4/2 A#4 G4/.75 C5/.25 A4/2 F4 D4/.75 G4/.25 C4/2"),
"swan_lake": dict(name="SWAN LAKE", sub="Tchaikovsky (1876)", cat="opera", level="Medium", beat=.25, check=True,
    notes="B4/4 E4 F#4 G4 A4 B4/3 G4 B4/3 G4 B4/3 E4 G4 E4 C4 G4 E4/4"),
"sugar_plum": dict(name="DANCE OF THE SUGAR PLUM FAIRY", sub="Tchaikovsky – The Nutcracker (1892)", cat="opera", level="Medium", beat=.28, check=True,
    notes="G4 E4 G4 F#4 D#4 E4 D4 D4 D4 C#4 C4 C4 C4 B3 E4 G4 E4 G4 F#4 D#4 E4/2"),
"bridal_chorus": dict(name="HERE COMES THE BRIDE", sub="Wagner – Bridal Chorus (1850)", cat="party", level="Easy", beat=.38,
    notes="F4 A#4/.75 A#4/.25 A#4/2 F4 C5/.75 A4/.25 A#4/2 F4 A#4/.75 D#5/.25 D#5 D5/.75 C5/.25 A#4 A4/.75 A#4/.25 C5/2"),
# ---------------- folk & famous tunes ----------------
"nokia": dict(name="NOKIA RINGTONE", sub="Gran Vals – Tárrega (1902)", cat="folk", level="Easy", beat=.2,
    notes="E5/.5 D5/.5 F#4 G#4 C#5/.5 B4/.5 D4 E4 B4/.5 A4/.5 C#4 E4 A4/3 R "
          "E5/.5 D5/.5 F#4 G#4 C#5/.5 B4/.5 D4 E4 B4/.5 A4/.5 C#4 E4 A4/3"),
"tetris": dict(name="TETRIS THEME", sub="Korobeiniki – Russian folk song", cat="folk", level="Easy", beat=.2,
    notes="E5 B4/.5 C5/.5 D5 C5/.5 B4/.5 A4 A4/.5 C5/.5 E5 D5/.5 C5/.5 B4/1.5 C5/.5 D5 E5 C5 A4 A4/2 R/.5 "
          "D5 F5/.5 A5 G5/.5 F5/.5 E5/1.5 C5/.5 E5 D5/.5 C5/.5 B4 B4/.5 C5/.5 D5 E5 C5 A4 A4/2"),
"greensleeves": dict(name="GREENSLEEVES", sub="English folk song (16th c.)", cat="folk", level="Medium", beat=.28,
    notes="A4 C5/2 D5 E5/1.5 F5/.5 E5 D5/2 B4 G4/1.5 A4/.5 B4 C5/2 A4 A4/1.5 G#4/.5 A4 B4/2 G#4 E4/2"),
"scarborough": dict(name="SCARBOROUGH FAIR", sub="English folk ballad", cat="folk", level="Medium", beat=.3,
    notes="D4/2 D4 A4/2 A4 E4/1.5 F4/.5 E4 D4/3 R A4 C5/2 D5 C5/2 A4 B4 G4 A4/4"),
"cucaracha": dict(name="LA CUCARACHA", sub="Mexican folk song", cat="folk", level="Easy", beat=.28,
    notes="C4/.5 C4/.5 C4/.5 F4/1.5 A4 C4/.5 C4/.5 C4/.5 F4/1.5 A4 R F4 F4/.5 E4/.5 E4/.5 D4/.5 D4/.5 C4/2"),
"saints": dict(name="WHEN THE SAINTS GO MARCHING IN", sub="Traditional spiritual", cat="folk", level="Easy", beat=.25,
    notes="C4 E4 F4 G4/4 C4 E4 F4 G4/4 C4 E4 F4 G4/2 E4/2 C4/2 E4/2 D4/4"),
"oh_susanna": dict(name="OH! SUSANNA", sub="Stephen Foster (1848)", cat="folk", level="Medium", beat=.3,
    notes="C4/.5 D4/.5 E4 G4 G4/1.5 A4/.5 G4 E4 C4/1.5 D4/.5 E4 E4 D4 C4 D4/3"),
"amazing_grace": dict(name="AMAZING GRACE", sub="Traditional hymn (1779)", cat="folk", level="Easy", beat=.33,
    notes="D4 G4/2 B4/.5 G4/.5 B4/2 A4 G4/2 E4 D4/2 D4 G4/2 B4/.5 G4/.5 B4/2 A4 D5/5"),
"auld_lang_syne": dict(name="AULD LANG SYNE", sub="Scottish folk song (1788)", cat="folk", level="Medium", beat=.33,
    notes="C4 F4/1.5 F4/.5 F4 A4 G4/1.5 F4/.5 G4 A4 F4/1.5 F4/.5 A4 C5 D5/3"),
"drunken_sailor": dict(name="DRUNKEN SAILOR", sub="Sea shanty (traditional)", cat="folk", level="Easy", beat=.25,
    notes="A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 D4 F4 A4 G4/.5 G4/.5 G4/.5 G4/.5 G4/.5 G4/.5 G4/.5 C4 E4 G4 "
          "A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 A4/.5 B4 C5 D5 C5 A4 G4 E4 D4/2"),
# ---------------- kids ----------------
"frere_jacques": dict(name="FRÈRE JACQUES", sub="French round (18th c.)", cat="kids", level="Easy", beat=.3,
    notes="C4 D4 E4 C4 C4 D4 E4 C4 E4 F4 G4/2 E4 F4 G4/2"),
"twinkle": dict(name="TWINKLE TWINKLE LITTLE STAR", sub="French melody (1761)", cat="kids", level="Easy", beat=.3,
    notes="C4 C4 G4 G4 A4 A4 G4/2 F4 F4 E4 E4 D4 D4 C4/2"),
"happy_birthday": dict(name="HAPPY BIRTHDAY", sub="Hill sisters (1893)", cat="kids", level="Easy", beat=.38,
    notes="G4/.75 G4/.25 A4 G4 C5 B4/2 G4/.75 G4/.25 A4 G4 D5 C5/2"),
"old_macdonald": dict(name="OLD MACDONALD HAD A FARM", sub="Traditional", cat="kids", level="Easy", beat=.3,
    notes="G4 G4 G4 D4 E4 E4 D4/2 B4 B4 A4 A4 G4/2"),
"row_boat": dict(name="ROW, ROW, ROW YOUR BOAT", sub="Traditional (1852)", cat="kids", level="Easy", beat=.15,
    notes="C4/3 C4/3 C4/2 D4 E4/3 E4/2 D4 E4/2 F4 G4/6"),
"london_bridge": dict(name="LONDON BRIDGE", sub="Traditional", cat="kids", level="Easy", beat=.3,
    notes="G4/1.5 A4/.5 G4 F4 E4 F4 G4/2 D4 E4 F4/2 E4 F4 G4/2"),
"mary_lamb": dict(name="MARY HAD A LITTLE LAMB", sub="Traditional (1830)", cat="kids", level="Easy", beat=.3,
    notes="E4 D4 C4 D4 E4 E4 E4/2 D4 D4 D4/2 E4 G4 G4/2"),
"itsy_bitsy": dict(name="ITSY BITSY SPIDER", sub="Traditional", cat="kids", level="Medium", beat=.18,
    notes="G4 C5/2 C5 C5/2 D5 E5/3 E5/2 E5 D5/2 C5 D5/2 E5 C5/6"),
"pop_weasel": dict(name="POP GOES THE WEASEL", sub="Traditional (1850s)", cat="kids", level="Medium", beat=.17, check=True,
    notes="C4/2 C4 D4/2 D4 E4 G4 E4 C4/3 C4/2 C4 D4/2 D4 E4/3 C4/3"),
"if_happy": dict(name="IF YOU'RE HAPPY AND YOU KNOW IT", sub="Traditional", cat="kids", level="Medium", beat=.3, check=True,
    notes="G4/.5 G4/.5 C5 C5 C5 C5 B4/.5 C5/.5 D5/2 R G4/.5 G4/.5 D5 D5 D5 D5 C5/.5 D5/.5 E5/2"),
"yankee_doodle": dict(name="YANKEE DOODLE", sub="Traditional (18th c.)", cat="kids", level="Medium", beat=.25,
    notes="C4 C4 D4 E4 C4 E4 D4/2 C4 C4 D4 E4 C4/2 B3/2"),
# ---------------- party ----------------
"jolly_fellow": dict(name="FOR HE'S A JOLLY GOOD FELLOW", sub="Traditional", cat="party", level="Easy", beat=.17,
    notes="C4 E4/2 E4 E4 D4 E4 F4/3 E4/2 E4 D4/2 D4 D4 C4 D4 E4/3 C4/3"),
"ball_game": dict(name="TAKE ME OUT TO THE BALL GAME", sub="Von Tilzer (1908)", cat="party", level="Medium", beat=.25, check=True,
    notes="C4/2 C5 A4 G4 E4 G4/3 D4/3 C4/2 C5 A4 G4 E4 G4/6"),
# ---------------- christmas ----------------
"jingle_bells": dict(name="JINGLE BELLS", sub="James Lord Pierpont (1857)", cat="xmas", level="Easy", beat=.25,
    notes="E4 E4 E4/2 E4 E4 E4/2 E4 G4 C4/1.5 D4/.5 E4/4 F4 F4 F4/1.5 F4/.5 F4 E4 E4 E4/.5 E4/.5 E4 D4 D4 E4 D4/2 G4/2"),
"silent_night": dict(name="SILENT NIGHT", sub="Gruber (1818)", cat="xmas", level="Easy", beat=.3,
    notes="G4/1.5 A4/.5 G4 E4/3 G4/1.5 A4/.5 G4 E4/3 D5/2 D5 B4/3 C5/2 C5 G4/3"),
"we_wish": dict(name="WE WISH YOU A MERRY CHRISTMAS", sub="English carol", cat="xmas", level="Easy", beat=.3,
    notes="D4 G4 G4/.5 A4/.5 G4/.5 F#4/.5 E4 C4 E4 A4 A4/.5 B4/.5 A4/.5 G4/.5 F#4 D4 D4 B4 B4/.5 C5/.5 B4/.5 A4/.5 G4 E4 D4/.5 D4/.5 E4 A4 F#4 G4/2"),
"deck_halls": dict(name="DECK THE HALLS", sub="Welsh carol", cat="xmas", level="Easy", beat=.28,
    notes="G4/1.5 F4/.5 E4 D4 C4 D4 E4 C4 D4/.5 E4/.5 F4/.5 D4/.5 E4/1.5 D4/.5 C4 B3 C4/2"),
"o_tannenbaum": dict(name="O CHRISTMAS TREE", sub="German carol (1824)", cat="xmas", level="Medium", beat=.38,
    notes="D4 G4/.75 G4/.25 G4/1.5 A4/.5 B4/.75 B4/.25 B4/1.5 B4/.5 A4/.5 B4/.5 C5 F#4 A4 G4"),
"joy_world": dict(name="JOY TO THE WORLD", sub="Handel / Mason arr. (1839)", cat="xmas", level="Medium", beat=.4,
    notes="C5/1.5 B4/.5 A4/.75 G4/.25 F4/1.5 E4/.5 D4 C4/1.5 R/.5 G4/.5 A4/1.5 A4/.5 B4/1.5 B4/.5 C5/3"),
"hark_herald": dict(name="HARK! THE HERALD ANGELS SING", sub="Mendelssohn (1840)", cat="xmas", level="Medium", beat=.3,
    notes="D4 G4 G4/1.5 F#4/.5 G4 B4 B4 A4 D5 D5 D5/1.5 C5/.5 B4 A4 B4/2"),
"carol_bells": dict(name="CAROL OF THE BELLS", sub="Leontovych (1914)", cat="xmas", level="Medium", beat=.22,
    notes="A#4 A4/.5 A#4/.5 G4 A#4 A4/.5 A#4/.5 G4 A#4 A4/.5 A#4/.5 G4 A#4 A4/.5 A#4/.5 G4 "
          "D5 C5/.5 D5/.5 A#4 D5 C5/.5 D5/.5 A#4"),
"god_rest": dict(name="GOD REST YE MERRY GENTLEMEN", sub="English carol", cat="xmas", level="Hard", beat=.28,
    notes="E4 E4 B4 B4 A4 G4 F#4 E4 D4 E4 F#4 G4 A4 B4/3"),
"o_come_faithful": dict(name="O COME, ALL YE FAITHFUL", sub="Wade (1751)", cat="xmas", level="Medium", beat=.3,
    notes="G4/2 G4/2 D4 G4 A4/2 D4/2 B4 A4 B4 C5 B4/2 A4 G4"),
"good_king": dict(name="GOOD KING WENCESLAS", sub="Traditional (1853)", cat="xmas", level="Hard", beat=.3,
    notes="G4 G4 G4 A4 G4 G4 D4/2 E4 D4 E4 F#4 G4/2 G4/2"),
"first_noel": dict(name="THE FIRST NOEL", sub="English carol", cat="xmas", level="Hard", beat=.35,
    notes="E4/.5 D4/.5 C4/1.5 D4/.5 E4/.5 F4/.5 G4/2 A4/.5 B4/.5 C5 B4 A4 G4/2"),
"angels_high": dict(name="ANGELS WE HAVE HEARD ON HIGH", sub="French carol", cat="xmas", level="Hard", beat=.3,
    notes="E4 E4 E4 G4 G4/1.5 F4/.5 E4/2 E4 D4 E4 G4 E4/1.5 D4/.5 C4/2"),
}

_NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

def to_midi(tok):
    n = _NOTE[tok[0]]; i = 1
    while i < len(tok) and tok[i] in "#b":
        n += 1 if tok[i] == "#" else -1; i += 1
    return 12 * (int(tok[i:]) + 1) + n

def parse(notes):
    """-> list of (midi or None, beats)"""
    out = []
    for tok in notes.split():
        nm, _, b = tok.partition("/")
        out.append((None if nm == "R" else to_midi(nm), float(b) if b else 1.0))
    return out

def build(key, fmt="normal", start=0.15):
    """Return [[time_s, midi, dur_s], ...] for a melody in a given quiz format."""
    m = M[key]; beat = m["beat"]; seq = parse(m["notes"])
    if fmt == "three_notes":
        first = [p for p in seq if p[0] is not None][:3]
        seq = (first + [(None, 2.5 / beat)]) * 3
    elif fmt == "backwards":
        seq = [p for p in reversed(seq)]
    elif fmt == "double_speed":
        beat = beat / 2; seq = seq * 2
    out, t = [], start
    for midi, b in seq:
        if midi is not None: out.append([round(t, 3), midi, b * beat])
        t += b * beat
    return out
