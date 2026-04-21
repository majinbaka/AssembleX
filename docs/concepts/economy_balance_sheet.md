# AssembleX Economy Balance Sheet

## 1. Muc tieu tai lieu

Tai lieu nay chot `economy sheet` cho MVP de:

1. team content co bang reward va cost nhat quan
2. `curve_id` trong `part_data_schema.md` co noi de tro toi
3. team code implement `reward_system`, `craft`, `upgrade` va `unlock pacing` ma khong can doan y
4. vertical slice co vong lap tai nguyen du de test build, nhung chua ep grind som

Tai lieu nay cover:

- resource enum va vai tro
- reward target theo stage
- upgrade cost curve theo `curve_id`
- craft cost theo rarity
- account unlock pacing cho MVP

Tai lieu nay khong cover:

- shop economy day du
- mission daily chi tiet
- monetization

## 2. Nguyen tac economy

Economy MVP phai giu 5 tinh chat:

1. `counter-accessible`: khi bi chan tien do, nguoi choi co the craft hoac nang part counter trong vai tran tiep theo
2. `no-hard-RNG-wall`: progression chinh khong duoc bi khoa boi drop den ngau nhien
3. `upgrade-before-hoard`: nguoi choi nen thay loi ich khi nang `1-2` part chu luc truoc khi om tai nguyen
4. `boss-feels-special`: boss phai tra reward ro rang hon regular stage
5. `launch-readable`: con so it, nhin la hieu, de debug va de balance lai

## 3. Resource enum va vai tro

## 3.1. Resource enum

- `coins`
- `scrap`
- `core_shard`
- `account_xp`

## 3.2. Vai tro tung resource

### `coins`

- dung cho `part upgrade`
- cung la thanh phan craft co ban
- la resource pho bien nhat

### `scrap`

- dung cho `part upgrade`
- dung cho `craft`
- la diem nghen vua phai de buoc nguoi choi chon uu tien build

### `core_shard`

- reward hiem tu boss
- dung de craft `rare part`
- khong dung cho `common part`

### `account_xp`

- dung de mo khoa tinh nang va zone
- khong tham gia truc tiep vao combat power

## 4. Progression pacing target

Khi nguoi choi di dung campaign launch:

- `10 phut dau`: mo du `craft`, so huu `6-7 part`
- `30 phut dau`: mo `module upgrade`, bat dau co `10-12 part`
- `1-2 gio dau`: clear toan bo campaign launch va chuan bi co full `17 part MVP`

Neu metric thuc te lech qua xa:

- thieu tai nguyen -> tang `first_clear reward`
- du tai nguyen nhung van thua -> sua `part roster` hoac `enemy tuning`, khong tang cost vo can

## 5. Reward model

## 5.1. Reward schema khuyen nghi

```json
{
  "reward_profile_id": "regular_zone_1",
  "first_clear": {
    "coins": 90,
    "scrap": 18,
    "core_shard": 0,
    "account_xp": 40
  },
  "repeat_clear": {
    "coins": 70,
    "scrap": 14,
    "core_shard_drop_rate": 0.0,
    "account_xp": 10
  },
  "defeat": {
    "coins": 25,
    "scrap": 4,
    "account_xp": 4
  }
}
```

## 5.2. Reward rules

### First clear

- tra reward day du
- dung de day progression chinh
- moi stage chi co `1 lan first_clear`

### Repeat clear

- tra it hon first clear
- van du de farm nhe khi can craft counter
- boss rematch moi co `core_shard_drop_rate`

### Defeat

- van tra mot it `coins` va `scrap`
- muc tieu la giu vong lap "thu build -> doc ket qua -> sua build -> thu lai"
- defeat reward khong duoc cao den muc khuyen khich thua de farm

## 5.3. Reward target tong quat

| Activity | Coins | Scrap | Core Shard |
| --- | --- | --- | --- |
| regular stage first clear | `70-120` | `12-25` | `0` |
| regular stage repeat clear | `60-90` | `10-18` | `0` |
| boss first clear | `250` | `60` | `1` |
| boss repeat clear | `120` | `25` | `10% drop` |
| defeat reward | `20-35` | `3-6` | `0` |

Bang nay ke thua target trong `concept.md`, bo sung them defeat reward de UX khong bi cut qua gat.

## 6. Launch campaign reward table

Bang nay la gia tri cu the de dung cho launch `12 battle`.

