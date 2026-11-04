# Measurama Shorts topic library.
# Each item: (name, size, kind, tag, sub)   size in `unit` (m for heights, km for diameters)
# Sources: Wikipedia articles for each object (retrieved Nov 2026). Planet/moon sizes = mean diameter (NASA fact sheets).
from data_tallest import BUILDINGS

_B = {b[1]: b for b in BUILDINGS}
def B(name):
    rank, n, h, year, city, country = _B[name]
    k = "burj" if n == "Burj Khalifa" else "twin" if n == "Petronas Towers" else "merdeka" if n == "Merdeka 118" else "bld"
    return (n, h, k, f"#{rank} WORLD", f"{city} · {country} · {year}")

HUMAN = ("Average adult", 1.8, "human", "FOR SCALE", "for scale")
EIFFEL = ("Eiffel Tower", 330, "eiffel", "FOR SCALE", "Paris · with antennas")
BURJ_REF = ("Burj Khalifa", 828, "burj", "FOR SCALE", "Dubai · tallest building")
LIBERTY = ("Statue of Liberty", 93, "statue", "LANDMARK", "ground to torch")

WIKI_BLD = "Wikipedia – List of tallest buildings"
WIKI_MTN = "Wikipedia – List of highest mountains on Earth / each mountain's article"

