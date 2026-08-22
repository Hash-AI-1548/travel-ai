from fastapi import APIRouter
from app.schemas.options import OptionsMetadataResponse, OptionItem, CurrencyOption

router = APIRouter(prefix="/options", tags=["Metadata & UI Options"])

# Comprehensive global currency database (160+ world currencies with ISO codes and USD baseline conversion rates)
GLOBAL_CURRENCIES = [
    CurrencyOption(code="INR", name="Indian Rupee", symbol="₹", usd_rate=0.0119),
    CurrencyOption(code="USD", name="US Dollar", symbol="$", usd_rate=1.0),
    CurrencyOption(code="EUR", name="Euro", symbol="€", usd_rate=1.087),
    CurrencyOption(code="GBP", name="British Pound", symbol="£", usd_rate=1.266),
    CurrencyOption(code="AED", name="UAE Dirham", symbol="د.إ", usd_rate=0.272),
    CurrencyOption(code="CAD", name="Canadian Dollar", symbol="C$", usd_rate=0.735),
    CurrencyOption(code="AUD", name="Australian Dollar", symbol="A$", usd_rate=0.658),
    CurrencyOption(code="SGD", name="Singapore Dollar", symbol="S$", usd_rate=0.746),
    CurrencyOption(code="JPY", name="Japanese Yen", symbol="¥", usd_rate=0.00658),
    CurrencyOption(code="SAR", name="Saudi Riyal", symbol="﷼", usd_rate=0.267),
    CurrencyOption(code="QAR", name="Qatari Riyal", symbol="QR", usd_rate=0.275),
    CurrencyOption(code="KWD", name="Kuwaiti Dinar", symbol="KD", usd_rate=3.26),
    CurrencyOption(code="BHD", name="Bahraini Dinar", symbol="BD", usd_rate=2.65),
    CurrencyOption(code="OMR", name="Omani Rial", symbol="OMR", usd_rate=2.60),
    CurrencyOption(code="CHF", name="Swiss Franc", symbol="Fr", usd_rate=1.136),
    CurrencyOption(code="CNY", name="Chinese Yuan", symbol="¥", usd_rate=0.138),
    CurrencyOption(code="HKD", name="Hong Kong Dollar", symbol="HK$", usd_rate=0.128),
    CurrencyOption(code="NZD", name="New Zealand Dollar", symbol="NZ$", usd_rate=0.612),
    CurrencyOption(code="THB", name="Thai Baht", symbol="฿", usd_rate=0.0274),
    CurrencyOption(code="MYR", name="Malaysian Ringgit", symbol="RM", usd_rate=0.213),
    CurrencyOption(code="IDR", name="Indonesian Rupiah", symbol="Rp", usd_rate=0.0000625),
    CurrencyOption(code="PHP", name="Philippine Peso", symbol="₱", usd_rate=0.0175),
    CurrencyOption(code="VND", name="Vietnamese Dong", symbol="₫", usd_rate=0.000039),
    CurrencyOption(code="KRW", name="South Korean Won", symbol="₩", usd_rate=0.000725),
    CurrencyOption(code="TWD", name="New Taiwan Dollar", symbol="NT$", usd_rate=0.031),
    CurrencyOption(code="PKR", name="Pakistani Rupee", symbol="₨", usd_rate=0.0036),
    CurrencyOption(code="BDT", name="Bangladeshi Taka", symbol="৳", usd_rate=0.0085),
    CurrencyOption(code="LKR", name="Sri Lankan Rupee", symbol="Rs", usd_rate=0.0033),
    CurrencyOption(code="NPR", name="Nepalese Rupee", symbol="Rs", usd_rate=0.0075),
    CurrencyOption(code="AFN", name="Afghan Afghani", symbol="؋", usd_rate=0.014),
    CurrencyOption(code="ALL", name="Albanian Lek", symbol="Lek", usd_rate=0.011),
    CurrencyOption(code="AMD", name="Armenian Dram", symbol="֏", usd_rate=0.0026),
    CurrencyOption(code="ANG", name="Netherlands Antillean Guilder", symbol="ƒ", usd_rate=0.556),
    CurrencyOption(code="AOA", name="Angolan Kwanza", symbol="Kz", usd_rate=0.0011),
    CurrencyOption(code="ARS", name="Argentine Peso", symbol="$", usd_rate=0.0011),
    CurrencyOption(code="AWG", name="Aruban Florin", symbol="ƒ", usd_rate=0.556),
    CurrencyOption(code="AZN", name="Azerbaijani Manat", symbol="₼", usd_rate=0.588),
    CurrencyOption(code="BAM", name="Bosnia-Herzegovina Mark", symbol="KM", usd_rate=0.555),
    CurrencyOption(code="BBD", name="Barbadian Dollar", symbol="Bds$", usd_rate=0.50),
    CurrencyOption(code="BGN", name="Bulgarian Lev", symbol="лв", usd_rate=0.555),
    CurrencyOption(code="BIF", name="Burundian Franc", symbol="FBu", usd_rate=0.00035),
    CurrencyOption(code="BMD", name="Bermudian Dollar", symbol="$", usd_rate=1.0),
    CurrencyOption(code="BND", name="Brunei Dollar", symbol="B$", usd_rate=0.746),
    CurrencyOption(code="BOB", name="Bolivian Boliviano", symbol="Bs.", usd_rate=0.145),
    CurrencyOption(code="BRL", name="Brazilian Real", symbol="R$", usd_rate=0.183),
    CurrencyOption(code="BSD", name="Bahamian Dollar", symbol="B$", usd_rate=1.0),
    CurrencyOption(code="BTN", name="Bhutanese Ngultrum", symbol="Nu.", usd_rate=0.0119),
    CurrencyOption(code="BWP", name="Botswanan Pula", symbol="P", usd_rate=0.074),
    CurrencyOption(code="BYN", name="Belarusian Ruble", symbol="Br", usd_rate=0.305),
    CurrencyOption(code="BZD", name="Belize Dollar", symbol="BZ$", usd_rate=0.50),
    CurrencyOption(code="CDF", name="Congolese Franc", symbol="FC", usd_rate=0.00036),
    CurrencyOption(code="CLP", name="Chilean Peso", symbol="$", usd_rate=0.00108),
    CurrencyOption(code="COP", name="Colombian Peso", symbol="$", usd_rate=0.00025),
    CurrencyOption(code="CRC", name="Costa Rican Colón", symbol="₡", usd_rate=0.0019),
    CurrencyOption(code="CUP", name="Cuban Peso", symbol="₱", usd_rate=0.042),
    CurrencyOption(code="CVE", name="Cape Verdean Escudo", symbol="Esc", usd_rate=0.0098),
    CurrencyOption(code="CZK", name="Czech Koruna", symbol="Kč", usd_rate=0.043),
    CurrencyOption(code="DJF", name="Djiboutian Franc", symbol="Fdj", usd_rate=0.0056),
    CurrencyOption(code="DKK", name="Danish Krone", symbol="kr", usd_rate=0.145),
    CurrencyOption(code="DOP", name="Dominican Peso", symbol="RD$", usd_rate=0.017),
    CurrencyOption(code="DZD", name="Algerian Dinar", symbol="DA", usd_rate=0.0074),
    CurrencyOption(code="EGP", name="Egyptian Pound", symbol="E£", usd_rate=0.021),
    CurrencyOption(code="ERN", name="Eritrean Nakfa", symbol="Nkf", usd_rate=0.067),
    CurrencyOption(code="ETB", name="Ethiopian Birr", symbol="Br", usd_rate=0.0084),
    CurrencyOption(code="FJD", name="Fijian Dollar", symbol="FJ$", usd_rate=0.445),
    CurrencyOption(code="FKP", name="Falkland Islands Pound", symbol="£", usd_rate=1.266),
    CurrencyOption(code="GEL", name="Georgian Lari", symbol="₾", usd_rate=0.37),
    CurrencyOption(code="GHS", name="Ghanaian Cedi", symbol="GH₵", usd_rate=0.065),
    CurrencyOption(code="GIP", name="Gibraltar Pound", symbol="£", usd_rate=1.266),
    CurrencyOption(code="GMD", name="Gambian Dalasi", symbol="D", usd_rate=0.014),
    CurrencyOption(code="GNF", name="Guinean Franc", symbol="FG", usd_rate=0.00012),
    CurrencyOption(code="GTQ", name="Guatemalan Quetzal", symbol="Q", usd_rate=0.129),
    CurrencyOption(code="GYD", name="Guyanaese Dollar", symbol="G$", usd_rate=0.0048),
    CurrencyOption(code="HNL", name="Honduran Lempira", symbol="L", usd_rate=0.040),
    CurrencyOption(code="HRK", name="Croatian Kuna", symbol="kn", usd_rate=0.144),
    CurrencyOption(code="HTG", name="Haitian Gourde", symbol="G", usd_rate=0.0076),
    CurrencyOption(code="HUF", name="Hungarian Forint", symbol="Ft", usd_rate=0.0028),
    CurrencyOption(code="ILS", name="Israeli New Shekel", symbol="₪", usd_rate=0.272),
    CurrencyOption(code="IQD", name="Iraqi Dinar", symbol="ID", usd_rate=0.00076),
    CurrencyOption(code="IRR", name="Iranian Rial", symbol="﷼", usd_rate=0.000024),
    CurrencyOption(code="ISK", name="Icelandic Króna", symbol="kr", usd_rate=0.0073),
    CurrencyOption(code="JMD", name="Jamaican Dollar", symbol="J$", usd_rate=0.0064),
    CurrencyOption(code="JOD", name="Jordanian Dinar", symbol="JD", usd_rate=1.41),
    CurrencyOption(code="KES", name="Kenyan Shilling", symbol="KSh", usd_rate=0.0077),
    CurrencyOption(code="KGS", name="Kyrgystani Som", symbol="с", usd_rate=0.0116),
    CurrencyOption(code="KHR", name="Cambodian Riel", symbol="៛", usd_rate=0.00024),
    CurrencyOption(code="KMF", name="Comorian Franc", symbol="CF", usd_rate=0.0022),
    CurrencyOption(code="KYD", name="Cayman Islands Dollar", symbol="CI$", usd_rate=1.20),
    CurrencyOption(code="KZT", name="Kazakhstani Tenge", symbol="₸", usd_rate=0.0021),
    CurrencyOption(code="LAK", name="Laotian Kip", symbol="₭", usd_rate=0.000046),
    CurrencyOption(code="LBP", name="Lebanese Pound", symbol="L£", usd_rate=0.000011),
    CurrencyOption(code="LRD", name="Liberian Dollar", symbol="L$", usd_rate=0.0051),
    CurrencyOption(code="LSL", name="Lesotho Loti", symbol="L", usd_rate=0.054),
    CurrencyOption(code="LYD", name="Libyan Dinar", symbol="LD", usd_rate=0.207),
    CurrencyOption(code="MAD", name="Moroccan Dirham", symbol="MAD", usd_rate=0.10),
    CurrencyOption(code="MDL", name="Moldovan Leu", symbol="L", usd_rate=0.056),
    CurrencyOption(code="MGA", name="Malagasy Ariary", symbol="Ar", usd_rate=0.00022),
    CurrencyOption(code="MKD", name="Macedonian Denar", symbol="ден", usd_rate=0.0176),
    CurrencyOption(code="MMK", name="Myanmar Kyat", symbol="K", usd_rate=0.00048),
    CurrencyOption(code="MNT", name="Mongolian Tugrik", symbol="₮", usd_rate=0.00029),
    CurrencyOption(code="MOP", name="Macanese Pataca", symbol="MOP$", usd_rate=0.124),
    CurrencyOption(code="MRU", name="Mauritanian Ouguiya", symbol="UM", usd_rate=0.025),
    CurrencyOption(code="MUR", name="Mauritian Rupee", symbol="₨", usd_rate=0.0215),
    CurrencyOption(code="MVR", name="Maldivian Rufiyaa", symbol="Rf", usd_rate=0.065),
    CurrencyOption(code="MWK", name="Malawian Kwacha", symbol="MK", usd_rate=0.00057),
    CurrencyOption(code="MXN", name="Mexican Peso", symbol="Mex$", usd_rate=0.0549),
    CurrencyOption(code="MZN", name="Mozambican Metical", symbol="MT", usd_rate=0.0156),
    CurrencyOption(code="NAD", name="Namibian Dollar", symbol="N$", usd_rate=0.054),
    CurrencyOption(code="NGN", name="Nigerian Naira", symbol="₦", usd_rate=0.00063),
    CurrencyOption(code="NIO", name="Nicaraguan Córdoba", symbol="C$", usd_rate=0.027),
    CurrencyOption(code="NOK", name="Norwegian Krone", symbol="kr", usd_rate=0.094),
    CurrencyOption(code="PAB", name="Panamanian Balboa", symbol="B/.", usd_rate=1.0),
    CurrencyOption(code="PEN", name="Peruvian Sol", symbol="S/.", usd_rate=0.268),
    CurrencyOption(code="PGK", name="Papua New Guinean Kina", symbol="K", usd_rate=0.255),
    CurrencyOption(code="PLN", name="Polish Zloty", symbol="zł", usd_rate=0.252),
    CurrencyOption(code="PYG", name="Paraguayan Guarani", symbol="₲", usd_rate=0.00013),
    CurrencyOption(code="RON", name="Romanian Leu", symbol="lei", usd_rate=0.218),
    CurrencyOption(code="RSD", name="Serbian Dinar", symbol="дин.", usd_rate=0.0093),
    CurrencyOption(code="RUB", name="Russian Ruble", symbol="₽", usd_rate=0.011),
    CurrencyOption(code="RWF", name="Rwandan Franc", symbol="FRw", usd_rate=0.00075),
    CurrencyOption(code="SBD", name="Solomon Islands Dollar", symbol="SI$", usd_rate=0.118),
    CurrencyOption(code="SCR", name="Seychellois Rupee", symbol="SR", usd_rate=0.073),
    CurrencyOption(code="SDG", name="Sudanese Pound", symbol="SDG", usd_rate=0.0017),
    CurrencyOption(code="SEK", name="Swedish Krona", symbol="kr", usd_rate=0.096),
    CurrencyOption(code="SOS", name="Somali Shilling", symbol="Sh.So.", usd_rate=0.00175),
    CurrencyOption(code="SRD", name="Surinamese Dollar", symbol="Sr$", usd_rate=0.028),
    CurrencyOption(code="SYP", name="Syrian Pound", symbol="LS", usd_rate=0.000077),
    CurrencyOption(code="SZL", name="Swazi Lilangeni", symbol="L", usd_rate=0.054),
    CurrencyOption(code="TJS", name="Tajikistani Somoni", symbol="SM", usd_rate=0.092),
    CurrencyOption(code="TMT", name="Turkmenistani Manat", symbol="T", usd_rate=0.286),
    CurrencyOption(code="TND", name="Tunisian Dinar", symbol="DT", usd_rate=0.32),
    CurrencyOption(code="TOP", name="Tongan Paʻanga", symbol="T$", usd_rate=0.42),
    CurrencyOption(code="TRY", name="Turkish Lira", symbol="₺", usd_rate=0.029),
    CurrencyOption(code="TTD", name="Trinidad & Tobago Dollar", symbol="TT$", usd_rate=0.147),
    CurrencyOption(code="TZS", name="Tanzanian Shilling", symbol="TSh", usd_rate=0.00038),
    CurrencyOption(code="UAH", name="Ukrainian Hryvnia", symbol="₴", usd_rate=0.024),
    CurrencyOption(code="UGX", name="Ugandan Shilling", symbol="USh", usd_rate=0.00027),
    CurrencyOption(code="UYU", name="Uruguayan Peso", symbol="$U", usd_rate=0.025),
    CurrencyOption(code="UZS", name="Uzbekistani Som", symbol="so'm", usd_rate=0.000079),
    CurrencyOption(code="VES", name="Venezuelan Bolívar", symbol="Bs.S", usd_rate=0.027),
    CurrencyOption(code="VUV", name="Vanuatu Vatu", symbol="VT", usd_rate=0.0083),
    CurrencyOption(code="WST", name="Samoan Tala", symbol="WS$", usd_rate=0.365),
    CurrencyOption(code="XAF", name="Central African CFA Franc", symbol="FCFA", usd_rate=0.00165),
    CurrencyOption(code="XCD", name="East Caribbean Dollar", symbol="EC$", usd_rate=0.370),
    CurrencyOption(code="XOF", name="West African CFA Franc", symbol="CFA", usd_rate=0.00165),
    CurrencyOption(code="XPF", name="CFP Franc", symbol="₣", usd_rate=0.0091),
    CurrencyOption(code="YER", name="Yemeni Rial", symbol="YR", usd_rate=0.0040),
    CurrencyOption(code="ZAR", name="South African Rand", symbol="R", usd_rate=0.054),
    CurrencyOption(code="ZMW", name="Zambian Kwacha", symbol="ZK", usd_rate=0.038)
]

