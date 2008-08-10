 var num, i, max ;
begin
num = 0;
i = (+ num 2);
if (< i 1)
then
  max = 0;
else
  max = 3;
endif;
write(max);
write(i);
read(i);
write( (+ i i) );
end
