# AssembleX

## 1. Product Definition

### 1.1. One-line pitch

`AssembleX` là game pixel sci-fi xây robot theo từng part, nơi người chơi kiếm linh kiện, lắp build theo chiến thuật và đưa robot vào các trận đấu semi-auto ngắn để vượt campaign, farm tài nguyên và tối ưu đội hình.

### 1.2. Product version this document defines

Tài liệu này định nghĩa:

- `Vertical Slice + MVP production scope`
- `PC first`
- `Single-player PvE first`
- `Async PvP` là phase mở rộng sau khi combat và balance ổn định

### 1.3. Design goal

Người chơi phải cảm thấy:

- mỗi part thay đổi cách robot vận hành thật sự
- thua trận là vì build sai hoặc chọn sai counter, không phải vì game mơ hồ
- mỗi trận ngắn, đọc được, có chỗ để test giả thuyết build

### 1.4. Non-goals for MVP

Không làm trong MVP:

- open world
- real-time action control
- co-op online
- gacha phức tạp
- 3v3 squad combat
- hệ thống xã hội sâu

MVP chỉ cần chứng minh một điều:

> build robot theo part tạo ra quyết định chiến thuật đủ thú vị để người chơi muốn thử build tiếp theo

## 2. Player Fantasy And Audience

### 2.1. Core fantasy

Người chơi bắt đầu như một thợ ráp robot ở xưởng nhỏ, đi lên bằng việc tận dụng linh kiện rẻ tiền để đánh bại những đối thủ có máy mạnh hơn nhưng build kém hơn.

Fantasy chính không phải:

- trở thành chiến binh điều khiển robot bằng tay

Fantasy chính là:

- trở thành kỹ sư biết ráp đúng đồ
- nhìn robot tự vận hành đúng như tính toán
- thắng bằng build thông minh và synergy

### 2.2. Target audience

Phù hợp với người chơi thích:

- buildcraft
- auto-battler nhẹ
- theorycraft build
- game có vòng lặp ngắn, dễ test build

Không nhắm tới người chơi cần:

- điều khiển action tốc độ cao
- cốt truyện dài làm trọng tâm
- MMO progression nhiều social layer

### 2.3. Session target

- `1 trận`: `45-90s`
- `1 session ngắn`: `10-15 phút`
- `1 session dài`: `30-45 phút`

## 3. Core Game Pillars

### 3.1. Build decides battle

Kết quả trận đấu được quyết định chủ yếu bởi:

- tổ hợp part
- nhịp gain energy
- khả năng counter effect của đối thủ

### 3.2. Fast readable battles

Combat phải ngắn và đọc được. Người chơi cần hiểu:

- robot mình đang làm gì
- skill nào đang mạnh
- vì sao vừa thắng hoặc thua

### 3.3. Small number, high meaning

Số lượng stat và effect không được quá nhiều ở giai đoạn đầu. Mỗi stat phải có tác động rõ ràng để balance và UI dễ đọc.

### 3.4. Test-improve loop

Loop chuẩn của game:

`Chọn map -> đọc đối thủ -> sửa build -> vào trận -> xem log kết quả -> nâng part -> thử lại`

## 4. Product Scope Decision

### 4.1. Scope chosen for first playable

Phiên bản đầu tiên của game tập trung vào:

- `1v1 robot duel`
- `campaign PvE`
- `build editor`
- `part inventory`
- `upgrade part`
- `combat result breakdown`

### 4.2. Scope moved out of MVP

Các mode vẫn có thể tồn tại trong tầm nhìn sản phẩm, nhưng chưa là trọng tâm sản xuất:

- `Puzzle mode`: phase 2
- `Gym mode`: phase 2
- `Tour mode`: phase 3
- `Async PvP`: phase 3

Lý do:

- core fun của AssembleX nằm ở build + combat outcome
- nếu combat chưa chắc tay thì các mode khác chỉ làm tăng scope chứ không tăng giá trị

## 5. Core Gameplay Loop

### 5.1. Macro loop

```text
Clear Stage
  -> Earn Coins + Scrap + Possible Part Drop
  -> Upgrade Existing Part or Craft Missing Part
  -> Adjust Build For Next Enemy
  -> Enter Next Stage
```

### 5.2. Micro loop per stage

```text
Read enemy preview
  -> pick robot parts
  -> start battle
  -> watch result and battle log
  -> compare damage / durability / energy tempo
  -> rematch or reassemble
```

