"""
Static reference dataset mapping country names to their real first-level
administrative divisions (states/provinces/regions/etc). Used to
auto-populate Region rows the moment a Country is created, so admins
never have to type region names by hand.

Same spirit as country_coordinates.py: offline, static, best-effort
accuracy — not meant to be a survey-grade authority on subnational
boundaries. Countries with no meaningful administrative subdivisions
(city-states, micro-nations) intentionally map to an empty list, which
keeps `has_regions` False for them so branches there go straight under
the country with no region step.

For a handful of countries with disputed/contested subdivisions (e.g.
Crimea, annexed territories), this dataset follows the internationally
recognized/standard baseline rather than disputed additions — consistent
with the "commonly recognized" principle already used for country names
in country_coordinates.py.

Keys here mirror COUNTRY_COORDINATES exactly. This is additive, editable
data: the Country post_save signal re-applies it on every save, so adding
or correcting a country's region list later just needs a re-save (or the
data migration re-run) to take effect — no schema change required.
"""

REGION_DATA: dict[str, list[str]] = {
    "Afghanistan": [
        "Badakhshan", "Badghis", "Baghlan", "Balkh", "Bamyan", "Daykundi", "Farah", "Faryab",
        "Ghazni", "Ghor", "Helmand", "Herat", "Jowzjan", "Kabul", "Kandahar", "Kapisa",
        "Khost", "Kunar", "Kunduz", "Laghman", "Logar", "Nangarhar", "Nimruz", "Nuristan",
        "Paktia", "Paktika", "Panjshir", "Parwan", "Samangan", "Sar-e Pol", "Takhar",
        "Urozgan", "Wardak", "Zabul",
    ],
    "Albania": [
        "Berat", "Dibër", "Durrës", "Elbasan", "Fier", "Gjirokastër", "Korçë", "Kukës",
        "Lezhë", "Shkodër", "Tiranë", "Vlorë",
    ],
    "Algeria": [
        "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", "Béchar",
        "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", "Tizi Ouzou",
        "Algiers", "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", "Sidi Bel Abbès", "Annaba",
        "Guelma", "Constantine", "Médéa", "Mostaganem", "M'Sila", "Mascara", "Ouargla",
        "Oran", "El Bayadh", "Illizi", "Bordj Bou Arréridj", "Boumerdès", "El Tarf",
        "Tindouf", "Tissemsilt", "El Oued", "Khenchela", "Souk Ahras", "Tipaza", "Mila",
        "Aïn Defla", "Naâma", "Aïn Témouchent", "Ghardaïa", "Relizane",
    ],
    "Andorra": [
        "Andorra la Vella", "Canillo", "Encamp", "Escaldes-Engordany", "La Massana",
        "Ordino", "Sant Julià de Lòria",
    ],
    "Angola": [
        "Bengo", "Benguela", "Bié", "Cabinda", "Cuando Cubango", "Cuanza Norte",
        "Cuanza Sul", "Cunene", "Huambo", "Huíla", "Luanda", "Lunda Norte", "Lunda Sul",
        "Malanje", "Moxico", "Namibe", "Uíge", "Zaire",
    ],
    "Antigua and Barbuda": [
        "Saint George", "Saint John", "Saint Mary", "Saint Paul", "Saint Peter",
        "Saint Philip", "Barbuda", "Redonda",
    ],
    "Argentina": [
        "Buenos Aires City", "Buenos Aires Province", "Catamarca", "Chaco", "Chubut",
        "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja",
        "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis",
        "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán",
    ],
    "Armenia": [
        "Aragatsotn", "Ararat", "Armavir", "Gegharkunik", "Kotayk", "Lori", "Shirak",
        "Syunik", "Tavush", "Vayots Dzor", "Yerevan",
    ],
    "Australia": [
        "New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia",
        "Tasmania", "Australian Capital Territory", "Northern Territory",
    ],
    "Austria": [
        "Burgenland", "Carinthia", "Lower Austria", "Upper Austria", "Salzburg", "Styria",
        "Tyrol", "Vorarlberg", "Vienna",
    ],
    "Azerbaijan": [
        "Absheron", "Aran", "Dagliq Shirvan", "Ganja-Gazakh", "Guba-Khachmaz", "Karabakh",
        "Lankaran", "Nakhchivan", "Shaki-Zaqatala", "Shirvan", "Baku",
    ],
    "Bahamas": [
        "Abaco", "Acklins", "Andros", "Berry Islands", "Bimini", "Cat Island",
        "Eleuthera", "Exuma", "Grand Bahama", "Inagua", "Long Island", "Mayaguana",
        "New Providence", "Ragged Island", "Rum Cay", "San Salvador",
    ],
    "Bahrain": ["Capital", "Muharraq", "Northern", "Southern"],
    "Bangladesh": [
        "Barisal", "Chittagong", "Dhaka", "Khulna", "Mymensingh", "Rajshahi", "Rangpur",
        "Sylhet",
    ],
    "Barbados": [
        "Christ Church", "Saint Andrew", "Saint George", "Saint James", "Saint John",
        "Saint Joseph", "Saint Lucy", "Saint Michael", "Saint Peter", "Saint Philip",
        "Saint Thomas",
    ],
    "Belarus": ["Brest", "Gomel", "Grodno", "Minsk Region", "Minsk City", "Mogilev", "Vitebsk"],
    "Belgium": [
        "Antwerp", "East Flanders", "Flemish Brabant", "Hainaut", "Liège", "Limburg",
        "Luxembourg", "Namur", "Walloon Brabant", "West Flanders", "Brussels-Capital",
    ],
    "Belize": ["Belize", "Cayo", "Corozal", "Orange Walk", "Stann Creek", "Toledo"],
    "Benin": [
        "Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Donga", "Kouffo",
        "Littoral", "Mono", "Ouémé", "Plateau", "Zou",
    ],
    "Bhutan": [
        "Bumthang", "Chukha", "Dagana", "Gasa", "Haa", "Lhuntse", "Mongar", "Paro",
        "Pemagatshel", "Punakha", "Samdrup Jongkhar", "Samtse", "Sarpang", "Thimphu",
        "Trashigang", "Trashiyangtse", "Trongsa", "Tsirang", "Wangdue Phodrang", "Zhemgang",
    ],
    "Bolivia": [
        "Beni", "Chuquisaca", "Cochabamba", "La Paz", "Oruro", "Pando", "Potosí",
        "Santa Cruz", "Tarija",
    ],
    "Bosnia and Herzegovina": [
        "Federation of Bosnia and Herzegovina", "Republika Srpska", "Brčko District",
    ],
    "Botswana": [
        "Central", "Chobe", "Ghanzi", "Kgalagadi", "Kgatleng", "Kweneng", "North-East",
        "North-West", "South-East", "Southern",
    ],
    "Brazil": [
        "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
        "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
        "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
        "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina",
        "São Paulo", "Sergipe", "Tocantins",
    ],
    "Brunei": ["Belait", "Brunei-Muara", "Temburong", "Tutong"],
    "Bulgaria": [
        "Blagoevgrad", "Burgas", "Dobrich", "Gabrovo", "Haskovo", "Kardzhali", "Kyustendil",
        "Lovech", "Montana", "Pazardzhik", "Pernik", "Pleven", "Plovdiv", "Razgrad", "Ruse",
        "Shumen", "Silistra", "Sliven", "Smolyan", "Sofia City", "Sofia Province",
        "Stara Zagora", "Targovishte", "Varna", "Veliko Tarnovo", "Vidin", "Vratsa", "Yambol",
    ],
    "Burkina Faso": [
        "Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord",
        "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord", "Plateau-Central",
        "Sahel", "Sud-Ouest",
    ],
    "Burundi": [
        "Bubanza", "Bujumbura Mairie", "Bujumbura Rural", "Bururi", "Cankuzo", "Cibitoke",
        "Gitega", "Karuzi", "Kayanza", "Kirundo", "Makamba", "Muramvya", "Muyinga", "Mwaro",
        "Ngozi", "Rumonge", "Rutana", "Ruyigi",
    ],
    "Cabo Verde": [
        "Boa Vista", "Brava", "Fogo", "Maio", "Santo Antão", "São Nicolau", "São Vicente",
        "Santiago", "Sal",
    ],
    "Cambodia": [
        "Banteay Meanchey", "Battambang", "Kampong Cham", "Kampong Chhnang", "Kampong Speu",
        "Kampong Thom", "Kampot", "Kandal", "Kep", "Koh Kong", "Kratié", "Mondulkiri",
        "Oddar Meanchey", "Pailin", "Phnom Penh", "Preah Vihear", "Prey Veng", "Pursat",
        "Ratanakiri", "Siem Reap", "Sihanoukville", "Stung Treng", "Svay Rieng", "Takéo",
        "Tboung Khmum",
    ],
    "Cameroon": [
        "Adamawa", "Centre", "East", "Far North", "Littoral", "North", "Northwest",
        "South", "Southwest", "West",
    ],
    "Canada": [
        "Alberta", "British Columbia", "Manitoba", "New Brunswick",
        "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island",
        "Quebec", "Saskatchewan", "Northwest Territories", "Nunavut", "Yukon",
    ],
    "Central African Republic": [
        "Bamingui-Bangoran", "Bangui", "Basse-Kotto", "Haute-Kotto", "Haut-Mbomou",
        "Kémo", "Lobaye", "Mambéré-Kadéï", "Mbomou", "Nana-Grébizi", "Nana-Mambéré",
        "Ombella-M'Poko", "Ouaka", "Ouham", "Ouham-Pendé", "Sangha-Mbaéré", "Vakaga",
    ],
    "Chad": [
        "Batha", "Chari-Baguirmi", "Guéra", "Hadjer-Lamis", "Kanem", "Lac",
        "Logone Occidental", "Logone Oriental", "Mandoul", "Mayo-Kebbi Est",
        "Mayo-Kebbi Ouest", "Moyen-Chari", "N'Djamena", "Ouaddaï", "Salamat", "Sila",
        "Tandjilé", "Tibesti", "Wadi Fira", "Barh El Gazel", "Ennedi Est", "Ennedi Ouest",
    ],
    "Chile": [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana de Santiago", "Libertador General Bernardo O'Higgins",
        "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos", "Los Lagos", "Aysén",
        "Magallanes",
    ],
    "China": [
        "Anhui", "Beijing", "Chongqing", "Fujian", "Gansu", "Guangdong", "Guangxi",
        "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan", "Hong Kong", "Hubei",
        "Hunan", "Inner Mongolia", "Jiangsu", "Jiangxi", "Jilin", "Liaoning", "Macau",
        "Ningxia", "Qinghai", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan",
        "Tianjin", "Tibet", "Xinjiang", "Yunnan", "Zhejiang",
    ],
    "Colombia": [
        "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas",
        "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca",
        "Guainía", "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta", "Nariño",
        "Norte de Santander", "Putumayo", "Quindío", "Risaralda",
        "San Andrés y Providencia", "Santander", "Sucre", "Tolima", "Valle del Cauca",
        "Vaupés", "Vichada", "Bogotá",
    ],
    "Comoros": ["Grande Comore", "Anjouan", "Mohéli"],
    "Costa Rica": [
        "Alajuela", "Cartago", "Guanacaste", "Heredia", "Limón", "Puntarenas", "San José",
    ],
    "Croatia": [
        "Bjelovar-Bilogora", "Brod-Posavina", "Dubrovnik-Neretva", "Istria", "Karlovac",
        "Koprivnica-Križevci", "Krapina-Zagorje", "Lika-Senj", "Međimurje",
        "Osijek-Baranja", "Požega-Slavonia", "Primorje-Gorski Kotar", "Šibenik-Knin",
        "Sisak-Moslavina", "Split-Dalmatia", "Varaždin", "Virovitica-Podravina",
        "Vukovar-Syrmia", "Zadar", "Zagreb County", "City of Zagreb",
    ],
    "Cuba": [
        "Artemisa", "Camagüey", "Ciego de Ávila", "Cienfuegos", "Granma", "Guantánamo",
        "Havana", "Holguín", "Isla de la Juventud", "Las Tunas", "Matanzas", "Mayabeque",
        "Pinar del Río", "Sancti Spíritus", "Santiago de Cuba", "Villa Clara",
    ],
    "Cyprus": ["Famagusta", "Kyrenia", "Larnaca", "Limassol", "Nicosia", "Paphos"],
    "Czech Republic": [
        "Central Bohemian", "South Bohemian", "Plzeň", "Karlovy Vary", "Ústí nad Labem",
        "Liberec", "Hradec Králové", "Pardubice", "Vysočina", "South Moravian", "Olomouc",
        "Zlín", "Moravian-Silesian", "Prague",
    ],
    "Democratic Republic of the Congo": [
        "Bas-Uele", "Équateur", "Haut-Katanga", "Haut-Lomami", "Haut-Uele", "Ituri",
        "Kasaï", "Kasaï-Central", "Kasaï-Oriental", "Kinshasa", "Kongo Central", "Kwango",
        "Kwilu", "Lomami", "Lualaba", "Mai-Ndombe", "Maniema", "Mongala", "Nord-Kivu",
        "Nord-Ubangi", "Sankuru", "Sud-Kivu", "Sud-Ubangi", "Tanganyika", "Tshopo",
        "Tshuapa",
    ],
    "Denmark": [
        "Capital Region", "Central Denmark", "North Denmark", "Region Zealand",
        "Region of Southern Denmark",
    ],
    "Djibouti": ["Ali Sabieh", "Arta", "Dikhil", "Djibouti", "Obock", "Tadjourah"],
    "Dominica": [
        "Saint Andrew", "Saint David", "Saint George", "Saint John", "Saint Joseph",
        "Saint Luke", "Saint Mark", "Saint Patrick", "Saint Paul", "Saint Peter",
    ],
    "Dominican Republic": [
        "Azua", "Baoruco", "Barahona", "Dajabón", "Distrito Nacional", "Duarte",
        "El Seibo", "Elías Piña", "Espaillat", "Hato Mayor", "Hermanas Mirabal",
        "Independencia", "La Altagracia", "La Romana", "La Vega",
        "María Trinidad Sánchez", "Monseñor Nouel", "Monte Cristi", "Monte Plata",
        "Pedernales", "Peravia", "Puerto Plata", "Samaná", "San Cristóbal",
        "San José de Ocoa", "San Juan", "San Pedro de Macorís", "Sánchez Ramírez",
        "Santiago", "Santiago Rodríguez", "Santo Domingo", "Valverde",
    ],
    "Ecuador": [
        "Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo", "Cotopaxi", "El Oro",
        "Esmeraldas", "Galápagos", "Guayas", "Imbabura", "Loja", "Los Ríos", "Manabí",
        "Morona-Santiago", "Napo", "Orellana", "Pastaza", "Pichincha", "Santa Elena",
        "Santo Domingo de los Tsáchilas", "Sucumbíos", "Tungurahua", "Zamora-Chinchipe",
    ],
    "Egypt": [
        "Alexandria", "Aswan", "Asyut", "Beheira", "Beni Suef", "Cairo", "Dakahlia",
        "Damietta", "Faiyum", "Gharbia", "Giza", "Ismailia", "Kafr el-Sheikh", "Luxor",
        "Matrouh", "Minya", "Monufia", "New Valley", "North Sinai", "Port Said",
        "Qalyubia", "Qena", "Red Sea", "Sharqia", "Sohag", "South Sinai", "Suez",
    ],
    "El Salvador": [
        "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad", "La Paz",
        "La Unión", "Morazán", "San Miguel", "San Salvador", "San Vicente", "Santa Ana",
        "Sonsonate", "Usulután",
    ],
    "Equatorial Guinea": [
        "Annobón", "Bioko Norte", "Bioko Sur", "Centro Sur", "Kié-Ntem", "Litoral",
        "Wele-Nzas",
    ],
    "Eritrea": ["Anseba", "Debub", "Gash-Barka", "Maekel", "Northern Red Sea", "Southern Red Sea"],
    "Estonia": [
        "Harju", "Hiiu", "Ida-Viru", "Järva", "Jõgeva", "Lääne", "Lääne-Viru", "Pärnu",
        "Põlva", "Rapla", "Saare", "Tartu", "Valga", "Viljandi", "Võru",
    ],
    "Eswatini": ["Hhohho", "Lubombo", "Manzini", "Shiselweni"],
    "Ethiopia": [
        "Addis Ababa", "Afar", "Amhara", "Benishangul-Gumuz", "Dire Dawa", "Gambela",
        "Harari", "Oromia", "Sidama", "Somali", "South Ethiopia",
        "South West Ethiopia Peoples", "Tigray", "Central Ethiopia",
    ],
    "Fiji": ["Central", "Eastern", "Northern", "Western"],
    "Finland": [
        "Åland", "Central Finland", "Central Ostrobothnia", "Kainuu", "Kanta-Häme",
        "Kymenlaakso", "Lapland", "North Karelia", "North Ostrobothnia", "North Savo",
        "Ostrobothnia", "Päijänne Tavastia", "Pirkanmaa", "Satakunta", "South Karelia",
        "South Ostrobothnia", "South Savo", "Southwest Finland", "Uusimaa",
    ],
    "France": [
        "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Brittany", "Centre-Val de Loire",
        "Corsica", "Grand Est", "Hauts-de-France", "Île-de-France", "Normandy",
        "Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Provence-Alpes-Côte d'Azur",
    ],
    "Gabon": [
        "Estuaire", "Haut-Ogooué", "Moyen-Ogooué", "Ngounié", "Nyanga", "Ogooué-Ivindo",
        "Ogooué-Lolo", "Ogooué-Maritime", "Woleu-Ntem",
    ],
    "Gambia": ["Banjul", "Central River", "Lower River", "North Bank", "Upper River", "West Coast"],
    "Georgia": [
        "Abkhazia", "Adjara", "Guria", "Imereti", "Kakheti", "Kvemo Kartli",
        "Mtskheta-Mtianeti", "Racha-Lechkhumi and Kvemo Svaneti",
        "Samegrelo-Zemo Svaneti", "Samtskhe-Javakheti", "Shida Kartli", "Tbilisi",
    ],
    "Germany": [
        "Baden-Württemberg", "Bavaria", "Berlin", "Brandenburg", "Bremen", "Hamburg",
        "Hesse", "Lower Saxony", "Mecklenburg-Vorpommern", "North Rhine-Westphalia",
        "Rhineland-Palatinate", "Saarland", "Saxony", "Saxony-Anhalt",
        "Schleswig-Holstein", "Thuringia",
    ],
    "Ghana": [
        "Greater Accra", "Ashanti", "Western", "Ahafo", "Bono", "Bono East", "Central",
        "Eastern", "North East", "Northern", "Oti", "Savannah", "Upper East",
        "Upper West", "Volta", "Western North",
    ],
    "Greece": [
        "Attica", "Central Greece", "Central Macedonia", "Crete",
        "Eastern Macedonia and Thrace", "Epirus", "Ionian Islands", "North Aegean",
        "Peloponnese", "South Aegean", "Thessaly", "West Greece", "West Macedonia",
    ],
    "Grenada": [
        "Saint Andrew", "Saint David", "Saint George", "Saint John", "Saint Mark",
        "Saint Patrick", "Carriacou and Petite Martinique",
    ],
    "Guatemala": [
        "Alta Verapaz", "Baja Verapaz", "Chimaltenango", "Chiquimula", "El Progreso",
        "Escuintla", "Guatemala", "Huehuetenango", "Izabal", "Jalapa", "Jutiapa",
        "Petén", "Quetzaltenango", "Quiché", "Retalhuleu", "Sacatepéquez", "San Marcos",
        "Santa Rosa", "Sololá", "Suchitepéquez", "Totonicapán", "Zacapa",
    ],
    "Guinea": ["Boké", "Conakry", "Faranah", "Kankan", "Kindia", "Labé", "Mamou", "Nzérékoré"],
    "Guinea-Bissau": [
        "Bafatá", "Biombo", "Bissau", "Bolama", "Cacheu", "Gabú", "Oio", "Quinara",
        "Tombali",
    ],
    "Guyana": [
        "Barima-Waini", "Cuyuni-Mazaruni", "Demerara-Mahaica", "East Berbice-Corentyne",
        "Essequibo Islands-West Demerara", "Mahaica-Berbice", "Pomeroon-Supenaam",
        "Potaro-Siparuni", "Upper Demerara-Berbice", "Upper Takutu-Upper Essequibo",
    ],
    "Haiti": [
        "Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord", "Nord-Est", "Nord-Ouest",
        "Ouest", "Sud", "Sud-Est",
    ],
    "Honduras": [
        "Atlántida", "Choluteca", "Colón", "Comayagua", "Copán", "Cortés",
        "El Paraíso", "Francisco Morazán", "Gracias a Dios", "Intibucá",
        "Islas de la Bahía", "La Paz", "Lempira", "Ocotepeque", "Olancho",
        "Santa Bárbara", "Valle", "Yoro",
    ],
    "Hungary": [
        "Bács-Kiskun", "Baranya", "Békés", "Borsod-Abaúj-Zemplén", "Budapest",
        "Csongrád-Csanád", "Fejér", "Győr-Moson-Sopron", "Hajdú-Bihar", "Heves",
        "Jász-Nagykun-Szolnok", "Komárom-Esztergom", "Nógrád", "Pest", "Somogy",
        "Szabolcs-Szatmár-Bereg", "Tolna", "Vas", "Veszprém", "Zala",
    ],
    "Iceland": [
        "Capital Region", "Southern Peninsula", "Western Region", "Westfjords",
        "Northwestern Region", "Northeastern Region", "Eastern Region", "Southern Region",
    ],
    "India": [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
        "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
        "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
        "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
        "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
    ],
    "Indonesia": [
        "Aceh", "Bali", "Bangka Belitung Islands", "Banten", "Bengkulu", "Central Java",
        "Central Kalimantan", "Central Sulawesi", "East Java", "East Kalimantan",
        "East Nusa Tenggara", "Gorontalo", "Jakarta", "Jambi", "Lampung", "Maluku",
        "North Kalimantan", "North Maluku", "North Sulawesi", "North Sumatra", "Papua",
        "Riau", "Riau Islands", "South Kalimantan", "South Sulawesi", "South Sumatra",
        "Southeast Sulawesi", "Southwest Papua", "West Java", "West Kalimantan",
        "West Nusa Tenggara", "West Papua", "West Sulawesi", "West Sumatra",
        "Yogyakarta", "Central Papua", "Highland Papua", "South Papua",
    ],
    "Iran": [
        "Alborz", "Ardabil", "Bushehr", "Chaharmahal and Bakhtiari", "East Azerbaijan",
        "Fars", "Gilan", "Golestan", "Hamadan", "Hormozgan", "Ilam", "Isfahan", "Kerman",
        "Kermanshah", "Khuzestan", "Kohgiluyeh and Boyer-Ahmad", "Kurdistan", "Lorestan",
        "Markazi", "Mazandaran", "North Khorasan", "Qazvin", "Qom", "Razavi Khorasan",
        "Semnan", "Sistan and Baluchestan", "South Khorasan", "Tehran",
        "West Azerbaijan", "Yazd", "Zanjan",
    ],
    "Iraq": [
        "Al Anbar", "Babil", "Baghdad", "Basra", "Dhi Qar", "Diyala", "Duhok", "Erbil",
        "Karbala", "Kirkuk", "Maysan", "Muthanna", "Najaf", "Nineveh", "Qadisiyyah",
        "Saladin", "Sulaymaniyah", "Wasit", "Halabja",
    ],
    "Ireland": [
        "Carlow", "Cavan", "Clare", "Cork", "Donegal", "Dublin", "Galway", "Kerry",
        "Kildare", "Kilkenny", "Laois", "Leitrim", "Limerick", "Longford", "Louth",
        "Mayo", "Meath", "Monaghan", "Offaly", "Roscommon", "Sligo", "Tipperary",
        "Waterford", "Westmeath", "Wexford", "Wicklow",
    ],
    "Israel": ["Central", "Haifa", "Jerusalem", "Northern", "Southern", "Tel Aviv"],
    "Italy": [
        "Abruzzo", "Aosta Valley", "Apulia", "Basilicata", "Calabria", "Campania",
        "Emilia-Romagna", "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardy",
        "Marche", "Molise", "Piedmont", "Sardinia", "Sicily", "Trentino-Alto Adige",
        "Tuscany", "Umbria", "Veneto",
    ],
    "Ivory Coast": [
        "Abidjan", "Bas-Sassandra", "Comoé", "Denguélé", "Gôh-Djiboua", "Lacs",
        "Lagunes", "Montagnes", "Sassandra-Marahoué", "Savanes", "Vallée du Bandama",
        "Woroba", "Yamoussoukro", "Zanzan",
    ],
    "Jamaica": [
        "Clarendon", "Hanover", "Kingston", "Manchester", "Portland", "Saint Andrew",
        "Saint Ann", "Saint Catherine", "Saint Elizabeth", "Saint James", "Saint Mary",
        "Saint Thomas", "Trelawny", "Westmoreland",
    ],
    "Japan": [
        "Aichi", "Akita", "Aomori", "Chiba", "Ehime", "Fukui", "Fukuoka", "Fukushima",
        "Gifu", "Gunma", "Hiroshima", "Hokkaido", "Hyogo", "Ibaraki", "Ishikawa",
        "Iwate", "Kagawa", "Kagoshima", "Kanagawa", "Kochi", "Kumamoto", "Kyoto",
        "Mie", "Miyagi", "Miyazaki", "Nagano", "Nagasaki", "Nara", "Niigata", "Oita",
        "Okayama", "Okinawa", "Osaka", "Saga", "Saitama", "Shiga", "Shimane",
        "Shizuoka", "Tochigi", "Tokushima", "Tokyo", "Tottori", "Toyama", "Wakayama",
        "Yamagata", "Yamaguchi", "Yamanashi",
    ],
    "Jordan": [
        "Ajloun", "Amman", "Aqaba", "Balqa", "Irbid", "Jerash", "Karak", "Ma'an",
        "Madaba", "Mafraq", "Tafilah", "Zarqa",
    ],
    "Kazakhstan": [
        "Abai", "Akmola", "Aktobe", "Almaty Region", "Almaty City", "Astana", "Atyrau",
        "East Kazakhstan", "Jambyl", "Karaganda", "Kostanay", "Kyzylorda", "Mangystau",
        "North Kazakhstan", "Pavlodar", "Shymkent", "Turkistan", "Ulytau",
        "West Kazakhstan",
    ],
    "Kenya": [
        "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu", "Garissa",
        "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", "Kiambu", "Kilifi",
        "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia", "Lamu",
        "Machakos", "Makueni", "Mandera", "Marsabit", "Meru", "Migori", "Mombasa",
        "Murang'a", "Nairobi", "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua",
        "Nyeri", "Samburu", "Siaya", "Taita-Taveta", "Tana River", "Tharaka-Nithi",
        "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot",
    ],
    "Kiribati": ["Gilbert Islands", "Line Islands", "Phoenix Islands"],
    "Kosovo": ["Ferizaj", "Gjakova", "Gjilan", "Mitrovica", "Peja", "Pristina", "Prizren"],
    "Kuwait": ["Al Ahmadi", "Al Farwaniyah", "Al Jahra", "Capital", "Hawalli", "Mubarak Al-Kabeer"],
    "Kyrgyzstan": [
        "Batken", "Bishkek", "Chuy", "Issyk-Kul", "Jalal-Abad", "Naryn", "Osh Region",
        "Osh City", "Talas",
    ],
    "Laos": [
        "Attapeu", "Bokeo", "Bolikhamsai", "Champasak", "Houaphanh", "Khammouane",
        "Luang Namtha", "Luang Prabang", "Oudomxay", "Phongsaly", "Sainyabuli",
        "Salavan", "Savannakhet", "Sekong", "Vientiane Province", "Vientiane Capital",
        "Xaisomboun", "Xiangkhouang",
    ],
    "Latvia": ["Kurzeme", "Latgale", "Riga", "Vidzeme", "Zemgale"],
    "Lebanon": [
        "Akkar", "Baalbek-Hermel", "Beirut", "Beqaa", "Mount Lebanon", "Nabatieh",
        "North", "South",
    ],
    "Lesotho": [
        "Berea", "Butha-Buthe", "Leribe", "Mafeteng", "Maseru", "Mohale's Hoek",
        "Mokhotlong", "Qacha's Nek", "Quthing", "Thaba-Tseka",
    ],
    "Liberia": [
        "Bomi", "Bong", "Gbarpolu", "Grand Bassa", "Grand Cape Mount", "Grand Gedeh",
        "Grand Kru", "Lofa", "Margibi", "Maryland", "Montserrado", "Nimba",
        "River Cess", "River Gee", "Sinoe",
    ],
    "Libya": [
        "Al Butnan", "Al Jabal al Akhdar", "Al Jabal al Gharbi", "Al Jfara", "Al Kufrah",
        "Al Marj", "Al Marqab", "Al Wahat", "Az Zawiyah", "Banghazi", "Darnah", "Ghat",
        "Misrata", "Murzuq", "Nalut", "Sabha", "Sirte", "Tripoli", "Wadi al Hayaa",
        "Wadi al Shatii", "Zwara",
    ],
    "Liechtenstein": [
        "Balzers", "Eschen", "Gamprin", "Mauren", "Planken", "Ruggell", "Schaan",
        "Schellenberg", "Triesen", "Triesenberg", "Vaduz",
    ],
    "Lithuania": [
        "Alytus", "Kaunas", "Klaipėda", "Marijampolė", "Panevėžys", "Šiauliai",
        "Tauragė", "Telšiai", "Utena", "Vilnius",
    ],
    "Luxembourg": ["Diekirch", "Grevenmacher", "Luxembourg"],
    "Madagascar": [
        "Alaotra-Mangoro", "Amoron'i Mania", "Analamanga", "Analanjirofo", "Androy",
        "Anosy", "Atsimo-Andrefana", "Atsimo-Atsinanana", "Atsinanana", "Betsiboka",
        "Boeny", "Bongolava", "Diana", "Haute Matsiatra", "Ihorombe", "Itasy",
        "Melaky", "Menabe", "Sava", "Sofia", "Vakinankaratra", "Vatovavy", "Fitovinany",
    ],
    "Malawi": ["Central Region", "Northern Region", "Southern Region"],
    "Malaysia": [
        "Johor", "Kedah", "Kelantan", "Malacca", "Negeri Sembilan", "Pahang", "Penang",
        "Perak", "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", "Kuala Lumpur",
        "Labuan", "Putrajaya",
    ],
    "Maldives": [
        "Haa Alif", "Haa Dhaalu", "Shaviyani", "Noonu", "Raa", "Baa", "Lhaviyani",
        "Kaafu", "Alifu Alifu", "Alifu Dhaalu", "Vaavu", "Meemu", "Faafu", "Dhaalu",
        "Thaa", "Laamu", "Gaafu Alifu", "Gaafu Dhaalu", "Gnaviyani", "Seenu",
    ],
    "Mali": [
        "Bamako", "Gao", "Kayes", "Kidal", "Koulikoro", "Mopti", "Ménaka", "Ségou",
        "Sikasso", "Taoudénit", "Tombouctou",
    ],
    "Malta": ["Gozo", "Malta"],
    "Marshall Islands": ["Ralik Chain", "Ratak Chain"],
    "Mauritania": [
        "Adrar", "Assaba", "Brakna", "Dakhlet Nouadhibou", "Gorgol", "Guidimaka",
        "Hodh Ech Chargui", "Hodh El Gharbi", "Inchiri", "Nouakchott Nord",
        "Nouakchott Ouest", "Nouakchott Sud", "Tagant", "Tiris Zemmour", "Trarza",
    ],
    "Mauritius": [
        "Black River", "Flacq", "Grand Port", "Moka", "Pamplemousses",
        "Plaines Wilhems", "Port Louis", "Rivière du Rempart", "Savanne",
    ],
    "Mexico": [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
        "Chiapas", "Chihuahua", "Coahuila", "Colima", "Durango", "Guanajuato",
        "Guerrero", "Hidalgo", "Jalisco", "Mexico City", "Mexico State", "Michoacán",
        "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro",
        "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
        "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas",
    ],
    "Micronesia": ["Chuuk", "Kosrae", "Pohnpei", "Yap"],
    "Moldova": [
        "Anenii Noi", "Bălți", "Basarabeasca", "Briceni", "Cahul", "Cantemir",
        "Călărași", "Căușeni", "Chișinău", "Cimișlia", "Criuleni", "Dondușeni",
        "Drochia", "Dubăsari", "Edineț", "Fălești", "Florești", "Gagauzia",
        "Glodeni", "Hîncești", "Ialoveni", "Nisporeni", "Ocnița", "Orhei", "Rezina",
        "Rîșcani", "Sîngerei", "Soroca", "Ștefan Vodă", "Strășeni", "Taraclia",
        "Telenești", "Transnistria", "Ungheni",
    ],
    "Monaco": [],
    "Mongolia": [
        "Arkhangai", "Bayan-Ölgii", "Bayankhongor", "Bulgan", "Darkhan-Uul", "Dornod",
        "Dornogovi", "Dundgovi", "Govi-Altai", "Govisümber", "Khentii", "Khovd",
        "Khövsgöl", "Ömnögovi", "Orkhon", "Övörkhangai", "Selenge", "Sükhbaatar",
        "Töv", "Uvs", "Zavkhan", "Ulaanbaatar",
    ],
    "Montenegro": [
        "Podgorica", "Nikšić", "Herceg Novi", "Bar", "Budva", "Cetinje", "Pljevlja",
        "Bijelo Polje", "Berane", "Kotor", "Tivat", "Ulcinj", "Rožaje", "Danilovgrad",
        "Mojkovac", "Kolašin", "Plav", "Andrijevica", "Žabljak", "Plužine", "Šavnik",
        "Gusinje", "Tuzi", "Petnjica",
    ],
    "Morocco": [
        "Tanger-Tétouan-Al Hoceïma", "L'Oriental", "Fès-Meknès", "Rabat-Salé-Kénitra",
        "Béni Mellal-Khénifra", "Casablanca-Settat", "Marrakech-Safi",
        "Drâa-Tafilalet", "Souss-Massa", "Guelmim-Oued Noun",
        "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab",
    ],
    "Mozambique": [
        "Cabo Delgado", "Gaza", "Inhambane", "Manica", "Maputo City", "Maputo Province",
        "Nampula", "Niassa", "Sofala", "Tete", "Zambezia",
    ],
    "Myanmar": [
        "Kachin", "Kayah", "Kayin", "Chin", "Mon", "Rakhine", "Shan", "Ayeyarwady",
        "Bago", "Magway", "Mandalay", "Sagaing", "Tanintharyi", "Yangon", "Naypyidaw",
    ],
    "Namibia": [
        "Erongo", "Hardap", "Karas", "Kavango East", "Kavango West", "Khomas",
        "Kunene", "Ohangwena", "Omaheke", "Omusati", "Oshana", "Oshikoto",
        "Otjozondjupa", "Zambezi",
    ],
    "Nauru": [
        "Aiwo", "Anabar", "Anetan", "Anibare", "Baiti", "Boe", "Buada", "Denigomodu",
        "Ewa", "Ijuw", "Meneng", "Nibok", "Uaboe", "Yaren",
    ],
    "Nepal": ["Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"],
    "Netherlands": [
        "Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen", "Limburg",
        "North Brabant", "North Holland", "Overijssel", "South Holland", "Utrecht",
        "Zeeland",
    ],
    "New Zealand": [
        "Auckland", "Bay of Plenty", "Canterbury", "Gisborne", "Hawke's Bay",
        "Manawatu-Whanganui", "Marlborough", "Nelson", "Northland", "Otago",
        "Southland", "Taranaki", "Tasman", "Waikato", "Wellington", "West Coast",
    ],
    "Nicaragua": [
        "Boaco", "Carazo", "Chinandega", "Chontales", "Estelí", "Granada", "Jinotega",
        "León", "Madriz", "Managua", "Masaya", "Matagalpa", "Nueva Segovia", "Rivas",
        "Río San Juan", "North Caribbean Coast", "South Caribbean Coast",
    ],
    "Niger": ["Agadez", "Diffa", "Dosso", "Maradi", "Niamey", "Tahoua", "Tillabéri", "Zinder"],
    "Nigeria": [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
        "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu",
        "Federal Capital Territory", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
        "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun",
        "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe",
        "Zamfara",
    ],
    "North Korea": [
        "Chagang", "North Hamgyong", "South Hamgyong", "North Hwanghae",
        "South Hwanghae", "Kangwon", "North Pyongan", "South Pyongan", "Ryanggang",
        "Pyongyang", "Rason",
    ],
    "North Macedonia": [
        "Vardar", "East", "Southwest", "Southeast", "Pelagonia", "Polog", "Northeast",
        "Skopje",
    ],
    "Norway": [
        "Agder", "Akershus", "Buskerud", "Finnmark", "Innlandet", "Møre og Romsdal",
        "Nordland", "Oslo", "Østfold", "Rogaland", "Telemark", "Troms", "Trøndelag",
        "Vestfold", "Vestland",
    ],
    "Oman": [
        "Ad Dakhiliyah", "Ad Dhahirah", "Al Batinah North", "Al Batinah South",
        "Al Buraimi", "Al Wusta", "Ash Sharqiyah North", "Ash Sharqiyah South",
        "Dhofar", "Musandam", "Muscat",
    ],
    "Pakistan": [
        "Balochistan", "Khyber Pakhtunkhwa", "Punjab", "Sindh", "Azad Kashmir",
        "Gilgit-Baltistan", "Islamabad Capital Territory",
    ],
    "Palau": [
        "Aimeliik", "Airai", "Angaur", "Hatohobei", "Kayangel", "Koror", "Melekeok",
        "Ngaraard", "Ngarchelong", "Ngardmau", "Ngatpang", "Ngchesar",
        "Ngeremlengui", "Ngiwal", "Peleliu", "Sonsorol",
    ],
    "Palestine": [
        "Bethlehem", "Deir al-Balah", "Gaza", "Hebron", "Jenin", "Jericho",
        "Jerusalem", "Khan Yunis", "Nablus", "North Gaza", "Qalqilya", "Rafah",
        "Ramallah and al-Bireh", "Salfit", "Tubas", "Tulkarm",
    ],
    "Panama": [
        "Bocas del Toro", "Chiriquí", "Coclé", "Colón", "Darién", "Herrera",
        "Los Santos", "Panamá", "Panamá Oeste", "Veraguas",
    ],
    "Papua New Guinea": [
        "Bougainville", "Central", "Chimbu", "Eastern Highlands", "East New Britain",
        "East Sepik", "Enga", "Gulf", "Hela", "Jiwaka", "Madang", "Manus",
        "Milne Bay", "Morobe", "National Capital District", "New Ireland",
        "Northern", "Southern Highlands", "West New Britain", "Sandaun", "Western",
        "Western Highlands",
    ],
    "Paraguay": [
        "Alto Paraguay", "Alto Paraná", "Amambay", "Boquerón", "Caaguazú", "Caazapá",
        "Canindeyú", "Central", "Concepción", "Cordillera", "Guairá", "Itapúa",
        "Misiones", "Ñeembucú", "Paraguarí", "Presidente Hayes", "San Pedro",
        "Asunción",
    ],
    "Peru": [
        "Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca",
        "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad",
        "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco",
        "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali",
    ],
    "Philippines": [
        "Ilocos", "Cagayan Valley", "Central Luzon", "Calabarzon", "Mimaropa",
        "Bicol", "Western Visayas", "Central Visayas", "Eastern Visayas",
        "Zamboanga Peninsula", "Northern Mindanao", "Davao", "Soccsksargen",
        "Caraga", "Bangsamoro", "Cordillera", "National Capital Region",
    ],
    "Poland": [
        "Greater Poland", "Kuyavian-Pomeranian", "Lesser Poland", "Łódź",
        "Lower Silesian", "Lublin", "Lubusz", "Masovian", "Opole", "Podkarpackie",
        "Podlaskie", "Pomeranian", "Silesian", "Świętokrzyskie",
        "Warmian-Masurian", "West Pomeranian",
    ],
    "Portugal": [
        "Aveiro", "Beja", "Braga", "Bragança", "Castelo Branco", "Coimbra", "Évora",
        "Faro", "Guarda", "Leiria", "Lisbon", "Portalegre", "Porto", "Santarém",
        "Setúbal", "Viana do Castelo", "Vila Real", "Viseu", "Azores", "Madeira",
    ],
    "Qatar": [
        "Al Daayen", "Al Khor", "Al Rayyan", "Al Shamal", "Al Wakrah", "Doha",
        "Madinat ash Shamal", "Umm Salal",
    ],
    "Republic of the Congo": [
        "Bouenza", "Brazzaville", "Cuvette", "Cuvette-Ouest", "Kouilou", "Lékoumou",
        "Likouala", "Niari", "Plateaux", "Pointe-Noire", "Pool", "Sangha",
    ],
    "Romania": [
        "Alba", "Arad", "Argeș", "Bacău", "Bihor", "Bistrița-Năsăud", "Botoșani",
        "Brăila", "Brașov", "București", "Buzău", "Călărași", "Caraș-Severin",
        "Cluj", "Constanța", "Covasna", "Dâmbovița", "Dolj", "Galați", "Giurgiu",
        "Gorj", "Harghita", "Hunedoara", "Ialomița", "Iași", "Ilfov", "Maramureș",
        "Mehedinți", "Mureș", "Neamț", "Olt", "Prahova", "Sălaj", "Satu Mare",
        "Sibiu", "Suceava", "Teleorman", "Timiș", "Tulcea", "Vâlcea", "Vaslui",
        "Vrancea",
    ],
    "Russia": [
        "Adygea", "Altai Krai", "Altai Republic", "Amur Oblast", "Arkhangelsk Oblast",
        "Astrakhan Oblast", "Bashkortostan", "Belgorod Oblast", "Bryansk Oblast",
        "Buryatia", "Chechnya", "Chelyabinsk Oblast", "Chukotka", "Chuvashia",
        "Dagestan", "Ingushetia", "Irkutsk Oblast", "Ivanovo Oblast",
        "Jewish Autonomous Oblast", "Kabardino-Balkaria", "Kaliningrad Oblast",
        "Kalmykia", "Kaluga Oblast", "Kamchatka Krai", "Karachay-Cherkessia",
        "Karelia", "Kemerovo Oblast", "Khabarovsk Krai", "Khakassia",
        "Khanty-Mansi", "Kirov Oblast", "Komi Republic", "Kostroma Oblast",
        "Krasnodar Krai", "Krasnoyarsk Krai", "Kurgan Oblast", "Kursk Oblast",
        "Leningrad Oblast", "Lipetsk Oblast", "Magadan Oblast", "Mari El",
        "Mordovia", "Moscow", "Moscow Oblast", "Murmansk Oblast", "Nenets",
        "Nizhny Novgorod Oblast", "North Ossetia-Alania", "Novgorod Oblast",
        "Novosibirsk Oblast", "Omsk Oblast", "Orenburg Oblast", "Oryol Oblast",
        "Penza Oblast", "Perm Krai", "Primorsky Krai", "Pskov Oblast",
        "Rostov Oblast", "Ryazan Oblast", "Saint Petersburg", "Sakha (Yakutia)",
        "Sakhalin Oblast", "Samara Oblast", "Saratov Oblast", "Smolensk Oblast",
        "Stavropol Krai", "Sverdlovsk Oblast", "Tambov Oblast", "Tatarstan",
        "Tomsk Oblast", "Tula Oblast", "Tuva", "Tver Oblast", "Tyumen Oblast",
        "Udmurtia", "Ulyanovsk Oblast", "Vladimir Oblast", "Volgograd Oblast",
        "Vologda Oblast", "Voronezh Oblast", "Yamalo-Nenets", "Yaroslavl Oblast",
        "Zabaykalsky Krai",
    ],
    "Rwanda": ["Kigali", "Eastern", "Northern", "Southern", "Western"],
    "Saint Kitts and Nevis": [
        "Christ Church Nichola Town", "Saint Anne Sandy Point",
        "Saint George Basseterre", "Saint George Gingerland",
        "Saint James Windward", "Saint John Capisterre", "Saint John Figtree",
        "Saint Mary Cayon", "Saint Paul Capisterre", "Saint Paul Charlestown",
        "Saint Peter Basseterre", "Saint Thomas Lowland", "Saint Thomas Middle Island",
        "Trinity Palmetto Point",
    ],
    "Saint Lucia": [
        "Anse la Raye", "Canaries", "Castries", "Choiseul", "Dennery", "Gros Islet",
        "Laborie", "Micoud", "Soufrière", "Vieux Fort",
    ],
    "Saint Vincent and the Grenadines": [
        "Charlotte", "Grenadines", "Saint Andrew", "Saint David", "Saint George",
        "Saint Patrick",
    ],
    "Samoa": [
        "A'ana", "Aiga-i-le-Tai", "Atua", "Fa'asaleleaga", "Gaga'emauga",
        "Gagaifomauga", "Palauli", "Satupa'itea", "Tuamasaga", "Va'a-o-Fonoti",
        "Vaisigano",
    ],
    "San Marino": [
        "Acquaviva", "Borgo Maggiore", "Chiesanuova", "Domagnano", "Faetano",
        "Fiorentino", "Montegiardino", "San Marino Città", "Serravalle",
    ],
    "Sao Tome and Principe": ["Príncipe", "São Tomé"],
    "Saudi Arabia": [
        "Al Bahah", "Al Jawf", "Al Madinah", "Al-Qassim", "Asir", "Eastern Province",
        "Hail", "Jazan", "Makkah", "Najran", "Northern Borders", "Riyadh", "Tabuk",
    ],
    "Senegal": [
        "Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack", "Kédougou", "Kolda",
        "Louga", "Matam", "Saint-Louis", "Sédhiou", "Tambacounda", "Thiès",
        "Ziguinchor",
    ],
    "Serbia": [
        "Belgrade", "Vojvodina", "Šumadija and Western Serbia",
        "Southern and Eastern Serbia",
    ],
    "Seychelles": [
        "Anse aux Pins", "Anse Boileau", "Anse Royale", "Baie Lazare", "Beau Vallon",
        "Cascade", "English River", "Glacis", "Grand Anse Mahé",
        "Grand Anse Praslin", "La Digue", "Mont Fleuri", "Plaisance", "Pointe La Rue",
        "Port Glaud", "Takamaka", "Victoria",
    ],
    "Sierra Leone": ["Eastern", "Northern", "North West", "Southern", "Western Area"],
    "Singapore": ["Central Singapore", "North East", "North West", "South East", "South West"],
    "Slovakia": [
        "Banská Bystrica", "Bratislava", "Košice", "Nitra", "Prešov", "Trenčín",
        "Trnava", "Žilina",
    ],
    "Slovenia": [
        "Central Slovenia", "Drava", "Carinthia", "Coastal-Karst", "Gorizia",
        "Lower Sava", "Mura", "Southeast Slovenia", "Savinja", "Central Sava",
        "Upper Carniola", "Littoral-Inner Carniola",
    ],
    "Solomon Islands": [
        "Central", "Choiseul", "Guadalcanal", "Honiara", "Isabel", "Makira-Ulawa",
        "Malaita", "Rennell and Bellona", "Temotu", "Western",
    ],
    "Somalia": [
        "Awdal", "Bakool", "Banaadir", "Bari", "Bay", "Galguduud", "Gedo", "Hiraan",
        "Lower Juba", "Lower Shabelle", "Middle Juba", "Middle Shabelle", "Mudug",
        "Nugal", "Sanaag", "Sool", "Togdheer", "Woqooyi Galbeed",
    ],
    "South Africa": [
        "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo",
        "Mpumalanga", "Northern Cape", "North West", "Western Cape",
    ],
    "South Korea": [
        "Seoul", "Busan", "Daegu", "Incheon", "Gwangju", "Daejeon", "Ulsan",
        "Sejong", "Gyeonggi", "Gangwon", "North Chungcheong", "South Chungcheong",
        "North Jeolla", "South Jeolla", "North Gyeongsang", "South Gyeongsang",
        "Jeju",
    ],
    "South Sudan": [
        "Central Equatoria", "Eastern Equatoria", "Jonglei", "Lakes",
        "Northern Bahr el Ghazal", "Unity", "Upper Nile", "Warrap",
        "Western Bahr el Ghazal", "Western Equatoria",
    ],
    "Spain": [
        "Andalusia", "Aragon", "Asturias", "Balearic Islands", "Basque Country",
        "Canary Islands", "Cantabria", "Castilla-La Mancha", "Castile and León",
        "Catalonia", "Extremadura", "Galicia", "La Rioja", "Madrid", "Murcia",
        "Navarre", "Valencia",
    ],
    "Sri Lanka": [
        "Central", "Eastern", "North Central", "Northern", "North Western",
        "Sabaragamuwa", "Southern", "Uva", "Western",
    ],
    "Sudan": [
        "Al Jazirah", "Blue Nile", "Central Darfur", "East Darfur", "Kassala",
        "Khartoum", "North Darfur", "North Kordofan", "Northern", "Red Sea",
        "River Nile", "Sennar", "South Darfur", "South Kordofan", "West Darfur",
        "West Kordofan", "White Nile", "Gedaref",
    ],
    "Suriname": [
        "Brokopondo", "Commewijne", "Coronie", "Marowijne", "Nickerie", "Para",
        "Paramaribo", "Saramacca", "Sipaliwini", "Wanica",
    ],
    "Sweden": [
        "Blekinge", "Dalarna", "Gävleborg", "Gotland", "Halland", "Jämtland",
        "Jönköping", "Kalmar", "Kronoberg", "Norrbotten", "Örebro", "Östergötland",
        "Skåne", "Södermanland", "Stockholm", "Uppsala", "Värmland",
        "Västerbotten", "Västernorrland", "Västmanland", "Västra Götaland",
    ],
    "Switzerland": [
        "Aargau", "Appenzell Ausserrhoden", "Appenzell Innerrhoden",
        "Basel-Landschaft", "Basel-Stadt", "Bern", "Fribourg", "Geneva", "Glarus",
        "Graubünden", "Jura", "Lucerne", "Neuchâtel", "Nidwalden", "Obwalden",
        "Schaffhausen", "Schwyz", "Solothurn", "St. Gallen", "Thurgau", "Ticino",
        "Uri", "Valais", "Vaud", "Zug", "Zurich",
    ],
    "Syria": [
        "Al-Hasakah", "Aleppo", "Al-Raqqah", "Damascus", "Daraa", "Deir ez-Zor",
        "Hama", "Homs", "Idlib", "Latakia", "Quneitra", "Rif Dimashq", "As-Suwayda",
        "Tartus",
    ],
    "Taiwan": [
        "Changhua", "Chiayi City", "Chiayi County", "Hsinchu City", "Hsinchu County",
        "Hualien", "Kaohsiung", "Keelung", "Kinmen", "Lienchiang", "Miaoli",
        "Nantou", "New Taipei", "Penghu", "Pingtung", "Taichung", "Tainan",
        "Taipei", "Taitung", "Taoyuan", "Yilan", "Yunlin",
    ],
    "Tajikistan": [
        "Districts of Republican Subordination", "Gorno-Badakhshan", "Khatlon",
        "Sughd", "Dushanbe",
    ],
    "Tanzania": [
        "Arusha", "Dar es Salaam", "Dodoma", "Geita", "Iringa", "Kagera", "Katavi",
        "Kigoma", "Kilimanjaro", "Lindi", "Manyara", "Mara", "Mbeya",
        "Mjini Magharibi", "Morogoro", "Mtwara", "Mwanza", "Njombe", "Pemba North",
        "Pemba South", "Pwani", "Rukwa", "Ruvuma", "Shinyanga", "Simiyu",
        "Singida", "Tabora", "Tanga", "Unguja North", "Unguja South", "Songwe",
    ],
    "Thailand": [
        "Central Thailand", "Eastern Thailand", "Northern Thailand",
        "Northeastern Thailand", "Southern Thailand", "Western Thailand",
    ],
    "Timor-Leste": [
        "Aileu", "Ainaro", "Baucau", "Bobonaro", "Covalima", "Dili", "Ermera",
        "Lautém", "Liquiçá", "Manatuto", "Manufahi", "Oecusse", "Viqueque",
    ],
    "Togo": ["Centrale", "Kara", "Maritime", "Plateaux", "Savanes"],
    "Tonga": ["'Eua", "Ha'apai", "Niuas", "Tongatapu", "Vava'u"],
    "Trinidad and Tobago": [
        "Couva-Tabaquite-Talparo", "Diego Martin", "Mayaro-Rio Claro",
        "Penal-Debe", "Princes Town", "San Juan-Laventille", "Sangre Grande",
        "Siparia", "Tunapuna-Piarco", "Port of Spain", "San Fernando", "Arima",
        "Point Fortin", "Chaguanas", "Tobago",
    ],
    "Tunisia": [
        "Ariana", "Béja", "Ben Arous", "Bizerte", "Gabès", "Gafsa", "Jendouba",
        "Kairouan", "Kasserine", "Kébili", "Kef", "Mahdia", "Manouba", "Médenine",
        "Monastir", "Nabeul", "Sfax", "Sidi Bouzid", "Siliana", "Sousse",
        "Tataouine", "Tozeur", "Tunis", "Zaghouan",
    ],
    "Turkey": [
        "Marmara", "Aegean", "Mediterranean", "Central Anatolia", "Black Sea",
        "Eastern Anatolia", "Southeastern Anatolia",
    ],
    "Turkmenistan": ["Ahal", "Balkan", "Dashoguz", "Lebap", "Mary", "Ashgabat"],
    "Tuvalu": [
        "Funafuti", "Nanumea", "Nanumaga", "Niutao", "Nui", "Nukufetau",
        "Nukulaelae", "Vaitupu",
    ],
    "Uganda": ["Central", "Eastern", "Northern", "Western"],
    "Ukraine": [
        "Cherkasy", "Chernihiv", "Chernivtsi", "Dnipropetrovsk", "Donetsk",
        "Ivano-Frankivsk", "Kharkiv", "Kherson", "Khmelnytskyi", "Kirovohrad",
        "Kyiv Oblast", "Kyiv City", "Luhansk", "Lviv", "Mykolaiv", "Odesa",
        "Poltava", "Rivne", "Sumy", "Ternopil", "Vinnytsia", "Volyn",
        "Zakarpattia", "Zaporizhzhia", "Zhytomyr", "Crimea",
    ],
    "United Arab Emirates": [
        "Abu Dhabi", "Ajman", "Dubai", "Fujairah", "Ras Al Khaimah", "Sharjah",
        "Umm Al Quwain",
    ],
    "United Kingdom": ["England", "Northern Ireland", "Scotland", "Wales"],
    "United States": [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
        "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
        "Washington", "West Virginia", "Wisconsin", "Wyoming",
        "District of Columbia",
    ],
    "Uruguay": [
        "Artigas", "Canelones", "Cerro Largo", "Colonia", "Durazno", "Flores",
        "Florida", "Lavalleja", "Maldonado", "Montevideo", "Paysandú", "Río Negro",
        "Rivera", "Rocha", "Salto", "San José", "Soriano", "Tacuarembó",
        "Treinta y Tres",
    ],
    "Uzbekistan": [
        "Andijan", "Bukhara", "Fergana", "Jizzakh", "Karakalpakstan", "Namangan",
        "Navoiy", "Qashqadaryo", "Samarqand", "Sirdaryo", "Surxondaryo",
        "Tashkent Region", "Tashkent City", "Xorazm",
    ],
    "Vanuatu": ["Malampa", "Penama", "Sanma", "Shefa", "Tafea", "Torba"],
    "Vatican City": [],
    "Venezuela": [
        "Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", "Bolívar",
        "Carabobo", "Cojedes", "Delta Amacuro", "Falcón", "Guárico", "Lara",
        "Mérida", "Miranda", "Monagas", "Nueva Esparta", "Portuguesa", "Sucre",
        "Táchira", "Trujillo", "Vargas", "Yaracuy", "Zulia", "Distrito Capital",
    ],
    "Vietnam": [
        "Red River Delta", "Northeast", "Northwest", "North Central Coast",
        "South Central Coast", "Central Highlands", "Southeast", "Mekong Delta",
    ],
    "Western Sahara": [],
    "Yemen": [
        "Abyan", "Aden", "Al Bayda", "Al Dhale'e", "Al Hudaydah", "Al Jawf",
        "Al Mahrah", "Al Mahwit", "Amanat Al Asimah", "Amran", "Dhamar",
        "Hadhramaut", "Hajjah", "Ibb", "Lahij", "Marib", "Raymah", "Saada",
        "Sana'a", "Shabwah", "Taiz",
    ],
    "Zambia": [
        "Central", "Copperbelt", "Eastern", "Luapula", "Lusaka", "Muchinga",
        "Northern", "North-Western", "Southern", "Western",
    ],
    "Zimbabwe": [
        "Bulawayo", "Harare", "Manicaland", "Mashonaland Central",
        "Mashonaland East", "Mashonaland West", "Masvingo", "Matabeleland North",
        "Matabeleland South", "Midlands",
    ],
}
