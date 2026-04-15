import json
import re
import urllib.request
import csv
from pathlib import Path

import ndspy.narc
import ndspy.rom


ROOT = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier")
BLACK_FR_ROM = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier\Rom pokemon pas mod\5587 - Pokemon - Version Noire (France) (NDSi Enhanced).nds")
WHITE_FR_ROM = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier\Rom pokemon pas mod\5586 - Pokemon - Version Blanche (DSi Enhanced) (F)(EXiMiUS).nds")
BLACK_EN_ROM = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier\Rom pokemon pas mod\Pokemon - Black Version (USA, Europe) (NDSi Enhanced).nds")
WHITE_EN_ROM = Path(r"C:\Users\Jonatan\Documents\Nouveau dossier\Rom pokemon pas mod\Pokemon - White Version (USA, Europe) (NDSi Enhanced).nds")
BLACK_LOG = Path(r"C:\Users\Jonatan\Downloads\PokeRandoZX-v4_6_1(1)\Pokenoir.nds.log")

URLS = {
    "pokemon": "https://raw.githubusercontent.com/ThirdLemon/TrainerTyrant/master/TrainerTyrantForm/DefaultJSON/DefaultPokemon.json",
    "moves": "https://raw.githubusercontent.com/ThirdLemon/TrainerTyrant/master/TrainerTyrantForm/DefaultJSON/DefaultMoves.json",
    "items": "https://raw.githubusercontent.com/ThirdLemon/TrainerTyrant/master/TrainerTyrantForm/DefaultJSON/DefaultItems.json",
    "slots": "https://raw.githubusercontent.com/ThirdLemon/TrainerTyrant/master/TrainerTyrantForm/DefaultJSON/BlackWhiteSlots.json",
}

LANG_FR = 5
LANG_EN = 9


def load_name_map(csv_path, id_field, lang_id):
    mapping = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["local_language_id"]) != lang_id:
                continue
            mapping[int(row[id_field])] = row["name"]
    return mapping


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Codex"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ability_choice_from_misc(value):
    return value // 16


def gender_from_misc(value):
    gender = value - (value // 16) * 16
    return {0: "Random", 1: "Male", 2: "Female"}.get(gender, "Random")


def iv_from_difficulty(value):
    if value >= 255:
        return 31
    return int(value * 31 / 255)


def sanitize_name(name):
    name = str(name or "").replace(r"\[PK]\[MN] ", "").strip()
    name = re.sub(r"\s+", " ", name)
    return name


def parse_full_names_from_log(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    names = {}
    for line in raw.splitlines():
        m = re.match(r"#(\d+)\s+\((.*?)\)\s+-", line.strip())
        if not m:
            continue
        trainer_id = int(m.group(1))
        names[trainer_id] = sanitize_name(m.group(2))
    return names


def parse_bw_learnsets(rom, moves):
    learnset_narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf("a/0/1/8")])
    learnsets = {}
    for species_id, raw in enumerate(learnset_narc.files):
        if species_id == 0:
            continue
        entries = []
        blob = bytes(raw)
        for offset in range(0, len(blob), 4):
            move_id = blob[offset] + blob[offset + 1] * 256
            level = blob[offset + 2] + blob[offset + 3] * 256
            if move_id == 0xFFFF and level == 0xFFFF:
                break
            if move_id <= 0 or move_id >= len(moves):
                continue
            entries.append({"move": moves[move_id], "move_id": move_id, "level": level})
        learnsets[species_id] = entries
    return learnsets


def get_level_up_moves(species_id, level, learnsets):
    entries = learnsets.get(species_id, [])
    eligible = [entry for entry in entries if entry["level"] <= level]
    if not eligible:
        return [], []
    last_four = eligible[-4:]
    return [entry["move"] for entry in last_four], [entry["move_id"] for entry in last_four]


