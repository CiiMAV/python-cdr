#ifdef __cplusplus
extern "C"
#endif
int max(int num1, int num2) 
{
  // local variable declaration
  int result;

  if (num1 > num2)
    result = num1;
  else
    result = num2;

  return result; 
}