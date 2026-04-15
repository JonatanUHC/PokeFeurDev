import csv
import json
import re
from pathlib import Path

import ndspy.narc
import ndspy.rom


ROOT = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier")
ROM_ROOT = ROOT / "Rom pokemon pas mod"
OUT_ROOT = ROOT / "vanilla_exports"
UPR_ROOT = ROOT / "_tmp_uprzx" / "universal-pokemon-randomizer-zx-master"
UPR_CONFIG = UPR_ROOT / "src" / "com" / "dabomstew" / "pkrandom" / "config"

LANG_FR = 5
LANG_EN = 9

TYPE_KEYS = {
    "gen4": {
        0x00: "Normal",
        0x01: "Fighting",
        0x02: "Flying",
        0x03: "Poison",
        0x04: "Ground",
        0x05: "Rock",
        0x06: "Bug",
        0x07: "Ghost",
        0x08: "Steel",
        0x0A: "Fire",
        0x0B: "Water",
        0x0C: "Grass",
        0x0D: "Electric",
        0x0E: "Psychic",
        0x0F: "Ice",
        0x10: "Dragon",
        0x11: "Dark",
    },
    "gen5": {
        0x00: "Normal",
        0x01: "Fighting",
        0x02: "Flying",
        0x03: "Poison",
        0x04: "Ground",
        0x05: "Rock",
        0x06: "Bug",
        0x07: "Ghost",
        0x08: "Steel",
        0x09: "Fire",
        0x0A: "Water",
        0x0B: "Grass",
        0x0C: "Electric",
        0x0D: "Psychic",
        0x0E: "Ice",
        0x0F: "Dragon",
        0x10: "Dark",
    },
}

ABILITY_SLOT_LABELS = {
    "fr": {
        0: "Talents possibles",
        1: "Talent 1",
        2: "Talent 2",
        3: "Talent caché",
    },
    "en": {
        0: "Possible abilities",
        1: "Ability 1",
        2: "Ability 2",
        3: "Hidden ability",
    },
}


ROM_CONFIGS = {
    "diamond": {
        "family": "gen4",
        "trdata": "poketool/trainer/trdata.narc",
        "trpoke": "poketool/trainer/trpoke.narc",
        "personal": "poketool/personal/personal.narc",
        "learnset": "poketool/personal/wotbl.narc",
        "move_data": "poketool/waza/waza_tbl.narc",
    },
    "pearl": {
        "family": "gen4",
        "trdata": "poketool/trainer/trdata.narc",
        "trpoke": "poketool/trainer/trpoke.narc",
        "personal": ["poketool/personal/personal.narc", "poketool/personal_pearl/personal.narc"],
        "learnset": "poketool/personal/wotbl.narc",
        "move_data": "poketool/waza/waza_tbl.narc",
    },
    "platinum": {
        "family": "gen4",
        "trdata": "poketool/trainer/trdata.narc",
        "trpoke": "poketool/trainer/trpoke.narc",
        "personal": "poketool/personal/pl_personal.narc",
        "learnset": "poketool/personal/wotbl.narc",
        "move_data": "poketool/waza/pl_waza_tbl.narc",
    },
    "heartgold": {
        "family": "gen4",
        "trdata": "a/0/5/5",
        "trpoke": "a/0/5/6",
        "personal": "a/0/0/2",
        "learnset": "a/0/3/3",
        "move_data": "a/0/1/1",
    },
    "soulsilver": {
        "family": "gen4",
        "trdata": "a/0/5/5",
        "trpoke": "a/0/5/6",
        "personal": "a/0/0/2",
        "learnset": "a/0/3/3",
        "move_data": "a/0/1/1",
    },
    "black": {
        "family": "gen5",
        "trdata": "a/0/9/2",
        "trpoke": "a/0/9/3",
        "personal": "a/0/1/6",
        "learnset": "a/0/1/8",
        "move_data": "a/0/2/1",
    },
    "white": {
        "family": "gen5",
        "trdata": "a/0/9/2",
        "trpoke": "a/0/9/3",
        "personal": "a/0/1/6",
        "learnset": "a/0/1/8",
        "move_data": "a/0/2/1",
    },
    "black2": {
        "family": "gen5",
        "trdata": "a/0/9/1",
        "trpoke": "a/0/9/2",
        "personal": "a/0/1/6",
        "learnset": "a/0/1/8",
        "move_data": "a/0/2/1",
    },
    "white2": {
        "family": "gen5",
        "trdata": "a/0/9/1",
        "trpoke": "a/0/9/2",
        "personal": "a/0/1/6",
        "learnset": "a/0/1/8",
        "move_data": "a/0/2/1",
    },
}

