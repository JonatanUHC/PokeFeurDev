(function () {
  const TYPE_KEYS = {
    gen4: {
      0x00: 'Normal', 0x01: 'Fighting', 0x02: 'Flying', 0x03: 'Poison', 0x04: 'Ground',
      0x05: 'Rock', 0x06: 'Bug', 0x07: 'Ghost', 0x08: 'Steel', 0x0A: 'Fire',
      0x0B: 'Water', 0x0C: 'Grass', 0x0D: 'Electric', 0x0E: 'Psychic',
      0x0F: 'Ice', 0x10: 'Dragon', 0x11: 'Dark'
    },
    gen5: {
      0x00: 'Normal', 0x01: 'Fighting', 0x02: 'Flying', 0x03: 'Poison', 0x04: 'Ground',
      0x05: 'Rock', 0x06: 'Bug', 0x07: 'Ghost', 0x08: 'Steel', 0x09: 'Fire',
      0x0A: 'Water', 0x0B: 'Grass', 0x0C: 'Electric', 0x0D: 'Psychic',
      0x0E: 'Ice', 0x0F: 'Dragon', 0x10: 'Dark'
    }
  };

  const ABILITY_SLOT_LABELS = {
    fr: { 0: 'Talents possibles', 1: 'Talent 1', 2: 'Talent 2', 3: 'Talent caché' },
    en: { 0: 'Possible abilities', 1: 'Ability 1', 2: 'Ability 2', 3: 'Hidden ability' }
  };

  const GAME_TITLES = {
    diamond: { fr: 'Pokémon Diamant', en: 'Pokémon Diamond' },
    pearl: { fr: 'Pokémon Perle', en: 'Pokémon Pearl' },
    platinum: { fr: 'Pokémon Platine', en: 'Pokémon Platinum' },
    heartgold: { fr: 'Pokémon Or HeartGold', en: 'Pokémon HeartGold' },
    soulsilver: { fr: 'Pokémon Argent SoulSilver', en: 'Pokémon SoulSilver' },
    black: { fr: 'Pokémon Noir', en: 'Pokémon Black' },
    white: { fr: 'Pokémon Blanc', en: 'Pokémon White' },
    black2: { fr: 'Pokémon Noir 2', en: 'Pokémon Black 2' },
    white2: { fr: 'Pokémon Blanc 2', en: 'Pokémon White 2' }
  };

  const GAME_CONFIGS = {
    diamond: {
      family: 'gen4',
      trdata: 'poketool/trainer/trdata.narc',
      trpoke: 'poketool/trainer/trpoke.narc',
      personal: ['poketool/personal/personal.narc'],
      learnset: 'poketool/personal/wotbl.narc',
      moveData: 'poketool/waza/waza_tbl.narc',
      textPath: 'msgdata/msg.narc',
      textOffsets: { pokemonNames: 362, trainerNames: 559, trainerClasses: 560, moveNames: 588, abilityNames: 552, itemNames: 344 }
    },
    pearl: {
      family: 'gen4',
      trdata: 'poketool/trainer/trdata.narc',
      trpoke: 'poketool/trainer/trpoke.narc',
      personal: ['poketool/personal/personal.narc', 'poketool/personal_pearl/personal.narc'],
      learnset: 'poketool/personal/wotbl.narc',
      moveData: 'poketool/waza/waza_tbl.narc',
      textPath: 'msgdata/msg.narc',
      textOffsets: { pokemonNames: 362, trainerNames: 559, trainerClasses: 560, moveNames: 588, abilityNames: 552, itemNames: 344 }
    },
    platinum: {
      family: 'gen4',
      trdata: 'poketool/trainer/trdata.narc',
      trpoke: 'poketool/trainer/trpoke.narc',
      personal: ['poketool/personal/pl_personal.narc'],
      learnset: 'poketool/personal/wotbl.narc',
      moveData: 'poketool/waza/pl_waza_tbl.narc',
      textPath: 'msgdata/pl_msg.narc',
      textOffsets: { pokemonNames: 412, trainerNames: 618, trainerClasses: 619, moveNames: 647, abilityNames: 610, itemNames: 392 }
    },
    heartgold: {
      family: 'gen4',
      trdata: 'a/0/5/5',
      trpoke: 'a/0/5/6',
      personal: ['a/0/0/2'],
      learnset: 'a/0/3/3',
      moveData: 'a/0/1/1',
      textPath: 'a/0/2/7',
      textOffsets: { pokemonNames: 237, trainerNames: 729, trainerClasses: 730, moveNames: 750, abilityNames: 720, itemNames: 222 }
    },
    soulsilver: {
      family: 'gen4',
      trdata: 'a/0/5/5',
      trpoke: 'a/0/5/6',
      personal: ['a/0/0/2'],
      learnset: 'a/0/3/3',
      moveData: 'a/0/1/1',
      textPath: 'a/0/2/7',
      textOffsets: { pokemonNames: 237, trainerNames: 729, trainerClasses: 730, moveNames: 750, abilityNames: 720, itemNames: 222 }
    },
    black: {
      family: 'gen5',
      trdata: 'a/0/9/2',
      trpoke: 'a/0/9/3',
      personal: ['a/0/1/6'],
      learnset: 'a/0/1/8',
      moveData: 'a/0/2/1',
      textPath: 'a/0/0/2',
      textOffsets: { pokemonNames: 70, trainerNames: 190, trainerClasses: 191, moveNames: 203, abilityNames: 182, itemNames: 54 }
    },
    white: {
      family: 'gen5',
      trdata: 'a/0/9/2',
      trpoke: 'a/0/9/3',
      personal: ['a/0/1/6'],
      learnset: 'a/0/1/8',
      moveData: 'a/0/2/1',
      textPath: 'a/0/0/2',
      textOffsets: { pokemonNames: 70, trainerNames: 190, trainerClasses: 191, moveNames: 203, abilityNames: 182, itemNames: 54 }
    },
    black2: {
      family: 'gen5',
      trdata: 'a/0/9/1',
      trpoke: 'a/0/9/2',
      personal: ['a/0/1/6'],
      learnset: 'a/0/1/8',
      moveData: 'a/0/2/1',
      textPath: 'a/0/0/2',
      textOffsets: { pokemonNames: 90, trainerNames: 382, trainerClasses: 383, moveNames: 403, abilityNames: 374, itemNames: 64 }
    },
    white2: {
      family: 'gen5',
      trdata: 'a/0/9/1',
      trpoke: 'a/0/9/2',
      personal: ['a/0/1/6'],
      learnset: 'a/0/1/8',
      moveData: 'a/0/2/1',
      textPath: 'a/0/0/2',
      textOffsets: { pokemonNames: 90, trainerNames: 382, trainerClasses: 383, moveNames: 403, abilityNames: 374, itemNames: 64 }
    }
  };

  const IDCODE_TO_GAME = {
    ADAE: 'diamond', ADAF: 'diamond',
    APAE: 'pearl', APAF: 'pearl',
    CPUE: 'platinum', CPUF: 'platinum',
    IPKE: 'heartgold', IPKF: 'heartgold',
    IPGE: 'soulsilver', IPGF: 'soulsilver',
    IRBO: 'black', IRBF: 'black',
    IRAO: 'white', IRAF: 'white',
    IREO: 'black2', IREF: 'black2',
    IRDO: 'white2', IRDF: 'white2'
  };

  function ascii(bytes) {
    return Array.from(bytes || []).map(b => (b >= 32 && b <= 126 ? String.fromCharCode(b) : '')).join('').replace(/\0/g, '').trim();
  }

  function read16(view, offset) { return view.getUint16(offset, true); }
  function read32(view, offset) { return view.getUint32(offset, true); }

  function cleanupTextValue(value) {
    let text = String(value || '');
    text = text.replace(/\uf000|\u0100/g, '');
    text = text.replace(/\[PK\]\[MN\]/g, 'Pokémon');
    text = text.replace(/\\\[PK]\\\[MN]/g, 'Pokémon');
    text = text.replace(/\\and/g, '&');
    text = text.replace(/\\n|\\r/g, ' ');
    text = text.replace(/\\xFFFF/gi, '').replace(/\\x0000/gi, '').replace(/\\xF000/gi, '');
    text = text.replace(/\\x[0-9A-Fa-f]{4}/g, '');
    text = text.replace(/\s+/g, ' ').trim();
    if (/^-+$/.test(text)) return '';
    return text;
  }

  function rotateRight16(value, count) {
    return ((value >>> count) | ((value << (16 - count)) & 0xFFFF)) & 0xFFFF;
  }

  function detectGameKey(idCode, filename = '') {
    if (IDCODE_TO_GAME[idCode]) return IDCODE_TO_GAME[idCode];
    const upper = String(filename || '').toUpperCase();
    if (upper.includes('BLACK VERSION 2') || upper.includes('NOIRE 2')) return 'black2';
    if (upper.includes('WHITE VERSION 2') || upper.includes('BLANCHE 2')) return 'white2';
    if (upper.includes('BLACK VERSION') || upper.includes('VERSION NOIRE')) return 'black';
    if (upper.includes('WHITE VERSION') || upper.includes('VERSION BLANCHE')) return 'white';
    if (upper.includes('PLATINE') || upper.includes('PLATINUM')) return 'platinum';
    if (upper.includes('HEARTGOLD') || upper.includes('OR HEARTGOLD')) return 'heartgold';
    if (upper.includes('SOULSILVER') || upper.includes('ARGENT SOULSILVER')) return 'soulsilver';
    if (upper.includes('DIAMOND') || upper.includes('DIAMANT')) return 'diamond';
    if (upper.includes('PEARL') || upper.includes('PERLE')) return 'pearl';
    return null;
  }

  function detectLanguage(idCode, filename = '') {
    if (String(idCode || '').endsWith('F')) return 'fr';
    return 'en';
  }

  function detectRegion(filename = '') {
    const upper = String(filename || '').toUpperCase();
    if (upper.includes('FRANCE') || upper.includes('(F)')) return 'fr';
    if (upper.includes('USA')) return 'usa';
    if (upper.includes('EUROPE') || upper.includes('(E)')) return 'eu';
    return 'unknown';
  }

  function parseNarc(buffer) {
    const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    if (ascii(bytes.slice(0, 4)) !== 'NARC') throw new Error('NARC invalide');
    let pos = 0x10;
    let entries = [];
    let dataStart = 0;
    while (pos + 8 <= bytes.length) {
      const tag = ascii(bytes.slice(pos, pos + 4));
      const size = read32(view, pos + 4);
      if (!size || pos + size > bytes.length) break;
      if (tag === 'BTAF') {
        const fileCount = read16(view, pos + 8);
        let ep = pos + 12;
        entries = [];
        for (let i = 0; i < fileCount; i++, ep += 8) {
          entries.push({ start: read32(view, ep), end: read32(view, ep + 4) });
        }
      } else if (tag === 'GMIF' || tag === 'FIMG') {
        dataStart = pos + 8;
      }
      pos += size;
    }
    if (!dataStart || !entries.length) return [];
    return entries.map(entry => bytes.slice(dataStart + entry.start, dataStart + entry.end));
  }

  function buildPathMap(romBytes) {
    const view = new DataView(romBytes.buffer, romBytes.byteOffset, romBytes.byteLength);
    const fntOffset = read32(view, 0x40);
    const fatOffset = read32(view, 0x48);
    const fatSize = read32(view, 0x4C);
    const fileCount = Math.floor(fatSize / 8);
    const fatEntries = [];
    for (let i = 0; i < fileCount; i++) {
      const pos = fatOffset + i * 8;
      fatEntries.push({ start: read32(view, pos), end: read32(view, pos + 4) });
    }
    const rootDirOffset = read32(view, fntOffset);
    const dirCount = read16(view, fntOffset + 6);
    const dirs = [];
    for (let i = 0; i < dirCount; i++) {
      const pos = fntOffset + i * 8;
      dirs.push({
        subTableOffset: read32(view, pos),
        firstFileId: read16(view, pos + 4),
        parentId: read16(view, pos + 6)
      });
    }
    const pathMap = {};
    function walkDir(dirIndex, basePath) {
      const dir = dirs[dirIndex];
      if (!dir) return;
      let pos = fntOffset + dir.subTableOffset;
      let fileId = dir.firstFileId;
      while (pos < romBytes.length) {
        const length = romBytes[pos++];
        if (!length) break;
        const isDirectory = !!(length & 0x80);
        const nameLength = length & 0x7F;
        const name = ascii(romBytes.slice(pos, pos + nameLength));
        pos += nameLength;
        if (isDirectory) {
          const subDirId = read16(view, pos);
          pos += 2;
          walkDir(subDirId - 0xF000, `${basePath}${name}/`);
        } else {
          pathMap[`${basePath}${name}`] = fileId;
          fileId += 1;
        }
      }
    }
    walkDir(0, '');
    return {
      pathMap,
      fileEntries: fatEntries,
      getFile(path) {
        const id = pathMap[path];
        if (typeof id !== 'number') return null;
        const entry = fatEntries[id];
        if (!entry) return null;
        return romBytes.slice(entry.start, entry.end);
      }
    };
  }

  function decodeGen4TextEntry(raw) {
    const table = (window.NDS_TEXT_TABLES && window.NDS_TEXT_TABLES.gen4) || {};
    const bytes = raw instanceof Uint8Array ? raw.slice() : new Uint8Array(raw);
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const count = read16(view, 0);
    let key = read16(view, 2);
    let sdidx = 4;
    key = (key * 0x2FD) & 0xFFFF;
    for (let i = 0; i < count; i++) {
      const key2 = (key * (i + 1)) & 0xFFFF;
      const realKey = (key2 | (key2 << 16)) >>> 0;
      const v1 = (read32(view, sdidx) ^ realKey) >>> 0;
      const v2 = (read32(view, sdidx + 4) ^ realKey) >>> 0;
      new DataView(bytes.buffer, bytes.byteOffset + sdidx, 4).setUint32(0, v1, true);
      new DataView(bytes.buffer, bytes.byteOffset + sdidx + 4, 4).setUint32(0, v2, true);
      sdidx += 8;
    }
    const outEntries = [];
    for (let i = 0; i < count; i++) {
      const ptr = read32(view, 4 + i * 8);
      const chars = read32(view, 8 + i * 8);
      let localKey = (0x91BD3 * (i + 1)) & 0xFFFF;
      let idx = ptr;
      let words = [];
      for (let k = 0; k < chars; k++) {
        const val = read16(view, idx) ^ localKey;
        words.push(val);
        localKey = (localKey + 0x493D) & 0xFFFF;
        idx += 2;
      }
      if (words.length && words[0] === 0xF100) {
        const uncomp = [];
        let j = 1, shift1 = 0, trans = 0;
        while (j < words.length) {
          if (shift1 >= 0xF) {
            shift1 -= 0xF;
            if (shift1 > 0) {
              const tmp1 = trans | ((words[j] << (9 - shift1)) & 0x1FF);
              if (tmp1 === 0x1FF) break;
              uncomp.push(tmp1);
            }
          } else {
            const tmp1 = (words[j] >>> shift1) & 0x1FF;
            if (tmp1 === 0x1FF) break;
            uncomp.push(tmp1);
            shift1 += 9;
            if (shift1 < 0xF) {
              trans = (words[j] >>> shift1) & 0x1FF;
              shift1 += 9;
            }
            j += 1;
          }
        }
        words = uncomp;
      }
      const out = [];
      for (let n = 0; n < words.length; n++) {
        const curr = words[n];
        if (Object.prototype.hasOwnProperty.call(table, String(curr))) {
          out.push(table[String(curr)]);
        } else if (curr === 0xFFFE) {
          n += 1;
          if (n < words.length) out.push('\\v' + words[n].toString(16).toUpperCase().padStart(4, '0'));
          n += 1;
          const total = n < words.length ? words[n] : 0;
          if (!total) out.push('\\x0000');
          for (let z = 0; z < total; z++) {
            n += 1;
            if (n < words.length) out.push('\\z' + words[n].toString(16).toUpperCase().padStart(4, '0'));
          }
        } else if (curr === 0xFFFF) {
          break;
        } else {
          out.push('\\x' + curr.toString(16).toUpperCase().padStart(4, '0'));
        }
      }
      outEntries.push(cleanupTextValue(out.join('')));
    }
    return outEntries;
  }

  function decodeGen5TextEntry(raw) {
    const tableRaw = (window.NDS_TEXT_TABLES && window.NDS_TEXT_TABLES.gen5) || {};
    const replacements = Object.entries(tableRaw).map(([k, v]) => [String.fromCodePoint(Number(k)), v]);
    const bytes = raw instanceof Uint8Array ? raw : new Uint8Array(raw);
    const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
    const numSections = read16(view, 0);
    const numEntries = read16(view, 2);
    if (numSections < 1) return [];
    const sectionOffset = read32(view, 12);
    let pos = sectionOffset + 4;
    const tableOffsets = [];
    const charCounts = [];
    for (let i = 0; i < numEntries; i++, pos += 8) {
      tableOffsets.push(read32(view, pos));
      charCounts.push(read16(view, pos + 4));
    }
    const entries = [];
    for (let j = 0; j < numEntries; j++) {
      pos = sectionOffset + tableOffsets[j];
      const chars = [];
      for (let k = 0; k < charCounts[j]; k++) chars.push(read16(view, pos + k * 2));
      if (!chars.length) { entries.push(''); continue; }
      let key = chars[chars.length - 1] ^ 0xFFFF;
      const dec = new Array(chars.length);
      for (let k = chars.length - 1; k >= 0; k--) {
        dec[k] = chars[k] ^ key;
        key = rotateRight16(key, 3);
      }
      let finalWords = dec;
      if (finalWords.length && finalWords[0] === 0xF100) {
        const uncomp = [];
        let idx = 1, shift1 = 0, trans = 0;
        while (idx < finalWords.length) {
          if (shift1 >= 0x10) {
            shift1 -= 0x10;
            if (shift1 > 0) {
              const tmp1 = trans | ((finalWords[idx] << (9 - shift1)) & 0x1FF);
              if ((tmp1 & 0xFF) === 0xFF) break;
              if (tmp1 !== 0x0 && tmp1 !== 0x1) uncomp.push(tmp1);
            }
          } else {
            const tmp1 = (finalWords[idx] >>> shift1) & 0x1FF;
            if ((tmp1 & 0xFF) === 0xFF) break;
            if (tmp1 !== 0x0 && tmp1 !== 0x1) uncomp.push(tmp1);
            shift1 += 9;
            if (shift1 < 0x10) {
              trans = (finalWords[idx] >>> shift1) & 0x1FF;
              shift1 += 9;
            }
            idx += 1;
          }
        }
        finalWords = uncomp;
      }
      let text = '';
      for (const val of finalWords) {
        if (val === 0xFFFF) text += '\\xFFFF';
        else if (val > 20 && val <= 0xFFF0) {
          try { text += String.fromCodePoint(val); } catch (e) { text += '\\x' + val.toString(16).toUpperCase().padStart(4, '0'); }
        } else text += '\\x' + val.toString(16).toUpperCase().padStart(4, '0');
      }
      for (const [src, repl] of replacements) text = text.split(src).join(repl);
      entries.push(cleanupTextValue(text));
    }
    return entries;
  }

  function parseGen4Learnsets(files) {
    const learnsets = {};
    files.forEach((raw, speciesId) => {
      if (!speciesId) return;
      const view = new DataView(raw.buffer, raw.byteOffset, raw.byteLength);
      const entries = [];
      for (let offset = 0; offset + 2 <= raw.length; offset += 2) {
        const value = read16(view, offset);
        if (value === 0xFFFF) break;
        const moveId = value & 0x01FF;
        const level = value >>> 9;
        if (moveId) entries.push({ move_id: moveId, level });
      }
      learnsets[speciesId] = entries;
    });
    return learnsets;
  }

  function parseGen5Learnsets(files) {
    const learnsets = {};
    files.forEach((raw, speciesId) => {
      if (!speciesId) return;
      const view = new DataView(raw.buffer, raw.byteOffset, raw.byteLength);
      const entries = [];
      for (let offset = 0; offset + 4 <= raw.length; offset += 4) {
        const moveId = read16(view, offset);
        const level = read16(view, offset + 2);
        if (moveId === 0xFFFF && level === 0xFFFF) break;
        if (moveId) entries.push({ move_id: moveId, level });
      }
      learnsets[speciesId] = entries;
    });
    return learnsets;
  }

  function getLevelUpMoves(speciesId, level, learnsets) {
    const entries = learnsets[speciesId] || [];
    return entries.filter(entry => entry.level <= level).slice(-4);
  }

  function parsePersonalEntry(raw, family) {
    return family === 'gen4'
      ? {
          baseStats: { hp: raw[0], atk: raw[1], def: raw[2], spd: raw[3], spAtk: raw[4], spDef: raw[5] },
          type1: raw[6], type2: raw[7], ability1: raw[22], ability2: raw[23], ability3: 0
        }
      : {
          baseStats: { hp: raw[0], atk: raw[1], def: raw[2], spd: raw[3], spAtk: raw[4], spDef: raw[5] },
          type1: raw[6], type2: raw[7], ability1: raw[24], ability2: raw[25], ability3: raw[26]
        };
  }

  function parseMoveDataMap(files, cfg, moveNames, lang) {
    const moveData = {};
    const familyTypeKeys = TYPE_KEYS[cfg.family] || {};
    files.forEach((raw, moveId) => {
      if (!moveId || !raw || !raw.length) return;
      const detail = {
        id: moveId,
        name: moveNames[moveId] || `Move #${moveId}`,
        type: null,
        damageClass: null,
        power: null,
        accuracy: null,
        accuracyKnown: true,
        pp: null,
      };
      if (cfg.family === 'gen4') {
        const catMap = ['physical', 'special', 'status'];
        detail.type = familyTypeKeys[raw[4]] || null;
        detail.damageClass = catMap[raw[2]] || null;
        detail.power = raw[3] || null;
        detail.accuracy = raw[5] || null;
        detail.pp = raw[6] || null;
      } else {
        const catMap = ['status', 'physical', 'special'];
        detail.type = familyTypeKeys[raw[0]] || null;
        detail.damageClass = catMap[raw[2]] || null;
        detail.power = raw[3] || null;
        detail.accuracy = raw[4] || null;
        detail.pp = raw[5] || null;
      }
      if (detail.accuracy === 0) detail.accuracy = null;
      moveData[moveId] = detail;
    });
    return moveData;
  }

  function ivFromDifficulty(value) {
    return value >= 255 ? 31 : Math.floor(value * 31 / 255);
  }

  function genderFromMisc(value) {
    return ({ 0: 'Random', 1: 'Male', 2: 'Female' })[value & 0x0F] || 'Random';
  }

  function abilityChoiceFromMisc(value) {
    return value >> 4;
  }

  function resolveAbilityNames(choice, personalEntry, abilityNames, lang, cfg) {
    const ids = [];
    const a1 = personalEntry.ability1 || 0;
    const a2 = personalEntry.ability2 || 0;
    const a3 = personalEntry.ability3 || 0;
    if (cfg.family === 'gen4' && (cfg === GAME_CONFIGS.diamond || cfg === GAME_CONFIGS.pearl || cfg === GAME_CONFIGS.platinum)) {
      if (a1) ids.push(a1);
    } else if (choice === 1 && a1) ids.push(a1);
    else if (choice === 2 && a2) ids.push(a2);
    else if (choice === 3 && a3) ids.push(a3);
    else [a1, a2, a3].forEach(id => { if (id && !ids.includes(id)) ids.push(id); });
    return {
      label: (ABILITY_SLOT_LABELS[lang] || ABILITY_SLOT_LABELS.en)[choice] || ABILITY_SLOT_LABELS[lang][0],
      ids,
      names: ids.map(id => abilityNames[id] || `Ability #${id}`)
    };
  }

  function parseTrainerEntry(idx, trdata, trpoke, cfg, resources, trainerNames, trainerClasses, lang) {
    if (!trdata || trdata.length < 20) return null;
    const speciesNames = resources.species;
    const moveNames = resources.moves;
    const moveDataMap = resources.moveData;
    const itemNames = resources.items;
    const abilityNames = resources.abilities;
    const personal = resources.personal;
    const learnsets = resources.learnsets;
    const view = new DataView(trdata.buffer, trdata.byteOffset, trdata.byteLength);
    const flags = trdata[0];
    const hasMoves = (flags & 1) === 1;
    const hasItems = (flags & 2) === 2;
    const trainerClass = trdata[1];
    const battleType = trdata[2];
    const numPokemon = trdata[3];
    const ai = read32(view, 12);
    const battleType2 = trdata[16];
    const trainerItemIds = [];
    const trainerItems = [];
    for (let offset = 4; offset < 12; offset += 2) {
      const itemId = read16(view, offset);
      if (!itemId) continue;
      trainerItemIds.push(itemId);
      trainerItems.push(itemNames[itemId] || `Item #${itemId}`);
    }
    const baseLen = cfg.family === 'gen4' ? 6 : 8;
    const extraLen = cfg.family === 'gen4' && cfg !== GAME_CONFIGS.diamond && cfg !== GAME_CONFIGS.pearl ? 2 : 0;
    const segmentLen = baseLen + (hasItems ? 2 : 0) + (hasMoves ? 8 : 0) + extraLen;
    const party = [];
    for (let monIndex = 0; monIndex < numPokemon; monIndex++) {
      const start = monIndex * segmentLen;
      if (start + baseLen > trpoke.length) break;
      const difficulty = trpoke[start];
      const misc = trpoke[start + 1];
      const pokeView = new DataView(trpoke.buffer, trpoke.byteOffset, trpoke.byteLength);
      const level = read16(pokeView, start + 2);
      let ball = 0;
      let speciesId = 0;
      let formId = 0;
      let unknown = 0;
      if (cfg.family === 'gen4') {
        const speciesWord = read16(pokeView, start + 4);
        speciesId = (speciesWord & 0xFF) + (((speciesWord >> 8) & 0x01) << 8);
        formId = (speciesWord >> 10) & 0x3F;
        unknown = (speciesWord >> 9) & 0x01;
      } else {
        ball = trpoke[start + 3];
        speciesId = read16(pokeView, start + 4);
        formId = read16(pokeView, start + 6);
      }
      let cursor = start + baseLen;
      if (!speciesId) continue;
      let heldItemId = 0;
      let heldItem = '';
      if (hasItems && cursor + 2 <= trpoke.length) {
        heldItemId = read16(pokeView, cursor);
        heldItem = heldItemId ? (itemNames[heldItemId] || `Item #${heldItemId}`) : '';
        cursor += 2;
      }
      const moveIds = [];
      const moveLabels = [];
      const moveDetails = [];
      if (hasMoves && cursor + 8 <= trpoke.length) {
        for (let i = 0; i < 4; i++, cursor += 2) {
          const moveId = read16(pokeView, cursor);
          if (!moveId) continue;
          moveIds.push(moveId);
          moveLabels.push(moveNames[moveId] || `Move #${moveId}`);
          if (moveDataMap[moveId]) moveDetails.push({ ...moveDataMap[moveId] });
        }
      } else {
        getLevelUpMoves(speciesId, level, learnsets).forEach(entry => {
          moveIds.push(entry.move_id);
          moveLabels.push(moveNames[entry.move_id] || `Move #${entry.move_id}`);
          if (moveDataMap[entry.move_id]) moveDetails.push({ ...moveDataMap[entry.move_id] });
        });
      }
      cursor += extraLen;
      const personalEntry = personal[speciesId] || { type1: 0, type2: 0, ability1: 0, ability2: 0, ability3: 0 };
      const typeIds = [personalEntry.type1];
      if (personalEntry.type2 !== personalEntry.type1) typeIds.push(personalEntry.type2);
      const familyTypeKeys = TYPE_KEYS[cfg.family] || {};
      const typeKeys = typeIds.map(id => familyTypeKeys[id]).filter(Boolean);
      const abilityInfo = resolveAbilityNames(abilityChoiceFromMisc(misc), personalEntry, abilityNames, lang, cfg);
      const iv = ivFromDifficulty(difficulty);
      party.push({
        speciesId,
        species: speciesNames[speciesId] || `Pokémon #${speciesId}`,
        formId,
        level,
        sex: genderFromMisc(misc),
        heldItemId,
        heldItem,
        movesetIds: moveIds,
        moveset: moveLabels,
        moveDetails,
        movesSource: 'rom',
        types: typeKeys,
        typeIds,
        abilityChoice: abilityChoiceFromMisc(misc),
        abilityLabel: abilityInfo.label,
        abilities: abilityInfo.names,
        abilityIds: abilityInfo.ids,
        baseStats: personalEntry.baseStats || {},
        ivs: { hp: iv, atk: iv, def: iv, spAtk: iv, spDef: iv, spd: iv },
        difficulty,
        ball,
        unknown
      });
    }
    if (!party.length) return null;
    const trainerName = (idx > 0 && idx <= trainerNames.length ? trainerNames[idx - 1] : '') || trainerClasses[trainerClass] || `Trainer ${idx}`;
    return {
      trainerId: idx,
      name: trainerName,
      trainerClassId: trainerClass,
      trainerClassName: trainerClasses[trainerClass] || '',
      battleType,
      battleType2,
      trainerItemIds,
      trainerItems,
      ai,
      party
    };
  }

  function parseRom(buffer, filename = '') {
    if (!window.NDS_TEXT_TABLES) throw new Error('Tables texte NDS manquantes');
    const romBytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    if (romBytes.length < 0x200) throw new Error('ROM trop petite');
    const headerTitle = ascii(romBytes.slice(0x00, 0x0C));
    const idCode = ascii(romBytes.slice(0x0C, 0x10));
    const gameKey = detectGameKey(idCode, filename);
    if (!gameKey || !GAME_CONFIGS[gameKey]) throw new Error(`ROM DS non prise en charge (${idCode || 'code inconnu'})`);
    const cfg = GAME_CONFIGS[gameKey];
    const lang = detectLanguage(idCode, filename);
    const region = detectRegion(filename);
    const fs = buildPathMap(romBytes);
    const readPath = path => {
      const data = fs.getFile(path);
      if (!data) throw new Error(`Fichier ROM introuvable: ${path}`);
      return data;
    };
    const textNarc = parseNarc(readPath(cfg.textPath));
    const textOffsets = cfg.textOffsets;
    const decodeText = cfg.family === 'gen4' ? decodeGen4TextEntry : decodeGen5TextEntry;
    const species = decodeText(textNarc[textOffsets.pokemonNames]);
    const trainerNames = (() => {
      const entries = decodeText(textNarc[textOffsets.trainerNames]);
      return entries.length && !entries[0] ? entries.slice(1) : entries;
    })();
    const trainerClasses = decodeText(textNarc[textOffsets.trainerClasses]);
    const moves = decodeText(textNarc[textOffsets.moveNames]);
    const abilities = decodeText(textNarc[textOffsets.abilityNames]);
    const items = decodeText(textNarc[textOffsets.itemNames]);
    const personalPath = cfg.personal.find(path => !!fs.getFile(path));
    if (!personalPath) throw new Error('Données personal introuvables');
    const personalFiles = parseNarc(readPath(personalPath));
    const personal = {};
    personalFiles.forEach((raw, speciesId) => { personal[speciesId] = parsePersonalEntry(raw, cfg.family); });
    const learnsetFiles = parseNarc(readPath(cfg.learnset));
    const learnsets = cfg.family === 'gen4' ? parseGen4Learnsets(learnsetFiles) : parseGen5Learnsets(learnsetFiles);
    const moveFiles = parseNarc(readPath(cfg.moveData));
    const moveData = parseMoveDataMap(moveFiles, cfg, moves, lang);
    const trdataFiles = parseNarc(readPath(cfg.trdata));
    const trpokeFiles = parseNarc(readPath(cfg.trpoke));
    const trainers = [];
    const limit = Math.min(trdataFiles.length, trpokeFiles.length);
    for (let idx = 0; idx < limit; idx++) {
      const trainer = parseTrainerEntry(idx, trdataFiles[idx], trpokeFiles[idx], cfg, { species, moves, items, abilities, personal, learnsets, moveData }, trainerNames, trainerClasses, lang);
      if (trainer) trainers.push(trainer);
    }
    const title = (GAME_TITLES[gameKey] && GAME_TITLES[gameKey][lang]) || headerTitle || gameKey;
    return {
      meta: {
        parser: 'browser-rom',
        title,
        game: gameKey,
        family: cfg.family,
        language: lang,
        region,
        idCode,
        sourceFile: filename || `${gameKey}.nds`,
        romTitle: headerTitle
      },
      trainers,
      lookups: {
        moveEntries: moves.map((name, id) => id ? ({
          id,
          name,
          ...(moveData[id] || {})
        }) : null).filter(Boolean),
        abilityEntries: abilities.map((name, id) => id ? ({ id, name }) : null).filter(Boolean),
        itemEntries: items.map((name, id) => id ? ({ id, name }) : null).filter(Boolean),
        speciesEntries: species.map((name, id) => {
          if (!id) return null;
          const personalEntry = personal[id] || { type1: 0, type2: 0, ability1: 0, ability2: 0, ability3: 0, baseStats: {} };
          const familyTypeKeys = TYPE_KEYS[cfg.family] || {};
          const typeIds = [personalEntry.type1];
          if (personalEntry.type2 && personalEntry.type2 !== personalEntry.type1) typeIds.push(personalEntry.type2);
          const types = typeIds.map(typeId => familyTypeKeys[typeId]).filter(Boolean);
          const abilityIds = [personalEntry.ability1, personalEntry.ability2, personalEntry.ability3].filter(Boolean);
          const abilityLabels = abilityIds.map(abilityId => abilities[abilityId]).filter(Boolean);
          return {
            id,
            name,
            typeIds,
            types,
            baseStats: personalEntry.baseStats || {},
            abilityIds,
            abilities: abilityLabels
          };
        }).filter(Boolean),
        game: gameKey,
        family: cfg.family,
        language: lang
      }
    };
  }

  window.NDSRomParser = { parse: parseRom };
})();
