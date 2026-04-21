# AssembleX Combat Spec

> **Document policy (2026-04 update):** Đây là tài liệu gốc để mở rộng dài hạn.
>
> - Không rút gọn/xóa nội dung lớn nếu chưa có quyết định design rõ ràng.
> - Mọi cập nhật mới nên theo kiểu **bổ sung versioned addendum** (MVP/Phase 2/Phase 3).
> - Nội dung MVP chỉ là lớp con của tài liệu này, không thay thế toàn bộ tầm nhìn dài hạn.


## 1. Muc tieu tai lieu

Tai lieu nay chot `combat loop` cho MVP cua AssembleX o muc do co the code truc tiep.

No tra loi 5 cau hoi:

1. battle chay theo `state flow` nao
2. event runtime duoc resolve theo `thu tu` nao
3. du lieu nao can duoc compile truoc khi vao tran
4. runtime state cua mot tran gom nhung gi
5. can log gi de debug, replay va hien thi post-battle

Tai lieu nay dung cho pham vi:

- `1v1`
- `semi-auto`
- `tick-based`
- `75s timeout`
- `MVP only`

Khong cover:

- `3v3`
- projectile thuc su co va cham trong scene
- action input thu cong
- online sync

## 2. Nguyen tac combat

Combat MVP phai giu 4 tinh chat:

1. `deterministic`: cung input, cung random seed thi ra cung ket qua
2. `readable`: event quan trong phai hien ra ro trong HUD va log
3. `data-first`: part, skill, effect, enemy duoc dinh nghia boi data
4. `small-number-high-meaning`: stat va effect it, nhung tac dong ro

## 3. Don vi mo phong

### 3.1. Tick va time

- `TICK_RATE = 0.2s`
- `TICKS_PER_SECOND = 5`
- `TIMEOUT_SECONDS = 75`
- `MAX_TICKS = 375`

Time trong runner nen duoc luu bang `tick_index` thay vi float. Neu can hien thi UI thi doi sang giay o lop presentation.

### 3.2. Random

Moi tran phai co:

- `battle_seed`
- `rng_state`

Tat ca hit roll, crit roll, proc roll deu lay tu cung RNG stream.

## 4. State Flow

```text
Garage Build
  -> Build Validation
  -> Stat Compile
  -> Combatant Snapshot Create
  -> Battle Init
  -> Tick Loop
  -> Winner Resolution
  -> Result Breakdown
  -> Reward / Rematch
```

### 4.1. Phase chi tiet

#### A. Build Validation

Check truoc khi vao tran:

- robot du `6 slot`
- moi slot dung item dung loai
- `Left Arm` xac dinh `Primary Skill`
- tong stat sau compile hop le
- enemy data hop le

#### B. Stat Compile

Bien `build loadout` thanh `compiled combat snapshot`.

Buoc nay resolve:

- stat base
- stat bonus tu part
- modifier % hop le
- skill gan voi `Left Arm`
- weapon profile tong hop tu hai arm
- head/module passive

#### C. Battle Init

Khoi tao state runtime:

- HP hien tai
- energy hien tai
- attack timer
- skill lock timer
- danh sach effect
- bo dem thong ke
- event log

#### D. Tick Loop

Moi tick resolve theo thu tu co dinh. Thu tu nay la contract quan trong nhat cua system.

#### E. Winner Resolution

Neu co robot chet, ket thuc ngay.

Neu het `MAX_TICKS`:

1. ai con `HP%` cao hon thang
2. neu bang nhau, ai `total_damage_dealt` cao hon thang
3. neu van bang nhau, enemy thang de tranh soft exploit farm draw

Muc 3 la `de xuat production default` do `concept.md` chua chot truong hop bang hoan toan.

## 5. Battle Order Contract

## 5.1. Tick order chinh thuc

Moi tick xu ly theo thu tu:

1. `start_of_tick hooks`
2. cong energy regen
3. giam duration effect
4. xu ly DOT
5. quyet dinh skill cast
6. cap nhat attack timer
7. resolve basic attack neu timer san sang
8. apply proc va on-hit effect
9. check death
10. ghi log tick summary neu can

Thu tu nay mo rong tu `concept.md` thanh event contract cu the de code va test.

### 5.2. Thu tu giua hai combatant trong cung mot tick

Trong tung buoc, runner luon resolve theo thu tu:

1. `player`
2. `enemy`

Tru khi can xep theo chi so. MVP khong dung initiative phuc tap. Neu ca hai cung co event hop le trong cung tick thi resolve `player` truoc de replay on dinh.

Day la `quyet dinh thiet ke bo sung` de tranh ket qua khac nhau do iteration order.

### 5.3. Quy tac "death gate"

Sau moi event gay damage, neu mot ben `hp <= 0`:

- danh dau `is_dead = true`
- ghi event `unit_down`
- chan moi event moi cua unit do
- khong cho resolve skill/basic attack con lai cua chinh no trong tick sau do

Neu `player` giet `enemy` o phase skill, enemy khong duoc basic attack sau do trong cung tick.

## 6. Data Flow truoc battle

```text
robot_build
  + part_data
  + upgrade_level
  + enemy_data
  -> stat_resolver
  -> weapon_profile_builder
  -> skill_binding
  -> passive_binding
  -> combatant_snapshot
```

## 6.1. Input schema toi thieu

```json
{
  "robot_id": "player_robot_01",
  "slots": {
    "head": "analyzer_node",
    "core": "stable_core",
    "left_arm": "laser_emitter",
    "right_arm": "capacitor_gun",
    "legs": "sprint_legs",
    "module": "heat_sink"
  },
  "part_levels": {
    "head": 1,
    "core": 1,
    "left_arm": 1,
    "right_arm": 1,
    "legs": 1,
    "module": 1
  }
}
```

## 6.2. CombatantSnapshot schema

Snapshot la du lieu da compile, khong con phu thuoc scene.

```json
{
  "unit_id": "player",
  "display_name": "Player Robot",
  "team": "player",
  "source_build_id": "player_robot_01",
  "base_stats": {
    "hp": 260,
    "atk": 31,
    "def": 18,
    "spd": 1.25,
    "energy_regen": 16,
    "max_energy": 90,
    "acc": 98,
    "eva": 8,
    "crit_rate": 0.12
  },
  "derived_stats": {
    "skill_damage_mult": 1.0,
    "burn_taken_mult": 0.7,
    "reflect_basic_ratio": 0.0,
    "extra_energy_on_hit": 2,
    "extra_energy_on_miss": 5,
    "receive_hit_energy_bonus": 0
  },
  "weapon_profile": {
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
  },
  "primary_skill": {
    "skill_id": "overheat_beam"
  },
  "passives": [
    {
      "type": "gain_energy_on_miss",
      "value": 5
    }
  ]
}
```

### 6.3. Compile rules

1. Cong tat ca `flat stat` truoc
2. Ap dung `modifier %` sau
3. Clamp theo guardrail cua MVP
4. Gan `primary_skill` tu `Left Arm`
5. Build `weapon_profile` tu `Left Arm` + `Right Arm`
6. Gan `head/module/core` passives vao snapshot

## 7. Runtime Battle State

## 7.1. BattleState schema

```json
{
  "battle_id": "battle_2026_04_20_001",
  "seed": 123456,
  "tick": 0,
  "elapsed_ticks": 0,
  "phase": "running",
  "timeout_ticks": 375,
  "player": {},
  "enemy": {},
  "event_log": [],
  "result": null
}
```

## 7.2. UnitRuntimeState schema