TEXT_CONFIGS = {
    "ADAE": {"family": "gen4", "text_path": "msgdata/msg.narc", "trainer_names_offset": 559, "trainer_classes_offset": 560},
    "ADAF": {"family": "gen4", "text_path": "msgdata/msg.narc", "trainer_names_offset": 559, "trainer_classes_offset": 560},
    "APAE": {"family": "gen4", "text_path": "msgdata/msg.narc", "trainer_names_offset": 559, "trainer_classes_offset": 560},
    "APAF": {"family": "gen4", "text_path": "msgdata/msg.narc", "trainer_names_offset": 559, "trainer_classes_offset": 560},
    "CPUE": {"family": "gen4", "text_path": "msgdata/pl_msg.narc", "trainer_names_offset": 618, "trainer_classes_offset": 619},
    "CPUF": {"family": "gen4", "text_path": "msgdata/pl_msg.narc", "trainer_names_offset": 618, "trainer_classes_offset": 619},
    "IPKE": {"family": "gen4", "text_path": "a/0/2/7", "trainer_names_offset": 729, "trainer_classes_offset": 730},
    "IPKF": {"family": "gen4", "text_path": "a/0/2/7", "trainer_names_offset": 729, "trainer_classes_offset": 730},
    "IPGE": {"family": "gen4", "text_path": "a/0/2/7", "trainer_names_offset": 729, "trainer_classes_offset": 730},
    "IPGF": {"family": "gen4", "text_path": "a/0/2/7", "trainer_names_offset": 729, "trainer_classes_offset": 730},
    "IRBO": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 190, "trainer_classes_offset": 191},
    "IRBF": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 190, "trainer_classes_offset": 191},
    "IRAO": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 190, "trainer_classes_offset": 191},
    "IRAF": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 190, "trainer_classes_offset": 191},
    "IREO": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 382, "trainer_classes_offset": 383},
    "IREF": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 382, "trainer_classes_offset": 383},
    "IRDO": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 382, "trainer_classes_offset": 383},
    "IRDF": {"family": "gen5", "text_path": "a/0/0/2", "trainer_names_offset": 382, "trainer_classes_offset": 383},
}


def load_name_map(csv_path, id_field, lang_id):
    mapping = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["local_language_id"]) != lang_id:
                continue
            mapping[int(row[id_field])] = row["name"]
    return mapping


def title_case_ascii(value):
    text = str(value or "").strip()
    if not text:
        return ""
    return text[:1].upper() + text[1:]


