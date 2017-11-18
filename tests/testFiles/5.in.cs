#if !test
head
#if sl
sl part
#else
not sl part
#endif
body
#elif portable
elif part
#else
else part
#endif