```json
{
  "unit_id": "player",
  "snapshot_ref": "player_snapshot",
  "current_hp": 260,
  "current_energy": 0,
  "shield_hp": 0,
  "is_dead": false,
  "attack_cooldown_ticks": 0,
  "skill_lock_ticks": 0,
  "effects": [],
  "runtime_flags": {
    "skip_basic_attack": false,
    "skip_skill_cast": false
  },
  "counters": {
    "basic_attacks": 0,
    "basic_hits": 0,
    "basic_misses": 0,
    "skill_casts": 0,
    "damage_dealt_total": 0,
    "damage_taken_total": 0,
    "damage_by_source": {
      "basic": 0,
      "skill": 0,
      "burn": 0,
      "reflect": 0
    },
    "status_uptime_ticks": {
      "burn": 0,
      "stun": 0,
      "shield": 0,
      "break_armor": 0
    }
  }
}
```

## 7.3. EffectInstance schema

```json
{
  "instance_id": "burn_player_0004",
  "effect_type": "burn",
  "source_unit_id": "enemy",
  "applied_tick": 12,
  "remaining_ticks": 20,
  "magnitude": 1.24,
  "stack_group": "burn",
  "stack_index": 2
}
```

`magnitude` phai la gia tri da snapshot o luc apply. Vi du Burn lay theo `4% ATK nguon gay hieu ung` tai thoi diem gay hieu ung, khong recompute moi tick.

## 8. Stat va cong thuc

## 8.1. Stat list chinh thuc

- `hp`
- `atk`
- `def`
- `spd`
- `energy_regen`
- `max_energy`
- `acc`
- `eva`
- `crit_rate`

Stats runtime phat sinh:

- `shield_hp`
- `skill_damage_mult`
- `burn_taken_mult`
- `reflect_basic_ratio`
- `extra_energy_on_hit`
- `extra_energy_on_miss`
- `receive_hit_energy_bonus`

## 8.2. Formula

### Basic raw damage

```text
raw_damage = attacker_atk * weapon_multiplier
```

### Skill raw damage

```text
raw_damage = attacker_atk * skill_multiplier * skill_damage_mult
```

`skill_damage_mult` la stat phat sinh tu part, vi du `Burst Core`.

### Defense reduction

```text
post_def_damage = raw_damage * (100 / (100 + effective_target_def))
```

### Crit

```text
if crit:
  post_def_damage = post_def_damage * 1.5
```

### Hit chance

```text
hit_chance = clamp(attacker_acc - target_eva, 20, 95)
```

### Attack interval

```text
attack_interval_seconds = 1 / spd
attack_interval_ticks = ceil(attack_interval_seconds / 0.2)
```

Dung `ceil` de giu pace de doc va khong cho toc do vuot qua tick grid.

### Damage rounding

MVP dung quy tac:

```text
final_damage = max(1, floor(post_def_damage))
```

Neu bi shield chan het thi HP khong mat.

## 8.3. Clamp guardrails

- `max_energy <= 160`
- `energy_regen_bonus_percent <= 35%` tu module
- `crit_rate` nen clamp `0% - 75%` de tranh crit build vo balance
- `hit_chance` da clamp `20 - 95`

Clamp crit la `de xuat production default`, vi `concept.md` chua neu guardrail nay.

## 9. Energy System

## 9.1. Sources

- hoi tu nhien moi tick: `energy_regen * 0.2`
- `+6` khi basic attack hit
- `+4 + receive_hit_energy_bonus` khi nhan damage tu basic attack
- `+8 + receive_hit_energy_bonus` khi nhan damage tu skill
- passive khac neu co, vi du `gain 5 energy when miss`

## 9.2. Rules

- energy khong vuot `max_energy`
- skill cast chi check sau khi cong energy regen va xu ly DOT
- cast xong tru energy ngay
- khong co cast time trong MVP
- co `skill_lock_ticks = ceil(cooldown_lock / 0.2)`

## 9.3. Rounding

De tranh float drift, energy runtime nen luu o don vi `integer x10`.

Vi du:

- `16 energy_regen / s`
- moi tick nhan `32` don vi noi bo
- UI chia lai cho `10`