### 5.3. Failure loop

Khi thua, game phải chỉ ra ít nhất một nguyên nhân rõ ràng:

- thiếu damage
- bị burst quá nhanh
- không đủ accuracy
- không đủ energy để xoay skill
- không có cách xử lý burn / shield / reflect

## 6. Game Structure

### 6.1. Launch structure

Game có `3 layer` rõ ràng:

1. `Garage`
2. `Battle`
3. `Progression`

### 6.2. Garage

Garage là màn chính. Từ đây người chơi làm các việc:

- xem inventory
- lắp robot
- nâng cấp part
- xem stage tiếp theo
- xem enemy preview

### 6.3. Battle

Battle là trận 1v1 semi-auto diễn ra trong arena ngang đơn giản, tập trung vào thông tin chứ không phải né đạn thủ công.

### 6.4. Progression

Progression trả phần thưởng, mở khóa part mới, mở map mới và tăng giới hạn phát triển build.

## 7. Robot Structure

### 7.1. Robot slots

Một robot trong MVP có đúng `6 slot`:

- `Head`
- `Core`
- `Left Arm`
- `Right Arm`
- `Legs`
- `Module`

Lý do chọn `6 slot`:

- đủ nhiều để tạo synergy
- chưa quá rối đối với UI và balance

### 7.2. Slot responsibility

| Slot | Vai trò chính |
| --- | --- |
| Head | AI pattern + stat phụ |
| Core | max energy + energy regen |
| Left Arm | attack pattern hoặc active skill |
| Right Arm | attack pattern hoặc active skill |
| Legs | speed + evasion/mobility trait |
| Module | passive đặc biệt |

### 7.3. Build rules

- mỗi robot phải có đủ 6 slot mới được vào trận
- mỗi robot chỉ có `1 active skill priority`
- nếu cả hai arm đều có skill, skill của arm bên trái là `Primary Skill`
- arm bên phải mặc định là `Basic Weapon Trait`

Rule này giúp combat dễ đọc và hạn chế spam skill mất kiểm soát trong MVP.

## 8. Stat System

### 8.1. Combat stats used in MVP

Chỉ dùng `9 stat`:

- `HP`
- `ATK`
- `DEF`
- `SPD`
- `ENERGY_REGEN`
- `MAX_ENERGY`
- `ACC`
- `EVA`
- `CRIT_RATE`

`CRIT_DMG` trong MVP cố định là `150%` để giảm độ phức tạp balance.

### 8.2. Base ranges at level 1

| Stat | Typical range |
| --- | --- |
| HP | `180 - 320` |
| ATK | `18 - 42` |
| DEF | `0 - 40` |
| SPD | `0.7 - 1.5` |
| ENERGY_REGEN | `6 - 14 / giây` |
| MAX_ENERGY | `60 - 120` |
| ACC | `75 - 110` |
| EVA | `0 - 25` |
| CRIT_RATE | `0% - 25%` |

### 8.3. Damage formula

```text
final_damage = raw_damage * (100 / (100 + target_def))
```

### 8.4. Basic attack formula

```text
raw_damage = attacker_atk * weapon_multiplier
```

`weapon_multiplier` mặc định nằm trong khoảng `0.85 - 1.25` tùy arm.

### 8.5. Crit formula

```text
if crit:
  final_damage = final_damage * 1.5
```

### 8.6. Hit chance formula

```text
hit_chance = clamp(attacker_acc - target_eva, 20, 95)
```

Nếu dùng hệ số phần trăm trong code:

```text
hit_roll <= hit_chance
```

### 8.7. Attack interval formula

```text
attack_interval = 1 / spd
```

Ví dụ:

- `SPD 1.0` -> `1 hit / giây`
- `SPD 1.25` -> `0.8 giây / hit`

## 9. Energy System

### 9.1. Why energy is the pacing core

Energy quyết định tần suất dùng skill, nên đây là stat tạo khác biệt build mạnh nhất sau ATK và DEF.

### 9.2. Energy gain sources in MVP

- hồi tự nhiên mỗi giây từ `ENERGY_REGEN`
- `+6` khi basic attack trúng
- `+4` khi nhận damage từ basic attack
- `+8` khi nhận damage từ skill

### 9.3. Skill cast rule

- robot dùng `Primary Skill` ngay khi `current_energy >= skill_cost`
- sau khi cast, trừ energy ngay
- không có cast time trong MVP
- có `skill_lock` tối thiểu `0.4s` để animation và log dễ đọc

