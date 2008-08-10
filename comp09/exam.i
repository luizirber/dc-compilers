
  var 
    i, j : integer;
    achou : boolean;
    ch : char;
begin
i = 1;
j = i*3 - 4%i + 3*2*i/2;
if i + 1 > j - 3 and i <= j + 5 or (4 < i)
then
  write(i);
  write(j);
endif;
ch = 'a';
achou = false;
if ch >= 'b'  and not achou 
then
  read(ch);
endif;
end
