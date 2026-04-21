# AssembleX MVP Task List

## 1. Cach dung

- `[ ]` chua lam
- `[~]` dang lam
- `[x]` xong
- `FP` = bat buoc cho `First Playable`
- `MVP` = bat buoc cho `Full MVP`

Tai lieu goc tham chieu: `docs/plan/mvp_breakdown.md`

## 2. First Playable checklist

Moc nay dat khi game choi duoc vong lap:

`Bootstrap -> Garage -> Battle -> Result -> Garage`

### A. Foundation

- [ ] `AX-001` `FP` Tao folder skeleton: `autoload/`, `core/`, `data/`, `features/`, `systems/`, `tests/`
- [ ] `AX-002` `FP` Tao `BootstrapScene` va set `main scene`
- [ ] `AX-003` `FP` Tao `game_constants` cho tick rate, timeout, stat cap, enum key
- [ ] `AX-004` `FP` Tao `SceneRouter` hoac `FlowCoordinator`
- [ ] `AX-005` `FP` Tao runtime model co ban:
  `RobotBuild`, `InventoryState`, `CombatantSnapshot`, `BattleRequest`, `BattleResult`, `RewardGrant`

### B. Data layer

- [ ] `AX-010` `FP` Tao data JSON khung cho `parts`, `part_levels`, `skills`, `enemy_archetypes`, `stages`, `reward_profiles`, `upgrade_curves`, `craft_recipes`, `account_levels`
- [ ] `AX-011` `FP` Code `part_repository`
- [ ] `AX-012` `FP` Code `enemy_repository`
- [ ] `AX-013` `FP` Code `stage_repository`
- [ ] `AX-014` `FP` Code `economy_repository`
- [ ] `AX-015` `FP` Code validator cho `slot`, `curve_id`, `enemy_ref`, `left_arm.skill_ref`, build du `6 slot`
- [ ] `AX-016` `FP` Them smoke test cho data load va validation

### C. Build compile

- [ ] `AX-020` `FP` Code `robot_build_builder`
- [ ] `AX-021` `FP` Code `enemy_build_builder`
- [ ] `AX-022` `FP` Code `build_validator`
- [ ] `AX-023` `FP` Code `stat_resolver`
- [ ] `AX-024` `FP` Code `weapon_profile_builder`
- [ ] `AX-025` `FP` Bind `left_arm -> primary_skill`
- [ ] `AX-026` `FP` Bind `right_arm -> offhand_passives`
- [ ] `AX-027` `FP` Bind passive tu `head/core/module`
- [ ] `AX-028` `FP` Tao preview model cho garage doc stat truoc/sau

### D. Combat core

- [ ] `AX-030` `FP` Code `BattleState`
- [ ] `AX-031` `FP` Code `combat_runner`
- [ ] `AX-032` `FP` Code RNG stream theo `battle_seed`
- [ ] `AX-033` `FP` Implement tick order contract:
  `start_of_tick`, energy regen, effect decay, DOT, skill decision, attack timer, on-hit proc, death gate
- [ ] `AX-034` `FP` Implement damage formula, hit chance, crit, attack interval
- [ ] `AX-035` `FP` Implement effect `burn`
- [ ] `AX-036` `FP` Implement effect `stun`
- [ ] `AX-037` `FP` Implement effect `shield`
- [ ] `AX-038` `FP` Implement effect `break_armor`
- [ ] `AX-039` `FP` Implement AI rule co ban cho skill cast
- [ ] `AX-040` `FP` Tao `event_log` va tick summary
- [ ] `AX-041` `FP` Code `result_analyzer`

### E. Progression toi thieu

- [ ] `AX-050` `FP` Code `reward_system`
- [ ] `AX-051` `FP` Grant `first_clear`
- [ ] `AX-052` `FP` Grant `repeat_clear`
- [ ] `AX-053` `FP` Grant `defeat`
- [ ] `AX-054` `FP` Cap nhat `InventoryState` sau reward

### F. UI vertical slice

