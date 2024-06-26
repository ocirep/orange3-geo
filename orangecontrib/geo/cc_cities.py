import re
from itertools import chain


_CC_NAME_TO_CC_NAME = {
    # EU
    'Kosovo': ['Kosovo, Republic of'],
    'Åland': ['Åland Islands', 'Aland'],
    'Bosnia and Herz.': ['Bosnia and Herzegovina'],
    'Czechia': ['Czech Rep.', 'Czech Republic'],
    'Faeroe Is.': ['Faroe Islands', 'Faeroe Islands'],
    'United Kingdom': ['Great Britain', 'England'],
    'Moldova': ['Moldova, Republic of'],
    'Macedonia': ['Macedonia, Republic of'],
    'Palestine': ['Palestine, State of'],
    'Russia': ['Russian Federation'],
    'Syria': ['Syrian Arab Republic'],
    # World
    'Brunei': ['Brunei Darussalam'],
    'Bolivia': ['Bolivia, Plurinational State of'],
    'Dem. Rep. Congo': ['Democratic Republic of the Congo', 'Democratic Republic of Congo', 'Congo, The Democratic Republic of the'],
    'Central African Rep.': ['Central African Republic'],
    'Dominican Rep.': ['Dominican Republic'],
    'W. Sahara': ['Western Sahara'],
    'Falkland Is.': ['Falkland Islands [Malvinas]', 'Falkland Islands', 'Malvinas'],
    'Eq. Guinea': ['Equatorial Guinea'],
    'Iran': ['Iran, Islamic Republic of'],
    'North Korea': ["Korea, Democratic People's Republic of", 'Democratic Republic of Korea', 'Dem. Rep. Korea'],
    'South Korea': ['Korea, Republic of', 'Korea'],
    'Laos': ["Lao People's Democratic Republic", 'Lao PDR'],
    'Solomon Is.': ['Solomon Islands'],
    'S. Sudan': ['South Sudan'],
    'Taiwan': ['Taiwan, Province of China'],
    'Tanzania': ['Tanzania, United Republic of'],
    'United States of America': ['United States'],
    'Venezuela': ['Venezuela, Bolivarian Republic of'],
    'Vietnam': ['Viet Nam'],
}


_REGION_NAME_TO_REGION_NAME = {
    # Municipalities in Slovenia
    'Apace': ['Apače'],
    'Braslovce': ['Braslovče'],
    'Crnomelj': ['Črnomelj'],
    'Divaca': ['Divača'],
    'Hoce-Slivnica': ['Hoče-Slivnica', 'Hoče - Slivnica'],
    'Ivancna Gorica': ['Ivančna Gorica'],
    'Kidricevo': ['Kidričevo'],
    'Kocevje': ['Kočevje'],
    'Luce': ['Luče'],
    'Mirna Pec': ['Mirna Peč'],
    'Moravce': ['Moravče'],
    'Nova Goriška': ['Nova Gorica'],
    'Novo Mesto': ['Novo mesto'],
    'Podcetrtek': ['Podčetrtek'],
    'Poljcane': ['Poljčane'],
    'Race-Fram': ['Rače-Fram', 'Rače - Fram'],
    'Radece': ['Radeče'],
    'Ravne na Koroškem': ['Ravne'],
    'Semic': ['Semič'],
    'Šmartno in Litiji': ['Šmartno pri Litiji'],
    'Solcava': ['Solčava'],
    'Sveti Andraž v Slovenskih Goricah': ['Sveti Andraž v Slovenskih goricah', 'Sveti Andraž v Slov. goricah', 'Sveti Andraž v Slov.goricah', 'Sveti Andraž v Sloven. goricah'],
    'Zasavska': ['Zagorje ob Savi'],
    'Zavrc': ['Zavrč'],
    'Zrece': ['Zreče'],
    'Koper': ['Koper/Capodistria'],
    'Piran': ['Piran/Pirano'],
    'Izola': ['Izola/Isola'],
    'Ankaran': ['Ankaran/Ancarano'],
    'Lendava': ['Lendava/Lendva'],
    'Dobrovnik': ['Dobrovnik/Dobronak'],
    'Hodoš': ['Hodoš/Hodos'],
    'Šempeter-Vrtojba': ['Šempeter - Vrtojba'],
    'Miren-Kostanjevica': ['Miren - Kostanjevica'],
    'Hrpelje-Kozina': ['Hrpelje - Kozina'],
    'Gorenja vas-Poljane': ['Gorenja vas - Poljane'],
    'Dobrova-Polhov Gradec': ['Dobrova - Polhov Gradec'],
}


