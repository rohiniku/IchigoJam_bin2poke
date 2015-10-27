# IchigoJam_bin2poke

## ここにあるものは?

Makefileとかbin2poke.pyとか

## なにこれ?

IchigJamでのマシン語利用を容易にするため、Cソース(.c)からBASICソース(.bas)を自動生成するための Makefileと、下働きのPythonスクリプト。

## どうなってるの?

以下の処理を実行するMakefileと、その第3段階を実際に行うPythonスクリプト(bin2poke.py)から構成される。

* Cソースをコンパイルしてオブジェクトファイル生成(.c -> .o)
* オブジェクトファイルから必要な命令部分だけを抽出(.o -> .bin)
* オブジェクトファイルをpoke文からなるBASICを生成(.bin -> .bas)

## 必要な環境は?

以下の環境で開発。

* Max OS X El Capitan (10.11)
* Homebrew
* make (type makeしたら/usr/bin/makeにありました)

    $ make -v
    GNU Make 3.81
    Copyright (C) 2006  Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.
    There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE.

    This program built for i386-apple-darwin11.3.0
* ツールチェーン (brewでインストールしたやつarm-none-eabi-gcc, arm-none-eabi-objcopy) 

    $ arm-none-eabi-gcc -v
    arm-none-eabi-gcc (GNU Tools for ARM Embedded Processors) 4.9.3 20150303 (release) [ARM/embedded-4_9-branch revision 221220]
    Copyright (C) 2014 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    $ arm-none-eabi-objcopy -v
    GNU objcopy (GNU Tools for ARM Embedded Processors) 2.24.0.20150304
    Copyright 2013 Free Software Foundation, Inc.
    This program is free software; you may redistribute it under the terms of
    the GNU General Public License version 3 or (at your option) any later version.
    This program has absolutely no warranty.
    
* python (brewでインストールしたやつ/usr/local/bin/pythonあたり)

    $ python
    Python 2.7.10 (default, Jul 31 2015, 14:00:49) 
    [GCC 4.2.1 Compatible Apple LLVM 6.1.0 (clang-602.0.53)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

## どうやって使うの?

1. Cソースを用意する
1. makeする

Cソースの置き場所はMakefileやらbin2poke.pyやらがあるのと同じディレクトリが便利。例えばusr_sample.cというCソースがあるときmake usr_sample.basとすることでBASICソースができあがる。これをIchigJamに送り込んで実行すればよい。

bin2poke.py の機能としては BASIC ソースの開始行番号(-sオプション)、行番号増分(-dオプション)、POKE開始アドレス(-aオプション)、出力書式(-o)、1行あたりのバイト数(-c)が指定できる。ファイル名が指定されなかった場合は標準入出力とのやり取りをするようになっているが、Makefileからはそれぞれ行番号100から、10ステップで、#700番地からのpoke命令群を生成するように指定している。利用環境にあわせて修正すればよい。

## オプションリファレンス

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

## 注意点は?

マシン語格納領域のアドレスをチェックしていない。