### 9.4. Balance guardrails

- không part nào được cho `free skill cast`
- energy regen bonus theo module bị giới hạn ở `+35%`
- `MAX_ENERGY` không vượt `160` trong MVP

## 10. Battle System

### 10.1. Battle format

- `1v1`
- `semi-auto`
- `tick-based`
- `0.2 giây / tick`
- `timeout`: `75 giây`

Nếu hết giờ:

1. ai còn nhiều `HP%` hơn thắng
2. nếu bằng nhau, ai gây tổng damage lớn hơn thắng

### 10.2. Battle flow

```text
Load combatants
  -> apply passive on start
  -> run tick loop
  -> resolve attack timers
  -> resolve skill checks
  -> apply damage and statuses
  -> check death or timeout
  -> show result breakdown
```

### 10.3. Tick order

Mỗi tick xử lý theo thứ tự:

1. cộng energy regen
2. giảm duration của effect
3. xử lý DOT
4. kiểm tra skill cast
5. cập nhật attack timer
6. resolve hit
7. kiểm tra death

Thứ tự này cần cố định để debug và replay ổn định.

### 10.4. Basic attack behavior

Mỗi arm đóng góp vào `weapon profile` tổng:

- nếu 2 arm cùng loại: nhận `same-family bonus`
- nếu khác loại: dùng profile của arm trái làm chính, arm phải thêm passive modifier

Ví dụ:

- `Laser + Laser` -> `+10% burn chance`
- `Laser + Hammer` -> basic attack vẫn là laser, hammer thêm `+8% break armor chance`

### 10.5. Result screen required data

Sau mỗi trận cần hiển thị:

- winner
- battle duration
- total damage dealt
- total damage taken
- number of skill casts
- damage by source
- status uptime

Nếu không có bảng này, người chơi khó học system.

## 11. Status Effect System

### 11.1. MVP effects

MVP chỉ dùng `4 effect`:

- `Burn`
- `Stun`
- `Shield`
- `Break Armor`

### 11.2. Effect definitions

| Effect | Logic |
| --- | --- |
| Burn | gây DOT mỗi giây bằng `4% ATK nguồn gây hiệu ứng`, stack tối đa `3` |
| Stun | mục tiêu không basic attack và không cast skill trong thời gian hiệu lực |
| Shield | chặn một lượng damage cố định trước khi trừ HP |
| Break Armor | giảm `25% DEF hiện tại`, duration ngắn |

### 11.3. Stack rules

- `Burn`: stack cộng dồn damage và refresh riêng từng stack
- `Stun`: không stack, chỉ refresh nếu thời lượng mới dài hơn
- `Shield`: không stack, lấy shield mới nếu giá trị cao hơn
- `Break Armor`: không stack, refresh duration

### 11.4. Duration rules

- `Burn`: `4s`
- `Stun`: `1.2s`
- `Shield`: `5s` hoặc tới khi vỡ
- `Break Armor`: `4s`

## 12. Skill System

### 12.1. Skill ownership rule

Trong MVP, `Primary Skill` luôn đến từ `Left Arm`.

Điều này giúp:

- data rõ ràng
- UI rõ
- người chơi hiểu arm trái là slot quyết định style build

### 12.2. Skill categories

MVP có đúng `5 loại skill`:

- direct damage
- damage + burn
- stun strike
- self shield
- energy burst

### 12.3. Skill design format

Mỗi skill cần có:

- `id`
- `name`
- `energy_cost`
- `target_rule`
- `effect_payload`
- `cooldown_lock`
- `vfx_key`
- `description_player_facing`

### 12.4. Example MVP skills

| Skill | Cost | Effect |
| --- | --- | --- |
| Overheat Beam | `50` | gây `180% ATK` và thêm `1 Burn` |
| Shock Ram | `45` | gây `140% ATK` và `Stun 1.2s` |
| Bulwark Pulse | `40` | tạo `Shield = 30% max HP` |
| Capacitor Dump | `60` | gây `220% ATK`, nếu crit hồi `20 energy` |
| Piercing Drill | `55` | gây `160% ATK` và `Break Armor 4s` |

### 12.5. Skill balance rule

Một skill mạnh không được vượt trội ở mọi mặt. Mỗi skill phải có đúng một lợi thế chính:

- damage cao
- utility cao
- survivability cao
- tempo energy cao

## 13. AI System

### 13.1. AI goal in MVP

AI không cần thông minh như player. AI chỉ cần ổn định, dễ đọc và dễ balance.

### 13.2. Targeting

Vì MVP là `1v1`, target rule đơn giản:

- luôn target đối thủ hiện tại

### 13.3. Skill logic

AI cast skill ngay khi đủ energy, trừ các trường hợp:

- `Shield skill` chỉ cast nếu HP dưới `70%`
- `Stun skill` cast ngay khi sẵn sàng
- `Damage skill` cast ngay khi sẵn sàng

### 13.4. Head-driven AI modifiers

Head không đổi target, nhưng đổi ưu tiên hành vi:

- `Hunter Head`: `+10 ACC`, ưu tiên damage đều
- `Analyzer Head`: `+5 energy on miss`, phù hợp build ổn định
- `Raider Head`: `+8% crit rate`, thiên burst

## 14. Part Design Framework

### 14.1. Part data template

Mỗi part cần các trường:

- `id`
- `slot`
- `rarity`
- `stat_bonus`
- `tags`
- `effect`
- `unlock_source`
- `upgrade_curve`

### 14.2. Part rarity in MVP

- `Common`
- `Rare`
- `Epic`

Không dùng `Legendary` trong MVP để tránh power creep sớm.

### 14.3. Upgrade levels

Mỗi part có `5 level`.

Ví dụ:

- level tăng stat chính
- không thay đổi effect logic
- effect chỉ mạnh hơn nếu part đạt `level 3` hoặc `level 5`

### 14.4. Upgrade cost curve

| Level up | Coins | Scrap |
| --- | --- | --- |
| 1 -> 2 | `100` | `20` |
| 2 -> 3 | `180` | `35` |
| 3 -> 4 | `320` | `60` |
| 4 -> 5 | `520` | `100` |

## 15. MVP Part List

### 15.1. Heads

| Part | Rarity | Effect |
| --- | --- | --- |
| Scout Visor | Common | `+8 ACC`, `+0.1 SPD` |
| Raider Chip | Rare | `+8% crit rate`, `-5 DEF` |
| Analyzer Node | Rare | `+10 max energy`, `gain 5 energy when miss` |

### 15.2. Cores

| Part | Rarity | Effect |
| --- | --- | --- |
| Stable Core | Common | `+10 energy regen`, `+20 max energy` |
| Burst Core | Rare | `+6 energy regen`, skill damage `+12%` |
| Guard Core | Rare | `+30 HP`, receive-hit energy `+2` |

### 15.3. Left Arms

| Part | Rarity | Skill |
| --- | --- | --- |
| Laser Emitter | Common | Overheat Beam |
| Ram Fist | Common | Shock Ram |
| Shield Projector | Rare | Bulwark Pulse |
| Drill Cannon | Rare | Piercing Drill |

### 15.4. Right Arms

| Part | Rarity | Passive |
| --- | --- | --- |
| Laser Emitter | Common | same-family laser bonus |
| Hammer Unit | Common | basic attacks có `8%` cơ hội Break Armor |
| Capacitor Gun | Rare | basic attack hit `+2` extra energy |

### 15.5. Legs

| Part | Rarity | Effect |
| --- | --- | --- |
| Sprint Legs | Common | `+0.25 SPD`, `-10 HP` |
| Tank Treads | Common | `+25 HP`, `+10 DEF`, `-0.15 SPD` |
| Balance Frame | Rare | `+12 EVA`, `+10 HP` |

### 15.6. Modules

| Part | Rarity | Effect |
| --- | --- | --- |
| Heat Sink | Common | burn damage taken `-30%` |
| Reflect Plate | Rare | phản `12%` damage nhận vào từ basic attack |
| Energy Coil | Rare | `+20% energy regen`, `-8 DEF` |
| Targeting Lens | Common | `+12 ACC` |

Tổng part MVP khuyến nghị: `17`.

Con số này đủ để tạo nhiều build mà vẫn balance được thủ công.

## 16. Build Archetypes

### 16.1. Burn Tempo

Build:

- Laser Emitter
- Capacitor Gun
- Stable Core
- Sprint Legs
- Heat Sink
- Analyzer Node

Play pattern:

- basic attack nhanh
- hồi energy đều
- spam burn để ăn mòn tank

Counter:

- Guard Core
- Heat Sink
- shield build