Day la `de xuat ky thuat` de implementation on dinh hon; neu team muon luu float thi van duoc, nhung test replay phai co epsilon ro rang.

## 10. Basic Attack Spec

## 10.1. Attack timer init

Moi unit vao tran voi:

```text
attack_cooldown_ticks = attack_interval_ticks
```

Khong cho free hit ngay tick 0. Dieu nay giu battle co nhip doc duoc va de canh tranh cong bang.

## 10.2. Attack timer update

Moi tick:

1. neu `is_dead`, bo qua
2. neu dang `stun`, timer van giam
3. `attack_cooldown_ticks -= 1`
4. neu `attack_cooldown_ticks <= 0`, unit duoc quyen basic attack
5. sau khi resolve xong, reset timer ve `attack_interval_ticks`

De timer van giam khi stun giup debuff nay la "mat luot tan cong" thay vi lam lech pha vinh vien.

## 10.3. Basic attack event flow

```text
basic_attack_declared
  -> hit_roll
  -> if miss: miss handlers
  -> if hit: crit_roll
  -> raw damage
  -> def reduction
  -> shield absorption
  -> hp loss
  -> on-hit energy gain
  -> on-take-basic-hit energy gain
  -> on-hit proc
  -> reflect
  -> death check
```

### 10.4. Miss handling

Khi miss:

- khong gay damage
- khong duoc `+6 basic hit energy`
- target khong duoc `receive-hit energy`
- passive `gain_energy_on_miss` neu co duoc apply
- van reset attack timer

## 10.5. Weapon profile rules

### Same family

Neu hai arm cung family:

- giu `family` do lam profile chinh
- them `same_family_bonus` tu data

### Mixed family

Neu khac family:

- `Left Arm` quyet dinh profile basic chinh
- `Right Arm` chi them passive/offhand modifier

Vi du:

- `Laser + Laser` -> them `burn_chance_bonus`
- `Laser + Hammer` -> basic van la laser, hammer them `break_armor_proc_chance`

## 11. Skill Spec

## 11.1. Skill ownership

- `Primary Skill` luon den tu `Left Arm`
- chi co `1 skill active`/robot trong MVP

## 11.2. Skill cast gate

Unit duoc cast neu thoa tat ca:

1. khong chet
2. khong dang stun
3. `skill_lock_ticks == 0`
4. `current_energy >= energy_cost`
5. AI condition cua skill cho phep

## 11.3. Skill categories MVP

- `direct_damage`
- `damage_burn`
- `stun_strike`
- `self_shield`
- `energy_burst`
- `break_armor_strike`

`break_armor_strike` duoc tach ro trong spec vi vi du `Piercing Drill` can mot category ro rang cho data va UI, du `concept.md` liet ke 5 nhom high-level.

## 11.4. Skill runtime flow

```text
skill_check
  -> ai_gate
  -> spend_energy
  -> apply_skill_lock
  -> emit skill_cast_start
  -> resolve hit if skill requires hit
  -> resolve damage/effect payload
  -> grant post-cast energy effects if any
  -> death check
```

### 11.5. Hit logic cho skill

MVP dung quy tac:

- `damage`, `damage_burn`, `stun_strike`, `energy_burst`, `break_armor_strike` phai qua `hit_roll`
- `self_shield` khong can hit

Day la `suy dien hop ly` tu logic ACC/EVA cua combat MVP; can giu nhat quan tren UI va balance.

## 11.6. Skill definitions MVP

### Overheat Beam

- `skill_id = overheat_beam`
- `energy_cost = 50`
- `multiplier = 1.8`
- `on_hit = apply 1 burn`
- `cooldown_lock = 0.4s`

### Shock Ram

- `skill_id = shock_ram`
- `energy_cost = 45`
- `multiplier = 1.4`
- `on_hit = apply stun 1.2s`
- `cooldown_lock = 0.4s`

### Bulwark Pulse

- `skill_id = bulwark_pulse`
- `energy_cost = 40`
- `shield_value = 30% max_hp`
- `cooldown_lock = 0.4s`

