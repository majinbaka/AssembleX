# AssembleX Part Data Schema

## 1. Muc tieu tai lieu

Tai lieu nay chot schema cho `part_data` de:

1. team content co format nhat quan khi them part moi
2. `stat_resolver` compile duoc `CombatantSnapshot` dung contract trong `combat_spec.md`
3. UI co du metadata de hien inventory, garage va battle preview
4. upgrade system tach ro giua `base definition` va `level scaling`

Tai lieu nay chi cover:

- `part_data`
- `part_level_data`
- enum va field contract lien quan
- compile mapping tu data sang snapshot

Tai lieu nay khong cover:

- enemy roster day du
- economy chi tiet
- scene setup hoac asset pipeline

## 2. Nguyen tac schema

Schema part cho MVP phai giu 5 tinh chat:

1. `data-first`: runner khong hard-code logic rieng cho tung part
2. `slot-safe`: moi part chi hop le voi 1 slot ro rang
3. `compile-friendly`: de bien thanh `CombatantSnapshot` bang quy tac on dinh
4. `ui-friendly`: co du text/tags de garage va tooltip dung lai
5. `upgrade-light`: effect logic co the giu nguyen, chi scale o cac moc duoc cho phep

## 3. Pham vi data

He thong nen tach thanh 2 lop:

1. `part_data`
2. `part_level_data`

`part_data` la definition co dinh cua part.

`part_level_data` la bang scaling theo level. Tach rieng de:

- de balance hang loat
- tranh lap lai field
- cho phep doi curve ma khong doi identity part

## 4. Dinh danh va enum chinh thuc

## 4.1. Slot enum

- `head`
- `core`
- `left_arm`
- `right_arm`
- `legs`
- `module`

## 4.2. Rarity enum

- `common`
- `rare`
- `epic`

`legendary` khong ton tai trong MVP.

## 4.3. Weapon family enum

- `laser`
- `impact`
- `drill`
- `shield`
- `support`

Ghi chu:

- `laser` dung cho `Laser Emitter`, `Capacitor Gun`
- `impact` dung cho `Ram Fist`, `Hammer Unit`
- `drill` dung cho `Drill Cannon`
- `shield` dung cho arm tao phong cach phong thu
- `support` chi dung neu can arm utility khong dong vai basic profile chinh

MVP co the chua dung het enum, nhung schema nen khoa tu dau.

## 4.4. Stat key enum

Stats compile truc tiep vao `base_stats`:

- `hp`
- `atk`
- `def`
- `spd`
- `energy_regen`
- `max_energy`
- `acc`
- `eva`
- `crit_rate`

Stats compile vao `derived_stats`:

- `skill_damage_mult`
- `burn_taken_mult`
- `reflect_basic_ratio`
- `extra_energy_on_hit`
- `extra_energy_on_miss`
- `receive_hit_energy_bonus`

## 4.5. Passive type enum

- `gain_energy_on_miss`
- `on_basic_hit_gain_energy`
- `on_receive_hit_gain_energy`
- `modify_skill_damage_mult`
- `modify_burn_taken_mult`
- `reflect_basic_damage`
- `grant_same_family_bonus`
- `grant_on_hit_effect`
- `grant_proc_chance`

Neu can logic moi, phai them type moi vao schema va combat compile rules, khong dung `script_name` tuy y.

## 4.6. Effect type enum

- `burn`
- `stun`
- `shield`
- `break_armor`

## 4.7. Skill ref enum MVP

- `overheat_beam`
- `shock_ram`
- `bulwark_pulse`
- `capacitor_dump`
- `piercing_drill`

## 5. PartData schema

## 5.1. Schema tong quat