| Stage | First Clear | Repeat Clear | Defeat |
| --- | --- | --- | --- |
| `rust_yard_01` | `70 / 12 / 0 / 40xp` | `60 / 10 / 0 / 10xp` | `20 / 3 / 0 / 4xp` |
| `rust_yard_02` | `80 / 14 / 0 / 40xp` | `60 / 10 / 0 / 10xp` | `20 / 3 / 0 / 4xp` |
| `rust_yard_03` | `90 / 18 / 0 / 40xp` | `70 / 14 / 0 / 10xp` | `25 / 4 / 0 / 4xp` |
| `rust_yard_04` | `100 / 20 / 0 / 40xp` | `70 / 14 / 0 / 10xp` | `25 / 4 / 0 / 4xp` |
| `rust_yard_05` | `110 / 22 / 0 / 40xp` | `80 / 16 / 0 / 10xp` | `30 / 5 / 0 / 4xp` |
| `rust_yard_06` | `250 / 60 / 1 / 100xp` | `120 / 25 / 10% / 25xp` | `35 / 6 / 0 / 6xp` |
| `neon_arena_01` | `100 / 18 / 0 / 45xp` | `70 / 14 / 0 / 10xp` | `25 / 4 / 0 / 4xp` |
| `neon_arena_02` | `110 / 20 / 0 / 45xp` | `80 / 16 / 0 / 10xp` | `25 / 4 / 0 / 4xp` |
| `neon_arena_03` | `110 / 22 / 0 / 45xp` | `80 / 16 / 0 / 10xp` | `30 / 5 / 0 / 4xp` |
| `neon_arena_04` | `120 / 24 / 0 / 45xp` | `90 / 18 / 0 / 10xp` | `30 / 5 / 0 / 4xp` |
| `neon_arena_05` | `120 / 25 / 0 / 45xp` | `90 / 18 / 0 / 10xp` | `30 / 5 / 0 / 4xp` |
| `neon_arena_06` | `250 / 60 / 1 / 100xp` | `120 / 25 / 10% / 25xp` | `35 / 6 / 0 / 6xp` |

Format tung o:

```text
coins / scrap / core_shard / account_xp
```

## 6.1. Tong tai nguyen neu clear campaign launch 1 lan

Neu clear tat ca `12 stage` o first clear:

- `coins = 1510`
- `scrap = 315`
- `core_shard = 2`
- `account_xp = 670`

Muc nay du de:

- nang 1 common part len `5`
- craft 1 rare counter part
- van con tai nguyen de nang them 1-2 moc cho part khac

Neu playtest cho thay chua du de "xoay build", uu tien tang `scrap` truoc khi tang `coins`.

## 7. Unlock va acquisition rules

## 7.1. `starter`

- grant ngay tu dau
- khong ton tai cost

## 7.2. `stage_clear`

- mo khoa chac chan khi clear stage dau tien
- khong dung RNG

## 7.3. `stage_drop`

MVP khong nen de `stage_drop` la RNG thuan.

Khuyen nghi:

- co the roi som hon qua drop chance
- nhung phai `guaranteed unlock` cham nhat o lan clear thu `4` cua dung stage

Day la `pity rule` de tranh hard wall cho part counter quan trong.

## 7.4. `craft`

- chi mo khi player dat `account_level` du dieu kien
- recipe lay tu bang craft ben duoi

## 7.5. `boss_reward`

- grant truc tiep o `first clear` boss neu part duoc dat lam reward
- khong thay cho `core_shard`; boss co the tra ca `part` va `resource`

## 8. Craft cost model

## 8.1. Nguyen tac

- `common part` craft bang `coins + scrap`
- `rare part` craft bang `coins + scrap + core_shard`
- MVP khong craft `epic`

## 8.2. Recipe theo rarity

| Recipe | Coins | Scrap | Core Shard |
| --- | --- | --- | --- |
| `craft_common_a` | `160` | `35` | `0` |
| `craft_common_b` | `200` | `45` | `0` |
| `craft_rare_a` | `260` | `60` | `1` |
| `craft_rare_b` | `320` | `75` | `1` |

Khuyen nghi su dung:

- `common starter-sidegrade` -> `craft_common_a`
- `common counter part` -> `craft_common_b`
- `rare head/core/module` -> `craft_rare_a`
- `rare arm` -> `craft_rare_b`

## 8.3. Vi du mapping recipe

| Part | Recipe |
| --- | --- |
| `burst_core` | `craft_rare_a` |
| `analyzer_node` | `craft_rare_a` |
| `shield_projector` | `craft_rare_b` |
| `drill_cannon` | `craft_rare_b` |

Neu mot part da la `stage_clear` hoac `boss_reward`, van co the them recipe ve sau de completionist craft lai. MVP chua can.

## 9. Upgrade cost curve

## 9.1. Nguyen tac

- `max_level = 5`
- player cam nhan duoc suc manh tang tu level `2-3` rat som
- moc `4-5` la dau tu ro rang, khong phai default cho moi part
- `core_shard` khong dung cho upgrade trong MVP; chi dung cho craft rare de giam phuc tap

## 9.2. Cost schema khuyen nghi

```json
{
  "curve_id": "arm_common_a",
  "upgrade_costs": {
    "2": { "coins": 100, "scrap": 20 },
    "3": { "coins": 180, "scrap": 35 },
    "4": { "coins": 320, "scrap": 60 },
    "5": { "coins": 520, "scrap": 100 }
  }
}
```

## 9.3. Cost curve chot

### `arm_common_a`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `100` | `20` |
| `3` | `180` | `35` |
| `4` | `320` | `60` |
| `5` | `520` | `100` |

