OUTPUT_ARCH(arm)
SECTIONS
{
  PROVIDE(__executable_start = 0x0000000);
  .entry          : { *(.entry .entry.*) }
  .text           : { *(.text .text.*) }
  .rodata         : { *(.rodata .rodata.*) }
  .tdata	  : { *(.tdata .tdata.*) }
  .tbss		  : { *(.tbss .tbss.*) }
  .data           :
  {
    __data_start = .;
    *(.data .data.*)
  }
  __bss_start = .;
  __bss_start__ = .;
  .bss            :
  {
   *(.bss .bss.*)
   . = ALIGN(. != 0 ? 32 / 8 : 1);
  }
  __bss_end__ = .;
  _bss_end__ = .;
  . = ALIGN(4);
  __end = .;
  _end = .;
  PROVIDE(end = .);
}