SHORTS = [
  # ---------- buildings ----------
  dict(id="nyc", hook=["NEW YORK'S 5", "TALLEST BUILDINGS"], items=[B("432 Park Avenue"), B("One Vanderbilt"), B("111 West 57th Street"), B("Central Park Tower"), B("One World Trade Center")],
       end="One WTC: 541 m = 1,776 ft", title="New York's 5 Tallest Buildings (to scale) 🗽 #shorts", src=WIKI_BLD, tags="#newyork #nyc #skyscrapers"),
  dict(id="shanghai", hook=["SHANGHAI'S", "3 GIANTS"], items=[B("Jin Mao Tower"), B("Shanghai World Financial Center"), B("Shanghai Tower")],
       end="All three stand side by side", title="Shanghai's 3 Giant Skyscrapers, to Scale #shorts", src=WIKI_BLD, tags="#shanghai #shanghaitower #skyscrapers"),
  dict(id="dubai", hook=["DUBAI'S", "TALLEST TOWERS"], items=[B("Princess Tower"), B("Marina 101"), B("Burj Khalifa")],
       end="Burj is almost 2× Marina 101", title="Dubai's Tallest Towers vs Burj Khalifa 🇦🇪 #shorts", src=WIKI_BLD, tags="#dubai #burjkhalifa #skyscrapers"),
  dict(id="china5", hook=["CHINA'S 5", "TALLEST BUILDINGS"], items=[B("CITIC Tower"), B("Tianjin CTF Finance Centre"), B("Guangzhou CTF Finance Centre"), B("Ping An Finance Centre"), B("Shanghai Tower")],
       end="Shanghai Tower: 632 m", title="China's 5 Tallest Buildings, to Scale 🇨🇳 #shorts", src=WIKI_BLD, tags="#china #shanghaitower #skyscrapers"),
  dict(id="new2025", hook=["NEWEST GIANTS", "FINISHED IN 2025"], items=[B("Nanjing Financial City II Tower 1"), B("270 Park Avenue"), B("Shandong International Financial Center"), BURJ_REF],
       end="Still nowhere near the Burj", title="The Newest Skyscrapers of 2025 vs Burj Khalifa #shorts", src=WIKI_BLD, tags="#skyscrapers #architecture #2025"),
  dict(id="over600", hook=["ONLY 4 BUILDINGS", "ARE TALLER THAN 600 m"], items=[EIFFEL, B("Mecca Royal Clock Tower"), B("Shanghai Tower"), B("Merdeka 118"), B("Burj Khalifa")],
       end="Ping An missed it by 0.9 m", title="Only 4 Buildings on Earth Are Taller Than 600 m #shorts", src=WIKI_BLD, tags="#burjkhalifa #merdeka118 #skyscrapers"),
  dict(id="taipei", hook=["TAIPEI 101 vs", "BURJ KHALIFA"], items=[EIFFEL, B("Taipei 101"), B("Burj Khalifa")],
       end="Taipei 101 was #1 until 2010", title="Taipei 101 vs Burj Khalifa (to scale) #shorts", src=WIKI_BLD, tags="#taipei101 #burjkhalifa #taiwan"),
  dict(id="chicago", hook=["CHICAGO'S", "SKY GIANTS"], items=[LIBERTY, B("Trump International Hotel & Tower"), B("Willis Tower")],
       end="Willis Tower: built in 1974", title="Chicago's Tallest: Willis Tower to Scale 🌆 #shorts", src=WIKI_BLD, tags="#chicago #willistower #skyscrapers"),

  dict(id="record", hook=["EVERY \"WORLD'S TALLEST\"", "SINCE 1974"], items=[B("Willis Tower"), B("Petronas Towers"), B("Taipei 101"), B("Burj Khalifa")],
       end="Who takes the crown next?", title="Every World's Tallest Building Since 1974 🏆 #shorts", src=WIKI_BLD, tags="#willistower #taipei101 #burjkhalifa"),

  # ---------- towers / statues / rockets ----------
  dict(id="towers", hook=["WORLD'S TALLEST", "TV TOWERS"], items=[("Eiffel Tower", 330, "eiffel", "PARIS · 1889", "with antennas"), ("Ostankino Tower", 540.1, "tower", "MOSCOW · 1967", "Russia"),
       ("CN Tower", 553.3, "tower", "TORONTO · 1976", "Canada"), ("Canton Tower", 604, "tower", "GUANGZHOU · 2010", "China"), ("Tokyo Skytree", 634, "tower", "TOKYO · 2012", "Japan · tallest tower")],
       end="Skytree: 634 m tall", title="World's Tallest Towers Compared 🗼 #shorts", src="Wikipedia – List of tallest towers", tags="#tokyoskytree #cntower #towers"),
  dict(id="statues", hook=["GIANT STATUES", "TO SCALE"], items=[HUMAN, ("Christ the Redeemer", 30, "figure", "RIO DE JANEIRO", "statue only · 38 m with pedestal"), ("Statue of Liberty", 46, "figure", "NEW YORK", "statue only · 93 m with pedestal"),
       ("The Motherland Calls", 85, "figure", "VOLGOGRAD", "Russia · incl. sword"), ("Ushiku Daibutsu", 100, "figure", "JAPAN", "statue only · 120 m with base"),
       ("Spring Temple Buddha", 128, "figure", "CHINA", "statue only · 208 m with base"), ("Statue of Unity", 182, "figure", "INDIA", "world's tallest statue")],
       end="Unity is 6× Christ the Redeemer", title="Giant Statues Compared (statue only) 🗿 #shorts", src="Wikipedia – List of tallest statues", tags="#statueofunity #statues #sizecomparison"),
  dict(id="rockets", hook=["ROCKETS", "TO SCALE"], items=[HUMAN, ("Soyuz-2", 46.3, "rocket", "RUSSIA", "crewed launcher"), ("Space Shuttle", 56.1, "rocket", "NASA · 1981–2011", "full stack"),
       ("Falcon 9", 70, "rocket", "SPACEX", "Block 5"), ("SLS", 98, "rocket", "NASA · Artemis", "Block 1"), ("Saturn V", 110.6, "rocket", "NASA · Apollo", "took humans to the Moon")],
       end="Saturn V: 110.6 m of rocket", title="Famous Rockets Compared to Scale 🚀 #shorts", src="Wikipedia – each rocket's article", tags="#saturnv #spacex #rockets"),
  dict(id="rocketland", hook=["SATURN V vs", "FAMOUS LANDMARKS"], items=[HUMAN, ("Statue of Liberty", 93, "statue", "NEW YORK", "ground to torch"), ("Big Ben", 96, "tower", "LONDON", "Elizabeth Tower"),
       ("Saturn V", 110.6, "rocket", "NASA · APOLLO", "1967–1973")],
       end="Taller than Big Ben!", title="Saturn V vs Big Ben vs Statue of Liberty #shorts", src="Wikipedia", tags="#saturnv #bigben #nasa"),

  # ---------- mountains ----------
  dict(id="top5mtn", hook=["5 HIGHEST", "MOUNTAINS ON EARTH"], items=[BURJ_REF, ("Makalu", 8485, "mountain", "#5", "Nepal / China"), ("Lhotse", 8516, "mountain", "#4", "Nepal / China"),
       ("Kangchenjunga", 8586, "mountain", "#3", "Nepal / India"), ("K2", 8611, "mountain", "#2", "Pakistan / China"), ("Mount Everest", 8849, "mountain", "#1", "Nepal / China")],
       end="Everest = 10.7 Burj Khalifas", title="5 Highest Mountains on Earth, to Scale ⛰️ #shorts", src=WIKI_MTN, tags="#everest #k2 #mountains"),
  dict(id="summits", hook=["HIGHEST PEAK OF", "EVERY CONTINENT"], items=[("Kosciuszko", 2228, "mountain", "AUSTRALIA", "Australia"), ("Vinson", 4892, "mountain", "ANTARCTICA", "Antarctica"),
       ("Elbrus", 5642, "mountain", "EUROPE", "Russia"), ("Kilimanjaro", 5895, "mountain", "AFRICA", "Tanzania"), ("Denali", 6190, "mountain", "NORTH AMERICA", "USA · Alaska"),
       ("Aconcagua", 6961, "mountain", "SOUTH AMERICA", "Argentina"), ("Mount Everest", 8849, "mountain", "ASIA", "Nepal / China")],
       end="The Seven Summits", title="The Highest Peak of Every Continent ⛰️ #shorts", src=WIKI_MTN, tags="#sevensummits #everest #mountains"),
  dict(id="georgia", hook=["GEORGIA'S", "HIGHEST PEAKS"], items=[BURJ_REF, ("Ushba", 4710, "mountain", "SVANETI", "Georgia"), ("Tetnuldi", 4858, "mountain", "SVANETI", "Georgia"),
       ("Kazbek", 5054, "mountain", "KAZBEGI", "Georgia / Russia border"), ("Shkhara", 5193, "mountain", "#1 IN GEORGIA", "Georgia / Russia border")],
       end="Shkhara beats Mont Blanc by 387 m", title="Georgia's Highest Mountains, to Scale 🇬🇪 #shorts", src=WIKI_MTN + " (heights vary by source)", tags="#georgia #kazbek #caucasus"),
  dict(id="europe", hook=["EUROPE'S", "FAMOUS PEAKS"], items=[("Matterhorn", 4478, "mountain", "ALPS", "Switzerland / Italy"), ("Mont Blanc", 4806, "mountain", "ALPS", "France / Italy"),
       ("Kazbek", 5054, "mountain", "CAUCASUS", "Georgia"), ("Elbrus", 5642, "mountain", "CAUCASUS", "Russia · Europe's highest")],
       end="The Caucasus beats the Alps", title="Matterhorn vs Mont Blanc vs Kazbek vs Elbrus #shorts", src=WIKI_MTN, tags="#montblanc #elbrus #mountains"),
  dict(id="fuji", hook=["FAMOUS MOUNTAINS", "vs EVEREST"], items=[("Mount Fuji", 3776, "mountain", "JAPAN", "Honshu"), ("Matterhorn", 4478, "mountain", "SWITZERLAND", "Alps"),
       ("Kilimanjaro", 5895, "mountain", "TANZANIA", "Africa's highest"), ("Mount Everest", 8849, "mountain", "NEPAL / CHINA", "Earth's highest")],
       end="Everest = 2.3 Mount Fujis", title="Mount Fuji vs Kilimanjaro vs Everest ⛰️ #shorts", src=WIKI_MTN, tags="#fuji #kilimanjaro #everest"),
  dict(id="maunakea", hook=["EVEREST ISN'T THE", "TALLEST MOUNTAIN?!"], items=[("Mount Everest", 8849, "mountain", "ABOVE SEA LEVEL", "Nepal / China"),
       ("Mauna Kea", 10211, "mountain", "BASE TO PEAK", "Hawaii · mostly underwater")],
       end="Only 4,207 m is above the sea", title="Mauna Kea Is Taller Than Everest?! 🌋 #shorts", src="Wikipedia – Mauna Kea", tags="#maunakea #everest #hawaii"),
  dict(id="olympus", hook=["TALLEST MOUNTAIN", "IN THE SOLAR SYSTEM"], items=[("Mount Everest", 8849, "mountain", "EARTH", "above sea level"), ("Mauna Kea", 10211, "mountain", "EARTH", "base to peak"),
       ("Olympus Mons", 21900, "mountain", "MARS", "above Mars datum")],
       end="2.5× taller than Everest", title="Olympus Mons vs Everest (to scale) 🔴 #shorts", src="Wikipedia – Olympus Mons", tags="#olympusmons #mars #space"),

  # ---------- space (diameters, km) ----------
  dict(id="planets", unit="km", hook=["PLANETS SIZE", "COMPARISON"], items=[("Mercury", 4879, "planet", "PLANET", "mean diameter"), ("Mars", 6779, "planet", "PLANET", "mean diameter"),
       ("Venus", 12104, "planet", "PLANET", "mean diameter"), ("Earth", 12742, "earth", "HOME", "mean diameter"), ("Neptune", 49244, "planet", "ICE GIANT", "mean diameter"),
       ("Uranus", 50724, "planet", "ICE GIANT", "mean diameter"), ("Saturn", 116460, "saturn", "GAS GIANT", "mean diameter, without rings"), ("Jupiter", 139820, "planet", "GAS GIANT", "largest planet")],
       end="1,300 Earths fit in Jupiter", title="All 8 Planets Size Comparison 🪐 #shorts", src="NASA planetary fact sheets", tags="#planets #space #solarsystem"),
  dict(id="sun", unit="km", hook=["EARTH vs JUPITER", "vs THE SUN"], items=[("Moon", 3475, "planet", "MOON", "mean diameter"), ("Earth", 12742, "earth", "HOME", "mean diameter"),
       ("Jupiter", 139820, "planet", "GAS GIANT", "11× Earth"), ("Sun", 1392700, "sun", "STAR", "109× Earth")],
       end="1.3 million Earths fit inside", title="Earth vs Jupiter vs The Sun (to scale) ☀️ #shorts", src="NASA fact sheets", tags="#sun #jupiter #space"),
  dict(id="moons", unit="km", hook=["BIGGEST MOONS", "IN THE SOLAR SYSTEM"], items=[("Pluto", 2377, "planet", "DWARF PLANET", "for scale"), ("Europa", 3122, "planet", "JUPITER", "moon"),
       ("Moon", 3475, "planet", "EARTH", "our Moon"), ("Io", 3643, "planet", "JUPITER", "moon"), ("Callisto", 4821, "planet", "JUPITER", "moon"),
       ("Mercury", 4879, "planet", "PLANET", "for scale"), ("Titan", 5149, "planet", "SATURN", "moon"), ("Ganymede", 5268, "planet", "JUPITER", "largest moon")],
       end="Ganymede is bigger than Mercury", title="Biggest Moons in the Solar System 🌕 #shorts", src="NASA fact sheets", tags="#moons #ganymede #space"),
  dict(id="pluto", unit="km", hook=["PLUTO vs", "OUR MOON"], items=[("Pluto", 2377, "planet", "DWARF PLANET", "mean diameter"), ("Moon", 3475, "planet", "EARTH'S MOON", "mean diameter"),
       ("Mercury", 4879, "planet", "PLANET", "smallest planet"), ("Earth", 12742, "earth", "HOME", "mean diameter")],
       end="Pluto is smaller than our Moon", title="Pluto vs The Moon vs Earth (to scale) #shorts", src="NASA fact sheets", tags="#pluto #moon #space"),
]