def parse_trainer(trdata, trpoke, idx, species, moves, items, slots, full_names, learnsets):
    if len(trdata) < 20:
        return None

    format_byte = trdata[0]
    has_moves = (format_byte & 1) == 1
    has_items = (format_byte & 2) == 2
    class_id = trdata[1]
    fight_type = trdata[2]
    pokemon_count = trdata[3]

    trainer_items = []
    for item_num in range(4):
        item_id = trdata[4 + item_num * 2] + trdata[5 + item_num * 2] * 256
        if item_id > 0:
            trainer_items.append(items[item_id])

    ai_flags = trdata[12]
    healer = bool(trdata[16])
    base_money = trdata[17]
    reward_id = trdata[18] + trdata[19] * 256
    reward = items[reward_id] if reward_id > 0 else ""

    segment_len = 8 + (2 if has_items else 0) + (8 if has_moves else 0)
    party = []
    for mon_index in range(pokemon_count):
        start = mon_index * segment_len
        difficulty = trpoke[start + 0]
        misc = trpoke[start + 1]
        level = trpoke[start + 2]
        species_id = trpoke[start + 4] + trpoke[start + 5] * 256
        form_id = trpoke[start + 6]
        start += 8

        held_item = ""
        held_item_id = 0
        if has_items:
            held_item_id = trpoke[start + 0] + trpoke[start + 1] * 256
            held_item = items[held_item_id] if held_item_id > 0 else ""
            start += 2

        moveset = []
        move_ids = []
        if has_moves:
            for move_index in range(4):
                move_id = trpoke[start + 0] + trpoke[start + 1] * 256
                if move_id > 0:
                    moveset.append(moves[move_id])
                    move_ids.append(move_id)
                start += 2
        else:
            moveset, move_ids = get_level_up_moves(species_id, level, learnsets)

        iv = iv_from_difficulty(difficulty)
        party.append(
            {
                "species": species[species_id],
                "_speciesId": species_id,
                "formID": form_id,
                "shiny": False,
                "level": level,
                "sex": gender_from_misc(misc),
                "nature": "",
                "ability": "",
                "_abilityChoice": ability_choice_from_misc(misc),
                "_difficulty": difficulty,
                "moveset": moveset,
                "_moveIds": move_ids,
                "heldItem": held_item,
                "_heldItemId": held_item_id,
                "ballID": -1,
                "seal": -1,
                "ivs": {"hp": iv, "atk": iv, "def": iv, "spAtk": iv, "spDef": iv, "spd": iv},
                "evs": {"hp": 0, "atk": 0, "def": 0, "spAtk": 0, "spDef": 0, "spd": 0},
            }
        )

    slot = slots[idx - 1] if 0 < idx <= len(slots) else {}
    raw_name = full_names.get(idx, sanitize_name(slot.get("Name", f"Trainer {idx}")))
    trainer = {
        "readOnly": {
            "trainerID": idx,
            "name": raw_name,
        },
        "trainerTypeID": class_id,
        "colorID": 0,
        "fightType": fight_type,
        "arenaID": -1,
        "effectID": 0,
        "gold": 0,
        "useItems": trainer_items,
        "hpRecoverFlag": healer,
        "giftItem": reward,
        "nameLabel": slot.get("Export Name", ""),
        "aiFlags": {
            "basicAI": bool(ai_flags & 0x01),
            "strongAI": bool(ai_flags & 0x02),
            "expertAI": bool(ai_flags & 0x04),
            "doubleBattleAI": bool(ai_flags & 0x80),
            "mercifulAI": False,
            "canUseItems": len(trainer_items) > 0,
            "canSwitchPokemon": bool(ai_flags & 0x20),
        },
        "_baseMoney": base_money,
        "_versionSource": "bw-vanilla",
        "party": party,
    }
    return trainer


def extract_game(rom_path, species, moves, items, slots, full_names):
    rom = ndspy.rom.NintendoDSRom.fromFile(str(rom_path))
    learnsets = parse_bw_learnsets(rom, moves)
    trdata_narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf("a/0/9/2")])
    trpoke_narc = ndspy.narc.NARC(rom.files[rom.filenames.idOf("a/0/9/3")])
    trainers = []
    for idx, (trdata, trpoke) in enumerate(zip(trdata_narc.files, trpoke_narc.files)):
        trainer = parse_trainer(trdata, trpoke, idx, species, moves, items, slots, full_names, learnsets)
        if not trainer or not trainer["party"]:
            continue
        trainers.append(trainer)
    return trainers


