# Cấu trúc project Godot đề xuất

## 1) Mục tiêu của cấu trúc tốt

Một cấu trúc chuẩn nên giúp bạn:

- tìm file nhanh
- tái sử dụng scene/script dễ
- không phụ thuộc chằng chịt
- tách rõ gameplay, UI, data, system
- scale từ prototype lên production mà không phải đập đi làm lại

Godot khuyến nghị tập trung vào scene organization, phân biệt khi nào nên dùng scene, khi nào nên dùng script, và tránh lạm dụng node cho mọi thứ.

## 2) Cấu trúc thư mục khuyên dùng

```text
res://
├─ project.godot
├─ icon.svg

├─ addons/                 # plugin/editor addon
├─ autoload/               # singleton global thật sự cần dùng
│  ├─ game_manager.gd
│  ├─ audio_manager.gd
│  ├─ save_manager.gd
│  └─ scene_router.gd

├─ core/                   # code nền tảng dùng chung toàn project
│  ├─ constants/
│  │  └─ game_constants.gd
│  ├─ utils/
│  │  ├─ math_utils.gd
│  │  ├─ file_utils.gd
│  │  └─ debug_utils.gd
│  ├─ base/
│  │  ├─ base_character.gd
│  │  ├─ base_enemy.gd
│  │  ├─ base_ui_panel.gd
│  │  └─ state.gd
│  ├─ systems/
│  │  ├─ save/
│  │  ├─ audio/
│  │  ├─ input/
│  │  └─ localization/
│  └─ resources/
│     ├─ stat_block.gd
│     ├─ weapon_data.gd
│     └─ enemy_data.gd

├─ features/               # tổ chức theo feature/domain
│  ├─ player/
│  │  ├─ player.tscn
│  │  ├─ player.gd
│  │  ├─ player_input.gd
│  │  ├─ player_animator.gd
│  │  └─ data/
│  │     └─ player_default_stats.tres
│  ├─ robot_parts/
│  │  ├─ part_inventory_ui.tscn
│  │  ├─ part_inventory_ui.gd
│  │  ├─ robot_part.gd
│  │  └─ data/
│  │     ├─ arm_laser.tres
│  │     └─ leg_booster.tres
│  ├─ combat/
│  │  ├─ bullet.tscn
│  │  ├─ bullet.gd
│  │  ├─ hitbox.gd
│  │  ├─ hurtbox.gd
│  │  └─ damage_system.gd
│  ├─ enemies/
│  │  ├─ enemy_grunt.tscn
│  │  ├─ enemy_grunt.gd
│  │  ├─ enemy_boss.tscn
│  │  └─ data/
│  │     ├─ enemy_grunt.tres
│  │     └─ enemy_boss.tres
│  ├─ stages/
│  │  ├─ gym/
│  │  │  ├─ gym_stage_01.tscn
│  │  │  └─ gym_stage_01.gd
│  │  ├─ tournament/
│  │  └─ shared/
│  ├─ ui/
│  │  ├─ hud/
│  │  ├─ menus/
│  │  ├─ dialogs/
│  │  └─ widgets/
│  └─ progression/
│     ├─ level_system.gd
│     ├─ reward_system.gd
│     └─ unlock_system.gd

├─ scenes/                 # composition scenes cấp cao
│  ├─ main/
│  │  ├─ main.tscn
│  │  └─ main.gd
│  ├─ bootstrap/
│  │  └─ bootstrap.tscn
│  └─ test/
│     ├─ test_combat.tscn
│     └─ test_robot_parts.tscn

├─ assets/
│  ├─ art/
│  │  ├─ characters/
│  │  ├─ environments/
│  │  ├─ ui/
│  │  └─ effects/
│  ├─ audio/
│  │  ├─ bgm/
│  │  ├─ sfx/
│  │  └─ voice/
│  ├─ fonts/
│  └─ vfx/

├─ data/
│  ├─ balance/
│  ├─ localization/
│  ├─ json/
│  └─ saves/

├─ tests/
├─ docs/
└─ third_party/
```

### Vì sao cấu trúc này tốt

- `features/` chứa logic theo miền nghiệp vụ của game.
- `core/` chứa thứ dùng chung, không phụ thuộc gameplay cụ thể.
- `autoload/` chỉ chứa global manager thật sự cần tồn tại xuyên scene.
- `scenes/` dành cho các scene cấp điều phối, entry point, test map.
- `assets/` tách khỏi code để project sạch hơn.
- `data/` giữ file config, balance, localization, resource ngoài logic.

## 3) Best practice quan trọng: tổ chức theo feature, không chỉ theo loại file

Không nên chỉ tách `scripts/`, `scenes/`, `textures/`, `sounds/` vì về sau khó tìm.

Nên gom theo feature, ví dụ `features/enemies/boss/` gồm scene, script, data, asset liên quan.

## 4) Quy tắc chia scene và script

**Dùng scene khi:**
- object có cây node riêng
- object có thể instantiate nhiều lần
- object là UI panel/enemy/bullet/player/map chunk
- object có animation, collision, effect, child node

