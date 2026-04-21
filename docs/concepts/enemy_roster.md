# AssembleX Enemy Roster

> **Document policy (2026-04 update):** Đây là tài liệu gốc để mở rộng dài hạn.
>
> - Không rút gọn/xóa nội dung lớn nếu chưa có quyết định design rõ ràng.
> - Mọi cập nhật mới nên theo kiểu **bổ sung versioned addendum** (MVP/Phase 2/Phase 3).
> - Nội dung MVP chỉ là lớp con của tài liệu này, không thay thế toàn bộ tầm nhìn dài hạn.


## 1. Muc tieu tai lieu

Tai lieu nay chot contract cho `enemy roster` cua AssembleX MVP de:

1. team content author enemy bang data thay vi hard-code trong scene
2. team code compile enemy thanh `CombatantSnapshot` dung contract trong `combat_spec.md`
3. UI co du du lieu de hien `enemy preview`, `stage card` va `post-loss hint`
4. campaign co roster nhat quan, moi enemy day nguoi choi 1 bai hoc build ro rang

Tai lieu nay cover:

- `enemy_archetype_data`
- `stage_encounter_data`
- compile rules tu enemy data sang `CombatantSnapshot`
- MVP roster va stage mapping de xuat cho launch

Tai lieu nay khong cover:

- reward economy chi tiet
- cutscene/dialogue
- scene animation cua tung enemy

## 2. Nguyen tac roster

Enemy roster cho MVP phai giu 5 tinh chat:

1. `same-rules`: enemy va player dung cung combat contract
2. `teach-through-fight`: moi enemy phai day it nhat 1 bai hoc build
3. `preview-readable`: truoc tran nguoi choi phai doc duoc moi de doa chinh
4. `data-first`: enemy identity, build va reward preview nam trong data
5. `small-tuning`: enemy co the duoc buff nhe, nhung khong duoc bien thanh "quai cong so" vo ly

## 3. Pham vi thiet ke

Enemy trong MVP la `robot combatant` duoc tao tu 3 lop:

1. `enemy_archetype_data`
2. `part_data` + `part_level_data`
3. `stage_encounter_data`

Y nghia:

- `enemy_archetype_data` dinh nghia danh tinh, build mau va preview
- `part_data` giu logic stat/skill/passive thong nhat voi player
- `stage_encounter_data` dat enemy vao campaign voi level, tuning va reward phu hop

Contract nay giup:

- tai su dung 1 archetype o nhieu stage
- tranh viec copy 1 enemy thanh 5 file gan giong nhau
- de test balance theo `enemy_ref + stage modifier`

## 4. Data flow truoc battle

```text
stage_encounter_data
  + enemy_archetype_data
  + part_data
  + part_level_data
  -> build enemy loadout
  -> compile base snapshot
  -> apply encounter tuning
  -> clamp guardrail
  -> enemy CombatantSnapshot
```

Enemy snapshot cuoi cung phai co cung schema voi player snapshot trong `combat_spec.md`.

## 5. Enemy archetype schema

## 5.1. Schema tong quat

```json
{
  "id": "burner_unit",
  "display_name": "Burner Unit",
  "tier": "regular",
  "tags": ["burn", "tempo", "zone_1"],
  "preview": {
    "summary": "Gay Burn deu va snowball neu tran keo dai.",
    "threat_tags": ["burn", "high_hit_rate"],
    "counter_tags": ["heat_sink", "fast_burst"],
    "danger_rating": 2
  },
  "build": {
    "slots": {
      "head": "analyzer_node",
      "core": "stable_core",
      "left_arm": "laser_emitter",
      "right_arm": "capacitor_gun",
      "legs": "sprint_legs",
      "module": "targeting_lens"
    },
    "part_levels": {
      "head": 1,
      "core": 1,
      "left_arm": 1,
      "right_arm": 1,
      "legs": 1,
      "module": 1
    }
  },
  "tuning": {
    "flat_stat_bonuses": {
      "hp": 0,
      "atk": 0,
      "def": 0
    },
    "derived_stat_bonuses": {},
    "notes": "Chi dung de canh pace stage, khong thay doi gimmick."
  },
  "authoring": {
    "design_lesson": "Day nguoi choi ve DOT va nhu cau dung Heat Sink.",
    "failure_hint_focus": "thieu counter Burn"
  }
}
```