_US_STATE_TO_US_STATE = {
    'NC': ['North Carolina', 'N. Carolina'],
    'ND': ['North Dakota', 'N. Dakota'],
    'SC': ['South Carolina', 'S. Carolina'],
    'SD': ['South Dakota', 'S. Dakota'],
}


_US_CITIES = {
    # From https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
    'AK': ['Anchorage'],
    'AL': ['Birmingham', 'Montgomery', 'Mobile', 'Huntsville'],
    'AR': ['Little Rock'],
    'AZ': ['Phoenix', 'Tucson', 'Mesa', 'Chandler', 'Gilbert', 'Glendale', 'Scottsdale', 'Tempe', 'Peoria', 'Surprise'],
    'CA': ['Los Angeles', 'San Diego', 'San Jose', 'San Francisco', 'Fresno', 'Sacramento', 'Long Beach', 'Oakland', 'Bakersfield', 'Anaheim', 'Santa Ana', 'Riverside', 'Stockton', 'Chula Vista', 'Irvine', 'Fremont', 'San Bernardino', 'Modesto', 'Oxnard', 'Fontana', 'Moreno Valley', 'Huntington Beach', 'Glendale', 'Santa Clarita', 'Garden Grove', 'Oceanside', 'Rancho Cucamonga', 'Santa Rosa', 'Ontario', 'Elk Grove', 'Corona', 'Lancaster', 'Palmdale', 'Salinas', 'Hayward', 'Pomona', 'Escondido', 'Sunnyvale', 'Torrance', 'Pasadena', 'Orange', 'Fullerton', 'Thousand Oaks', 'Visalia', 'Roseville', 'Concord', 'Simi Valley', 'Santa Clara', 'Victorville', 'Vallejo', 'Berkeley', 'El Monte', 'Downey', 'Costa Mesa', 'Carlsbad', 'Inglewood', 'Fairfield', 'Ventura', 'Temecula', 'Antioch', 'Richmond', 'West Covina', 'Murrieta', 'Norwalk', 'Daly City', 'Burbank', 'Santa Maria', 'El Cajon', 'San Mateo', 'Rialto', 'Clovis', 'East Los Angeles'],
    'CO': ['Denver', 'Colorado Springs', 'Aurora', 'Fort Collins', 'Lakewood', 'Thornton', 'Arvada', 'Westminster', 'Pueblo', 'Centennial', 'Boulder'],
    'CT': ['Bridgeport', 'New Haven', 'Stamford', 'Hartford', 'Waterbury'],
    'DE': ['Dover',],
    'DC': ['Washington', 'Washington, D.C.', 'Washington D.C.', 'Washington DC', 'D.C.'],
    'FL': ['Jacksonville', 'Miami', 'Tampa', 'Orlando', 'St. Petersburg', 'Hialeah', 'Tallahassee', 'Fort Lauderdale', 'Port St. Lucie', 'Cape Coral', 'Pembroke Pines', 'Hollywood', 'Miramar', 'Gainesville', 'Coral Springs', 'Miami Gardens', 'Clearwater', 'Pompano Beach', 'Palm Bay', 'West Palm Beach', 'Lakeland', 'Brandon'],
    'GA': ['Atlanta', 'Columbus', 'Augusta', 'Macon', 'Savannah', 'Athens', 'Sandy Springs'],
    'HI': ['Honolulu'],
    'IA': ['Des Moines', 'Cedar Rapids', 'Davenport'],
    'ID': ['Boise'],
    'IL': ['Chicago', 'Aurora', 'Rockford', 'Joliet', 'Naperville', 'Springfield', 'Peoria', 'Elgin'],
    'IN': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend'],
    'KS': ['Wichita', 'Overland Park', 'Kansas City', 'Olathe', 'Topeka'],
    'KY': ['Louisville', 'Lexington'],
    'LA': ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette', 'Metairie'],
    'MA': ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge'],
    'MD': ['Annapolis', 'Baltimore'],
    'ME': ['Portland', 'Augusta'],
    'MI': ['Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights', 'Ann Arbor', 'Lansing'],
    'MN': ['Minneapolis', 'St. Paul', 'Rochester'],
    'MO': ['Kansas City', 'St. Louis', 'Springfield', 'Independence', 'Columbia'],
    'MS': ['Jackson'],
    'MT': ['Billings'],
    'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham', 'Winston–Salem', 'Fayetteville', 'Cary', 'Wilmington', 'High Point'],
    'ND': ['Fargo'],
    'NE': ['Omaha', 'Lincoln'],
    'NH': ['Manchester'],
    'NJ': ['Newark', 'Jersey City', 'Paterson', 'Elizabeth'],
    'NM': ['Albuquerque', 'Las Cruces'],
    'NV': ['Las Vegas', 'Henderson', 'Reno', 'North Las Vegas', 'Paradise', 'Sunrise Manor', 'Spring Valley', 'Enterprise'],
    'NY': ['New York City', 'Buffalo', 'Rochester', 'Yonkers', 'Syracuse'],
    'OH': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron', 'Dayton'],
    'OK': ['Oklahoma City', 'Tulsa', 'Norman', 'Broken Arrow'],
    'OR': ['Portland', 'Salem', 'Eugene', 'Gresham'],
    'PA': ['Philadelphia', 'Pittsburgh', 'Allentown'],
    'RI': ['Providence'],
    'SC': ['Columbia', 'Charleston', 'North Charleston'],
    'SD': ['Sioux Falls'],
    'TN': ['Memphis', 'Nashville', 'Knoxville', 'Chattanooga', 'Clarksville', 'Murfreesboro'],
    'TX': ['Houston', 'San Antonio', 'Dallas', 'Austin', 'Fort Worth', 'El Paso', 'Arlington', 'Corpus Christi', 'Plano', 'Laredo', 'Lubbock', 'Garland', 'Irving', 'Amarillo', 'Grand Prairie', 'Brownsville', 'McKinney', 'Pasadena', 'Frisco', 'Mesquite', 'McAllen', 'Killeen', 'Waco', 'Carrollton', 'Denton', 'Midland', 'Abilene', 'Beaumont', 'Odessa', 'Round Rock', 'Richardson', 'Wichita Falls', 'College Station', 'Pearland', 'Lewisville', 'Tyler'],
    'UT': ['Salt Lake City', 'West Valley City', 'Provo', 'West Jordan'],
    'VA': ['Virginia Beach', 'Norfolk', 'Chesapeake', 'Richmond', 'Newport News', 'Alexandria', 'Hampton', 'Arlington County'],
    'VT': ['Burlington'],
    'WA': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver', 'Bellevue', 'Kent', 'Everett'],
    'WI': ['Milwaukee', 'Madison', 'Green Bay'],
    'WV': ['Charleston'],
    'WY': ['Cheyenne'],
}

