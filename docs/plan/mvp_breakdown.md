# AssembleX MVP Breakdown

## 1. Muc tieu tai lieu

Tai lieu nay chuyen cac concept trong `docs/concepts/` thanh backlog thuc thi cho `AssembleX MVP`.

Muc tieu cua MVP:

- chung minh `build robot theo part` tao ra quyet dinh chien thuat thu vi
- co duoc vong lap hoan chinh `Garage -> Battle -> Result -> Progression -> Rematch`
- cho phep clear tron campaign launch `12 stage`
- giu scope du nho de co the ship mot ban choi duoc va debug duoc

Tai lieu nay uu tien:

- thu tu implement giam rui ro
- dependency giua cac he thong
- deliverable cu the
- definition of done de dong scope

## 2. MVP scope da khoa

### 2.1. Scope bat buoc

- `1v1 semi-auto tick-based combat`
- `GarageScene`, `BattleScene`, `ResultScene`
- `6 slot robot`: `head`, `core`, `left_arm`, `right_arm`, `legs`, `module`
- `17 part MVP`
- `5 skill MVP`
- `4 effect MVP`: `burn`, `stun`, `shield`, `break_armor`
- `5 enemy archetype`
- `12 campaign stage`: `2 zone x 6 stage`
- `reward`, `upgrade`, `craft`, `unlock pacing`
- `battle result breakdown` de nguoi choi doc ly do thang/thua

### 2.2. Khong lam trong MVP

- PvP
- online
- 3v3
- real-time manual control
- world navigation
- social system
- content pipeline nang cao

## 3. Target san pham

### 3.1. First Playable

Ban nay phai choi duoc vong lap co ban:

- build starter hop le
- vao 1 tran
- combat chay on dinh va deterministic
- hien ket qua va grant reward
- quay lai garage de doi part/nang cap/thu lai

First Playable khong can du `17 part` va `12 stage`. Chi can du de kiem chung core fun.

### 3.2. Full MVP

Ban nay phai dat du cac dieu kien:

- clear duoc full campaign launch
- co it nhat `3 build archetype` kha dung
- thua tran van doc ra nguyen nhan
- khong co build auto-win ro rang

## 4. Phan ra backlog cap cao

### 4.1. Epic A - Project skeleton va runtime contracts

Muc tieu:

- dung skeleton dung huong truoc khi viet system

Task:

1. tao folder theo huong `autoload/`, `core/`, `data/`, `features/`, `systems/`, `tests/`
2. khai bao `main scene` toi thieu va `BootstrapScene`
3. tao cac model/rules co ban:
   - `RobotBuild`
   - `InventoryState`
   - `CombatantSnapshot`
   - `BattleRequest`
   - `BattleResult`
   - `RewardGrant`
4. them `game_constants` cho tick rate, timeout, stat cap, enum key
5. tao `SceneRouter` hoac `FlowCoordinator`

Deliverable:

- project mo duoc vao `BootstrapScene`
- class/model khung ton tai, compile khong vo

Definition of done:

- co scene flow toi thieu `Bootstrap -> Garage`
- cac runtime contract duoc dung thong nhat, khong copy schema o nhieu noi

### 4.2. Epic B - Data layer va validators

Muc tieu:

- data-first tu ngay dau, tranh hard-code combat/content trong scene

Task:

1. tao file data JSON cho:
   - `parts`
   - `part_levels`
   - `skills`
   - `enemy_archetypes`
   - `stages`
   - `reward_profiles`
   - `upgrade_curves`
   - `craft_recipes`
   - `account_levels`
2. code repository:
   - `part_repository`
   - `enemy_repository`
   - `stage_repository`
   - `economy_repository`
3. code validator:
   - slot dung enum
   - `curve_id` ton tai
   - `enemy_ref` hop le
   - `stage reward` dung schema
   - `left_arm` co `skill_ref`
   - moi build du `6 slot`
4. them smoke test cho repository load va validation

Deliverable:

- data load duoc vao runtime
- fail fast neu schema sai

Definition of done:

- startup co the load data ma khong crash
- validator bat duoc loi content co y nghia

### 4.3. Epic C - Build assembly va stat compile

Muc tieu:

- tu loadout garage compile ra snapshot battle dung contract

Task:

1. code `robot_build_builder`
2. code `enemy_build_builder`
3. code `build_validator`
4. code `stat_resolver`
5. code `weapon_profile_builder`
6. code binding:
   - `left_arm -> primary_skill`
   - `right_arm -> offhand_passives`
   - passive tu `head/core/module`
7. them preview model de Garage doc duoc stat truoc/sau

Deliverable:

- `RobotBuild` + data part -> `CombatantSnapshot`
- enemy stage data -> `CombatantSnapshot`