### 16.2. Tank Reflect

Build:

- Ram Fist
- Hammer Unit
- Guard Core
- Tank Treads
- Reflect Plate
- Scout Visor

Play pattern:

- chịu đòn tốt
- stun đúng nhịp
- thắng build quá thiên basic attack

Counter:

- build burst skill cao
- break armor

### 16.3. Burst Crit

Build:

- Drill Cannon
- Capacitor Gun
- Burst Core
- Sprint Legs
- Targeting Lens
- Raider Chip

Play pattern:

- đánh nhanh
- crit cao
- dồn damage skill để kết thúc trước khi bị outscale

Counter:

- tank shield
- high HP + moderate DEF

## 17. Enemy Design

### 17.1. Enemy role in campaign

Enemy không chỉ là HP bag. Mỗi enemy archetype phải dạy người chơi một bài học build.

### 17.2. MVP enemy archetypes

| Enemy | Ý đồ thiết kế |
| --- | --- |
| Scrap Brawler | tutorial enemy, chỉ số cơ bản dễ đọc |
| Burner Unit | dạy người chơi về DOT và Heat Sink |
| Guard Walker | dạy người chơi về shield và break armor |
| Raider Duelist | dạy về accuracy và burst |
| Iron Bastion Boss | ép người chơi chuẩn bị counter tank |

### 17.3. Boss rule

Mỗi boss cần:

- một gimmick rõ
- một cửa sổ bị counter rõ
- một reward part hoặc resource đủ hấp dẫn

Ví dụ boss đầu:

- `Iron Bastion`
- dùng shield lớn mỗi `12 giây`
- counter đúng bằng `Piercing Drill` hoặc build burn tempo kéo dài

## 18. Campaign Structure

### 18.1. Launch campaign layout

Campaign launch có `2 khu vực`, mỗi khu gồm:

- `5 regular stage`
- `1 boss stage`

Tổng:

- `12 battle`
- `2 boss`

### 18.2. Zone themes

| Zone | Theme | Gameplay lesson |
| --- | --- | --- |
| Rust Yard | xưởng phế liệu | học stat cơ bản, energy, burn |
| Neon Arena | giải đấu nội thành | học shield, crit, anti-tank |

### 18.3. Stage pacing

- Stage 1-2: giới thiệu cơ chế
- Stage 3-4: buộc đổi part
- Stage 5: pre-boss check
- Stage 6: boss

### 18.4. Difficulty rule

Không tăng độ khó chỉ bằng cộng số. Mỗi mốc phải thêm một bài test:

- kiểm tra damage
- kiểm tra sống sót
- kiểm tra counter effect
- kiểm tra ổn định accuracy

## 19. Progression System

### 19.1. Player progression

Player có `Account Level` dùng để:

- mở zone mới
- mở chức năng craft
- mở chức năng module upgrade

### 19.2. Account level sources

- clear stage lần đầu
- complete mission ngày
- clear boss

### 19.3. Part progression

Part tăng bằng:

- `Coins`
- `Scrap`

Không dùng duplicate fusion trong MVP.

### 19.4. Unlock pacing

Người chơi không nên có toàn bộ part quá sớm. Nhịp mở khóa đề xuất:

- `10 phút đầu`: 6-7 part
- `30 phút đầu`: 10-12 part
- `1-2 giờ đầu`: full bộ MVP 17 part

## 20. Economy

### 20.1. Resources in MVP

- `Coins`: nâng cấp part
- `Scrap`: craft part và nâng cấp sâu
- `Core Shard`: reward hiếm từ boss, dùng mở part rare

### 20.2. Reward targets

| Activity | Coins | Scrap | Core Shard |
| --- | --- | --- | --- |
| thường thắng stage | `60-120` | `10-25` | `0` |
| clear boss lần đầu | `250` | `60` | `1` |
| rematch boss | `120` | `25` | `10% drop` |

### 20.3. Craft rule

- common part: chỉ cần `Coins + Scrap`
- rare part: cần thêm `Core Shard`
- epic part: chưa craft được trong first MVP, chỉ reward từ boss hoặc chapter completion

### 20.4. Economy principle

Người chơi nên đủ tài nguyên để:

- nâng `1-2 part chủ lực` sau mỗi vài trận
- craft một part counter khi bị chặn tiến độ

Không nên để economy ép grind quá sớm.

## 21. Missions And Retention