```json
{
  "id": "laser_emitter",
  "slot": "left_arm",
  "name": "Laser Emitter",
  "rarity": "common",
  "version": 1,
  "tags": ["starter", "burn", "laser"],
  "icon_key": "part_laser_emitter",
  "sort_order": 100,
  "is_obtainable": true,
  "unlock": {
    "source_type": "starter"
  },
  "ui": {
    "title": "Laser Emitter",
    "short_description": "Arm laser co skill Burn co ban.",
    "archetype_hint": "burn_tempo",
    "strength_hint": "gay pressure theo nhiep bang Burn",
    "weakness_hint": "khong burst manh vao muc tieu shield day"
  },
  "compile": {
    "stat_bonuses": [],
    "derived_stat_bonuses": [],
    "passives": [],
    "skill_ref": "overheat_beam",
    "weapon_contribution": {
      "family": "laser",
      "role": "primary",
      "weapon_multiplier": 1.0,
      "same_family_bonus": {
        "burn_chance_bonus": 0.1
      },
      "offhand_passives": [],
      "on_hit_effects": []
    }
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "arm_common_a",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 5.2. Field bat buoc

- `id`
- `slot`
- `name`
- `rarity`
- `version`
- `tags`
- `ui`
- `compile`
- `upgrade`

## 5.3. Field rules

### `id`

- snake_case
- duy nhat toan bo game data
- khong doi sau khi da phat hanh neu co save data

### `slot`

- phai thuoc `slot enum`
- moi part chi co 1 slot duy nhat

### `tags`

Dung cho:

- filter inventory
- build suggestion
- future analytics

Tag khuyen nghi trong MVP:

- `starter`
- `campaign_drop`
- `burn`
- `stun`
- `shield`
- `energy`
- `crit`
- `tank`
- `evasion`
- `anti_tank`
- `laser`
- `impact`
- `drill`

### `unlock`

Schema toi thieu:

```json
{
  "source_type": "starter"
}
```

Gia tri hop le cua `source_type`:

- `starter`
- `stage_drop`
- `stage_clear`
- `craft`
- `boss_reward`

Neu can them metadata:

```json
{
  "source_type": "stage_clear",
  "stage_id": "rust_yard_03"
}
```

### `ui`

`ui` la data player-facing, khong dung cho resolve combat. Cac field bat buoc:

- `title`
- `short_description`
- `archetype_hint`
- `strength_hint`
- `weakness_hint`

### `compile`

La khoi quan trong nhat, dung de build `CombatantSnapshot`.

### `upgrade`

Field bat buoc:

- `max_level`
- `curve_id`
- `effect_upgrade_points`

Rule:

- `max_level = 5` trong MVP
- `effect_upgrade_points` chi duoc chua `3` va/hoac `5`
- khong cho moc nang effect ngoai cac moc nay neu chua doi balance rule

## 6. Compile block schema

## 6.1. Flat stat bonus

```json
{
  "stat_bonuses": [
    {
      "stat": "atk",
      "value": 6
    },
    {
      "stat": "acc",
      "value": 8
    }
  ]
}
```

Rule:

- `value` la flat bonus tru khi `mode` duoc khai bao ro
- MVP uu tien flat bonus de balance de doc

Neu can modifier %, dung format:

```json
{
  "stat": "energy_regen",
  "value": 0.2,
  "mode": "multiplier"
}
```

`mode` hop le:

- `flat`
- `multiplier`

Mac dinh la `flat`.

## 6.2. Derived stat bonus

```json
{
  "derived_stat_bonuses": [
    {
      "stat": "skill_damage_mult",
      "value": 0.12,
      "mode": "add_ratio"
    }
  ]
}
```

`mode` hop le:

- `flat`
- `add_ratio`
- `set_min`
- `set_max`

Quy uoc compile:

- `skill_damage_mult` bat dau tu `1.0`, `add_ratio 0.12` thanh `1.12`
- `burn_taken_mult` bat dau tu `1.0`, `add_ratio -0.3` thanh `0.7`
- `reflect_basic_ratio` bat dau tu `0.0`, `add_ratio 0.12` thanh `0.12`

## 6.3. Passive schema

```json
{
  "passives": [
    {
      "type": "gain_energy_on_miss",
      "value": 5
    }
  ]
}
```

Passive co the co them `params`:

```json
{
  "type": "grant_proc_chance",
  "value": 0.08,
  "params": {
    "proc_key": "break_armor_on_basic_hit"
  }
}
```

Rule:

- `type` phai thuoc `passive type enum`
- `value` la scalar chinh
- `params` chi dung khi passive can them context

## 6.4. Skill binding

Chi `left_arm` moi duoc co `skill_ref`.

```json
{
  "skill_ref": "shock_ram"
}
```

Rule:

- `left_arm` bat buoc co `skill_ref`
- slot khac phai de `null` hoac omit
- `right_arm` khong duoc quyen tranh `Primary Skill`

## 6.5. Weapon contribution schema

```json
{
  "weapon_contribution": {
    "family": "laser",
    "role": "primary",
    "weapon_multiplier": 1.0,
    "same_family_bonus": {
      "burn_chance_bonus": 0.1
    },
    "offhand_passives": [
      {
        "type": "on_basic_hit_gain_energy",
        "value": 2
      }
    ],
    "on_hit_effects": [
      {
        "effect_type": "break_armor",
        "chance": 0.08,
        "duration_ticks": 20
      }
    ]
  }
}
```

Field rules:

- `family` bat buoc voi `left_arm` va `right_arm`
- `role` hop le: `primary`, `offhand`, `support`
- `weapon_multiplier` chi dung cho `primary`
- `same_family_bonus` chi duoc dung neu part co logic synergy khi 2 arm cung family
- `offhand_passives` la passive runtime them vao `weapon_profile`
- `on_hit_effects` la packet effect cua basic attack

## 6.6. On-hit effect schema

```json
{
  "effect_type": "burn",
  "chance": 0.1,
  "duration_ticks": 20,
  "max_stacks": 3,
  "magnitude_mode": "source_atk_ratio",
  "magnitude_value": 0.04
}
```

Field rules:

- `chance` nam trong `0.0 - 1.0`
- `duration_ticks` phai phu hop `combat_spec.md`
- `magnitude_mode` hop le:
  - `flat`
  - `source_atk_ratio`
  - `target_max_hp_ratio`
  - `shield_ratio`

MVP chu yeu dung:

- `burn` voi `source_atk_ratio = 0.04`
- `break_armor` khong can `magnitude_value`
- `stun` khong can `magnitude_value`

## 7. PartLevelData schema

## 7.1. Schema tong quat

```json
{
  "part_id": "laser_emitter",
  "levels": {
    "1": {
      "stat_bonuses": [],
      "derived_stat_bonuses": [],
      "effect_overrides": {}
    },
    "2": {
      "stat_bonuses": [
        {
          "stat": "atk",
          "value": 2
        }
      ],
      "derived_stat_bonuses": [],
      "effect_overrides": {}
    },
    "3": {
      "stat_bonuses": [
        {
          "stat": "atk",
          "value": 4
        }
      ],
      "derived_stat_bonuses": [],
      "effect_overrides": {
        "weapon_contribution.same_family_bonus.burn_chance_bonus": 0.12
      }
    }
  }
}
```

## 7.2. Rule

- `part_id` phai tro toi mot `part_data.id`
- moi level tu `1` den `5` phai ton tai
- level `1` la baseline
- `effect_overrides` chi duoc dung tai cac moc nam trong `effect_upgrade_points`

## 7.3. Upgrade cost schema

Neu muon gom economy reference vao cung data, dung schema:

```json
{
  "upgrade_costs": {
    "2": { "coins": 100, "scrap": 20 },
    "3": { "coins": 180, "scrap": 35 },
    "4": { "coins": 320, "scrap": 60 },
    "5": { "coins": 520, "scrap": 100 }
  }
}
```

Rare part co the them:

```json
{
  "5": { "coins": 520, "scrap": 100, "core_shard": 1 }
}
```

Neu team muon tach economy khoi schema nay, van duoc. Khi do `curve_id` chi can tro sang `economy_balance_sheet.md`.

## 8. Compile mapping sang CombatantSnapshot

## 8.1. Thu tu compile chinh thuc

1. load `part_data` theo `slots`
2. load `part_level_data` theo level tung slot
3. cong `stat_bonuses` cua tat ca part
4. ap dung `multiplier` neu co
5. build `derived_stats`
6. bind `primary_skill` tu `left_arm.skill_ref`
7. build `weapon_profile` tu `left_arm.weapon_contribution` + `right_arm.weapon_contribution`
8. append `passives` tu `head`, `core`, `module`, va offhand arm neu co
9. clamp theo `combat_spec.md`

## 8.2. Mapping quy uoc

### Head

- thuong them `acc`, `crit_rate`, hoac `extra_energy_on_miss`
- khong doi target rule bang code

### Core

- thuong them `energy_regen`, `max_energy`, `skill_damage_mult`, `receive_hit_energy_bonus`

### Left Arm

- la nguon `primary_skill`
- dong vai `weapon_profile` chinh khi basic attack

### Right Arm

- neu cung family voi left arm: them `same_family_bonus`
- neu khac family: chi dong gop `offhand_passives` va `on_hit_effects`

### Legs

- thuong them `spd`, `eva`, `hp`, `def`

### Module

- thuong them `burn_taken_mult`, `reflect_basic_ratio`, `energy_regen` modifier, `acc`

## 8.3. Weapon profile build rule

Input:

- `left_arm.compile.weapon_contribution`
- `right_arm.compile.weapon_contribution`

Output:

```json
{
  "family": "laser",
  "weapon_multiplier": 1.0,
  "same_family_bonus": {
    "burn_chance_bonus": 0.1
  },
  "offhand_passives": [
    {
      "type": "on_basic_hit_gain_energy",
      "value": 2
    }
  ],
  "on_hit_effects": []
}
```

Rule:

1. `family` va `weapon_multiplier` lay tu `left_arm`
2. neu `right_arm.family == left_arm.family`, merge `same_family_bonus`
3. neu khac family, bo qua `right_arm.weapon_multiplier`
4. `offhand_passives` va `on_hit_effects` tu `right_arm` van duoc merge vao profile

## 9. Validation rules bat buoc

## 9.1. Data validation

- `id` duy nhat
- `slot` hop le
- `rarity` hop le
- `max_level = 5`
- `left_arm` phai co `skill_ref`
- `right_arm` khong duoc co `skill_ref`
- `weapon_multiplier` cua arm nam trong `0.85 - 1.25` tru khi co phe duyet balance rieng
- `chance` nam trong `0.0 - 1.0`
- `effect_type` phai thuoc enum duoc phep

## 9.2. Combat guardrail validation

Sau compile, snapshot phai duoc clamp theo `combat_spec.md`:

- `max_energy <= 160`
- `energy_regen_bonus_percent <= 35%`
- `crit_rate` clamp `0.0 - 0.75`

Part data khong nen dat gia tri khien build nao cung vuot guardrail de tranh content "hop le schema nhung sai balance".

## 9.3. Save compatibility

Neu mot part doi meaning compile, phai tang `version`.

Khuyen nghi:

- save game luu `part_id` + `part_version`
- migration layer map version cu sang schema moi neu can

## 10. Vi du part MVP

## 10.1. Head: Analyzer Node

```json
{
  "id": "analyzer_node",
  "slot": "head",
  "name": "Analyzer Node",
  "rarity": "rare",
  "version": 1,
  "tags": ["energy", "stability"],
  "icon_key": "part_analyzer_node",
  "sort_order": 210,
  "is_obtainable": true,
  "unlock": {
    "source_type": "stage_clear",
    "stage_id": "rust_yard_04"
  },
  "ui": {
    "title": "Analyzer Node",
    "short_description": "Tang max energy va hoi energy khi danh hut.",
    "archetype_hint": "energy_tempo",
    "strength_hint": "giu nhip cast skill on dinh hon",
    "weakness_hint": "khong tang damage truc tiep"
  },
  "compile": {
    "stat_bonuses": [
      {
        "stat": "max_energy",
        "value": 10
      }
    ],
    "derived_stat_bonuses": [],
    "passives": [
      {
        "type": "gain_energy_on_miss",
        "value": 5
      }
    ],
    "skill_ref": null,
    "weapon_contribution": null
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "head_rare_a",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 10.2. Core: Burst Core

```json
{
  "id": "burst_core",
  "slot": "core",
  "name": "Burst Core",
  "rarity": "rare",
  "version": 1,
  "tags": ["energy", "burst", "skill"],
  "icon_key": "part_burst_core",
  "sort_order": 320,
  "is_obtainable": true,
  "unlock": {
    "source_type": "craft"
  },
  "ui": {
    "title": "Burst Core",
    "short_description": "Energy regen on va skill damage tang.",
    "archetype_hint": "skill_burst",
    "strength_hint": "day tempo skill nhanh va manh",
    "weakness_hint": "khong them phong thu"
  },
  "compile": {
    "stat_bonuses": [
      {
        "stat": "energy_regen",
        "value": 6
      }
    ],
    "derived_stat_bonuses": [
      {
        "stat": "skill_damage_mult",
        "value": 0.12,
        "mode": "add_ratio"
      }
    ],
    "passives": [],
    "skill_ref": null,
    "weapon_contribution": null
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "core_rare_a",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 10.3. Left Arm: Laser Emitter

```json
{
  "id": "laser_emitter",
  "slot": "left_arm",
  "name": "Laser Emitter",
  "rarity": "common",
  "version": 1,
  "tags": ["laser", "burn", "starter"],
  "icon_key": "part_laser_emitter",
  "sort_order": 410,
  "is_obtainable": true,
  "unlock": {
    "source_type": "starter"
  },
  "ui": {
    "title": "Laser Emitter",
    "short_description": "Arm laser co basic on dinh va skill Burn.",
    "archetype_hint": "burn_tempo",
    "strength_hint": "giam mau doi thu deu theo thoi gian",
    "weakness_hint": "it utility khi gap shield day"
  },
  "compile": {
    "stat_bonuses": [],
    "derived_stat_bonuses": [],
    "passives": [],
    "skill_ref": "overheat_beam",
    "weapon_contribution": {
      "family": "laser",
      "role": "primary",
      "weapon_multiplier": 1.0,
      "same_family_bonus": {
        "burn_chance_bonus": 0.1
      },
      "offhand_passives": [],
      "on_hit_effects": []
    }
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "arm_common_a",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 10.4. Right Arm: Hammer Unit

```json
{
  "id": "hammer_unit",
  "slot": "right_arm",
  "name": "Hammer Unit",
  "rarity": "common",
  "version": 1,
  "tags": ["impact", "anti_tank", "break_armor"],
  "icon_key": "part_hammer_unit",
  "sort_order": 470,
  "is_obtainable": true,
  "unlock": {
    "source_type": "stage_drop",
    "stage_id": "guard_walker_01"
  },
  "ui": {
    "title": "Hammer Unit",
    "short_description": "Offhand tao co hoi Break Armor cho basic attack.",
    "archetype_hint": "anti_tank",
    "strength_hint": "mo khoa sat thuong vao muc tieu DEF cao",
    "weakness_hint": "khong tang toc do energy"
  },
  "compile": {
    "stat_bonuses": [],
    "derived_stat_bonuses": [],
    "passives": [],
    "skill_ref": null,
    "weapon_contribution": {
      "family": "impact",
      "role": "offhand",
      "weapon_multiplier": 1.0,
      "same_family_bonus": {},
      "offhand_passives": [],
      "on_hit_effects": [
        {
          "effect_type": "break_armor",
          "chance": 0.08,
          "duration_ticks": 20
        }
      ]
    }
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "arm_common_b",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 10.5. Legs: Sprint Legs

```json
{
  "id": "sprint_legs",
  "slot": "legs",
  "name": "Sprint Legs",
  "rarity": "common",
  "version": 1,
  "tags": ["speed", "tempo", "starter"],
  "icon_key": "part_sprint_legs",
  "sort_order": 520,
  "is_obtainable": true,
  "unlock": {
    "source_type": "starter"
  },
  "ui": {
    "title": "Sprint Legs",
    "short_description": "Tang toc tan cong nhung doi bang do ben.",
    "archetype_hint": "tempo",
    "strength_hint": "basic attack nhanh hon",
    "weakness_hint": "HP tong thap hon"
  },
  "compile": {
    "stat_bonuses": [
      {
        "stat": "spd",
        "value": 0.25
      },
      {
        "stat": "hp",
        "value": -10
      }
    ],
    "derived_stat_bonuses": [],
    "passives": [],
    "skill_ref": null,
    "weapon_contribution": null
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "legs_common_a",
    "effect_upgrade_points": []
  }
}
```

## 10.6. Module: Reflect Plate

```json
{
  "id": "reflect_plate",
  "slot": "module",
  "name": "Reflect Plate",
  "rarity": "rare",
  "version": 1,
  "tags": ["tank", "reflect", "anti_basic"],
  "icon_key": "part_reflect_plate",
  "sort_order": 630,
  "is_obtainable": true,
  "unlock": {
    "source_type": "boss_reward",
    "stage_id": "neon_arena_02"
  },
  "ui": {
    "title": "Reflect Plate",
    "short_description": "Phan sat thuong basic attack nhan vao.",
    "archetype_hint": "anti_basic",
    "strength_hint": "trung phat doi thu danh basic nhieu",
    "weakness_hint": "khong counter duoc skill burst"
  },
  "compile": {
    "stat_bonuses": [],
    "derived_stat_bonuses": [
      {
        "stat": "reflect_basic_ratio",
        "value": 0.12,
        "mode": "add_ratio"
      }
    ],
    "passives": [
      {
        "type": "reflect_basic_damage",
        "value": 0.12
      }
    ],
    "skill_ref": null,
    "weapon_contribution": null
  },
  "upgrade": {
    "max_level": 5,
    "curve_id": "module_rare_a",
    "effect_upgrade_points": [3, 5]
  }
}
```

## 11. Dinh dang luu tru khuyen nghi

Co 2 cach hop le cho MVP:

### Cach A: 1 file / 1 part

```text
data/parts/head/analyzer_node.json
data/parts/core/burst_core.json
data/parts/left_arm/laser_emitter.json
```

Uu diem:

- de review
- conflict git nho
- de patch tung part

### Cach B: 1 file index / 1 slot

```text
data/parts/head_parts.json
data/parts/core_parts.json
data/parts/arm_parts.json
```

Uu diem:

- de load bulk
- de xem toan bo balance mot slot

Khuyen nghi cho repo nay:

- `part_data`: `1 file / 1 part`
- `part_level_data`: co the gom theo slot hoac theo `curve_id`

## 12. Test cases data bat buoc

1. moi `left_arm` co `skill_ref` hop le
2. moi `right_arm` khong co `skill_ref`
3. compile build `Laser + Laser` tao `same_family_bonus.burn_chance_bonus`
4. compile build `Laser + Hammer` giu `family = laser`
5. `Reflect Plate` chi tao `reflect_basic_ratio`, khong them stat ngoai y dinh
6. `Heat Sink` compile ra `burn_taken_mult = 0.7`
7. `Burst Core` compile ra `skill_damage_mult = 1.12`
8. level data khong override effect ngoai moc `3` hoac `5`

## 13. Quyet dinh chot trong tai lieu nay

1. `part_data` va `part_level_data` tach rieng
2. `compile` la block chinh, khong dat stat/effect o root rai rac
3. `right_arm` khong duoc bind active skill
4. `weapon_profile` luon lay `left_arm` lam profile basic chinh
5. effect upgrade chi duoc doi o level `3` va `5`
6. passive phai qua `type enum`, khong nhung script name tuy y vao data

## 14. Tai lieu tiep theo

Sau `part_data_schema.md`, nen viet:

1. `enemy_roster.md`
2. `economy_balance_sheet.md`
3. `godot_system_architecture.md`

Vi den muc nay contract part da du ro de:

- team content dien data part
- team code viet validator va stat compiler
- team UI dung chung tooltip va filter