def cleanup_text_value(value):
    text = str(value or "")
    text = text.replace("\uf000", "").replace("\u0100", "")
    text = text.replace("[PK][MN]", "Pokémon").replace("\\[PK]\\[MN]", "Pokémon")
    text = text.replace("\\and", "&")
    text = text.replace("\\n", " ").replace("\\r", " ")
    text = re.sub(r"\\xFFFF", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\\x0000", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\\xF000", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\\x[0-9A-Fa-f]{4}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if re.fullmatch(r"-+", text):
        return ""
    return text


def detect_game_key(path, rom):
    code = bytes(rom.idCode).decode("ascii", "ignore")
    upper = path.name.upper()
    if code.startswith("ADA"):
        return "diamond"
    if code.startswith("APA"):
        return "pearl"
    if code.startswith("CPU"):
        return "platinum"
    if code.startswith("IPK"):
        return "heartgold"
    if code.startswith("IPG"):
        return "soulsilver"
    if code.startswith("IRE"):
        return "black2"
    if code.startswith("IRD"):
        return "white2"
    if code.startswith("IRB"):
        return "black"
    if code.startswith("IRA"):
        return "white"
    if "BLACK VERSION 2" in upper or "NOIRE 2" in upper:
        return "black2"
    if "WHITE VERSION 2" in upper or "BLANCHE 2" in upper:
        return "white2"
    if "BLACK VERSION" in upper or "VERSION NOIRE" in upper:
        return "black"
    if "WHITE VERSION" in upper or "VERSION BLANCHE" in upper:
        return "white"
    raise ValueError(f"Jeu non reconnu pour {path.name}")


def detect_language(path, rom):
    code = bytes(rom.idCode).decode("ascii", "ignore")
    if code.endswith("F"):
        return "fr"
    upper = path.name.upper()
    if "FRANCE" in upper or "(F)" in upper:
        return "fr"
    return "en"


def load_generation4_table():
    mapping = {}
    path = UPR_CONFIG / "Generation4.tbl"
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            mapping[int(key, 16)] = value
    return mapping


def load_generation5_table():
    mapping = {}
    path = UPR_CONFIG / "Generation5.tbl"
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            mapping[chr(int(key, 16))] = value
    return mapping


def detect_regions(path):
    upper = path.name.upper()
    regions = []
    if "USA" in upper:
        regions.append("usa")
    if "EUROPE" in upper:
        regions.append("eu")
    if "FRANCE" in upper or "(F)" in upper:
        regions.append("fr")
    if not regions:
        regions.append("unknown")
    return regions


def sanitize_slug(name):
    text = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return text or "rom"


def gender_from_misc(value):
    return {0: "Random", 1: "Male", 2: "Female"}.get(value & 0x0F, "Random")


def ability_choice_from_misc(value):
    return value >> 4


def iv_from_difficulty(value):
    if value >= 255:
        return 31
    return int(value * 31 / 255)


def parse_gen4_learnsets(blob):
    learnsets = {}
    for species_id, raw in enumerate(blob.files):
        if species_id == 0:
            continue
        entries = []
        data = bytes(raw)
        for offset in range(0, len(data), 2):
            value = int.from_bytes(data[offset:offset + 2], "little")
            if value == 0xFFFF:
                break
            move_id = value & 0x01FF
            level = value >> 9
            if move_id:
                entries.append({"move_id": move_id, "level": level})
        learnsets[species_id] = entries
    return learnsets


def parse_gen5_learnsets(blob):
    learnsets = {}
    for species_id, raw in enumerate(blob.files):
        if species_id == 0:
            continue
        entries = []
        data = bytes(raw)
        for offset in range(0, len(data), 4):
            move_id = int.from_bytes(data[offset:offset + 2], "little")
            level = int.from_bytes(data[offset + 2:offset + 4], "little")
            if move_id == 0xFFFF and level == 0xFFFF:
                break
            if move_id:
                entries.append({"move_id": move_id, "level": level})
        learnsets[species_id] = entries
    return learnsets


def read16(data, ofs):
    return int.from_bytes(data[ofs:ofs + 2], "little")


def read32(data, ofs):
    return int.from_bytes(data[ofs:ofs + 4], "little")


def decode_gen4_text_entry(raw, table):
    data = bytearray(raw)
    count = read16(data, 0)
    key = read16(data, 2)
    sdidx = 4
    key = (key * 0x2FD) & 0xFFFF
    for i in range(count):
        key2 = (key * (i + 1)) & 0xFFFF
        realkey = key2 | (key2 << 16)
        value1 = read32(data, sdidx) ^ realkey
        value2 = read32(data, sdidx + 4) ^ realkey
        data[sdidx:sdidx + 4] = value1.to_bytes(4, "little")
        data[sdidx + 4:sdidx + 8] = value2.to_bytes(4, "little")
        sdidx += 8

    entries = []
    for i in range(count):
        ptr = read32(data, 4 + i * 8)
        chars = read32(data, 8 + i * 8)
        local_key = (0x91BD3 * (i + 1)) & 0xFFFF
        idx = ptr
        words = []
        for _ in range(chars):
            val = read16(data, idx) ^ local_key
            words.append(val)
            local_key = (local_key + 0x493D) & 0xFFFF
            idx += 2

        if words and words[0] == 0xF100:
            uncomp = []
            j = 1
            shift1 = 0
            trans = 0
            while j < len(words):
                if shift1 >= 0xF:
                    shift1 -= 0xF
                    if shift1 > 0:
                        tmp1 = trans | ((words[j] << (9 - shift1)) & 0x1FF)
                        if tmp1 == 0x1FF:
                            break
                        uncomp.append(tmp1)
                else:
                    tmp1 = (words[j] >> shift1) & 0x1FF
                    if tmp1 == 0x1FF:
                        break
                    uncomp.append(tmp1)
                    shift1 += 9
                    if shift1 < 0xF:
                        trans = (words[j] >> shift1) & 0x1FF
                        shift1 += 9
                    j += 1
            words = uncomp

        out = []
        i2 = 0
        while i2 < len(words):
            curr = words[i2]
            if curr in table:
                out.append(table[curr])
            elif curr == 0xFFFE:
                i2 += 1
                if i2 < len(words):
                    out.append("\\v" + f"{words[i2]:04X}")
                i2 += 1
                total = words[i2] if i2 < len(words) else 0
                if total == 0:
                    out.append("\\x0000")
                for _ in range(total):
                    i2 += 1
                    if i2 < len(words):
                        out.append("\\z" + f"{words[i2]:04X}")
            elif curr == 0xFFFF:
                break
            else:
                out.append("\\x" + f"{curr:04X}")
            i2 += 1
        entries.append(cleanup_text_value("".join(out)))
    return entries


def rotate_right_16(value, count):
    return ((value >> count) | ((value << (16 - count)) & 0xFFFF)) & 0xFFFF


def decode_gen5_text_entry(raw, table):
    data = bytes(raw)
    num_sections = read16(data, 0)
    num_entries = read16(data, 2)
    if num_sections < 1:
        return []
    section_offset = read32(data, 12)
    pos = section_offset + 4
    entries = []
    table_offsets = []
    char_counts = []
    for _ in range(num_entries):
        table_offsets.append(read32(data, pos))
        char_counts.append(read16(data, pos + 4))
        pos += 8

    for j in range(num_entries):
        pos = section_offset + table_offsets[j]
        chars = [read16(data, pos + k * 2) for k in range(char_counts[j])]
        if not chars:
            entries.append("")
            continue
        key = chars[-1] ^ 0xFFFF
        dec = [0] * len(chars)
        for k in range(len(chars) - 1, -1, -1):
            dec[k] = chars[k] ^ key
            key = rotate_right_16(key, 3)

        if dec and dec[0] == 0xF100:
            uncomp = []
            j2 = 1
            shift1 = 0
            trans = 0
            while j2 < len(dec):
                if shift1 >= 0x10:
                    shift1 -= 0x10
                    if shift1 > 0:
                        tmp1 = trans | ((dec[j2] << (9 - shift1)) & 0x1FF)
                        if (tmp1 & 0xFF) == 0xFF:
                            break
                        if tmp1 not in (0x0, 0x1):
                            uncomp.append(tmp1)
                else:
                    tmp1 = (dec[j2] >> shift1) & 0x1FF
                    if (tmp1 & 0xFF) == 0xFF:
                        break
                    if tmp1 not in (0x0, 0x1):
                        uncomp.append(tmp1)
                    shift1 += 9
                    if shift1 < 0x10:
                        trans = (dec[j2] >> shift1) & 0x1FF
                        shift1 += 9
                    j2 += 1
            dec = uncomp

        out = []
        for val in dec:
            if val == 0xFFFF:
                out.append("\\xFFFF")
            elif 20 < val <= 0xFFF0:
                try:
                    out.append(chr(val))
                except ValueError:
                    out.append("\\x" + f"{val:04X}")
            else:
                out.append("\\x" + f"{val:04X}")
        text = "".join(out)
        for src, repl in table.items():
            text = text.replace(src, repl)
        entries.append(cleanup_text_value(text))
    return entries


def extract_trainer_texts(rom):
    code = bytes(rom.idCode).decode("ascii", "ignore")
    cfg = TEXT_CONFIGS.get(code)
    if not cfg:
        return [], []
    narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf(cfg["text_path"])])
    if cfg["family"] == "gen4":
        table = load_generation4_table()
        name_entries = decode_gen4_text_entry(narc.files[cfg["trainer_names_offset"]], table)
        class_entries = decode_gen4_text_entry(narc.files[cfg["trainer_classes_offset"]], table)
    else:
        table = load_generation5_table()
        name_entries = decode_gen5_text_entry(narc.files[cfg["trainer_names_offset"]], table)
        class_entries = decode_gen5_text_entry(narc.files[cfg["trainer_classes_offset"]], table)
    if name_entries and not name_entries[0]:
        name_entries = name_entries[1:]
    return name_entries, class_entries