### `arm_common_b`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `100` | `20` |
| `3` | `180` | `35` |
| `4` | `320` | `60` |
| `5` | `520` | `100` |

### `legs_common_a`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `90` | `18` |
| `3` | `170` | `32` |
| `4` | `300` | `55` |
| `5` | `480` | `90` |

### `head_rare_a`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `140` | `30` |
| `3` | `240` | `50` |
| `4` | `400` | `80` |
| `5` | `640` | `120` |

### `core_rare_a`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `150` | `32` |
| `3` | `260` | `55` |
| `4` | `430` | `85` |
| `5` | `680` | `130` |

### `module_rare_a`

| To Level | Coins | Scrap |
| --- | --- | --- |
| `2` | `130` | `28` |
| `3` | `230` | `48` |
| `4` | `380` | `76` |
| `5` | `620` | `118` |

## 9.4. Tong cost tham chieu

Tong cost tu `1 -> 5`:

- `arm_common_a` = `1120 coins`, `215 scrap`
- `legs_common_a` = `1040 coins`, `195 scrap`
- `head_rare_a` = `1420 coins`, `280 scrap`
- `core_rare_a` = `1520 coins`, `302 scrap`
- `module_rare_a` = `1360 coins`, `270 scrap`

Doc bang nay de kiem tra pacing:

- 1 common part len max ~= clear gan tron campaign launch
- 1 rare part len max can them repeat clear hoac bo bot craft

Day la chu dich, vi rare part khong nen tro thanh default max som.

## 10. Account level pacing

## 10.1. XP source

| Activity | Account XP |
| --- | --- |
| regular stage first clear | `40-45` |
| regular stage repeat clear | `10` |
| boss first clear | `100` |
| boss repeat clear | `25` |
| defeat | `4-6` |

## 10.2. Level threshold

| Account Level | XP Tong | Unlock |
| --- | --- | --- |
| `1` | `0` | co san garage co ban |
| `2` | `80` | mo `craft` |
| `3` | `180` | mo `module upgrade` |
| `4` | `320` | mo `neon_arena` |
| `5` | `520` | khong mo them system moi, dung lam pacing buffer |

Voi bang reward o tren:

- sau `rust_yard_02`, player dat `Level 2`
- sau `rust_yard_04`, player dat `Level 3`
- sau khi clear `rust_yard_06`, player du `Level 4`

Day la nhip mo khoa hop ly cho campaign launch.

## 11. Priority spend guidance cho UX

Game nen goi y nguoi choi:

1. nang `left_arm` hoac `core` truoc
2. craft part counter neu gap boss/shield/burn wall
3. chi dau tu len `4-5` khi part do da la core cua build

Neu co nut `Auto Suggest`, quy tac MVP co the la:

- uu tien nang part dang dung
- neu thua va `failure_hint = thieu counter Burn`, de xuat `Heat Sink`
- neu thua va `failure_hint = thieu anti-shield`, de xuat `Drill Cannon` hoac `Hammer Unit`

## 12. Storage format khuyen nghi

Khuyen nghi tach economy ra 4 file:

```text
data/economy/reward_profiles.json
data/economy/upgrade_curves.json
data/economy/craft_recipes.json
data/economy/account_levels.json
```

Ly do:

- de balance ma khong sua combat code
- de validator check `curve_id`, `recipe_id`, `reward_profile_id`
- de UI doc duoc chi phi truoc khi player xac nhan

## 13. Test cases data bat buoc

1. moi `curve_id` trong `part_data` phai ton tai trong `upgrade_curves`
2. `common` craft recipe khong duoc yeu cau `core_shard`
3. `rare` craft recipe bat buoc co `core_shard >= 1`
4. boss `repeat_clear.core_shard_drop_rate = 0.10`
5. defeat reward luon nho hon repeat clear cung stage
6. `account_level 2` mo craft truoc khi player can rare counter dau tien
7. tong reward first clear campaign launch >= `1400 coins` va `280 scrap`
8. tong reward first clear campaign launch >= `2 core_shard`
9. `core_shard` khong xuat hien trong regular stage reward
10. khong co upgrade curve nao dung `core_shard` trong MVP

## 14. Quyet dinh chot trong tai lieu nay

1. reward chinh cua campaign la `first_clear`, khong phai grind repeat
2. `core_shard` chi dung cho craft rare, khong dung cho upgrade
3. `stage_drop` phai co pity, khong duoc RNG thuan
4. 1 common part max level duoc coi la dau tu lon cua phase launch
5. unlock pacing phai mo `craft` truoc, `module upgrade` sau, `zone 2` cuoi zone 1

## 15. Tai lieu tiep theo

Sau `economy_balance_sheet.md`, nen viet:

1. `godot_system_architecture.md`

Vi den muc nay team da co:

- combat contract
- part contract
- enemy roster
- economy va progression pacing

Nhu vay da du de:

- code `reward_system`
- code `upgrade_system`
- code `craft_system`
- lap vertical slice tu garage -> battle -> reward -> nang part -> rematch
