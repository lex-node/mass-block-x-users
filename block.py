from typing import Dict, Iterable
from io import StringIO

import requests


# List of SOL shill usernames provided by the user
SOL_SHILLS = [
    "@0xSweep",
    "@0xzZyat",
    "@38v4So5Kt",
    "@9trew",
    "@_thespac",
    "@abawebs",
    "@abgwebs",
    "@abrarthec",
    "@adameshelton",
    "@Advyth",
    "@aenuinedegen",
    "@ahostassassinn",
    "@aisercore",
    "@aleexsix",
    "@aleywebs",
    "@aleywors",
    "@ApeMP5",
    "@apemps",
    "@arcane_c",
    "@Arcane_Crypto_",
    "@astawebs",
    "@astro_nu",
    "@Atitty",
    "@atitty_",
    "@atsarcore",
    "@azgloban",
    "@bagcalls",
    "@bazza_aped",
    "@bazza_ay",
    "@bitcoinza",
    "@Biteoinzac",
    "@Block100x",
    "@bloodweb3",
    "@bloodwet",
    "@bon",
    "@bon_g",
    "@brommm",
    "@brommmyy",
    "@Bronsixbt",
    "@Brookcalls",
    "@broskisol",
    "@bruca",
    "@bryanros",
    "@bryanrosswins",
    "@busraeth",
    "@bysukie",
    "@c_potens",
    "@Capitalist",
    "@capitalistog",
    "@Cardcabz",
    "@cardcabz",
    "@cometealls",
    "@cottonxbt",
    "@cryplobul",
    "@Crypto_ED7",
    "@CryptoAnalio",
    "@cryptoazyra",
    "@CryptoBaldwinlY",
    "@cryptobul",
    "@cryptobullying",
    "@cryptoext",
    "@CryptoLady_M",
    "@cryptostorm",
    "@cryptowifeyx",
    "@Daokwon",
    "@DaoKwonDo",
    "@darky1k",
    "@Darky1k",
    "@de_rugger",
    "@dea_ape",
    "@deaenbrody",
    "@Decentralpapi",
    "@degencru",
    "@degencruise",
    "@dehkunle",
    "@deviled_megas",
    "@DMTLAND",
    "@DotComParker",
    "@drallio",
    "@dyorwami",
    "@eddyXBT",
    "@eih_danx",
    "@elhousesol",
    "@enpt0iace",
    "@eottonxbt",
    "@erypto_a",
    "@erypto_e",
    "@eryptolad",
    "@eryptopizzaairl",
    "@eryptopo",
    "@eryptosto",
    "@etrckk_c",
    "@evancrypt",
    "@EzMoneyGems",
    "@farmercis",
    "@ferreweb3",
    "@FezWeb3",
    "@Flowslike",
    "@flowslikeosmo",
    "@fuelkek",
    "@fwtyo",
    "@GemsScope",
    "@gG1PeMtQQY9E",
    "@ghostess",
    "@Goboovi",
    "@goodness",
    "@GoodnessDeFi",
    "@GryptoTony",
    "@HairHustler",
    "@HairHustler128_",
    "@hellernen",
    "@henrys0x",
    "@herrocryp",
    "@herrocrypto",
    "@hezr",
    "@HiswatDofa",
    "@hiswatdot",
    "@hubaity",
    "@iamehuc",
    "@iamiekingston",
    "@illlyvivvi",
    "@iockweos",
    "@ireryptex",
    "@its_braz",
    "@itsthurstxn",
    "@ix_wilson",
    "@jeremyyb",
    "@Jeremyybte",
    "@jetxbt",
    "@katherine",
    "@kokid951",
    "@krypto_hy",
    "@kryptohun",
    "@kuzoeth",
    "@lamehucky",
    "@leffnta",
    "@lefinta",
    "@leochaind",
    "@leochaint",
    "@leowebs",
    "@leowers_",
    "@Lin_DAO",
    "@lin_dao_",
    "@littlemust",
    "@lockedinlucas",
    "@lockedint",
    "@lockweb3",
    "@lowkeyric",
    "@lowkeyrich",
    "@luaweb3",
    "@luno_solt",
    "@lynkOx",
    "@lynkox",
    "@macee",
    "@marcellox1",
    "@marcex",
    "@matrixon",
    "@mattinwe",
    "@MattinWeb3",
    "@Mduz_NET",
    "@mduz_nt",
    "@mediagir",
    "@MediaGiraffes",
    "@mistooor",
    "@mobyme",
    "@MobyMedia",
    "@monstera",
    "@MonyWeb3",
    "@mooonda",
    "@mooondat",
    "@mortywet",
    "@mostangr",
    "@mowiweb3",
    "@mowkive",
    "@nbweb3",
    "@nbwebs",
    "@nfipriest_",
    "@nftoriest_1",
    "@noahhealls",
    "@notdecu",
    "@notEezzy",
    "@oa_tery0",
    "@obeyauyy",
    "@obeyguyy",
    "@odicrypt",
    "@oexghost",
    "@officialsky",
    "@officialskywee1",
    "@offshoda",
    "@oGTerryox",
    "@ohouses",
    "@ola_crrypt",
    "@Ony3oku",
    "@oryploda",
    "@oryptoton",
    "@OxSweep",
    "@Oxxhost",
    "@OxZyaf",
    "@oyptojac",
    "@parcifap_defi",
    "@Parsa_Nfit",
    "@praxmedia",
    "@president",
    "@princeracks",
    "@purpurrp",
    "@queencry",
    "@raintures",
    "@realpablo",
    "@realpabloheman",
    "@Regrets10x",
    "@regrets1C",
    "@rentowth",
    "@renzosalp",
    "@renzosalpha",
    "@Rizzyic",
    "@Roarweb3",
    "@roarwebs",
    "@romejayx",
    "@rozer100x",
    "@rozert00",
    "@rP9k3k",
    "@rutradebt",
    "@rutradebtc",
    "@rypto",
    "@rypto_",
    "@s0B00",
    "@satoshiov",
    "@Satoshiowl",
    "@selor",
    "@seph_jim",
    "@sephjim",
    "@SexyMichill",
    "@shmoonft",
    "@ShmooNt",
    "@sibeleth",
    "@soapweb",
    "@soapweb3",
    "@SOLFistc",
    "@SOLFisTooShort_",
    "@solidtrad",
    "@solidtradesz",
    "@sorambil",
    "@spond",
    "@steezehur",
    "@stevenas",
    "@stevenascher",
    "@Strew",
    "@tedadycley",
    "@TeddyCleps",
    "@tedpillow",
    "@TedPillows",
    "@TheDefia",
    "@TheDefiApe",
    "@tnzz",
    "@tomgenzx",
    "@trapjuices",
    "@trapjuicesol",
    "@trentownt",
    "@tunmi_f",
    "@tunmi_t",
    "@tvbzify",
    "@uallstreet",
    "@ubzity",
    "@uxdubem",
    "@vainyz",
    "@vasta",
    "@vee",
    "@vikinaxbt",
    "@wasted0x",
    "@web3ma",
    "@Web3Maxx",
    "@web3righteous",
    "@webowan",
    "@webwarior",
    "@WisdomMatic",
    "@wisdomn",
    "@wtfisdave",
    "@wtfisdavee",
    "@xelf_sol",
    "@xiacalls",
    "@xxldubem",
    "@zacknfa",
    "@zacknia",
    "@zeusrebir",
    "@ZeusRebirth",
    "@ziyic",
]


