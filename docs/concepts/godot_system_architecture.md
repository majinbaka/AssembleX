# AssembleX Godot System Architecture

## 1. Muc tieu tai lieu

Tai lieu nay chot kien truc he thong Godot cho AssembleX MVP de:

1. team code co khung ro rang de implement `garage -> battle -> result -> progression`
2. boundary giua `scene`, `system`, `data`, `runtime state` duoc tach ro
3. cac contract trong `combat_spec.md`, `part_data_schema.md`, `enemy_roster.md`, `economy_balance_sheet.md` di vao code ma khong bi meo
4. vertical slice co the duoc build dan ma khong can dap cau truc sau nay

Tai lieu nay cover:

- folder structure de xuat cho repo Godot
- scene flow cap cao
- system split va trach nhiem
- runtime data pipeline
- autoload va resource classes can co
- test strategy cho MVP

Tai lieu nay khong cover:

- art pipeline chi tiet
- animation graph chi tiet
- editor tooling nang cao

## 2. Nguyen tac kien truc

Kien truc nay giu 6 nguyen tac:

1. `data-first`: part, skill, enemy, reward, upgrade deu doc tu data
2. `deterministic-core`: combat runner la logic thuần, khong phu thuoc scene tree
3. `thin-scenes`: scene chu yeu dung de compose UI, animation va input, khong om business logic
4. `single-source-of-truth`: build, snapshot, battle result moi loai chi co 1 schema chinh
5. `feature-oriented`: code duoc gom theo domain thay vi theo loai file thuần tuy
6. `vertical-slice-friendly`: co the xay tung system doc lap roi noi lai nhanh

## 3. Kien truc tong the

```text
JSON Data
  -> Repository Loaders
  -> Domain Models / Resources
  -> Services
  -> Scene Presenters
  -> UI / Animation
```

Trong MVP, he thong chia thanh 4 tang:

1. `Data layer`
2. `Domain services`
3. `Flow / scene orchestration`
4. `Presentation`

## 4. Scene flow chinh thuc

```text
BootstrapScene
  -> GarageScene
  -> BattleScene
  -> ResultScene
  -> quay ve GarageScene hoac vao stage tiep
```

## 4.1. Trach nhiem tung scene

### `BootstrapScene`

- nap save
- nap data repository
- khoi tao autoload state neu can
- chuyen vao `GarageScene`

### `GarageScene`

- hien build hien tai
- mo inventory va doi part
- hien enemy preview cua stage ke tiep
- goi `stat_resolver` de preview build
- bat dau battle khi build hop le

### `BattleScene`

- nhan `player_snapshot`, `enemy_snapshot`, `battle_seed`
- goi `combat_runner`
- phat animation/event dua tren `event_log`
- khong tu tinh damage hay effect

### `ResultScene`

- hien `BattleResult`
- hien `failure_reason_hints`
- grant reward
- cho nang cap/craft/rematch/chuyen stage

## 4.2. Scene transition rule

Chi co 1 lop dieu huong scene:

- `SceneRouter` hoac `FlowCoordinator`

Khong cho:

- `BattleScene` tu y sua save file
- `GarageScene` tu y tinh reward
- `ResultScene` tu y chay combat lai

## 5. Folder structure de xuat

`setting.md` da dua ra khung tong quat. Với AssembleX, repo nay nen chot structure cu the hon nhu sau:

```text
res://
├─ autoload/
│  ├─ app_state.gd
│  ├─ save_manager.gd
│  ├─ data_registry.gd
│  └─ scene_router.gd
│
├─ core/
│  ├─ constants/
│  │  └─ game_constants.gd
│  ├─ utils/
│  │  ├─ math_utils.gd
│  │  ├─ json_utils.gd
│  │  └─ validation_utils.gd
│  ├─ domain/
│  │  ├─ models/
│  │  ├─ enums/
│  │  └─ value_objects/
│  └─ test_support/
│
├─ data/
│  ├─ parts/
│  ├─ enemies/
│  ├─ stages/
│  ├─ economy/
│  └─ localization/
│
├─ features/
│  ├─ garage/
│  │  ├─ garage_scene.tscn
│  │  ├─ garage_scene.gd
│  │  ├─ build_editor_panel.gd
│  │  ├─ inventory_panel.gd
│  │  └─ stage_preview_panel.gd
│  ├─ battle/
│  │  ├─ battle_scene.tscn
│  │  ├─ battle_scene.gd
│  │  ├─ battle_presenter.gd
│  │  ├─ battle_timeline_player.gd
│  │  └─ widgets/
│  ├─ results/
│  │  ├─ result_scene.tscn
│  │  ├─ result_scene.gd
│  │  └─ reward_panel.gd
│  ├─ progression/
│  │  ├─ upgrade_panel.gd
│  │  ├─ craft_panel.gd
│  │  └─ account_level_panel.gd
│  └─ shared_ui/
│     ├─ part_tooltip.gd
│     └─ stat_block_widget.gd
│
├─ systems/
│  ├─ repositories/
│  │  ├─ part_repository.gd
│  │  ├─ enemy_repository.gd
│  │  ├─ stage_repository.gd
│  │  └─ economy_repository.gd
│  ├─ builders/
│  │  ├─ robot_build_builder.gd
│  │  ├─ enemy_build_builder.gd
│  │  └─ combat_snapshot_builder.gd
│  ├─ combat/
│  │  ├─ stat_resolver.gd
│  │  ├─ combat_runner.gd
│  │  ├─ damage_resolver.gd
│  │  ├─ effect_system.gd
│  │  ├─ combat_log_builder.gd
│  │  └─ result_analyzer.gd
│  ├─ progression/
│  │  ├─ reward_system.gd
│  │  ├─ upgrade_system.gd
│  │  ├─ craft_system.gd
│  │  └─ unlock_system.gd
│  ├─ validation/
│  │  ├─ build_validator.gd
│  │  ├─ data_validator.gd
│  │  └─ economy_validator.gd
│  └─ save/
│     └─ save_codec.gd
│
├─ resources/
│  ├─ data/
│  └─ runtime/
│
├─ scenes/
│  ├─ bootstrap/
│  └─ test/
│
└─ tests/
   ├─ unit/
   ├─ integration/
   └─ replay/
```

## 6. System split can code

## 6.1. Data repositories

### `part_repository`

- load `part_data` va `part_level_data`
- tra part theo `id`
- validate `curve_id`, `slot`, `unlock`

### `enemy_repository`

- load `enemy_archetype_data`
- tra archetype theo `enemy_ref`

### `stage_repository`

- load `stage_encounter_data`
- tra stage theo `stage_id`
- tra `reward_profile` va enemy mapping

### `economy_repository`

- load `reward_profiles`, `upgrade_curves`, `craft_recipes`, `account_levels`
- tra cost va reward theo `id`

Repository layer khong duoc chua combat logic.

## 6.2. Build va compile services

### `robot_build_builder`

- tao `RobotBuild` tu loadout trong garage
- merge inventory level va slot state

### `enemy_build_builder`

- tao build enemy tu `enemy_archetype_data + stage_encounter_data`

### `build_validator`

- check du `6 slot`
- check part dung slot
- check unlock state neu build la player

### `stat_resolver`

- nhan build data
- doc `part_data` + `part_level_data`
- tra `CombatantSnapshot`

Day la service can duoc test ky nhat vi no la cau noi giua data va combat.

## 6.3. Combat services

Theo `combat_spec.md`, tach thanh 6 khoi:

1. `combat_runner`
2. `damage_resolver`
3. `effect_system`
4. `combat_log_builder`
5. `result_analyzer`
6. `battle_seed_provider`

### `combat_runner`

- tao `BattleState`
- chay tick loop
- goi `damage_resolver` va `effect_system`
- khong biet gi ve HUD

### `damage_resolver`

- resolve miss, crit, def, shield, hp loss, reflect
- cap nhat packet damage

### `effect_system`

- apply/remove/tick effect
- quan ly `burn`, `stun`, `shield`, `break_armor`

### `combat_log_builder`

- emit event theo schema da chot
- dam bao `tick` va `seq` on dinh

### `result_analyzer`

- tong hop `player_summary`, `enemy_summary`
- tao `failure_reason_hints`

### `battle_seed_provider`

- sinh seed cho tran moi
- luu lai seed de replay/debug

## 6.4. Progression services

### `reward_system`

- nhan `BattleResult + StageEncounter + clear_state`
- tinh `first_clear`, `repeat_clear`, `defeat`
- tra `RewardGrant`

### `upgrade_system`

- doc `curve_id`
- tinh chi phi upgrade
- tru resource
- tang level part

### `craft_system`

- check recipe
- check unlock account level
- tru resource
- them part vao inventory

### `unlock_system`

- chot xem part/stage/system da mo chua
- xu ly `starter`, `stage_clear`, `stage_drop`, `craft`, `boss_reward`

### `save_manager`

- ghi/nap save state
- khong nhung combat logic

## 7. Runtime object model