## 5.2. Field bat buoc

- `id`
- `display_name`
- `tier`
- `tags`
- `preview`
- `build`
- `authoring`

`tuning` co the rong, nhung field van nen ton tai de schema on dinh.

## 5.3. Enum chinh thuc

### `tier`

- `regular`
- `elite`
- `boss`

### `preview.threat_tags`

- `burn`
- `stun`
- `shield`
- `break_armor`
- `reflect`
- `burst`
- `high_eva`
- `high_def`
- `high_hit_rate`
- `energy_tempo`

### `preview.counter_tags`

- `heat_sink`
- `targeting_lens`
- `break_armor`
- `piercing_drill`
- `burst_damage`
- `shield_break`
- `high_def`
- `sustain`

`danger_rating` dung thang `1-5` cho UI. MVP khong can cong thuc tu dong phuc tap.

## 6. Stage encounter schema

## 6.1. Schema tong quat

```json
{
  "id": "rust_yard_03",
  "zone_id": "rust_yard",
  "stage_index": 3,
  "encounter_type": "regular",
  "enemy_ref": "burner_unit",
  "seed": 10303,
  "level_profile": {
    "head": 2,
    "core": 2,
    "left_arm": 2,
    "right_arm": 2,
    "legs": 2,
    "module": 2
  },
  "encounter_tuning": {
    "flat_stat_bonuses": {
      "hp": 10,
      "atk": 1
    },
    "derived_stat_bonuses": {}
  },
  "preview_override": {
    "summary": null,
    "recommended_power_note": "Can counter Burn on dinh."
  },
  "rewards": {
    "first_clear": {
      "coins": 90,
      "scrap": 18,
      "core_shard": 0
    },
    "repeat_clear": {
      "coins": 70,
      "scrap": 14,
      "core_shard_drop_rate": 0.0
    }
  }
}
```

## 6.2. Field rules

### `enemy_ref`

- phai tro toi `enemy_archetype_data.id` hop le
- 1 archetype co the duoc dung lai o nhieu stage

### `level_profile`

- override `build.part_levels` cua archetype cho stage cu the
- neu bo trong slot nao, lay level mac dinh tu archetype
- MVP nen giu cac slot cung cap level de doc balance de hon

### `encounter_tuning`

- chi duoc dung cho canh pace stage
- khong duoc them effect moi khong co trong `part_data`
- boss co the dung offset lon hon regular, nhung van phai qua clamp guardrail

### `rewards`

- chi giu preview va target cho content
- cong thuc kinh te cu the se duoc chot o `economy_balance_sheet.md`

## 7. Compile rules cho enemy snapshot

1. doc `enemy_archetype_data.build`
2. merge `stage_encounter_data.level_profile`
3. compile build bang cung `stat_resolver` cua player
4. cong `archetype.tuning.flat_stat_bonuses` vao `base_stats`
5. cong `encounter_tuning.flat_stat_bonuses` vao `base_stats`
6. cong `derived_stat_bonuses` theo thu tu archetype -> encounter
7. clamp theo guardrail trong `combat_spec.md`
8. set `unit_id = enemy`
9. dat `display_name` bang `stage preview name` neu co override, neu khong thi dung `archetype.display_name`

Quy tac quan trong:

- enemy khong co stat hay effect nao ma player system khong hieu
- khong co "boss-only combat code" nam ngoai data tru khi tai lieu khac chot ro
- moi enemy active skill van theo rule `left_arm`

## 8. Preview contract cho UI

Garage va stage card toi thieu can hien:

- `display_name`
- `tier`
- `preview.summary`
- toi da `2 threat_tags`
- toi da `2 counter_tags`
- `danger_rating`

Khong nen lo qua nhieu chi so tho. Preview cua MVP la de nguoi choi nhin ra:

- doi thu dang muon lam gi
- build nao co kha nang tra loi

Vi du:

```text
Burner Unit
Threat: Burn, High Hit Rate
Counter: Heat Sink, Burst Damage
```

## 9. MVP roster chot

## 9.1. Scrap Brawler

- `id = scrap_brawler`
- `tier = regular`
- vai tro: enemy tutorial, thong so de doc
- bai hoc: hieu nhip `basic attack`, `stun`, va battle log co ban

