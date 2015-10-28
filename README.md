# IchigoJam_bin2poke

## ここにあるものは?

`Makefile`とか`bin2poke.py`とか

## なにこれ?

IchigJamでのマシン語利用を容易にするため、Cソース(`.c`)からBASICソース(`.bas`)を自動生成するための `Makefile`と、下働きのPythonスクリプト`bin2poke.py`。

## どうなってるの?

以下の処理を実行する`Makefile`と、その第3段階を実際に行うPythonスクリプト`bin2poke.py`から構成される。

* Cソースをコンパイルしてオブジェクトファイル生成 by `gcc` (`.c`->`.o`)
* オブジェクトファイルから必要な命令部分だけを抽出 by `objcopy` (`.o`->`.bin`)
* オブジェクトファイルをPOKE文からなるBASICを生成 by `bin2poke.py` (`.bin`->`.bas`)

## 必要な環境は?

以下の環境で開発。

* Max OS X El Capitan (10.11)
* Homebrew
* make (type makeしたら/usr/bin/makeにありました)
```
$ make -v
GNU Make 3.81
Copyright (C) 2006  Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
This program built for i386-apple-darwin11.3.0
```
* ツールチェーン (brewでインストールしたやつarm-none-eabi-gcc, arm-none-eabi-objcopy) 
```
$ arm-none-eabi-gcc -v
arm-none-eabi-gcc (GNU Tools for ARM Embedded Processors) 4.9.3 20150303 (release) [ARM/embedded-4_9-branch revision 221220]
Copyright (C) 2014 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

```
$ arm-none-eabi-objcopy -v
GNU objcopy (GNU Tools for ARM Embedded Processors) 2.24.0.20150304
Copyright 2013 Free Software Foundation, Inc.
This program is free software; you may redistribute it under the terms of
the GNU General Public License version 3 or (at your option) any later version.
This program has absolutely no warranty.
```

* python (brewでインストールしたやつ/usr/local/bin/pythonあたり)
```
$ python
Python 2.7.10 (default, Jul 31 2015, 14:00:49) 
[GCC 4.2.1 Compatible Apple LLVM 6.1.0 (clang-602.0.53)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## どうやって使うの?
### Makefileを使用する場合

1. Cソースを用意する
1. makeする

Cソースの置き場所は`Makefile`や`bin2poke.py`があるのと同じディレクトリが便利。例えば`usr_sample.c`というCソースがあるとき以下のコマンドによりBASICソース`usr_sample.bas`が生成される。これをIchigJamに送り込んで実行すればよい。
```
make usr_sample.bas
```
    
#### Makefileでの処理内容
`Makefile`では`gcc`によりCソース(`.c`)をコンパイルしオブジェクトファイル(`.o`)を作成し、次に`objcopy`によりそのコード本体を取り出しバイナリファイル(`.bin`)を作成する。最後に`python`にスクリプト`bin2poke.py`を実行させることで、BASICソース(`.bas`)を生成している。
Makefileでは変数`BIN2POKE_OPT`を以下のように設定している。これらは利用環境にあわせて修正すればよい。
```
BIN2POKE_OPT=-a 0x700 -s 100 -d 10
```
    
上記の`BIN2POKE_OPT`で指定していないオプションにつては、それぞれ初期値が使用される。
結果、入力ファイル名はmakeのターゲットに指定されたファイル名(例: usr_sample.bas)のうち、拡張子部を`.bin`に差し替えたもの(例:usr_sample.bin)が指定され、`bin2poke.py`は以下のコマンドラインで実行される。
```
python bin2poke.py -a 0x700 -s 100 -d 10 usr_sample.bin usr_sample.bas
```

出力されるBASICソースは以下の形式で出力される。
* #700番地からのPOKE文形式出力(`-a 0x700`指定による)
* 行番号は100から10単位で増加(`-s 100`と`-d 10`指定による)
* POKEデータ部は16進数形式出力(`-o`オプションを指定しないため初期値`hex`としての動作)
* 1行あたりのデータ数は8(`-c`オプションを指定しないため初期値`8`としての動作)

#### bin2poke.pyの処理内容
bin2poke.py の機能としては BASIC ソースの開始行番号(`-s`オプション)、行番号増分(`-d`オプション)、POKE開始アドレス(`-a`オプション)、出力書式(`-o`)、1行あたりのバイト数(`-c`オプション)が指定できる。ファイル名が指定されなかった場合は標準入出力とのやり取りをするようになっている。入出力ファイル名に制限はない。指定された出力ファイル名と同じファイルがすでに存在した場合は、上書きされる。(ファイルパーミッションの設定によっては、書き込みエラーが発生する場合がある)

入力ファイル指定および出力ファイル指定ともになしの場合、標準入力から入力されるバイト列をBASICコードに変換して標準出力に出力する。
```
python bin2poke.py
```

入力ファイル指定あり、出力ファイル指定ありの場合、入力ファイルのバイト列をBASICコードに変換し、結果を標準出力に出力する。
```
python bin2poke.py infile.bin
```

入力ファイル指定および出力ファイル指定ともにありの場合、入力ファイルのバイト列をBASICコードに変換し、結果を出力ファイルに出力する。
```
python bin2poke.py infile.bin outfile.bas
```

## オプションリファレンス
以下のオプションが利用できる。以下のように`bin2poke.py`に続けてオプション指定を記述する。
```
python bin2poke.py -a 900 infile.bin outfile.bas
```

各オプションはそれぞれ個別の引数を指定する必要がある。現状はオプション引数の範囲チェックを省略しているため、引数によっては出力結果が壊れる等の不正な動作を引き起こす可能性がある。
オプションとその引数の間、また先行するオプションの引数と後続のオプションとの間には空白文字による区切りが必要である。
オプションの指定順序は特に限定しない。同じオプションを複数回指定してもよいが後方での指定が優先される。

### -s &lt;行番号&gt;
* 開始行番号を指定する
* 初期値: 100

### -d &lt;行番号増分&gt;
* 行番号増分を指定する
* 初期値: 10

### -a &lt;POKE開始アドレス&gt;
* 開始アドレスに0以外を指定した場合、POKE文で指定するアドレスの開始値とする
* 開始アドレスに0を指定した場合、POKE文の代わりに[0]から始まる配列への代入文を生成する
* '0x'付与の有無に関わらず指定値は16進数として解釈される(-a 700と-a 0x700は同じ結果になる)
* 初期値: 0x700

### -o {hex | dec | bin}
* POKEデータ部の出力書式を指定する
* -o hex指定により'%#02d'形式で出力する
* -o dec指定により'%d'形式で出力する(出力するBASICコードサイズの削減が可能)
* -o bin指定により'`%08b'形式で出力する
* 初期値: hex

### -c &lt;1行あたりのデータ数&gt;
* 1行に出力するデータ部の個数を指定する
* POKE形式出力(-aで0以外を指定した場合)ではデータ数はバイト数となる
* 配列形式出力(-aで0を指定した場合)ではデータ数はワード数となる
* 初期値: 8

### 特別なオプションの組み合わせ
* -a 0 -o bin -c 1 を指定した場合にのみ、ソースのコメント部に逆アセンブルコードを出力する
* 命令体系は [マシン語メモリアクセスで画面超速表示！ - IchigoJamではじめるARMマシン語その3](http://fukuno.jig.jp/1188)にある命令表「IchigoJamで使えるマシン語表（基本＋1byteメモリアクセス編）」にあげられた疑似コードとなる
* 当該表に記載されないARM Cortex-M0については、コメント部にunknownを出力する
* 定数テーブルのような命令以外の領域を判断できないため、無意味なコメントを出力する場合がある
```
python bin2poke.py -a 0 -o bin -c 1 infile.bin outfile.bas
```

## 注意点は?

* マシン語格納領域のアドレスをチェックしていない
* オプション引数の範囲チェックが不十分

## その他の環境での動作報告／使用例
`Makefile`で使用しているツールチェーン(`gcc`や`objcopy`)が、実行環境で使用可能なツールチェーンと異なっている場合は`Makefile`の修正が必要。`gcc`の場合はprefixの修正だけでよいかもしれない。`gcc`以外や大きくバージョンの異なる`gcc`の場合は指定するオプションが異なる場合がある。

以下の環境では、それぞれ`Makefile`で使用しているのと同じツールチェーンをインストールすることで、`Makefile`の修正なしに使用できている。

* Windows + Cygwin / 参考: [IchigoJamのメモリ内のバイナリデータをテキスト・プログラム化するツール](http://blogs.yahoo.co.jp/bokunimowakaru/55096847.html)
* Linux (Ubuntu)