@router.get("", response_model=OptionsMetadataResponse)
def get_options_metadata():
    """Returns all available metadata options for the 8-step onboarding UI."""
    return OptionsMetadataResponse(
        traveler_types=[
            OptionItem(
                id="solo",
                title="Solo",
                description="Autonomous self-guided paths, flexible schedules, single rooms.",
                icon="user"
            ),
            OptionItem(
                id="couple",
                title="Couple",
                description="Romantic stays, fine dining, intimate private tour routes.",
                icon="users"
            ),
            OptionItem(
                id="family",
                title="Family",
                description="Kid-friendly attractions, multi-room suites, gentle transit pace.",
                icon="home"
            ),
            OptionItem(
                id="friends",
                title="Friends",
                description="Group activities, high-energy spots, shared budgets, double beds.",
                icon="smile"
            ),
            OptionItem(
                id="senior",
                title="Senior Traveler",
                description="Comfortable transit, accessible walks, deep cultural pacing.",
                icon="compass"
            )
        ],
        accessibility_options=[
            OptionItem(
                id="accessibility_mobility",
                title="Mobility / Wheelchair Access",
                description="No stairs, step-free entries, extra wide doorways, roll-in showers."
            ),
            OptionItem(
                id="accessibility_visual",
                title="Visual Assistance friendly",
                description="High-contrast markings, braille signs, audio guides, guide-dog friendly stays."
            ),
            OptionItem(
                id="accessibility_hearing",
                title="Hearing / Audio support",
                description="Visual fire alarms, captioned assistance devices, vibration indicators."
            ),
            OptionItem(
                id="accessibility_senior",
                title="Elderly & Senior friendly",
                description="Sturdy handrails, minimal walking distances, elevators highlighted."
            ),
            OptionItem(
                id="accessibility_child",
                title="Child-friendly (Toddlers/Infants)",
                description="Crib options, high chairs, safety gates available, stroller ramps."
            ),
            OptionItem(
                id="accessibility_none",
                title="None / Not applicable",
                description="No specific mobility or visual accommodations required."
            )
        ],
        travel_styles=[
            OptionItem(id="adventure", title="Adventure", icon="zap"),
            OptionItem(id="nature", title="Nature", icon="trees"),
            OptionItem(id="culture", title="Culture", icon="award"),
            OptionItem(id="history", title="History", icon="book-open"),
            OptionItem(id="food", title="Food", icon="coffee"),
            OptionItem(id="wine", title="Wine", icon="glass"),
            OptionItem(id="shopping", title="Shopping", icon="tag"),
            OptionItem(id="relaxation", title="Relaxation", icon="wind"),
            OptionItem(id="spiritual", title="Spiritual", icon="sun"),
            OptionItem(id="photography", title="Photography", icon="camera")
        ],
        dietary_standards=[
            OptionItem(
                id="vegetarian",
                title="Vegetarian",
                description="No meat, poultry, or fish."
            ),
            OptionItem(
                id="non_vegetarian",
                title="Non-vegetarian",
                description="Includes poultry, red meat, seafood."
            ),
            OptionItem(
                id="vegan",
                title="Vegan",
                description="Entirely plant-based culinary tracks."
            ),
            OptionItem(
                id="halal",
                title="Halal",
                description="Strictly Halal-certified dining recommendations."
            ),
            OptionItem(
                id="jain",
                title="Jain",
                description="No meat, root vegetables, or garlic/onions."
            ),
            OptionItem(
                id="other_custom",
                title="Other / Custom",
                description="Specify custom dietary guidelines below."
            )
        ],
        clothing_pack_styles=[
            "Western", "Traditional", "Casual", "Winter", "Summer", "Formals", "Other"
        ],
        clothing_toggles=[
            OptionItem(
                id="modest_clothing",
                title="Modest clothing filters",
                description="Flag temple and local custom friendly outfits covering shoulders & knees."
            ),
            OptionItem(
                id="prioritize_hot_weather",
                title="Prioritize hot weather comfort",
                description="Suggest light fabrics, breathable synthetics, and sun protection."
            )
        ],
        budget_tiers=[
            OptionItem(
                id="budget",
                title="Budget / Low Range",
                symbol="₹",
                description="₹1,500 – ₹3,500 / day per person ($18 – $42 USD). Economical & smart. Clean hostels / guesthouses, local metro & bus transit, authentic street food, and free walking tours."
            ),
            OptionItem(
                id="moderate",
                title="Moderate / Mid Range",
                symbol="₹₹",
                description="₹4,000 – ₹8,500 / day per person ($48 – $102 USD). Balanced comfort. 3-star/4-star boutique stays, private rideshares, popular local cafes & dining, and curated entry tours."
            ),
            OptionItem(
                id="premium_luxury",
                title="Premium / Luxury Range",
                symbol="₹₹₹",
                description="₹10,000 – ₹25,000+ / day per person ($120 – $300+ USD). Indulgent travel. 5-star luxury resorts, private chauffeurs/cabs, gourmet fine dining, and VIP skip-the-line access."
            ),
            OptionItem(
                id="flexible",
                title="Flexible Range",
                symbol="₹ – ₹₹₹",
                description="₹3,000 – ₹15,000 / day per person ($36 – $180 USD). Dynamic mix. Smart balance between boutique stays and premium dining or luxury experiences."
            )
        ],
        languages=[
            "English", "Spanish", "French", "German", "Mandarin Chinese", "Cantonese",
            "Japanese", "Hindi", "Arabic", "Portuguese", "Russian", "Bengali", "Italian",
            "Korean", "Turkish", "Vietnamese", "Polish", "Dutch", "Swedish", "Greek",
            "Thai", "Indonesian", "Malay", "Persian / Farsi", "Hebrew", "Tagalog / Filipino",
            "Swahili", "Punjabi", "Telugu", "Tamil", "Marathi", "Urdu", "Gujarati",
            "Kannada", "Malayalam", "Ukrainian", "Romanian", "Czech", "Hungarian",
            "Danish", "Finnish", "Norwegian", "Irish", "Croatian", "Serbian", "Slovak",
            "Bulgarian", "Lithuanian", "Latvian", "Estonian", "Icelandic", "Basque",
            "Catalan", "Galician", "Welsh", "Scottish Gaelic", "Yoruba", "Igbo",
            "Hausa", "Zulu", "Xhosa", "Amharic", "Somali", "Nepali", "Sinhala",
            "Burmese", "Khmer", "Lao", "Mongolian", "Georgian", "Armenian", "Azerbaijani",
            "Kazakh", "Uzbek", "Esperanto", "Latin", "Afrikaans", "Albanian", "Bosnian",
            "Macedonian", "Slovenian", "Maltese", "Tibetan", "Yiddish"
        ],
        nationalities=[
            "Indian", "American", "Canadian", "British", "Australian", "French", "German",
            "Japanese", "Spanish", "Italian", "Brazilian", "Chinese", "Mexican", "Dutch",
            "Swedish", "Swiss", "Irish", "New Zealander", "South African", "Singaporean",
            "South Korean", "Argentine", "Colombian", "Egyptian", "Emirati", "Greek",
            "Indonesian", "Israeli", "Malaysian", "Nigerian", "Norwegian", "Pakistani",
            "Philippine / Filipino", "Polish", "Portuguese", "Saudi", "Thai", "Turkish",
            "Ukrainian", "Vietnamese", "Other"
        ],
        currencies=GLOBAL_CURRENCIES
    )