def parse_personal_entry(raw, family):
    if family == "gen4":
        return {
            "baseStats": {"hp": raw[0], "atk": raw[1], "def": raw[2], "spd": raw[3], "spAtk": raw[4], "spDef": raw[5]},
            "type1": raw[6],
            "type2": raw[7],
            "ability1": raw[22],
            "ability2": raw[23],
            "ability3": 0,
        }
    return {
        "baseStats": {"hp": raw[0], "atk": raw[1], "def": raw[2], "spd": raw[3], "spAtk": raw[4], "spDef": raw[5]},
        "type1": raw[6],
        "type2": raw[7],
        "ability1": raw[24],
        "ability2": raw[25],
        "ability3": raw[26],
    }


def build_personal_map(rom, cfg):
    personal_path = cfg["personal"]
    if isinstance(personal_path, list):
        file_id = None
        for candidate in personal_path:
            file_id = rom.filenames.idOf(candidate)
            if file_id is not None:
                break
        if file_id is None:
            raise ValueError(f"Personal introuvable pour {personal_path}")
    else:
        file_id = rom.filenames.idOf(personal_path)
    narc = ndspy.narc.NARC(rom.files[file_id])
    personal = {}
    for species_id, raw in enumerate(narc.files):
        personal[species_id] = parse_personal_entry(bytes(raw), cfg["family"])
    return personal