- [ ] `AX-060` `FP` Tao `GarageScene` toi thieu
- [ ] `AX-061` `FP` Hien build hien tai theo `6 slot`
- [ ] `AX-062` `FP` Hien inventory co ban de thay part
- [ ] `AX-063` `FP` Cap nhat preview stat khi doi part
- [ ] `AX-064` `FP` Hien stage ke tiep va enemy preview co `display_name`, `summary`, `threat_tags`, `counter_tags`, `danger_rating`
- [ ] `AX-065` `FP` Chan nut battle neu build khong hop le
- [ ] `AX-066` `FP` Tao `BattleRequest` tu garage
- [ ] `AX-067` `FP` Tao `BattleScene`
- [ ] `AX-068` `FP` BattleScene goi `combat_runner`
- [ ] `AX-069` `FP` Playback `event_log`
- [ ] `AX-070` `FP` Hien HUD toi thieu: `HP`, `energy`, `effect icon`, `skill cast`, `battle timer`
- [ ] `AX-071` `FP` Them toc do `1x` va `2x`
- [ ] `AX-072` `FP` Route tu `BattleScene` sang `ResultScene`
- [ ] `AX-073` `FP` Tao `ResultScene`
- [ ] `AX-074` `FP` Hien `winner`, `battle duration`, `damage dealt`, `damage taken`, `skill casts`
- [ ] `AX-075` `FP` Hien `failure_reason_hints`
- [ ] `AX-076` `FP` Hien reward grant tren result
- [ ] `AX-077` `FP` Cho `rematch` va `back to garage`

### G. First Playable content toi thieu

- [ ] `AX-080` `FP` Author `6-8 part` dau tien de test vertical slice
- [ ] `AX-081` `FP` Author `3 skill` dau tien
- [ ] `AX-082` `FP` Author `3 enemy` dau tien: `scrap_brawler`, `burner_unit`, `guard_walker`
- [ ] `AX-083` `FP` Author `3-4 stage` dau tien o `rust_yard`
- [ ] `AX-084` `FP` Map reward cho cac stage dau

### H. First Playable done gate

- [ ] `AX-090` `FP` Project boot vao `BootstrapScene` khong loi
- [ ] `AX-091` `FP` Garage compile duoc build hop le
- [ ] `AX-092` `FP` 1 tran chay deterministic tu dau den cuoi
- [ ] `AX-093` `FP` Result screen doc duoc ly do thang/thua o muc co ban
- [ ] `AX-094` `FP` Reward grant xong quay lai garage duoc

## 3. Full MVP checklist

Moc nay dat khi full campaign launch choi duoc va balance du dung.

### I. Content expansion

- [ ] `AX-100` `MVP` Author du `17 part MVP`
- [ ] `AX-101` `MVP` Author du `5 skill MVP`
- [ ] `AX-102` `MVP` Author du `5 enemy archetype`
- [ ] `AX-103` `MVP` Author du `12 stage`
- [ ] `AX-104` `MVP` Hoan tat zone `rust_yard_01 -> rust_yard_06`
- [ ] `AX-105` `MVP` Hoan tat zone `neon_arena_01 -> neon_arena_06`
- [ ] `AX-106` `MVP` Map reward toan bo `12 stage`
- [ ] `AX-107` `MVP` Map unlock source cho tat ca part: `starter`, `stage_clear`, `stage_drop`, `craft`, `boss_reward`
- [ ] `AX-108` `MVP` Cau hinh `stage_drop` co pity rule
- [ ] `AX-109` `MVP` Setup `3 build archetype` kha dung:
  `Burn Tempo`, `Tank Reflect`, `Burst / Anti-Tank`

### J. Progression day du

- [ ] `AX-110` `MVP` Code `upgrade_system`
- [ ] `AX-111` `MVP` Code `craft_system`
- [ ] `AX-112` `MVP` Code `unlock_system`
- [ ] `AX-113` `MVP` Implement account XP + account level
- [ ] `AX-114` `MVP` Unlock `craft` o `Level 2`
- [ ] `AX-115` `MVP` Unlock `module upgrade` o `Level 3`
- [ ] `AX-116` `MVP` Unlock `neon_arena` o `Level 4`
- [ ] `AX-117` `MVP` Guardrail: rare craft can `core_shard`
- [ ] `AX-118` `MVP` Guardrail: upgrade MVP khong dung `core_shard`
- [ ] `AX-119` `MVP` Goi y spend co ban tren UI hoac result flow

### K. Save/load