### Capacitor Dump

- `skill_id = capacitor_dump`
- `energy_cost = 60`
- `multiplier = 2.2`
- `on_crit = gain 20 energy`
- `cooldown_lock = 0.4s`

### Piercing Drill

- `skill_id = piercing_drill`
- `energy_cost = 55`
- `multiplier = 1.6`
- `on_hit = apply break_armor 4s`
- `cooldown_lock = 0.4s`

## 11.7. Shield skill AI gate

`Bulwark Pulse` chi cast neu:

- `hp_ratio <= 0.7`
- va `shield_hp == 0`

Dieu kien `shield_hp == 0` la bo sung can thiet de tranh AI spam shield vao luc van con shield cu.

## 12. Status Effect Spec

## 12.1. Burn

### Definition

- DOT moi giay bang `4% ATK nguon gay`
- duration `4s`
- toi da `3 stack`
- moi stack la mot `EffectInstance` rieng

### Runtime

- `remaining_ticks = 20`
- tick DOT moi `5 tick`
- moi stack track bo dem rieng

### Apply rule

1. neu chua du 3 stack, them stack moi
2. neu da du 3 stack, thay stack cu nhat bang stack moi

Quy tac thay stack cu nhat la `de xuat production default`. `concept.md` moi chot la stack cong don va refresh rieng tung stack.

### Damage rule

```text
burn_damage = source_atk_snapshot * 0.04 * target_burn_taken_mult
```

`Heat Sink` lam giam `target_burn_taken_mult`.

## 12.2. Stun

### Definition

- duration `1.2s`
- `remaining_ticks = 6`
- khong stack
- neu ap dung moi dai hon thi refresh

### Effect

- khong duoc basic attack
- khong duoc cast skill
- van nhan energy regen
- van bi DOT
- attack timer van tiep tuc giam

## 12.3. Shield

### Definition

- ton tai toi da `5s`
- `remaining_ticks = 25`
- khong stack
- neu shield moi lon hon shield hien tai thi thay the

### Runtime

Shield la mot state rieng:

- `shield_hp` luu tren `UnitRuntimeState`
- effect instance chi can luu duration va source

### Absorb order

1. damage vao shield truoc
2. phan con lai moi vao HP
3. neu shield ve `0`, emit event `shield_broken`

## 12.4. Break Armor

### Definition

- duration `4s`
- `remaining_ticks = 20`
- khong stack
- refresh duration neu apply lai

### Effect

```text
effective_target_def = floor(base_runtime_def * 0.75)
```

`base_runtime_def` o day la DEF sau compile va stat modifier khac, nhung truoc damage calculation cua tung hit.

Khong cho Break Armor "an chong" voi chinh no.

## 12.5. Effect tick semantics

Vi tick order giam duration truoc DOT, quy tac can chot ro:

- effect duoc apply trong tick N se bat dau co tac dung ngay neu payload yeu cau ngay lap tuc
- DOT Burn bat dau gay sat thuong tu tick DOT tiep theo, khong dot ngay luc apply
- effect het duration khi `remaining_ticks <= 0` truoc khi den phase cua no

Dieu nay giup log ro rang va tranh burn "double dip" trong cung tick vua apply.

## 13. AI Spec

## 13.1. MVP AI loop

Moi tick, AI lam 2 viec:

1. kiem tra co du dieu kien cast skill khong
2. neu khong, de basic attack van chay theo timer

AI khong:

- doi target
- giu energy de combo
- doc status doi thu sau o muc phuc tap

## 13.2. AI rules theo skill type

- `self_shield`: chi cast neu `hp_ratio <= 0.7` va `shield_hp == 0`
- `stun_strike`: cast ngay khi du energy
- `direct_damage`: cast ngay khi du energy
- `damage_burn`: cast ngay khi du energy
- `energy_burst`: cast ngay khi du energy
- `break_armor_strike`: cast ngay khi du energy