Build de xuat:

- `head = scout_visor`
- `core = stable_core`
- `left_arm = ram_fist`
- `right_arm = hammer_unit`
- `legs = tank_treads`
- `module = targeting_lens`

Preview:

- `threat_tags = ["stun"]`
- `counter_tags = ["high_def"]`
- `danger_rating = 1`

## 9.2. Burner Unit

- `id = burner_unit`
- `tier = regular`
- vai tro: day nguoi choi ve `burn` va snowball theo thoi gian
- bai hoc: neu tran dai, `Heat Sink` va burst som co gia tri lon

Build de xuat:

- `head = analyzer_node`
- `core = stable_core`
- `left_arm = laser_emitter`
- `right_arm = capacitor_gun`
- `legs = sprint_legs`
- `module = targeting_lens`

Preview:

- `threat_tags = ["burn", "energy_tempo"]`
- `counter_tags = ["heat_sink", "burst_damage"]`
- `danger_rating = 2`

## 9.3. Guard Walker

- `id = guard_walker`
- `tier = regular`
- vai tro: day ve `shield` va nhu cau co anti-tank
- bai hoc: chi build damage deu co the bi keo tran va thua shield cycle

Build de xuat:

- `head = scout_visor`
- `core = guard_core`
- `left_arm = shield_projector`
- `right_arm = hammer_unit`
- `legs = tank_treads`
- `module = energy_coil`

Preview:

- `threat_tags = ["shield", "high_def"]`
- `counter_tags = ["piercing_drill", "shield_break"]`
- `danger_rating = 3`

## 9.4. Raider Duelist

- `id = raider_duelist`
- `tier = elite`
- vai tro: day ve `high_eva`, burst va combat tempo nhanh
- bai hoc: build thieu `ACC` se mat tran vi miss va thua trade burst

Build de xuat:

- `head = raider_chip`
- `core = burst_core`
- `left_arm = drill_cannon`
- `right_arm = capacitor_gun`
- `legs = balance_frame`
- `module = targeting_lens`

Preview:

- `threat_tags = ["break_armor", "high_eva", "burst"]`
- `counter_tags = ["targeting_lens", "sustain"]`
- `danger_rating = 4`

## 9.5. Iron Bastion Boss

- `id = iron_bastion_boss`
- `tier = boss`
- vai tro: boss zone 1, ep nguoi choi chuan bi counter tank ro rang
- gimmick: shield lon theo chu ky, neu khong pha duoc se bi keo tran roi thua
- bai hoc: `Piercing Drill`, burn tempo dai hoi, hoac skill burst dung cua so

Build de xuat:

- `head = scout_visor`
- `core = guard_core`
- `left_arm = shield_projector`
- `right_arm = hammer_unit`
- `legs = tank_treads`
- `module = reflect_plate`

Archetype tuning de xuat:

- `flat_stat_bonuses.hp = 35`
- `flat_stat_bonuses.def = 6`

Preview:

- `threat_tags = ["shield", "reflect", "high_def"]`
- `counter_tags = ["piercing_drill", "burn", "shield_break"]`
- `danger_rating = 5`

Ghi chu:

- do `Bulwark Pulse` co AI gate `hp_ratio <= 0.7`, boss nay se tao cua so "vao shield roi cau gio"
- neu can muc tieu "12 giay / 1 shield lon" nhu `concept.md`, can tinh lai `max_energy`, `energy_regen` va lock thong qua level/tuning thay vi them rule rieng

## 10. Stage mapping de xuat cho launch

Bang nay uu tien tai su dung it archetype nhung tang bai hoc ro rang theo stage.