_EUROPE_CITIES = {
    # As by https://www.countries-ofthe-world.com/capitals-of-europe.html
    'PS': ['Pristina', 'Priština', 'Priština', 'Prishtina', 'Prishtinë'],
    'AD': ['Andorra la Vella'],
    'AL': ['Tirana'],
    'AT': ['Vienna', 'Wien'],
    'AX': ['Mariehamn'],
    'BA': ['Sarajevo'],
    'BE': ['Brussels', 'Bruxelles', 'Brussel'],
    'BG': ['Sofia'],
    'BY': ['Minsk'],
    'CH': ['Bern', 'Zürich', 'Zurich', 'Geneva'],
    'CY': ['Nicosia', 'North Nicosia'],
    'CZ': ['Prague', 'Praha', 'Praga'],
    'DE': ['Berlin', 'Hanover', 'Hamburg', 'Munich', 'München', 'Stuttgart', 'Frankfurt', 'Düsseldorf', 'Cologne', 'Essen', 'Dresden', 'Leipzig'],
    'DK': ['Copenhagen', 'København'],
    'DZ': ['Algiers'],
    'EE': ['Tallinn'],
    'EG': ['Cairo'],
    'ES': ['Madrid', 'Barcelona', 'Murcia', 'Malaga', 'Seville', 'Bilbao', 'Zaragoza', 'Valencia'],
    'FI': ['Helsinki'],
    'FO': ['Tórshavn', 'Torshavn'],
    'FR': ['Paris', 'Nice', 'Montpellier', 'Marseille', 'Lyon', 'Toulouse', 'Bordeaux', 'Nantes'],
    'GB': ['London', 'London Heathrow', 'Manchester', 'Liverpool', 'Bristol', 'Cardiff', 'Oxford', 'Cambridge', 'Glasgow', 'Edinburgh', 'Belfast'],
    'GE': ['Tbilisi'],
    'GG': ['Saint Peter Port'],
    'GR': ['Athens', 'Thessaloniki'],
    'HR': ['Zagreb'],
    'HU': ['Budapest'],
    'IE': ['Dublin'],
    'IL': ['Jerusalem', 'Tel Aviv'],
    'IM': ['Douglas'],
    'IQ': ['Baghdad'],
    'IS': ['Reykjavik'],
    'IT': ['Rome', 'Roma'],
    'JE': ['Saint Helier'],
    'JO': ['Amman'],
    'LB': ['Beirut'],
    'LI': ['Vaduz'],
    'LT': ['Vilnius'],
    'LU': ['Luxembourg'],
    'LV': ['Riga'],
    'LY': ['Tripoli'],
    'MA': ['Rabat', 'Fes', 'Casablanca', 'Marrakesh', 'Marrakech', 'Tangier'],
    'MD': ['Chisinau', 'Chișinău'],
    'ME': ['Podgorica'],
    'MK': ['Skopje'],
    'MT': ['Valletta'],
    'NL': ['Amsterdam', 'The Hague', 'Rotterdam'],
    'NO': ['Oslo', 'Bergen', 'Trondheim'],
    'PL': ['Warsaw', 'Warszawa', 'Krakow', 'Lublin', 'Bialystok', 'Lodz', 'Gdansk', 'Wroclaw'],
    'PT': ['Lisbon', 'Porto'],
    'RO': ['Bucharest', 'București'],
    'RS': ['Belgrade', 'Beograd'],
    'RU': ['Moscow', 'Moskva', 'Saint Petersburg', 'St. Petersburg', 'Kazan', 'Vladivostok', 'Irkutsk', 'Novosibirsk', 'Krasnoyarsk', 'Nizhny Novgorod'],
    'SA': ['Riyadh'],
    'SE': ['Stockholm', 'Gothenburg', 'Malmo'],
    'SI': ['Ljubljana'],
    'SK': ['Bratislava'],
    'SM': ['San Marino'],
    'SY': ['Damascus'],
    'TN': ['Tunis'],
    'TR': ['Ankara', 'Istanbul', 'Constantinople'],
    'UA': ['Kyiv', 'Kiev', 'Kharkiv', 'Odessa', 'Lviv'],
}