Definition of done:

- doi 1 part trong garage thi stat preview doi dung
- snapshot player/enemy co schema thong nhat

### 4.4. Epic D - Combat core

Muc tieu:

- co combat runner thuần logic, deterministic, debug duoc

Task:

1. code `combat_runner`
2. code `BattleState`
3. code he thong tick:
   - `start_of_tick`
   - energy regen
   - effect duration decay
   - DOT
   - skill decision
   - basic attack timer
   - on-hit proc
   - death gate
4. code RNG stream theo `battle_seed`
5. code damage formula, hit chance, crit, attack interval
6. code effect system cho:
   - `burn`
   - `stun`
   - `shield`
   - `break_armor`
7. code AI rule toi thieu:
   - skill thuong cast ngay khi du energy
   - `shield skill` chi cast khi HP thap hon nguong
8. code event log va tick summary
9. code `result_analyzer`

Deliverable:

- 1 tran 1v1 chay den ket thuc
- tao ra `BattleResult` + `event_log`

Definition of done:

- cung `snapshot + seed` ra cung ket qua
- kill trong cung tick chan duoc event tiep theo cua unit da chet
- timeout resolve dung contract

### 4.5. Epic E - Progression core

Muc tieu:

- hoan chinh vong lap thu build, thua, nang/craft, thu lai

Task:

1. code `reward_system`
2. code `upgrade_system`
3. code `craft_system`
4. code `unlock_system`
5. code grant:
   - `first_clear`
   - `repeat_clear`
   - `defeat`
6. code account XP + account level unlock
7. code inventory state update sau reward/craft/upgrade
8. them guardrail:
   - rare craft can `core_shard`
   - upgrade MVP khong dung `core_shard`

Deliverable:

- sau tran co reward dung
- player co the upgrade/craft hop le

Definition of done:

- clear stage dau tien grant dung reward
- defeat van co reward nho
- unlock `craft`, `module upgrade`, `zone 2` theo pacing dung

### 4.6. Epic F - Garage scene

Muc tieu:

- nguoi choi doc duoc build va dua ra quyet dinh truoc tran

Task:

1. tao `GarageScene` toi thieu
2. hien build hien tai theo `6 slot`
3. hien inventory theo slot/filter co ban
4. cho thay part va cap nhat preview stat truoc/sau
5. hien stage ke tiep va enemy preview:
   - `display_name`
   - `summary`
   - toi da `2 threat_tags`
   - toi da `2 counter_tags`
   - `danger_rating`
6. chan nut battle neu build khong hop le
7. tao `BattleRequest` tu garage

Deliverable:

- garage dung duoc lam man chinh

Definition of done:

- nguoi choi thay part, xem stat doi, doc duoc threat/counter cua stage
- co the bam vao battle khi build hop le

### 4.7. Epic G - Battle scene va playback

Muc tieu:

- hien combat de doc, khong dua logic vao scene

Task:

1. tao `BattleScene`
2. nhan `BattleRequest`
3. goi `combat_runner`
4. phat playback tu `event_log`
5. them HUD toi thieu:
   - HP
   - energy
   - effect icon
   - skill cast event
   - timer/battle duration
6. them speed mode toi thieu:
   - `1x`
   - `2x`
7. ket thuc tran thi route sang `ResultScene`

Deliverable:

- tran danh xem duoc, doc duoc

Definition of done:

- combat khong tinh damage trong scene
- player co the theo doi event quan trong bang HUD/log

### 4.8. Epic H - Result scene

Muc tieu:

- sau moi tran nguoi choi hieu vi sao vua thang/thua va lam gi tiep theo

Task:

1. tao `ResultScene`
2. hien:
   - winner
   - battle duration
   - total damage dealt
   - total damage taken
   - number of skill casts
   - damage by source
   - status uptime
3. hien `failure_reason_hints`
4. hien reward grant
5. cho:
   - rematch
   - quay ve garage
   - sang stage tiep neu clear

Deliverable:

- result screen hoan chinh du thong tin hoc build

Definition of done:

- thua `burner_unit` van co hint co nghia
- nguoi choi co it nhat 1 hanh dong tiep theo ro rang

### 4.9. Epic I - Content MVP

Muc tieu:

- day du content toi thieu de balance va clear full launch campaign

Task:

1. author `17 part MVP`
2. author `5 skill MVP`
3. author `5 enemy archetype`
4. author `12 stage`
5. map reward cho tung stage
6. map unlock source cho part:
   - `starter`
   - `stage_clear`
   - `stage_drop` co pity
   - `craft`
   - `boss_reward`
7. setup `3 build archetype` co kha nang clear:
   - `Burn Tempo`
   - `Tank Reflect`
   - `Burst / Anti-Tank`

