#include <stdint.h>

// <使用例>
// このCソースコードをmake usr_sample.basにより配列へのlet文からなる
// BASICプログラムが生成される。
//   $ make usr_sample.bas
//
// <出力結果例: usr_sample.bas>
//   100 let[0],#b508,#2807,#dc02,#f000,#f810,#e001,#f000,#f802
//   110 let[8],#b200,#bd08,#2300,#2800,#dd05,#b280,#18c3,#3801
//   120 let[16],#b29b,#b200,#e7f7,#b218,#4770,#2301,#2800,#d005
//   130 let[24],#b282,#4353,#1e50,#b200,#b29b,#e7f7,#b218,#4770
// 出力内容は使用するコンパイラ、リンカにより結果は異なる可能性がある。
//
// 上記のBASICプログラムをIchigoJamで実行することで、#800からのメモリ
// にマシン語プログラムが格納される。
//
// 以下の命令を実行することで動作を確認できる。
//   for i = 0 to 10 : ? usr(#800, i) : next
//
// <出力結果>
// 0から7まではfact()、8から10まではsum()の戻り値が出力される。
//   1
//   1
//   2
//   6
//   24
//   120
//   720
//   5040
//   36
//   45
//   55
//   OK

// オブジェクトファイル内における関数配置の確認のため以下の関数はあえ
// てstaticとはしていない。本来、コンパイラによる同一オブジェクトファ
// イル内のさらなる最適化を望む場合はstaticとしておくべき。
int16_t sum(int16_t n);
int16_t fact(int16_t n);

// 注意: USR()で呼び出す関数にだけ以下の__attribute__指定を付与する
__attribute__ ((section (".entry")))
int16_t usr_sample(int16_t param, void *vmem_offset, void *cmem_offset)
{
  int16_t result;

  // 8以上はfact()するとBASICの正数の範囲を超えるので代わりにsum()する
  if (param <= 7) {
    result = fact(param);
  } else {
    result = sum(param);
  }

  return result;
}

// 以下の関数は.textセクションに配置される
int16_t sum(int16_t n)
{
  int16_t result = 0;

  while (n > 0) {
    result += n;
    n--;
  }
  return result;
}

// 以下の関数は.textセクションに配置される
int16_t fact(int16_t n)
{
  if (n == 0) {
    return 1;
  }
  return fact(n - 1) * n;
}

// __attribute__ ((section (".entry")))によるセクション指定について
//   リンクスクリプトbin2poke.ldにて.entryセクションを.textセクション
//   よりも前に配置させるよう指定している。
//   一般の関数は.textセクションに配置され、唯一.entryセクションへの配
//   置を指定された関数がもっとも小さいアドレスに配置される。
//   これにより、bin2poke.pyの-aオプションによる開始アドレスをUSR()で
//   呼び出すことで、.entryセクションの関数を呼び出すことが可能になる。