### 21.1. Why missions exist

Missions không phải để kéo retention giả tạo. Chúng có vai trò hướng người chơi thử build mới.

### 21.2. Daily mission examples

- thắng 3 trận với `Burn` build
- cast shield 5 lần
- clear 2 stage mà không dùng module rare

### 21.3. Weekly mission examples

- đánh bại boss bằng 3 build khác nhau
- nâng 2 part lên level 4

## 22. UI And UX Requirements

### 22.1. Garage screen must show

- robot hiện tại
- tổng stat
- skill đang dùng
- module effect
- nút đổi part
- preview enemy kế tiếp

### 22.2. Part selection UX

Khi chọn part, UI phải cho biết:

- stat tăng giảm ngay lập tức
- tag build liên quan
- part này giúp chống cái gì
- part này yếu ở đâu

### 22.3. Battle HUD must show

- HP hai bên
- energy hai bên
- icon status
- skill name khi cast
- combat log rút gọn

### 22.4. Post-battle UX

Màn kết quả phải trả lời được:

- vì sao thắng hoặc thua
- nguồn damage lớn nhất
- effect nào quyết định trận
- nên đổi part nào nếu muốn rematch

## 23. Art And Presentation Direction

### 23.1. Visual target

- pixel art gọn
- silhouette robot dễ đọc
- mỗi slot part đổi hình rõ ràng
- hiệu ứng combat nhỏ nhưng sắc

### 23.2. Camera and scene choice

- side-view arena 2D
- nền đơn giản, ít parallax
- ưu tiên readability hơn spectacle

### 23.3. Animation priority

Nếu phải cắt scope, giữ theo thứ tự:

1. hit reaction
2. skill cast flash
3. burn / shield status feedback
4. idle polish

## 24. Narrative Layer

### 24.1. Story function

Cốt truyện chỉ cần đủ để tạo ngữ cảnh, không được làm chậm loop build-test-fight.

### 24.2. Story setup

Người chơi là kỹ sư trẻ tại `Rust Yard`, bị buộc tham gia chuỗi đấu robot để cứu xưởng khỏi việc bị tập đoàn `Heliox Systems` thâu tóm.

### 24.3. Factions

- `Rust Yard Builders`: dân ráp máy underground, tận dụng đồ phế liệu
- `Heliox Systems`: tập đoàn chuẩn hóa robot thương mại và kiểm soát giải đấu
- `Arena Brokers`: bên trung gian tổ chức trận đấu, bán thông tin và linh kiện

### 24.4. Narrative delivery

- intro ngắn dưới `60s`
- dialogue trước boss
- không quá `3-4 câu` mỗi sự kiện

## 25. MVP First 20 Minutes

### 25.1. Expected player journey

Phút `0-5`:

- nhận robot khung cơ bản
- học thay `Left Arm`
- thắng tutorial stage

Phút `5-10`:

- mở Core và Module
- gặp Burner Unit
- học value của counter build

Phút `10-15`:

- thua hoặc thắng sít sao một stage tank
- được dạy nâng cấp part

Phút `15-20`:

- chuẩn bị build để đánh boss đầu
- hiểu vòng lặp `đọc đối thủ -> sửa build -> rematch`

## 26. Balance Principles

### 26.1. What must never happen

- dodge build đạt trạng thái gần như bất tử
- energy build cast skill liên tục không có cửa phản ứng
- reflect build tự thắng mọi basic attack build
- burst crit xóa mục tiêu trước khi combat có thời gian đọc

### 26.2. Hard caps

- `CRIT_RATE <= 40%`
- `EVA <= 35`
- `SPD <= 1.8`
- `ENERGY_REGEN bonus <= +35%`
- `reflect <= 20%`

### 26.3. Balance process

Mỗi lần thêm part mới phải tự kiểm tra:

- part này thuộc archetype nào
- counter của nó là gì
- nếu người chơi không có counter đúng, vẫn có cửa thắng bằng nâng cấp hay không

## 27. Technical Direction For Godot

### 27.1. Scene structure

```text
GarageScene
BattleScene
ResultScene
```

### 27.2. Gameplay systems required

- `part_data`
- `robot_build`
- `stat_resolver`
- `combat_runner`
- `effect_system`
- `reward_system`

### 27.3. Data-first rule

Part, skill, enemy nên đi theo data definition trước, không hard-code rải rác trong scene.

Lý do:

- balance nhanh hơn
- thêm content dễ hơn
- build simulator sau này dễ làm

## 28. Production Backlog Order

### 28.1. Vertical slice order

1. Robot build data model
2. Stat resolver
3. Single battle simulation
4. Basic battle UI
5. 6-8 part đầu tiên
6. 3 enemy đầu tiên
7. reward + upgrade screen
8. boss đầu tiên

### 28.2. MVP completion criteria

MVP được coi là xong khi:

- người chơi có thể clear full campaign launch từ đầu tới boss cuối
- có ít nhất `3 build archetype` khả dụng
- thua trận vẫn đọc ra nguyên nhân
- balance không có build auto-win rõ ràng

## 29. Expansion After MVP

### 29.1. Phase 2

- Puzzle mode dùng cùng part system
- Gym mode để target stat training nhẹ
- thêm `2 module slot` nếu build depth thực sự cần

### 29.2. Phase 3

- Tour mode dạng node map
- Async PvP dùng battle replay từ build snapshot
- thêm faction part sets

### 29.3. Expansion rule

Chỉ mở rộng khi `campaign PvE core` đã chứng minh được:

- retention ổn
- build variety thật
- combat log đủ đọc

## 30. Final Product Statement

`AssembleX` ở phiên bản khả thi nhất không phải là game “có rất nhiều mode”, mà là game:

- có một loop build robot rất rõ
- có combat semi-auto ngắn, đọc được
- có part đủ khác nhau để người chơi muốn thử build mới
- có campaign buộc người chơi học cách counter và tối ưu

Nếu phải ưu tiên tuyệt đối, hãy ưu tiên theo thứ tự:

1. build clarity
2. combat readability
3. content pacing
4. progression
5. feature expansion

## 31. Next Design Documents To Create

Sau tài liệu này, nên viết tiếp đúng thứ tự:

1. `combat_spec.md`
2. `part_data_schema.md`
3. `enemy_roster.md`
4. `economy_balance_sheet.md`
5. `godot_system_architecture.md`

Nếu làm production thật, tài liệu quan trọng nhất kế tiếp là:

> `combat_spec.md` với state flow, event order, data schema và pseudo code đủ để code trực tiếp

## 32. Concept Audit Fixes For Production Readiness

Mục này bổ sung các điểm `cụ thể + thực tế` để team dùng ngay khi triển khai, giảm tình trạng tài liệu đúng ý tưởng nhưng khó đi vào việc.

### 32.1. "Definition of Done" cho từng trụ cột

Một build/combat iteration chỉ được coi là xong khi đạt đủ các điều kiện:

#### Build clarity

- Garage hiển thị rõ `stat trước/sau` khi đổi part
- Có cảnh báo đỏ nếu build thiếu slot hoặc sai slot
- Preview phải hiện được `1 threat chính` và `1 counter gợi ý` cho stage kế tiếp

#### Combat readability

- Mỗi trận đều có `battle timeline` và `post-battle breakdown`
- Khi thua, hệ thống trả về tối thiểu `1 failure reason`
- Người chơi có thể rematch trong `<= 2 click`

#### Progression pacing

- Sau `3 trận đầu`, người chơi phải đủ tài nguyên để nâng `ít nhất 1 part`
- Sau boss zone 1, người chơi có ít nhất `1 lựa chọn counter mới` (drop/craft/unlock)
- Không có stage nào bắt buộc farm lặp lại quá `3 lần` để đi tiếp

### 32.2. Combat clarity checklist bắt buộc cho mỗi build

Trước khi merge part/skill mới, designer phải check:

1. Skill mới có `telegraph text` ngắn trong log không?
2. Có thể chỉ ra counter trong `<= 1 câu` không?
3. Có tạo tình huống "không thể phản ứng" trong `10s đầu` không?
4. Có làm vỡ hard cap ở mục `26.2` không?
5. Có ít nhất `1 enemy` trong campaign dùng được part đó để dạy bài học build không?

Nếu câu 2 hoặc 3 fail, part chưa được đưa vào roster chính.

### 32.3. Economy guardrail thực dụng

Để tránh mất fun do tuning lệch, thêm 3 ngưỡng cảnh báo:

- `Red flag A`: thua liên tục 4 trận mà không đủ tài nguyên nâng/craft 1 lựa chọn hợp lý
- `Red flag B`: clear zone nhưng không thay đổi build lần nào vì không có động lực
- `Red flag C`: phần thưởng boss không tạo được bước nhảy build rõ rệt