_WORLD_CITIES = {
    # Capitals and larger cities. Does NOT include CC_EUROPE.
    'AE': ['Abu Dhabi'],
    'AF': ['Kabul'],
    'AM': ['Yerevan'],
    'AO': ['Luanda'],
    'AR': ['Buenos Aires'],
    'AU': ['Canberra', 'Sydney', 'Melbourne', 'Cairns', 'Adelaide', 'Perth'],
    'AZ': ['Baku'],
    'BD': ['Dhaka'],
    'BF': ['Ouagadougou'],
    'BI': ['Bujumbura'],
    'BJ': ['Porto-Novo', 'Porto Novo', 'Cotonou'],
    'BN': ['Bandar Seri Begawani'],
    'BO': ['La Paz', 'Sucre'],
    'BR': ['Brasília', 'Brasilia', 'Sao Paulo', 'Sao Paulo', 'Rio de Janeiro'],
    'BS': ['Nassau'],
    'BT': ['Thimphu'],
    'BW': ['Gaborone'],
    'BZ': ['Belmopan'],
    'CA': ['Ottawa', 'Vancouver', 'Calgary', 'Edmonton', 'Winnipeg', 'Toronto', 'Montreal', 'Québec', 'Quebec'],
    'CD': ['Kinshasa'],
    'CF': ['Bangui'],
    'CG': ['Brazzaville'],
    'CI': ['Yamoussoukro', 'Abidjan'],
    'CL': ['Santiago'],
    'CM': ['Yaoundé', 'Yaounde'],
    'CN': ['Beijing'],
    'CO': ['Bogotá', 'Bogota'],
    'CR': ['San José', 'San Jose'],
    'CU': ['Havana'],
    'DJ': ['Djibouti'],
    'DO': ['Santo Domingo'],
    'EC': ['Quito'],
    'EH': ['Laayoune'],
    'ER': ['Asmara'],
    'ET': ['Addis Ababa'],
    'FJ': ['Suva'],
    'FK': ['Stanley'],
    'GA': ['Libreville'],
    'GH': ['Accra'],
    'GL': ['Nuuk'],
    'GM': ['Banjul'],
    'GN': ['Conakry'],
    'GQ': ['Malabo'],
    'GT': ['Guatemala City'],
    'GW': ['Bissau'],
    'GY': ['Georgetown'],
    'HN': ['Tegucigalpa'],
    'HT': ['Port-au-Prince', 'Port au Prince'],
    'ID': ['Jakarta'],
    'IN': ['New Delhi', 'Mumbai', 'Bombay', 'Bengaluru', 'Hyderabad'],
    'IR': ['Tehran'],
    'JM': ['Kingston'],
    'JP': ['Tokyo', 'Osaka', 'Hiroshima', 'Fukuoka', 'Sapporo'],
    'KE': ['Nairobi'],
    'KG': ['Bishkek'],
    'KH': ['Phnom Penh'],
    'KP': ['Pyongyang'],
    'KR': ['Seoul'],
    'KW': ['Kuwait City'],
    'KZ': ['Astana'],
    'LA': ['Vientiane'],
    'LK': ['Sri Jayawardenepura Kotte', 'Colombo'],
    'LR': ['Monrovia'],
    'LS': ['Maseru'],
    'MG': ['Antananarivo'],
    'ML': ['Bamako'],
    'MM': ['Naypyidaw'],
    'MN': ['Ulaanbaatar', 'Ulan Bator'],
    'MR': ['Nouakchott'],
    'MW': ['Lilongwe'],
    'MX': ['Mexico City'],
    'MY': ['Kuala Lumpur', 'Putrajaya'],
    'MZ': ['Maputo'],
    'NA': ['Windhoek'],
    'NC': ['Nouméa', 'Noumea'],
    'NE': ['Niamey'],
    'NG': ['Abuja'],
    'NI': ['Managua'],
    'NP': ['Kathmandu'],
    'NZ': ['Wellington', 'Auckland', 'Christchurch', 'Queenstown'],
    'OM': ['Muscat'],
    'PA': ['Panama City'],
    'PE': ['Lima'],
    'PG': ['Port Moresby'],
    'PH': ['Manila'],
    'PK': ['Islamabad'],
    'PR': ['San Juan'],
    'PY': ['Asunción', 'Asuncion'],
    'QA': ['Doha'],
    'RW': ['Kigali'],
    'SB': ['Honiara'],
    'SD': ['Khartoum'],
    'SL': ['Freetown'],
    'SN': ['Dakar'],
    'SO': ['Mogadishu'],
    'SR': ['Paramaribo'],
    'SS': ['Juba'],
    'SV': ['San Salvador'],
    'SZ': ['Mbabane', 'Lobamba'],
    'TD': ['N\'Djamena', 'NDjamena', 'N Djamena'],
    'TG': ['Lomé', 'Lome'],
    'TH': ['Bangkok'],
    'TJ': ['Dushanbe'],
    'TL': ['Dili'],
    'TM': ['Ashgabat'],
    'TT': ['Port of Spain'],
    'TW': ['Taipei'],
    'TZ': ['Dodoma'],
    'UG': ['Kampala'],
    'UY': ['Montevideo'],
    'UZ': ['Tashkent'],
    'VE': ['Caracas'],
    'VN': ['Hanoi', 'Ho Chi Minh'],
    'VU': ['Port Vila'],
    'YE': ['Sana\'a', 'Sanaa'],
    'ZA': ['Pretoria', 'Bloemfontein', 'Cape Town', 'Johannesburg'],
    'ZM': ['Lusaka'],
    'ZW': ['Harare'],
}