def build_learnset_map(rom, cfg):
    narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf(cfg["learnset"])])
    if cfg["family"] == "gen4":
        return parse_gen4_learnsets(narc)
    return parse_gen5_learnsets(narc)


def build_move_data_map(rom, cfg, move_names):
    narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf(cfg["move_data"])])
    move_data = {}
    type_keys = TYPE_KEYS[cfg["family"]]
    for move_id, raw in enumerate(narc.files):
        if move_id == 0:
            continue
        detail = {
            "id": move_id,
            "name": move_names.get(move_id, f"Move #{move_id}"),
            "type": None,
            "damageClass": None,
            "power": None,
            "accuracy": None,
            "accuracyKnown": True,
            "pp": None,
        }
        if cfg["family"] == "gen4":
            detail["type"] = type_keys.get(raw[4])
            detail["damageClass"] = ["physical", "special", "status"][raw[2]] if raw[2] < 3 else None
            detail["power"] = raw[3] or None
            detail["accuracy"] = raw[5] or None
            detail["pp"] = raw[6] or None
        else:
            detail["type"] = type_keys.get(raw[0])
            detail["damageClass"] = ["status", "physical", "special"][raw[2]] if raw[2] < 3 else None
            detail["power"] = raw[3] or None
            detail["accuracy"] = raw[4] or None
            detail["pp"] = raw[5] or None
        move_data[move_id] = detail
    return move_data


def get_level_up_moves(species_id, level, learnsets):
    entries = learnsets.get(species_id, [])
    eligible = [entry for entry in entries if entry["level"] <= level]
    return eligible[-4:]


def resolve_ability_names(choice, personal_entry, ability_names, lang, cfg):
    ids = []
    a1 = personal_entry.get("ability1", 0)
    a2 = personal_entry.get("ability2", 0)
    a3 = personal_entry.get("ability3", 0)
    if cfg["family"] == "gen4" and cfg is not None and cfg in (ROM_CONFIGS["diamond"], ROM_CONFIGS["pearl"], ROM_CONFIGS["platinum"]):
        if a1:
            ids = [a1]
    elif choice == 1 and a1:
        ids = [a1]
    elif choice == 2 and a2:
        ids = [a2]
    elif choice == 3 and a3:
        ids = [a3]
    else:
        ids = [aid for aid in [a1, a2, a3] if aid]
    seen = set()
    names = []
    for aid in ids:
        if aid in seen:
            continue
        seen.add(aid)
        names.append(ability_names.get(aid, f"Ability #{aid}"))
    return {
        "label": ABILITY_SLOT_LABELS[lang].get(choice, ABILITY_SLOT_LABELS[lang][0]),
        "ids": ids,
        "names": names,
    }


