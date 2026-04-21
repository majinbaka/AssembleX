# AssembleX

Project Godot 4.6 cho game `AssembleX`.

Hien tai repo dang o trang thai scaffold:

- chua co `README.md` cu
- chua cau hinh `main scene` trong `project.godot`
- chua co `export_presets.cfg`
- thu muc `tests/` dang trong

Vi vay tai lieu nay huong dan cach `start`, `build`, `dev`, `test` va `debug` theo trang thai hien tai cua repo, dong thoi chi ro nhung phan con thieu de chay end-to-end.

## 1. Yeu cau moi truong

- Godot `4.6` hoac ban tuong thich voi `config/features=PackedStringArray("4.6", "GL Compatibility")`
- Project dang bat `Jolt Physics` trong `project.godot`
- Git

Khuyen nghi dat binary Godot vao bien moi truong:

```bash
export GODOT_BIN="/path/to/Godot_v4.6-stable_linux.x86_64"
```

Neu khong dung bien moi truong, thay `$GODOT_BIN` bang duong dan thuc te den binary Godot cua ban.

## 2. Start

### 2.1. Mo project trong editor

```bash
$GODOT_BIN --editor --path .
```

Lenh nay la cach `start` an toan nhat cho repo hien tai vi project chua co `main scene`.

### 2.2. Chay game tu command line

Chi dung duoc sau khi da:

- tao scene khoi dong, vi du `scenes/main/main.tscn`
- vao `Project Settings -> Application -> Run -> Main Scene`
- gan `main scene` cho project

Khi da cau hinh xong:

```bash
$GODOT_BIN --path .
```

Neu muon chay mot scene cu the trong luc phat trien:

```bash
$GODOT_BIN --path . scenes/main/main.tscn
```

## 3. Dev

Vong lap dev de xuat:

1. Mo editor:

```bash
$GODOT_BIN --editor --path .
```

2. Tao va gan `main scene` neu chua co.

3. Dat code theo cau truc dang co san:

- `autoload/` cho singleton toan cuc that su can song xuyen scene
- `core/` cho utility va foundation dung chung
- `features/` cho logic theo domain
- `scenes/` cho cac scene dieu phoi, bootstrap, test map
- `data/` cho balance, localization, save data

4. Chay scene dang lam viec hoac nhan `F5`/`F6` trong editor de lap lai nhanh.

5. Neu can log chi tiet tu terminal:

```bash
$GODOT_BIN --path . --verbose
```

Luu y:

- Repo hien chua co script build system rieng nhu `Makefile`, `package.json` hay `justfile`
- Quy trinh dev hien tai nen xoay quanh Godot Editor

## 4. Build

Repo hien tai chua the `build/export` ngay vi thieu `export_presets.cfg`.

### 4.1. Cau hinh export lan dau

Trong Godot Editor:

1. Mo project
2. Vao `Project -> Export`
3. Tao it nhat mot preset, vi du:
   - `Linux/X11`
   - `Windows Desktop`
4. Chon output path, vi du:
   - `build/linux/assemblex.x86_64`
   - `build/windows/assemblex.exe`
5. Save de Godot tao file `export_presets.cfg` o root repo

### 4.2. Build tu command line

Sau khi da co `export_presets.cfg`, co the export bang CLI.

Vi du build debug:

```bash
$GODOT_BIN --headless --path . --export-debug "Linux/X11" build/linux/assemblex.x86_64
```

Vi du build release:

```bash
$GODOT_BIN --headless --path . --export-release "Linux/X11" build/linux/assemblex.x86_64
```

Vi du build Windows:

```bash
$GODOT_BIN --headless --path . --export-release "Windows Desktop" build/windows/assemblex.exe
```

Neu build loi, kiem tra lai:

- `main scene` da duoc set chua
- preset name co dung y chang trong `Project -> Export` khong
- output directory da ton tai hoac co quyen ghi khong

## 5. Test

Trang thai hien tai:

- thu muc `tests/` dang rong
- chua tich hop framework test nhu `GUT` hay `WAT`
- chua co scene test trong repo thuc te

### 5.1. Test hien tai co the lam ngay

Day la muc smoke test toi thieu trong giai doan scaffold:

1. Mo project bang editor:

```bash
$GODOT_BIN --editor --path .
```

2. Xac nhan project mo duoc, khong vo import database.

3. Sau khi tao `main scene`, chay:

```bash
$GODOT_BIN --path .
```

4. Kiem tra:

- scene load thanh cong
- khong co error spam trong Output
- input, scene transition, autoload hoat dong dung nhu ky vong

### 5.2. De xuat de co automated test

Neu muon them test tu dong, nen:

1. Cai `GUT`
2. Them test script vao `tests/`
3. Chuan hoa lenh chay test trong README nay

Sau khi tich hop `GUT`, lenh thuong gap se co dang:

```bash
$GODOT_BIN --headless --path . -s res://addons/gut/gut_cmdln.gd
```

Luu y: lenh tren chi la mau tham khao, hien tai repo chua co `addons/gut`.

## 6. Debug

### 6.1. Debug trong editor

Day la cach debug chinh cho repo hien tai.

1. Mo project:

```bash
$GODOT_BIN --editor --path .
```

2. Dat breakpoint trong script GDScript.

3. Chay bang `F5` hoac `F6`.

4. Dung cac panel:

- `Debugger`
- `Stack Frames`
- `Locals`
- `Remote Scene Tree`
- `Profiler`

### 6.2. Debug bang log tu terminal

```bash
$GODOT_BIN --path . --verbose
```

Neu can doc log de hon, uu tien:

- them `print()` co ngu canh ro rang
- log state chuyen scene
- log data input/output cua system dang debug

### 6.3. Debug van de khoi dong

Neu project khong chay duoc tu CLI, thu kiem tra theo thu tu sau:

1. Binary Godot dung version `4.6`
2. `project.godot` doc duoc
3. Da dat `main scene`
4. Scene path ton tai that
5. Plugin hay autoload moi them khong gay loi `_ready()`

## 7. Lenh nhanh

Mo editor:

```bash
$GODOT_BIN --editor --path .
```

Chay project:

```bash
$GODOT_BIN --path .
```

Chay scene cu the:

```bash
$GODOT_BIN --path . scenes/main/main.tscn
```

Chay voi log verbose:

```bash
$GODOT_BIN --path . --verbose
```

Export debug:

```bash
$GODOT_BIN --headless --path . --export-debug "Linux/X11" build/linux/assemblex.x86_64
```

Export release:

```bash
$GODOT_BIN --headless --path . --export-release "Linux/X11" build/linux/assemblex.x86_64
```

## 8. Viec nen lam tiep theo

De README nay tro thanh quy trinh chay that su tron ven, nen uu tien:

1. Tao `scenes/main/main.tscn`
2. Set `Project Settings -> Main Scene`
3. Tao `export_presets.cfg`
4. Them test framework vao `addons/`
5. Viet it nhat mot smoke test trong `tests/`
