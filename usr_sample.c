#include <stdint.h>

int16_t sum(int16_t n)
{
  int16_t result = 0;

  while (n > 0) {
    result += n;
    n--;
  }
  return result;
}

int16_t fact(int16_t n)
{
  if (n == 0) {
    return 1;
  }
  return fact(n - 1) * n;
}

__attribute__ ((section (".entry")))
int16_t usr_sample(int16_t param, void *vmem_offset, void *cmem_offset)
{
  int16_t result;

  if (param <= 7) {
    result = fact(param);
  } else {
    result = sum(param);
  }

  return result;
}