## 13.3. Head modifier hooks

Head khong thay target rule, chi them modifier:

- `Hunter Head`: `+10 ACC`
- `Analyzer Head`: `+5 energy when miss`
- `Raider Head`: `+8% crit rate`

Nhung modifier nay phai duoc compile vao snapshot, khong resolve bang code hard-coded trong runner.

## 14. Damage Resolution Contract

## 14.1. Generic damage packet

Moi nguon damage nen duoc resolve qua cung mot packet:

```json
{
  "source_unit_id": "player",
  "target_unit_id": "enemy",
  "source_type": "basic",
  "can_crit": true,
  "can_miss": true,
  "raw_damage": 31.0,
  "tags": ["laser"],
  "applied_effects": []
}
```

## 14.2. Damage resolve order

```text
miss check
  -> crit check
  -> defense reduction
  -> shield absorb
  -> hp damage
  -> retaliation/reflect
  -> on-damage energy gain
  -> statistics update
  -> event emit
```

Reflect phai xay ra sau khi damage chinh da vao target, va reflect khong crit, khong miss, khong trigger reflect tiep.

## 14.3. Reflect Plate

`Reflect Plate`:

- chi phan damage nhan tu `basic attack`
- ratio `12%`
- damage reflect bo qua ACC/EVA
- damage reflect bo qua crit
- damage reflect khong kich hoat `receive-hit energy`

Quy tac cuoi cung la `de xuat production default` de tranh loop exploit energy.

## 15. Event Log Contract

## 15.1. Muc dich

Event log phuc vu:

- HUD combat log rut gon
- post-battle breakdown
- QA debug
- replay determinism test

## 15.2. Event schema

```json
{
  "tick": 14,
  "seq": 3,
  "type": "damage_applied",
  "source_unit_id": "player",
  "target_unit_id": "enemy",
  "payload": {
    "source_type": "skill",
    "skill_id": "overheat_beam",
    "amount": 42,
    "is_crit": false,
    "hit_result": "hit"
  }
}
```

`seq` la so thu tu event trong cung tick.

## 15.3. Event types bat buoc

- `battle_started`
- `tick_started`
- `energy_gained`
- `skill_cast`
- `basic_attack`
- `attack_missed`
- `damage_applied`
- `shield_gained`
- `shield_broken`
- `effect_applied`
- `effect_expired`
- `effect_tick_damage`
- `unit_down`
- `battle_ended`

HUD co the khong hien thi het, nhung runner van nen log day du.

## 16. Result Breakdown Contract

## 16.1. Required fields

```json
{
  "winner_unit_id": "player",
  "end_reason": "enemy_down",
  "duration_ticks": 87,
  "duration_seconds": 17.4,
  "player_summary": {},
  "enemy_summary": {},
  "failure_reason_hints": []
}
```

## 16.2. Summary fields moi ben

- `total_damage_dealt`
- `total_damage_taken`
- `damage_by_source.basic`
- `damage_by_source.skill`
- `damage_by_source.burn`
- `damage_by_source.reflect`
- `skill_cast_count`
- `basic_hit_count`
- `basic_miss_count`
- `status_uptime.burn`
- `status_uptime.stun`
- `status_uptime.shield`
- `status_uptime.break_armor`
- `peak_shield_value`

## 16.3. Failure reason hints

Post-battle screen nen tao 1-3 hint tu thong ke. Quy tac MVP:

- neu `miss_rate >= 35%` -> `khong du accuracy`
- neu `skill_cast_count == 0` va co skill -> `khong du energy de xoay skill`
- neu `burn_damage_taken >= 25% total_damage_taken` -> `thieu counter Burn`
- neu `enemy_shield_absorbed >= 20% damage_out` -> `thieu anti-shield`
- neu `time_to_die <= 10s` -> `bi burst qua nhanh`

Day la logic UX, khong phai rule combat, nhung nen nam chung contract data.

## 17. Pseudo Code

## 17.1. Entry point