def localize_dataset(dataset, species_names, move_names, item_names):
    localized = json.loads(json.dumps(dataset))
    for trainer in localized:
        for mon in trainer.get("party", []):
            species_id = mon.get("_speciesId")
            if species_id in species_names:
                mon["species"] = species_names[species_id]
            held_item_id = mon.get("_heldItemId", 0)
            if held_item_id and held_item_id in item_names:
                mon["heldItem"] = item_names[held_item_id]
            move_ids = mon.get("_moveIds") or []
            if move_ids:
                mon["moveset"] = [move_names.get(move_id, move) for move_id, move in zip(move_ids, mon.get("moveset", []))]
            elif mon.get("moveset"):
                mon["moveset"] = [move_names.get(-1, move) if False else move for move in mon["moveset"]]
    return localized


def main():
    pokemon = fetch_json(URLS["pokemon"])["Pokemon"]
    moves = fetch_json(URLS["moves"])["Moves"]
    items = fetch_json(URLS["items"])["Items"]
    slots = fetch_json(URLS["slots"])["Slots"]
    full_names = parse_full_names_from_log(BLACK_LOG)
    species_fr = load_name_map(ROOT / "pokemon_species_names.csv", "pokemon_species_id", LANG_FR)
    species_en = load_name_map(ROOT / "pokemon_species_names.csv", "pokemon_species_id", LANG_EN)
    moves_fr = load_name_map(ROOT / "move_names.csv", "move_id", LANG_FR)
    moves_en = load_name_map(ROOT / "move_names.csv", "move_id", LANG_EN)
    items_fr = load_name_map(ROOT / "item_names.csv", "item_id", LANG_FR)
    items_en = load_name_map(ROOT / "item_names.csv", "item_id", LANG_EN)

    black_fr = extract_game(BLACK_FR_ROM, pokemon, moves, items, slots, full_names)
    white_fr = extract_game(WHITE_FR_ROM, pokemon, moves, items, slots, full_names)
    black_en = extract_game(BLACK_EN_ROM, pokemon, moves, items, slots, full_names)
    white_en = extract_game(WHITE_EN_ROM, pokemon, moves, items, slots, full_names)

    black_fr = localize_dataset(black_fr, species_fr, moves_fr, items_fr)
    white_fr = localize_dataset(white_fr, species_fr, moves_fr, items_fr)
    black_en = localize_dataset(black_en, species_en, moves_en, items_en)
    white_en = localize_dataset(white_en, species_en, moves_en, items_en)

    payload = {
        "black_fr": black_fr,
        "white_fr": white_fr,
        "black_en": black_en,
        "white_en": white_en,
    }
    out_path = ROOT / "bw_vanilla_data.js"
    base = "window.BW_VANILLA_DATA=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";"
    aliases = """
window.BW_VANILLA_DATA.black_usa=window.BW_VANILLA_DATA.black_en;
window.BW_VANILLA_DATA.black_eu=window.BW_VANILLA_DATA.black_en;
window.BW_VANILLA_DATA.white_usa=window.BW_VANILLA_DATA.white_en;
window.BW_VANILLA_DATA.white_eu=window.BW_VANILLA_DATA.white_en;
"""
    out_path.write_text(base + aliases, encoding="utf-8")
    (ROOT / "bw1_vanilla_fr.json").write_text(json.dumps({"black": black_fr, "white": white_fr}, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "bw1_vanilla_usa.json").write_text(json.dumps({"black": black_en, "white": white_en}, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "bw1_vanilla_eu.json").write_text(json.dumps({"black": black_en, "white": white_en}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)
    print(f"black_fr={len(black_fr)} white_fr={len(white_fr)} black_en={len(black_en)} white_en={len(white_en)}")


if __name__ == "__main__":
    main()