assert not (set(_WORLD_CITIES) & set(_EUROPE_CITIES))
assert 'US' not in _WORLD_CITIES
assert 'US' not in _EUROPE_CITIES


def _invert(mapping):
    return {v.lower(): k
            for k in mapping
            for v in mapping[k]}


def _regexify(mapping):
    """Make key literals a "contains key" regex so the mapping can be used
    with pandas' .replace()"""
    return {re.compile(r'.*\b' + k + r'\b.*', re.IGNORECASE): v
            for k, v in mapping.items()}


CC_NAME_TO_CC_NAME = _regexify(_invert(_CC_NAME_TO_CC_NAME))
REGION_NAME_TO_REGION_NAME = _regexify(_invert(_REGION_NAME_TO_REGION_NAME))
US_STATE_TO_US_STATE = _regexify(_invert(_US_STATE_TO_US_STATE))

EUROPE_CITIES = _regexify(_invert(_EUROPE_CITIES))
US_CITIES = _regexify(_invert(_US_CITIES))

WORLD_CITIES = _WORLD_CITIES.copy()
WORLD_CITIES.update(US=list(chain.from_iterable(_US_CITIES.values())))
WORLD_CITIES.update(_EUROPE_CITIES)
WORLD_CITIES = _regexify(_invert(WORLD_CITIES))

EUROPE_CITIES_LIST = sorted(chain.from_iterable(_EUROPE_CITIES.values()))
US_CITIES_LIST = sorted(chain.from_iterable(_US_CITIES.values()))
WORLD_CITIES_LIST = sorted(set(chain(chain.from_iterable(_WORLD_CITIES.values()),
                                     EUROPE_CITIES_LIST,
                                     US_CITIES_LIST)))