## 7.1. Data objects

Nen co cac object sau:

- `PartData`
- `PartLevelData`
- `EnemyArchetypeData`
- `StageEncounterData`
- `RewardProfileData`
- `UpgradeCurveData`
- `CraftRecipeData`
- `AccountLevelData`

## 7.2. Domain objects

- `RobotBuild`
- `InventoryState`
- `PlayerProgressState`
- `CombatantSnapshot`
- `BattleResult`
- `RewardGrant`

## 7.3. Runtime-only objects

- `BattleState`
- `UnitRuntimeState`
- `EffectInstance`
- `DamagePacket`

Quy tac:

- object o muc `runtime-only` khong duoc serialize vao save goc cua campaign
- neu can replay, serialize `snapshot + seed + battle version`, khong serialize nguyen node tree

## 8. Data pipeline chi tiet

## 8.1. Garage preview flow

```text
Player equip/unequip part
  -> RobotBuildBuilder
  -> BuildValidator
  -> StatResolver
  -> PreviewViewModel
  -> Garage UI
```

Garage UI chi doc `PreviewViewModel`, khong doc truc tiep JSON raw.

## 8.2. Enter battle flow

```text
GarageScene
  -> StageRepository.get(stage_id)
  -> EnemyBuildBuilder
  -> StatResolver(player_build)
  -> StatResolver(enemy_build)
  -> BattleRequest
  -> SceneRouter.to_battle()
```

`BattleRequest` toi thieu gom:

```json
{
  "stage_id": "rust_yard_03",
  "battle_seed": 123456,
  "player_snapshot": {},
  "enemy_snapshot": {}
}
```

## 8.3. Battle to result flow

```text
BattleScene
  -> CombatRunner.run(request)
  -> BattleResult
  -> RewardSystem.preview()
  -> ResultScene
```

Luu y:

- reward nen duoc tinh o `ResultScene enter` hoac `result flow controller`
- `BattleScene` chi nen tra `BattleResult`, khong grant thang vao save

## 8.4. Result to garage flow

```text
ResultScene
  -> apply reward
  -> optional upgrade/craft
  -> save state
  -> route ve garage hoac stage tiep theo
```

## 9. Autoload de xuat

Chi giu nhung singleton can thiet that su:

### `app_state`

- giu `current_profile`
- giu `current_stage_id`
- giu `last_battle_result`

### `data_registry`

- cache repository sau khi load
- cho scene truy cap thong qua API ro rang

### `scene_router`

- dieu huong scene
- truyen payload scene-to-scene

### `save_manager`

- doc/ghi profile

Khong nen them vao autoload:

- `combat_runner`
- `reward_system`
- `stat_resolver`

Nhung system nay nen duoc instantiate hoac inject ro rang de test de hon.

## 10. Resource hay script thuần?

Quyet dinh khuyen nghi:

- data authoring goc: dung `JSON`
- runtime domain model: dung `GDScript class` hoac `RefCounted`
- chi dung `Resource` khi can editor integration manh hoac can serialize trong Godot inspector

Ly do:

- tai lieu da chot schema theo JSON
- diff text de review hon
- de dung chung cho validator/tooling ve sau

MVP khong can chuyen toan bo data sang `.tres` ngay tu dau.

## 11. Scene composition rule

## 11.1. Garage scene

```text
GarageScene
├─ BuildEditorPanel
├─ InventoryPanel
├─ StagePreviewPanel
├─ RobotPreviewViewport
└─ FooterActions
```

`GarageScene.gd` chi nen:

- lang nghe action UI
- goi service
- cap nhat view model

Khong nen:

- tu parse JSON
- tu tinh stat bang tay

## 11.2. Battle scene

```text
BattleScene
├─ ArenaRoot
├─ PlayerRobotView
├─ EnemyRobotView
├─ BattleHud
├─ TimelineController
└─ OverlayLayer
```

Battle scene doc `event_log` va `BattleResult` de phat animation.

Hai mode hop le cho MVP:

1. `simulate-all-then-playback`
2. `tick-and-render-live`

Khuyen nghi:

- vertical slice dau dung `simulate-all-then-playback`

Ly do:

- de debug determinism
- de replay
- de tach logic khoi frame rate

## 11.3. Result scene

```text
ResultScene
├─ ResultSummaryPanel
├─ RewardPanel
├─ FailureHintsPanel
├─ UpgradeShortcutPanel
└─ ActionButtons
```

Result scene khong nen co inventory day du. Chi hien:

- reward nhan duoc
- vi sao thang/thua
- shortcut nang cap hoac rematch