Deliverable:

- full content dataset de choi het campaign launch

Definition of done:

- co the clear tu `rust_yard_01` den `neon_arena_06`
- khong stage nao bat buoc farm lap qua `3` lan de tiep tuc neu build dung

### 4.10. Epic J - Save/load va app state

Muc tieu:

- game giu duoc progression co ban giua cac lan mo

Task:

1. code `app_state`
2. code `save_manager`
3. code `save_codec`
4. luu:
   - inventory
   - part level
   - stage clear state
   - account xp / level
   - current stage
5. load save tu `BootstrapScene`

Deliverable:

- tat game mo lai van giu tien do

Definition of done:

- clear 1 stage, craft/upgrade 1 part, restart game, du lieu van con

### 4.11. Epic K - Test va balance pass

Muc tieu:

- khoa chat core system truoc khi xem la xong MVP

Task:

1. unit test cho `stat_resolver`
2. replay test cho `combat_runner`
3. integration test cho `Garage -> Battle -> Result`
4. test data validation cho `parts/enemies/stages/economy`
5. can bang 3 nhom build kha dung
6. ra soat red flags:
   - thua 4 tran lien khong du tai nguyen sua build
   - reflect qua manh
   - energy spam skill qua da
   - dodge build gan nhu bat tu

Deliverable:

- bo smoke test toi thieu cho MVP
- pass balance co ghi nhan bug/risk

Definition of done:

- deterministic replay pass
- full campaign clear duoc bang it nhat 3 huong build

## 5. Thu tu implement de xuat

### Phase 0 - Foundation

- Epic A
- Epic B

### Phase 1 - First Playable core

- Epic C
- Epic D
- Epic E phan toi thieu

Output can dat:

- data load duoc
- 1 tran chay duoc
- reward grant duoc

### Phase 2 - Vertical slice UI

- Epic F
- Epic G
- Epic H

Output can dat:

- choi duoc `Garage -> Battle -> Result -> Garage`

### Phase 3 - Content expansion

- Epic I
- Epic E phan con lai
- Epic J

Output can dat:

- co campaign `12 stage`
- co craft/upgrade/unlock pacing day du

### Phase 4 - Stabilization

- Epic K

Output can dat:

- build on dinh, test du toi thieu, MVP co the playtest noi bo

## 6. Danh sach uu tien rat cao

Neu can cat nho de chay nhanh, uu tien dung thu tu sau:

1. `repositories`
2. `RobotBuild + CombatantSnapshot`
3. `build_validator`
4. `stat_resolver`
5. `combat_runner + effect_system`
6. `result_analyzer`
7. `reward_system`
8. `GarageScene` toi thieu
9. `BattleScene` playback toi thieu
10. `ResultScene`
11. `upgrade_system + craft_system`

## 7. Content checklist can author cho MVP

### 7.1. Parts

- `3 head`
- `3 core`
- `4 left_arm`
- `3 right_arm`
- `3 legs`
- `4 module`

Tong: `17 part`

### 7.2. Skills

- `overheat_beam`
- `shock_ram`
- `bulwark_pulse`
- `capacitor_dump`
- `piercing_drill`

### 7.3. Enemies

- `scrap_brawler`
- `burner_unit`
- `guard_walker`
- `raider_duelist`
- `iron_bastion_boss`

### 7.4. Stages

- `rust_yard_01` -> `rust_yard_06`
- `neon_arena_01` -> `neon_arena_06`

## 8. Acceptance criteria cuoi cung

MVP duoc xem la dat khi:

1. project boot vao game flow binh thuong
2. player co the lap build hop le o garage
3. enemy preview hien du threat/counter
4. 1 tran 1v1 chay deterministic va ket thuc dung contract
5. result screen noi duoc ly do thang/thua
6. reward, upgrade, craft, unlock hoat dong dung pacing
7. clear duoc full campaign launch
8. save/load giu duoc tien do co ban
9. co replay/data validation smoke test
10. khong con bug blocker trong flow chinh

## 9. Rui ro lon nhat can canh giu

- scene om business logic lam meo combat contract
- hard-code part/enemy trong UI thay vi qua repository
- them content truoc khi combat runner va result breakdown on dinh
- mo rong qua som sang PvP/3v3 khi 1v1 chua chot
- balance bang tang so thuan thay vi sua bai hoc stage va counter access

## 10. De xuat cach dung tai lieu nay

Nen tach backlog thuc thi tiep theo 3 lop:

1. `must-have for first playable`
2. `must-have for full MVP`
3. `nice-to-have after content lock`

Neu sprint nho, co the bien moi `Epic` thanh 1 issue lon, sau do tach theo `Task` thanh issue con.