```text
func run_battle(player_snapshot, enemy_snapshot, seed) -> BattleResult:
    state = init_battle_state(player_snapshot, enemy_snapshot, seed)
    log_battle_started(state)

    while state.phase == RUNNING and state.tick < state.timeout_ticks:
        run_tick(state)
        if has_winner(state):
            finalize_battle(state, end_reason_from_death(state))
            return state.result

    if state.phase == RUNNING:
        finalize_battle(state, "timeout")

    return state.result
```

## 17.2. Tick loop

```text
func run_tick(state):
    state.tick += 1
    emit_tick_started(state)

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        apply_energy_regen(unit, state.tick)

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        tick_effect_durations(unit, state.tick)

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        resolve_dot_effects(unit, opposing_unit(state, unit), state.tick)
        if has_winner(state):
            return

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        try_cast_primary_skill(unit, opposing_unit(state, unit), state.tick)
        if has_winner(state):
            return

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        tick_attack_timer(unit)

    for unit in [state.player, state.enemy]:
        if unit.is_dead:
            continue
        try_basic_attack(unit, opposing_unit(state, unit), state.tick)
        if has_winner(state):
            return

    for unit in [state.player, state.enemy]:
        update_status_uptime_counters(unit)
        tick_skill_lock(unit)
```

## 17.3. Skill cast

```text
func try_cast_primary_skill(caster, target, tick):
    skill = caster.snapshot.primary_skill
    if skill == null:
        return false
    if caster.skill_lock_ticks > 0:
        return false
    if caster.current_energy < skill.energy_cost:
        return false
    if has_effect(caster, STUN):
        return false
    if not ai_allows_skill_cast(caster, skill):
        return false

    spend_energy(caster, skill.energy_cost, tick)
    caster.skill_lock_ticks = to_ticks(skill.cooldown_lock)
    emit_skill_cast(caster, skill, tick)

    return resolve_skill_payload(caster, target, skill, tick)
```

## 17.4. Basic attack

```text
func try_basic_attack(attacker, target, tick):
    if attacker.attack_cooldown_ticks > 0:
        return false
    if has_effect(attacker, STUN):
        reset_attack_timer(attacker)
        emit_basic_skipped(attacker, "stunned", tick)
        return false

    emit_basic_attack(attacker, target, tick)
    packet = build_basic_damage_packet(attacker, target)
    resolve_damage_packet(packet, tick)
    reset_attack_timer(attacker)
    return true
```

## 17.5. Damage packet

```text
func resolve_damage_packet(packet, tick):
    if packet.can_miss and roll_miss(packet):
        emit_attack_missed(packet, tick)
        apply_miss_hooks(packet.source_unit_id, tick)
        return DamageResult.miss()

    is_crit = packet.can_crit and roll_crit(packet)
    damage = packet.raw_damage
    damage = apply_defense_formula(damage, packet.target_unit_id)
    if is_crit:
        damage *= 1.5
    damage = floor(max(1, damage))

    absorbed, hp_loss = apply_shield_then_hp(packet.target_unit_id, damage, tick)
    emit_damage_applied(packet, hp_loss, absorbed, is_crit, tick)
    apply_on_damage_energy_hooks(packet, hp_loss, tick)
    apply_packet_effects(packet, tick)
    apply_reflect_if_needed(packet, hp_loss, tick)
    update_battle_stats(packet, hp_loss)
    check_and_mark_death(packet.target_unit_id, tick)

    return DamageResult.hit(hp_loss, absorbed, is_crit)
```

## 18. Test cases bat buoc

## 18.1. Determinism

1. cung snapshot + cung seed -> event log giong het
2. doi seed -> ket qua co the khac, nhung van hop le

## 18.2. Energy

1. basic hit cho attacker `+6`
2. basic hit cho defender `+4` hoac them bonus neu co `Guard Core`
3. skill hit cho defender `+8`
4. miss khong cho `on_hit energy`
5. skill cast tru energy truoc damage resolve