## 12. Dependency rule

```text
autoload
  ↓
repositories
  ↓
services
  ↓
scene controllers
  ↓
widgets / presenters
```

Rule bat buoc:

- repository khong goi scene
- service khong goi node tree
- widget khong tu sua save
- presenter khong duoc viet combat formula rieng

Neu vi pham rule nay, ve sau se rat kho test replay va kho balance.

## 13. Interface de xuat

## 13.1. `stat_resolver`

```gdscript
class_name StatResolver
extends RefCounted

func build_snapshot(build: RobotBuild) -> CombatantSnapshot:
    return CombatantSnapshot.new()
```

## 13.2. `combat_runner`

```gdscript
class_name CombatRunner
extends RefCounted

func run_battle(player_snapshot: CombatantSnapshot, enemy_snapshot: CombatantSnapshot, seed: int) -> BattleResult:
    return BattleResult.new()
```

## 13.3. `reward_system`

```gdscript
class_name RewardSystem
extends RefCounted

func build_reward_grant(stage: StageEncounterData, did_win: bool, was_first_clear: bool) -> RewardGrant:
    return RewardGrant.new()
```

API co the doi sau, nhung boundary nen giu:

- input la domain object ro rang
- output la domain object ro rang
- scene khong lam thay service

## 14. Save data boundary

Save game toi thieu nen luu:

```json
{
  "profile_id": "slot_01",
  "account_level": 3,
  "account_xp": 205,
  "resources": {
    "coins": 420,
    "scrap": 78,
    "core_shard": 1
  },
  "owned_parts": {
    "laser_emitter": {
      "owned": true,
      "level": 3
    }
  },
  "stage_progress": {
    "rust_yard_03": {
      "cleared": true,
      "first_clear_claimed": true,
      "best_result": "win"
    }
  },
  "current_build": {
    "head": "analyzer_node",
    "core": "stable_core",
    "left_arm": "laser_emitter",
    "right_arm": "capacitor_gun",
    "legs": "sprint_legs",
    "module": "heat_sink"
  }
}
```

Khong nen luu vao save:

- `CombatantSnapshot` da compile san
- `BattleState`
- event log cua moi tran thuong

Chi luu nhung thu do neu can `debug replay` va tach sang file rieng.

## 15. Test strategy

## 15.1. Unit tests bat buoc

- `part_repository` load dung schema
- `stat_resolver` compile dung snapshot
- `combat_runner` cho ket qua on dinh voi cung seed
- `reward_system` tra dung first clear / repeat / defeat
- `upgrade_system` tru dung resource va tang dung level

## 15.2. Integration tests bat buoc

- `Garage -> Battle -> Result` chay tron voi build starter
- clear `rust_yard_01` grant reward dung
- thua `burner_unit` van hien `failure_reason_hints`
- craft part counter xong quay lai clear duoc stage check

## 15.3. Replay tests

Can co it nhat cac replay test:

1. cung `player_snapshot`, `enemy_snapshot`, `seed` -> cung `BattleResult`
2. `Laser + Hammer` van resolve basic profile la `laser`
3. `Reflect Plate` khong chain reflect
4. `Bulwark Pulse` chi cast khi `shield_hp == 0`

## 16. Vertical slice implementation order

Thu tu code de toi uu rui ro:

1. `repositories`
2. `RobotBuild` + `InventoryState`
3. `build_validator`
4. `stat_resolver`
5. `combat_runner` + `effect_system`
6. `result_analyzer`
7. `reward_system`
8. `GarageScene` toi thieu
9. `BattleScene` playback toi thieu
10. `ResultScene`
11. `upgrade_system` + `craft_system`

Thu tu nay bam sat backlog trong `concept.md` nhung bo sung dependency code thuc te.

## 17. Quyet dinh chot trong tai lieu nay

1. combat la pure service, khong nam trong node scene
2. scene flow chot la `Garage -> Battle -> Result`
3. data authoring uu tien `JSON`, khong ep `.tres` tu dau
4. repository, service, presentation la 3 boundary chinh can giu
5. MVP battle rendering uu tien `simulate-all-then-playback`

## 18. Viec nen lam ngay sau tai lieu nay

1. tao skeleton folder va class rong theo structure tren
2. code `part_repository`, `enemy_repository`, `economy_repository`
3. code `RobotBuild`, `CombatantSnapshot`, `BattleResult`
4. code `stat_resolver`
5. code replay test dau tien cho `combat_runner`

Vi den muc nay design docs da du de chuyen sang implementation vertical slice.