- [ ] `AX-120` `MVP` Code `app_state`
- [ ] `AX-121` `MVP` Code `save_manager`
- [ ] `AX-122` `MVP` Code `save_codec`
- [ ] `AX-123` `MVP` Luu inventory
- [ ] `AX-124` `MVP` Luu part levels
- [ ] `AX-125` `MVP` Luu stage clear state
- [ ] `AX-126` `MVP` Luu account xp / level
- [ ] `AX-127` `MVP` Luu `current_stage`
- [ ] `AX-128` `MVP` Load save tu `BootstrapScene`

### L. Result va readability nang cap

- [ ] `AX-130` `MVP` Result scene hien `damage by source`
- [ ] `AX-131` `MVP` Result scene hien `status uptime`
- [ ] `AX-132` `MVP` Failure hint chi ra it nhat 1 ly do ro:
  `thieu damage`, `bi burst nhanh`, `thieu accuracy`, `khong du energy`, `thieu counter burn/shield/reflect`
- [ ] `AX-133` `MVP` Battle HUD hien icon status ro rang
- [ ] `AX-134` `MVP` Enemy preview gioi han toi da `2 threat` + `2 counter` de doc nhanh

### M. Testing

- [ ] `AX-140` `MVP` Unit test cho `stat_resolver`
- [ ] `AX-141` `MVP` Replay test cho `combat_runner`
- [ ] `AX-142` `MVP` Integration test `Garage -> Battle -> Result`
- [ ] `AX-143` `MVP` Test schema validation cho `parts/enemies/stages/economy`
- [ ] `AX-144` `MVP` Test save/load smoke
- [ ] `AX-145` `MVP` Test reward pacing smoke

### N. Balance pass

- [ ] `AX-150` `MVP` Balance pass cho `Burn Tempo`
- [ ] `AX-151` `MVP` Balance pass cho `Tank Reflect`
- [ ] `AX-152` `MVP` Balance pass cho `Burst / Anti-Tank`
- [ ] `AX-153` `MVP` Kiem tra khong co build auto-win ro rang
- [ ] `AX-154` `MVP` Kiem tra dodge build khong gan nhu bat tu
- [ ] `AX-155` `MVP` Kiem tra energy spam skill khong vuot guardrail
- [ ] `AX-156` `MVP` Kiem tra reflect khong chain va khong qua manh
- [ ] `AX-157` `MVP` Kiem tra khong stage nao bat buoc farm > `3 lan` neu build dung
- [ ] `AX-158` `MVP` Kiem tra defeat reward khong cao den muc farm-thua

### O. Full MVP done gate

- [ ] `AX-160` `MVP` Clear duoc full campaign launch tu `rust_yard_01` den `neon_arena_06`
- [ ] `AX-161` `MVP` Co it nhat `3 build archetype` kha dung
- [ ] `AX-162` `MVP` Thua tran van doc duoc ly do chinh
- [ ] `AX-163` `MVP` Save/load giu duoc tien do co ban
- [ ] `AX-164` `MVP` Replay deterministic pass
- [ ] `AX-165` `MVP` Khong con bug blocker trong flow chinh

## 4. Thu tu uu tien de lam ngay

Neu chi chon mot danh sach ngan de bat dau, dung thu tu nay:

- [ ] `P1` `part_repository`, `enemy_repository`, `stage_repository`, `economy_repository`
- [ ] `P2` `RobotBuild`, `CombatantSnapshot`, `BattleRequest`, `BattleResult`
- [ ] `P3` `build_validator`
- [ ] `P4` `stat_resolver`
- [ ] `P5` `combat_runner` + `effect_system`
- [ ] `P6` `result_analyzer`
- [ ] `P7` `reward_system`
- [ ] `P8` `GarageScene` toi thieu
- [ ] `P9` `BattleScene` playback toi thieu
- [ ] `P10` `ResultScene`
- [ ] `P11` `upgrade_system` + `craft_system`

## 5. De xuat tach issue

Neu ban muon dua vao issue tracker, nen tach theo 4 nhom:

1. `Core Systems`
2. `Scenes + UI`
3. `Content Data`
4. `QA + Balance`

Moi issue nen chua:

- `task id`
- `scope`
- `dependency`
- `definition of done`
- `test note`