**Dùng script khi:**
- logic thuần
- helper/service
- calculator/formatter/parser
- AI utility
- state machine state class
- config wrapper

**Dùng Resource khi:**
- dữ liệu cần lưu, tái sử dụng, serialize
- stats, weapon config, enemy config, skill data
- item definition, robot part data, dialogue data, mission data

## 5) Quy tắc đặt tên

- File: `snake_case` (`player.gd`, `enemy_boss_stats.tres`)
- Class: `PascalCase` (`class_name Player`)
- Biến/hàm: `snake_case`
- Constant: `UPPER_SNAKE_CASE`

## 6) Mẫu chia code trong một feature

```text
features/player/
├─ player.tscn
├─ player.gd
├─ player_input.gd
├─ player_animator.gd
├─ player_state_machine.gd
├─ states/
│  ├─ player_idle_state.gd
│  ├─ player_run_state.gd
│  ├─ player_attack_state.gd
│  └─ player_dead_state.gd
└─ data/
   └─ player_default_stats.tres
```

Tách `input`, `animator`, `state_machine`, `states` để tránh `player.gd` quá dài.

## 7) Mẫu script production-friendly

```gdscript
extends CharacterBody2D
class_name Player

@export var move_speed: float = 180.0
@export var stats: StatBlock

@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var state_machine: PlayerStateMachine = $StateMachine

var move_input: Vector2 = Vector2.ZERO

func _ready() -> void:
    _validate_dependencies()
    state_machine.initialize(self)

func _physics_process(delta: float) -> void:
    _read_input()
    _apply_movement()
    move_and_slide()

func _read_input() -> void:
    move_input = Input.get_vector("move_left", "move_right", "move_up", "move_down")

func _apply_movement() -> void:
    velocity = move_input * move_speed

func take_damage(amount: int) -> void:
    if stats == null:
        return
    stats.current_hp = max(stats.current_hp - amount, 0)

func _validate_dependencies() -> void:
    assert(sprite != null, "Player requires AnimatedSprite2D")
    assert(state_machine != null, "Player requires PlayerStateMachine")
```

## 8) Autoload: dùng đúng cách

Chỉ autoload cho thứ sống xuyên toàn game, truy cập từ nhiều nơi, không thuộc scene gameplay cụ thể.

Nên: `GameManager`, `AudioManager`, `SaveManager`, `SceneRouter`, `ConfigManager`.

## 9) Tách data khỏi logic bằng Resource

Ví dụ:

```gdscript
extends Resource
class_name WeaponData

@export var weapon_id: String
@export var display_name: String
@export var damage: int = 10
@export var cooldown: float = 0.5
@export var projectile_scene: PackedScene
```

## 10) Quy tắc dependency

```text
autoload
   ↓
core
   ↓
features
   ↓
scenes
```

- `core` không phụ thuộc feature cụ thể.
- Feature A tránh gọi sâu vào internals của feature B.
- UI gọi service/API public, không chọc sâu node tree gameplay.
- Scene cấp cao chỉ compose, không ôm hết business logic.

## 11) Quy tắc tổ chức scene tree

Ví dụ:

```text
Player (CharacterBody2D)
├─ Visual
│  ├─ AnimatedSprite2D
│  └─ WeaponSocket
├─ Collision
│  └─ CollisionShape2D
├─ StateMachine
├─ Hurtbox
├─ CameraAnchor
└─ Effects
```

## 12) Pattern folder nên có

- `core/base/`: base class dùng chung
- `core/utils/`: hàm thuần, không giữ global state
- `core/constants/`: constant dùng chung
- `tests/`: test scene/script theo từng hệ thống

## 13) Version control

Nên commit:
- `.gd`, `.tscn`, `.tres`
- asset nguồn cần thiết
- `project.godot`

Nên tránh commit:
- import cache
- build/export output
- temp/debug file

## 14) Mẫu cho game pixel robot

```text
features/
├─ player/
├─ robot_assembly/
├─ combat/
├─ ai/
├─ gyms/
├─ tournament/
├─ inventory/
├─ rewards/
├─ progression/
└─ ui/
```

## 15) 10 rule ngắn gọn

1. Mỗi scene một trách nhiệm chính
2. Script > 300–400 dòng thì tách
3. Data cấu hình đưa sang Resource
4. Autoload ít thôi
5. Không hardcode path node quá nhiều
6. Dùng type hint đầy đủ khi có thể
7. Tên file/node/class nhất quán
8. UI không can thiệp logic sâu
9. Tạo test scene riêng cho từng hệ thống
10. Tổ chức theo feature trước, theo loại file sau

## 16) Cấu trúc tối giản cho giai đoạn bắt đầu

```text
res://
├─ autoload/
├─ core/
├─ features/
│  ├─ player/
│  ├─ enemies/
│  ├─ combat/
│  ├─ ui/
│  └─ stages/
├─ assets/
├─ scenes/
└─ data/
```

Triết lý: shared vào `core`, gameplay vào `features`, global vào `autoload`, data riêng vào `data` hoặc `*.tres`.