Khi gặp red flag, ưu tiên sửa theo thứ tự:

1. tăng `first_clear scrap`
2. giảm cost `craft_common_b` hoặc `upgrade level 2-3`
3. chỉnh encounter tuning

Không sửa bằng cách tăng ATK/HP thô trên diện rộng.

## 33. Practical Content Plan For Launch

### 33.1. Enemy teaching map (12 stage launch)

Mỗi stage chính phải dạy đúng `1 bài`, tránh dồn quá nhiều cơ chế:

- `rust_yard_01-02`: làm quen nhịp đánh + hit/miss
- `rust_yard_03-04`: burn pressure và nhu cầu module counter
- `rust_yard_05`: bài học shield/def break cơ bản
- `rust_yard_06`: boss tổng hợp zone 1
- `neon_arena_01-02`: burst tempo và năng lượng
- `neon_arena_03-04`: evasion/accuracy check
- `neon_arena_05`: sustained duel và resource management
- `neon_arena_06`: boss kiểm tra năng lực đọc preview + tái lắp build

Nguyên tắc triển khai: nếu một stage dạy quá 1 bài và tỷ lệ thua tăng đột ngột, tách stage hoặc giảm 1 nguồn áp lực.

### 33.2. Build archetype tối thiểu phải "playable"

Ngoài việc "tồn tại", 3 archetype phải có khả năng clear campaign launch:

1. `Burn Tempo`
2. `Burst Crit`
3. `Shield Sustain`

Tiêu chí playable:

- clear được regular stage cùng cấp mà không cần perfect RNG
- có route nâng cấp rõ ràng level `1 -> 3 -> 5`
- có ít nhất `1 counter` và `1 mirror weakness` để tránh auto-win

### 33.3. Content authoring checklist

Mỗi part/enemy/stage mới cần đủ bộ metadata:

- `design_lesson`
- `failure_hint_focus`
- `preview.threat_tags`
- `preview.counter_tags`
- `economy reward profile`

Thiếu metadata thì không đưa vào build release, vì sẽ phá vòng lặp "thua -> hiểu lý do -> chỉnh build".

## 34. Live Playtest Protocol (MVP Internal)

### 34.1. 3 chỉ số theo dõi bắt buộc

- `Retry Rate / Stage`: stage nào bị retry quá cao
- `Build Change Rate`: người chơi có thực sự đổi part sau khi thua không
- `Time To First Meaningful Upgrade`: mất bao lâu để nâng cấp có tác động rõ

### 34.2. Ngưỡng đánh giá đề xuất

- Retry rate hợp lý: `1.3 - 2.2` mỗi stage khó
- Build change rate tối thiểu: `>= 45%` sau các trận thua
- Time to first meaningful upgrade: `< 8 phút`

Nếu build change rate thấp nhưng retry cao, vấn đề thường nằm ở preview/hint chứ không phải chỉ số damage.

### 34.3. Quy trình fix mỗi vòng playtest

1. Khóa seed cho 5 trận mẫu để so sánh trước/sau
2. Sửa đúng `1 nhóm` (combat hoặc economy hoặc enemy preview)
3. Chạy lại cùng route 20 phút đầu
4. Ghi rõ lý do thay đổi vào changelog design

Không gộp nhiều thay đổi lớn trong 1 vòng vì khó truy nguyên nguyên nhân.

## 35. UX Rules To Reduce Frustration

### 35.1. Sau mỗi trận thua phải có "next step" rõ

UI result cần hiển thị tối thiểu:

- lý do thua chính
- 1 gợi ý thay part
- 1 gợi ý nâng part
- nút rematch nhanh

### 35.2. Cảnh báo sớm trong garage

Trước khi vào stage, garage nên cảnh báo:

- `ACC thấp` so với enemy EVA
- `thiếu counter burn/shield/reflect` nếu enemy threat tag có
- `energy tempo thấp` nếu skill cost quá cao so với regen

Mục tiêu: giảm thua "mù", tăng thua "học được".

### 35.3. Principle cuối cùng cho mọi quyết định

Nếu có nhiều phương án, chọn phương án giúp người chơi trả lời được 3 câu hỏi sau nhanh nhất:

1. Tôi vừa thua vì gì?
2. Tôi nên đổi gì ngay bây giờ?
3. Tôi có đủ tài nguyên để thử lại không?