## 18.3. Status

1. Burn toi da `3 stack`
2. Burn khong gay damage ngay tick vua apply
3. Stun chan basic va skill
4. Shield moi chi overwrite neu lon hon
5. Break Armor khong stack

## 18.4. Death and timeout

1. unit chet trong phase skill thi khong basic attack nua
2. timeout uu tien `HP%`
3. neu `HP%` bang nhau thi uu tien `total_damage_dealt`

## 18.5. Weapon profile

1. `Laser + Laser` nhan same-family bonus
2. `Laser + Hammer` van la laser basic
3. passive offhand van proc dung tan suat

## 19. Implementation split de code

Nen tach system thanh 5 khoi:

1. `stat_resolver`
2. `combat_runner`
3. `effect_system`
4. `combat_log_builder`
5. `result_analyzer`

## 19.1. Trach nhiem tung khoi

### stat_resolver

- nhan build/enemy data
- tra `CombatantSnapshot`

### combat_runner

- chay tick loop
- goi effect va damage resolver
- xac dinh winner

### effect_system

- apply/remove/tick effect
- tra modifier runtime

### combat_log_builder

- tao event log co schema on dinh

### result_analyzer

- tong hop thong ke
- tao `failure_reason_hints`

## 20. Cac quyet dinh bo sung duoc chot trong spec nay

Nhung muc duoi day la cac cho `concept.md` chua chot du den muc code, nen spec nay da chot de tranh ambiguity:

1. resolve thu tu `player` truoc `enemy` trong cung phase
2. timeout neu van bang hoan toan thi `enemy thang`
3. `attack_interval_ticks = ceil((1 / spd) / 0.2)`
4. basic attack khong duoc free hit tick 0
5. Burn khong dot ngay tick vua apply
6. AI shield chi cast khi `shield_hp == 0`
7. reflect khong chain, khong crit, khong miss
8. energy runtime nen luu dang fixed-point

Neu team muon doi mot trong cac diem nay, can doi ca:

- unit tests
- replay tests
- HUD expectation
- balance sheet

## 21. Thu tu tai lieu tiep theo

Sau `combat_spec.md`, nen viet tiep:

1. `part_data_schema.md`
2. `enemy_roster.md`
3. `economy_balance_sheet.md`
4. `godot_system_architecture.md`

Vi `combat_spec.md` da chot contract runtime, cac tai lieu sau phai phu hop voi contract nay, khong duoc dinh nghia effect/skill/phu kien trai nhau.

---

## 18. Addendum 2026-04 (chi tiet thuc thi combat runner)

### 18.1. Kien truc class runtime de de debug

De xuat toi thieu cac class/value-object sau:

- `BattleConfig` (tick_rate, timeout, clamp)
- `BattleState` (tick_index, rng_state, units, event_log)
- `UnitRuntimeState` (hp, energy, timers, effects)
- `BattleEvent` (type, tick, actor, target, payload)
- `BattleResult` (winner, end_reason, stats, hints)

Tat ca object tren nen serializable de replay va regression test.

### 18.2. Quy tac version combat

Them `combat_version` vao ket qua tran va replay file.

- Neu co thay doi thu tu resolve hoac cong thuc damage, phai tang `combat_version`.
- Replay khac version khong duoc doc chung parser cu ma khong canh bao.

### 18.3. Regression suite khuyen nghi truoc moi balance patch

- `50 seed x 10 matchups` co dinh (tong 500 tran)
- doi chieu: winner, end_reason, total_damage, event_count
- nguong canh bao: lech > `5%` o bat ky chi so nao thi buoc review

### 18.4. KPI doc duoc tran dau tren HUD

Do 3 chi so nay trong user test:

- `nguoi choi tra loi dung ly do thua` >= `70%`
- `thoi gian doc thong tin sau tran` <= `20 giay`
- `skip_rate cua result screen` <= `40%` (neu qua cao, thong tin chua huu ich)