| Stage | Enemy | Y do |
| --- | --- | --- |
| `rust_yard_01` | `scrap_brawler` | doc basic loop, stun co ban |
| `rust_yard_02` | `scrap_brawler` | check lai DEF va pace basic |
| `rust_yard_03` | `burner_unit` | gioi thieu Burn |
| `rust_yard_04` | `burner_unit` | buoc can nhac Heat Sink hoac burst |
| `rust_yard_05` | `guard_walker` | pre-boss anti-shield check |
| `rust_yard_06` | `iron_bastion_boss` | boss zone 1 |
| `neon_arena_01` | `raider_duelist` | gioi thieu Evasion + burst |
| `neon_arena_02` | `burner_unit` | test build co du on dinh khong |
| `neon_arena_03` | `guard_walker` | test anti-tank lan 2 |
| `neon_arena_04` | `raider_duelist` | check ACC nghiem tuc |
| `neon_arena_05` | `guard_walker` | pre-boss sustain va shield break |
| `neon_arena_06` | `raider_duelist` | tam dung elite tuning cao cho boss cuoi neu MVP launch chua co boss zone 2 rieng |

Dong cuoi la `production compromise`. Neu team co du scope content, nen thay `neon_arena_06` bang 1 boss rieng truoc content lock.

## 11. Encounter tuning guardrail

De tranh enemy bi "buff so" qua da:

- `regular`: tong flat bonus khuyen nghi khong vuot `+20 HP`, `+3 ATK`, `+3 DEF`
- `elite`: tong flat bonus khuyen nghi khong vuot `+30 HP`, `+4 ATK`, `+4 DEF`
- `boss`: tong flat bonus khuyen nghi khong vuot `+45 HP`, `+6 ATK`, `+6 DEF`

Neu can vuot moc nay, uu tien:

1. tang `part_levels`
2. doi part cho dung bai hoc
3. chi sau do moi cong them tuning

## 12. Test cases data bat buoc

1. moi `stage_encounter.enemy_ref` tro toi archetype hop le
2. moi `enemy_archetype.build.slots` du `6 slot`
3. moi `enemy_archetype.build.left_arm` compile ra `primary_skill` hop le
4. enemy snapshot sau compile dung cung schema `CombatantSnapshot` voi player
5. `burner_unit` preview co `burn` trong `threat_tags`
6. `guard_walker` co `left_arm = shield_projector`
7. `iron_bastion_boss.tier = boss`
8. `danger_rating` nam trong `1-5`
9. `encounter_tuning` khong them stat ngoai enum trong `combat_spec.md`
10. `neon_arena_06` bi canh bao neu van dung `raider_duelist` placeholder luc content lock

## 13. Quyet dinh chot trong tai lieu nay

1. enemy duoc build tu cung `part_data` system voi player
2. tuning enemy la lop nho, khong thay the build
3. preview phai hien `threat` va `counter`, khong chi la ten enemy
4. stage data tach rieng khoi archetype de tai su dung roster
5. boss van dung cung combat rules, khong co logic dac quyen rieng o runner

## 14. Tai lieu tiep theo

Sau `enemy_roster.md`, nen viet:

1. `economy_balance_sheet.md`
2. `godot_system_architecture.md`

Vi den muc nay team da co:

- contract part
- contract combat
- contract enemy va stage preview

Nhu vay da du de:

- code `enemy compiler`
- code validator `stage encounter`
- lap roster vertical slice va campaign launch ban dau

---

## 13. Addendum 2026-04 (authoring roster thuc te)

### 13.1. Mau phan bo encounter theo cam xuc nguoi choi

Trong moi zone 6 stage:

- stage `1-2`: day co che co ban, do kho vua
- stage `3-4`: bat dau ep nguoi choi doi build
- stage `5`: mini-kiem-tra counter
- stage `6`: boss tong hop bai hoc cua zone

### 13.2. Enemy readability checklist cho animator/VFX

Moi enemy can co:

- 1 dau hieu ro truoc skill nguy hiem (wind-up)
- 1 mau hieu ung uu tien theo threat chinh (vi du Burn = tone nong)
- 1 icon status de thay ngay effect dang tac dong

Khong dat readability vao animation dep hon thong tin.

### 13.3. Chinh sach buff/nerf roster sau playtest

- `regular`: uu tien tinh lai reward va preview truoc khi buff so
- `elite`: cho phep buff nhe `hp/def` neu bi clear qua de
- `boss`: neu bi "stat check", phai sua mechanic telegraph truoc khi tang chi so

### 13.4. Bang theo doi suc khoe roster moi sprint

- ti le clear first-attempt theo tung stage
- 3 ly do thua pho bien nhat theo stage
- ti le doi build truoc va sau stage kho
- so luong part duoc dung (de phat hien part bi that nghiep)
