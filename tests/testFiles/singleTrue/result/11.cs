start body
#if test1
test1 body
#elif test2
test2 body
#else
test body
#endif
#if !test1 && !test2
#if test3
test3 body
#else
else body
#endif
#endif
end body