def parse_trainer_entry(idx, trdata, trpoke, cfg, species_names, move_names, item_names, ability_names, personal, learnsets, move_data_map, lang, trainer_names, trainer_classes):
    if len(trdata) < 20:
        return None

    flags = trdata[0]
    has_moves = (flags & 1) == 1
    has_items = (flags & 2) == 2
    trainer_class = trdata[1]
    battle_type = trdata[2]
    num_pokemon = trdata[3]
    ai = int.from_bytes(trdata[12:16], "little")
    battle_type_2 = trdata[16]

    trainer_items = []
    trainer_item_ids = []
    for offset in range(4, 12, 2):
        item_id = int.from_bytes(trdata[offset:offset + 2], "little")
        if item_id:
            trainer_item_ids.append(item_id)
            trainer_items.append(item_names.get(item_id, f"Item #{item_id}"))

    base_len = 6 if cfg["family"] == "gen4" else 8
    extra_len = 2 if cfg["family"] == "gen4" and cfg not in (ROM_CONFIGS["diamond"], ROM_CONFIGS["pearl"]) else 0
    segment_len = base_len + (2 if has_items else 0) + (8 if has_moves else 0) + extra_len
    party = []
    for mon_index in range(num_pokemon):
        start = mon_index * segment_len
        if start + base_len > len(trpoke):
            break
        difficulty = trpoke[start]
        misc = trpoke[start + 1]
        level = int.from_bytes(trpoke[start + 2:start + 4], "little")
        ball = 0
        if cfg["family"] == "gen4":
            species_word = int.from_bytes(trpoke[start + 4:start + 6], "little")
            species_id = (species_word & 0xFF) + (((species_word >> 8) & 0x01) << 8)
            form_id = (species_word >> 10) & 0x3F
            unknown = (species_word >> 9) & 0x01
        else:
            ball = trpoke[start + 3]
            species_id = int.from_bytes(trpoke[start + 4:start + 6], "little")
            form_id = int.from_bytes(trpoke[start + 6:start + 8], "little")
            unknown = 0
        cursor = start + base_len
        if not species_id:
            continue

        held_item_id = 0
        held_item = ""
        if has_items and cursor + 2 <= len(trpoke):
            held_item_id = int.from_bytes(trpoke[cursor:cursor + 2], "little")
            held_item = item_names.get(held_item_id, f"Item #{held_item_id}") if held_item_id else ""
            cursor += 2

        move_ids = []
        move_names_local = []
        move_details = []
        source = "explicit"
        if has_moves and cursor + 8 <= len(trpoke):
            for _ in range(4):
                move_id = int.from_bytes(trpoke[cursor:cursor + 2], "little")
                if move_id:
                    move_ids.append(move_id)
                    move_names_local.append(move_names.get(move_id, f"Move #{move_id}"))
                    if move_id in move_data_map:
                        move_details.append(dict(move_data_map[move_id]))
                cursor += 2
        else:
            source = "learnset"
            for entry in get_level_up_moves(species_id, level, learnsets):
                move_ids.append(entry["move_id"])
                move_names_local.append(move_names.get(entry["move_id"], f"Move #{entry['move_id']}"))
                if entry["move_id"] in move_data_map:
                    move_details.append(dict(move_data_map[entry["move_id"]]))

        cursor += extra_len

        personal_entry = personal.get(species_id, {"type1": 0, "type2": 0, "ability1": 0, "ability2": 0, "ability3": 0})
        type_ids = [personal_entry.get("type1", 0)]
        type2 = personal_entry.get("type2", 0)
        if type2 not in type_ids:
            type_ids.append(type2)
        type_keys = [TYPE_KEYS[cfg["family"]].get(tid) for tid in type_ids if TYPE_KEYS[cfg["family"]].get(tid)]
        ability_info = resolve_ability_names(ability_choice_from_misc(misc), personal_entry, ability_names, lang, cfg)
        iv = iv_from_difficulty(difficulty)

        party.append(
            {
                "speciesId": species_id,
                "species": species_names.get(species_id, f"Pokémon #{species_id}"),
                "formId": form_id,
                "level": level,
                "sex": gender_from_misc(misc),
                "heldItemId": held_item_id,
                "heldItem": held_item,
                "movesetIds": move_ids,
                "moveset": move_names_local,
                "moveDetails": move_details,
                "movesSource": source,
                "types": type_keys,
                "typeIds": type_ids,
                "abilityChoice": ability_choice_from_misc(misc),
                "abilityLabel": ability_info["label"],
                "abilities": ability_info["names"],
                "abilityIds": ability_info["ids"],
                "baseStats": personal_entry.get("baseStats", {}),
                "ivs": {"hp": iv, "atk": iv, "def": iv, "spAtk": iv, "spDef": iv, "spd": iv},
                "difficulty": difficulty,
                "ball": ball,
                "unknown": unknown,
            }
        )

    if not party:
        return None

    trainer_name = trainer_names[idx - 1] if 0 < idx <= len(trainer_names) else ""
    trainer_class_name = trainer_classes[trainer_class] if 0 <= trainer_class < len(trainer_classes) else ""
    if not trainer_name:
        trainer_name = trainer_class_name or f"Trainer {idx}"

    return {
        "trainerId": idx,
        "name": trainer_name or f"Trainer {idx}",
        "trainerClassId": trainer_class,
        "trainerClassName": trainer_class_name,
        "battleType": battle_type,
        "battleType2": battle_type_2,
        "trainerItemIds": trainer_item_ids,
        "trainerItems": trainer_items,
        "ai": ai,
        "party": party,
    }