def block_from_file(
    file_obj: Iterable[str], source_id: str, token: str
) -> Dict[str, str]:
    """Block users listed in ``file_obj`` using the X web API.

    Parameters
    ----------
    file_obj:
        Iterable yielding usernames, one per line.  Each line may be ``str`` or
        ``bytes``.
    source_id:
        Numeric X user id of the account performing the block.  Included for
        completeness; the current implementation sends it with the request but
        the server may not require it.
    token:
        ``auth_token`` cookie from the user's X session.  This authenticates
        the request.

    Returns
    -------
    dict
        Mapping of the original username lines to ``"blocked"`` or an error
        message if the request failed.

    Notes
    -----
    The real X API requires many headers and cookies.  This function performs a
    minimal request using ``requests`` so that it can be easily mocked during
    tests.  It posts to ``https://api.twitter.com/1.1/blocks/create.json`` for
    each username.  Any network or HTTP errors are captured and returned in the
    results mapping.
    """

    results: Dict[str, str] = {}
    url = "https://api.twitter.com/1.1/blocks/create.json"
    headers = {"User-Agent": "mass-block-x-users"}
    cookies = {"auth_token": token}

    for line in file_obj:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        raw_username = line.strip()
        if not raw_username:
            continue

        # The API expects the username without the leading '@'.  Store the
        # original username for reporting but strip the symbol for the request.
        screen_name = raw_username.lstrip("@")
        payload = {"screen_name": screen_name, "source_id": source_id}

        try:
            response = requests.post(
                url, json=payload, headers=headers, cookies=cookies, timeout=10
            )
            if response.status_code == 200:
                results[raw_username] = "blocked"
            else:
                results[raw_username] = f"error: {response.status_code}"
        except requests.RequestException as exc:  # pragma: no cover - network
            results[raw_username] = f"error: {exc}"

    return results


def block_sol_shills(source_id: str, token: str) -> Dict[str, str]:
    """Block the preset list of SOL shill usernames."""

    buffer = StringIO("\n".join(SOL_SHILLS))
    return block_from_file(buffer, source_id, token)