def extract_rom(rom_path, shared):
    rom = ndspy.rom.NintendoDSRom.fromFile(str(rom_path))
    game_key = detect_game_key(rom_path, rom)
    cfg = ROM_CONFIGS[game_key]
    lang = detect_language(rom_path, rom)
    species_names = shared[f"species_{lang}"]
    move_names = shared[f"moves_{lang}"]
    item_names = shared[f"items_{lang}"]
    ability_names = shared[f"abilities_{lang}"]
    trainer_names, trainer_classes = extract_trainer_texts(rom)

    personal = build_personal_map(rom, cfg)
    learnsets = build_learnset_map(rom, cfg)
    move_data_map = build_move_data_map(rom, cfg, move_names)
    trdata_narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf(cfg["trdata"])])
    trpoke_narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf(cfg["trpoke"])])

    trainers = []
    for idx, (trdata, trpoke) in enumerate(zip(trdata_narc.files, trpoke_narc.files)):
        trainer = parse_trainer_entry(
            idx,
            bytes(trdata),
            bytes(trpoke),
            cfg,
            species_names,
            move_names,
            item_names,
            ability_names,
            personal,
            learnsets,
            move_data_map,
            lang,
            trainer_names,
            trainer_classes,
        )
        if trainer:
            trainers.append(trainer)

    title = bytes(rom.name).decode("ascii", "ignore").strip("\x00")
    code = bytes(rom.idCode).decode("ascii", "ignore")
    return {
        "meta": {
            "sourceFile": rom_path.name,
            "title": title,
            "idCode": code,
            "game": game_key,
            "family": cfg["family"],
            "language": lang,
            "regions": detect_regions(rom_path),
            "trainerCount": len(trainers),
        },
        "trainers": trainers,
    }


def build_shared_maps():
    return {
        "species_fr": load_name_map(ROOT / "pokemon_species_names.csv", "pokemon_species_id", LANG_FR),
        "species_en": load_name_map(ROOT / "pokemon_species_names.csv", "pokemon_species_id", LANG_EN),
        "moves_fr": load_name_map(ROOT / "move_names.csv", "move_id", LANG_FR),
        "moves_en": load_name_map(ROOT / "move_names.csv", "move_id", LANG_EN),
        "items_fr": load_name_map(ROOT / "item_names.csv", "item_id", LANG_FR),
        "items_en": load_name_map(ROOT / "item_names.csv", "item_id", LANG_EN),
        "abilities_fr": load_name_map(ROOT / "ability_names.csv", "ability_id", LANG_FR),
        "abilities_en": load_name_map(ROOT / "ability_names.csv", "ability_id", LANG_EN),
    }


def main():
    OUT_ROOT.mkdir(exist_ok=True)
    shared = build_shared_maps()
    manifest = []
    rom_paths = sorted(ROM_ROOT.glob("*.nds"))
    for rom_path in rom_paths:
        dataset = extract_rom(rom_path, shared)
        slug = sanitize_slug(rom_path.stem)
        out_path = OUT_ROOT / f"{slug}.json"
        out_path.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
        js_out_path = OUT_ROOT / f"{slug}.js"
        js_out_path.write_text(
            "window.VANILLA_ROM_DATA = window.VANILLA_ROM_DATA || {};\n"
            f'window.VANILLA_ROM_DATA["{slug}"] = '
            + json.dumps(dataset, ensure_ascii=False)
            + ";\n",
            encoding="utf-8",
        )
        manifest.append(
            {
                "slug": slug,
                "file": out_path.name,
                **dataset["meta"],
            }
        )
        print(f"Wrote {out_path.name} ({dataset['meta']['trainerCount']} trainers)")

    (OUT_ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_ROOT / "manifest.js").write_text(
        "window.VANILLA_MANIFEST = " + json.dumps(manifest, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote manifest.json ({len(manifest)} roms)")


if __name__ == "__main__":
    main()
